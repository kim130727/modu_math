from __future__ import annotations

import argparse
import ast
import os
import re
import tempfile
from pathlib import Path

try:
    from tools.llm_client import (
        load_dotenv_if_available,
        resolve_mode,
        resolve_provider,
        run_llm_or_load_output,
    )
except ImportError:
    from llm_client import load_dotenv_if_available, resolve_mode, resolve_provider, run_llm_or_load_output


DEFAULT_SYSTEM_PROMPT = Path("prompts/dsl_agent_system.md")
DEFAULT_USER_TEMPLATE = Path("prompts/dsl_agent_user_template.md")
DEFAULT_USER_TEMPLATE_STRICT = Path("prompts/dsl_agent_user_template_strict.md")
DEFAULT_RULES_MD = Path("prompts/dsl_generation_rules.md")
DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_MAX_ATTEMPTS = 3
DSL_SCHEMA_HINT = """\
Current DSL slot keyword signatures (must follow exactly):
- TextSlot(id, prompt, text, style_role, x?, y?, font_size?, font_family?, anchor?, fill?, semantic_role?)
- RectSlot(id, prompt, x, y, width, height, stroke?, stroke_width?, rx?, ry?, fill?, semantic_role?)
- CircleSlot(id, prompt, cx, cy, r, stroke?, stroke_width?, fill?, semantic_role?)
- LineSlot(id, prompt, x1, y1, x2, y2, stroke?, stroke_width?, stroke_dasharray?, semantic_role?)
- PolygonSlot(id, prompt, points, x?, y?, stroke?, stroke_width?, fill?, semantic_role?)
- PathSlot(id, prompt, d, x?, y?, stroke?, stroke_width?, stroke_dasharray?, fill?, semantic_role?)

Do not use legacy CircleSlot(x=..., y=...) and do not use style_role on non-TextSlot.
"""
ANSWER_ALIGNMENT_BLOCK = """
# answer contract alignment
if isinstance(SEMANTIC_OVERRIDE.get("answer"), dict) and isinstance(SOLVABLE.get("answer"), dict):
    _answer = dict(SEMANTIC_OVERRIDE["answer"])
    _answer.setdefault("blanks", [])
    _answer.setdefault("choices", [])
    _answer.setdefault("answer_key", [])
    SOLVABLE["answer"] = _answer
""".strip()


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_user_prompt(template: str, problem_id: str) -> str:
    return template.replace("{{problem_id}}", problem_id).replace("{problem_id}", problem_id)


def strip_markdown_code_fence(text: str) -> str:
    match = re.search(r"```(?:python|py)?\s*\n(?P<code>[\s\S]*?)\n```", text, flags=re.IGNORECASE)
    if match:
        return match.group("code").strip()
    return text


def _render_retry_feedback(attempt: int, errors: list[str]) -> str:
    lines = [
        "",
        f"[RETRY {attempt}] Previous output failed validation.",
        "Fix the following and regenerate full Python DSL:",
    ]
    for index, err in enumerate(errors, start=1):
        lines.append(f"{index}. {err}")
    lines.append("Return Python code only.")
    lines.append("Must use ProblemTemplate(id=..., title=..., canvas=..., regions=..., slots=...).")
    lines.append("Avoid legacy/problem_id keyword and avoid assigning problem.semantic/problem.layout dicts directly.")
    lines.append("")
    lines.append(DSL_SCHEMA_HINT.strip())
    return "\n".join(lines)


def _normalize_legacy_slot_kwargs(source: str) -> str:
    """Normalize common legacy kwargs emitted by LLMs to current DSL signatures."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    class _Transformer(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:  # noqa: N802
            self.generic_visit(node)
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name is None:
                return node

            kw_map = {kw.arg: kw for kw in node.keywords if kw.arg}
            if func_name == "CircleSlot":
                if "x" in kw_map and "cx" not in kw_map:
                    kw_map["x"].arg = "cx"
                if "y" in kw_map and "cy" not in kw_map:
                    kw_map["y"].arg = "cy"
            if func_name == "RectSlot":
                if "w" in kw_map and "width" not in kw_map:
                    kw_map["w"].arg = "width"
                if "h" in kw_map and "height" not in kw_map:
                    kw_map["h"].arg = "height"
            if func_name == "PathSlot":
                if "path" in kw_map and "d" not in kw_map:
                    kw_map["path"].arg = "d"

            if func_name != "TextSlot":
                node.keywords = [kw for kw in node.keywords if kw.arg != "style_role"]
            return node

    normalized = _Transformer().visit(tree)
    ast.fix_missing_locations(normalized)
    try:
        return ast.unparse(normalized)
    except Exception:
        return source


def _sanitize_semantic_and_region_refs(source: str) -> str:
    """Best-effort cleanup for common build-time integrity failures.

    - Remove invalid domain.relations items with empty from_id/to_id.
    - Remove unknown slot ids from Region(..., slot_ids=...).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    def _is_named_assign(node: ast.Assign, name: str) -> bool:
        return any(isinstance(t, ast.Name) and t.id == name for t in node.targets)

    def _literal(node: ast.AST | None) -> object | None:
        if node is None:
            return None
        try:
            return ast.literal_eval(node)
        except Exception:
            return None

    def _to_node(value: object) -> ast.AST:
        return ast.parse(repr(value), mode="eval").body

    changed = False

    # 1) sanitize SEMANTIC_OVERRIDE.domain.relations
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not _is_named_assign(node, "SEMANTIC_OVERRIDE"):
            continue
        data = _literal(node.value)
        if not isinstance(data, dict):
            continue
        domain = data.get("domain")
        if not isinstance(domain, dict):
            continue
        relations = domain.get("relations")
        if not isinstance(relations, list):
            continue
        cleaned: list[object] = []
        for rel in relations:
            if not isinstance(rel, dict):
                continue
            from_id = rel.get("from_id")
            to_id = rel.get("to_id")
            if isinstance(from_id, str) and from_id.strip() and isinstance(to_id, str) and to_id.strip():
                cleaned.append(rel)
        if len(cleaned) != len(relations):
            domain["relations"] = cleaned
            node.value = _to_node(data)
            changed = True

    # 2) remove answer/explanation rendering slots from TextSlot
    # Keep answers only in SEMANTIC_OVERRIDE / SOLVABLE.
    banned_markers = ("(정답)", "(해설)", "정답)", "해설)", "(??)")
    banned_id_tokens = ("answer", "ans", "explain", "exp")

    class _AnswerExplainSlotRemover(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST | None:  # noqa: N802
            self.generic_visit(node)
            if not (isinstance(node.func, ast.Name) and node.func.id == "TextSlot"):
                return node

            kw = {k.arg: k.value for k in node.keywords if k.arg}
            slot_id = _literal(kw.get("id"))
            text_val = _literal(kw.get("text"))
            style_role = _literal(kw.get("style_role"))

            id_flag = isinstance(slot_id, str) and any(tok in slot_id.lower() for tok in banned_id_tokens)
            text_flag = isinstance(text_val, str) and any(m in text_val for m in banned_markers)
            style_flag = isinstance(style_role, str) and style_role.lower() in {"answer", "explanation"}

            if id_flag or text_flag or style_flag:
                nonlocal_changed[0] = True
                removed_slot_ids.add(slot_id if isinstance(slot_id, str) else "")
                return None
            return node

    removed_slot_ids: set[str] = set()
    nonlocal_changed = [False]
    remover = _AnswerExplainSlotRemover()
    tree = remover.visit(tree)
    if nonlocal_changed[0]:
        changed = True

    # 3) sanitize Region.slot_ids references against defined slot ids
    defined_slot_ids: set[str] = set()
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        if isinstance(n.func, ast.Name) and n.func.id.endswith("Slot"):
            for kw in n.keywords:
                if kw.arg != "id":
                    continue
                v = _literal(kw.value)
                if isinstance(v, str) and v.strip():
                    defined_slot_ids.add(v.strip())

    class _RegionFixer(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:  # noqa: N802
            self.generic_visit(node)
            if not (isinstance(node.func, ast.Name) and node.func.id == "Region"):
                return node
            for kw in node.keywords:
                if kw.arg != "slot_ids":
                    continue
                v = _literal(kw.value)
                if isinstance(v, tuple):
                    new_ids = tuple(x for x in v if isinstance(x, str) and x in defined_slot_ids)
                    if new_ids != v:
                        kw.value = _to_node(new_ids)
                        nonlocal_changed[0] = True
            return node

    nonlocal_changed = [False]
    fixer = _RegionFixer()
    tree = fixer.visit(tree)
    if nonlocal_changed[0]:
        changed = True

    if not changed:
        return source
    ast.fix_missing_locations(tree)
    try:
        return ast.unparse(tree)
    except Exception:
        return source


def _normalize_solvable_schema_fields(source: str) -> str:
    """Backfill SOLVABLE required keys to match the current solvable schema."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    def _is_solvable_assign(node: ast.Assign) -> bool:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "SOLVABLE":
                return True
        return False

    def _literal(node: ast.AST | None) -> object | None:
        if node is None:
            return None
        try:
            return ast.literal_eval(node)
        except Exception:
            return None

    def _to_node(value: object) -> ast.AST:
        return ast.parse(repr(value), mode="eval").body

    updated = False
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not _is_solvable_assign(node):
            continue
        data = _literal(node.value)
        if not isinstance(data, dict):
            continue

        # Canonicalize solvable schema to current target version.
        data["schema"] = "modu.solvable.v1.2"

        steps = data.get("steps")
        if isinstance(steps, list):
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                step_id = step.get("id")
                if not isinstance(step_id, str) or not step_id.strip():
                    step["id"] = f"step.{i + 1}"
                if "expr" not in step or not isinstance(step.get("expr"), str) or not step.get("expr"):
                    expr = step.get("description") or step.get("operation") or step.get("result") or step.get("id") or f"step_{i + 1}"
                    step["expr"] = str(expr)
                if "value" not in step:
                    if "result" in step:
                        step["value"] = step.get("result")
                    elif "sub_steps" in step:
                        step["value"] = step.get("sub_steps")
                    else:
                        step["value"] = None

        checks = data.get("checks")
        if isinstance(checks, list):
            for i, check in enumerate(checks):
                if not isinstance(check, dict):
                    continue
                check_id = check.get("id")
                if not isinstance(check_id, str) or not check_id.strip():
                    check["id"] = f"check.{i + 1}"
                if "expr" not in check or not isinstance(check.get("expr"), str) or not check.get("expr"):
                    check["expr"] = str(check.get("id") or f"check_{i + 1}")
                if "expected" not in check:
                    check["expected"] = None
                if "actual" not in check:
                    check["actual"] = None
                if "pass" not in check:
                    check["pass"] = False

        node.value = _to_node(data)
        updated = True

    if not updated:
        return source
    ast.fix_missing_locations(tree)
    try:
        return ast.unparse(tree)
    except Exception:
        return source


def _synchronize_answer_values(source: str) -> str:
    """Keep SEMANTIC_OVERRIDE.answer.value and SOLVABLE.answer.value consistent."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    def _is_named_assign(node: ast.Assign, name: str) -> bool:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == name:
                return True
        return False

    def _literal(node: ast.AST | None) -> object | None:
        if node is None:
            return None
        try:
            return ast.literal_eval(node)
        except Exception:
            return None

    def _to_node(value: object) -> ast.AST:
        return ast.parse(repr(value), mode="eval").body

    solvable_assign: ast.Assign | None = None
    semantic_assign: ast.Assign | None = None
    solvable_data: dict[str, object] | None = None
    semantic_data: dict[str, object] | None = None

    for node in tree.body:
        if isinstance(node, ast.Assign) and _is_named_assign(node, "SOLVABLE"):
            data = _literal(node.value)
            if isinstance(data, dict):
                solvable_assign = node
                solvable_data = data
        if isinstance(node, ast.Assign) and _is_named_assign(node, "SEMANTIC_OVERRIDE"):
            data = _literal(node.value)
            if isinstance(data, dict):
                semantic_assign = node
                semantic_data = data

    if not solvable_assign or not semantic_assign or solvable_data is None or semantic_data is None:
        return source

    solvable_answer = solvable_data.get("answer")
    semantic_answer = semantic_data.get("answer")
    if not isinstance(solvable_answer, dict) or not isinstance(semantic_answer, dict):
        return source

    solvable_value = solvable_answer.get("value")
    semantic_value = semantic_answer.get("value")

    changed = False
    if semantic_value in (None, "") and solvable_value not in (None, ""):
        semantic_answer["value"] = solvable_value
        changed = True
    elif solvable_value in (None, "") and semantic_value not in (None, ""):
        solvable_answer["value"] = semantic_value
        changed = True
    elif semantic_value != solvable_value:
        # Prefer SOLVABLE value for pipeline consistency.
        semantic_answer["value"] = solvable_value
        changed = True

    if not changed:
        return source

    solvable_assign.value = _to_node(solvable_data)
    semantic_assign.value = _to_node(semantic_data)
    ast.fix_missing_locations(tree)
    try:
        return ast.unparse(tree)
    except Exception:
        return source


def _detect_text_corruption(source: str) -> list[str]:
    errors: list[str] = []
    if "�" in source:
        errors.append("Detected replacement character '�' (encoding corruption).")
    if "??" in source:
        errors.append("Detected repeated '??' tokens (possible mojibake).")
    return errors


def _normalize_answer_alignment_block(source: str) -> str:
    # Remove forbidden direction first.
    source = re.sub(
        r'^\s*SEMANTIC_OVERRIDE\[(?:"answer"|\'answer\')\]\s*=\s*SOLVABLE\[(?:"answer"|\'answer\')\]\s*$\n?',
        "",
        source,
        flags=re.MULTILINE,
    )

    # Remove existing alignment block variants to keep exactly one canonical block.
    source = re.sub(
        r'^\s*# answer contract alignment[^\n]*\n'
        r'^\s*if isinstance\(SEMANTIC_OVERRIDE\.get\((?:"answer"|\'answer\')\), dict\) and isinstance\(SOLVABLE\.get\((?:"answer"|\'answer\')\), dict\):\n'
        r'^(?:\s+.*\n){1,12}',
        "",
        source,
        flags=re.MULTILINE,
    )

    if "SEMANTIC_OVERRIDE" in source and "SOLVABLE" in source:
        source = source.rstrip() + "\n\n" + ANSWER_ALIGNMENT_BLOCK + "\n"
    return source


def validate_dsl_source(source: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        errors.append(f"Python syntax error at line {exc.lineno}: {exc.msg}")
        return errors

    import_from_dsl = False
    imported_problem_template = False
    has_build_problem_template = False
    has_problem_template_symbol = False
    has_semantic_override = False
    has_solvable = False

    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "modu_math.dsl":
            import_from_dsl = True
            for alias in node.names:
                if alias.name == "ProblemTemplate" or alias.name == "*":
                    imported_problem_template = True
        if isinstance(node, ast.FunctionDef) and node.name == "build_problem_template":
            has_build_problem_template = True
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "PROBLEM_TEMPLATE":
                    has_problem_template_symbol = True
                if isinstance(target, ast.Name) and target.id == "SEMANTIC_OVERRIDE":
                    has_semantic_override = True
                if isinstance(target, ast.Name) and target.id == "SOLVABLE":
                    has_solvable = True

    if not import_from_dsl:
        errors.append("Must import from modu_math.dsl.")
    if not imported_problem_template:
        errors.append("Must import ProblemTemplate (or use wildcard import) from modu_math.dsl.")
    if not (has_build_problem_template or has_problem_template_symbol):
        errors.append("Must define build_problem_template() or PROBLEM_TEMPLATE.")
    if not has_semantic_override:
        errors.append("Must define SEMANTIC_OVERRIDE dict.")
    if not has_solvable:
        errors.append("Must define SOLVABLE dict.")

    return errors


def validate_dsl_buildable(source: str, *, strict: bool = True) -> list[str]:
    try:
        from tools.validate_generated_dsl import _run_build
    except ModuleNotFoundError:
        import importlib.util

        validator_path = Path(__file__).with_name("validate_generated_dsl.py")
        spec = importlib.util.spec_from_file_location("validate_generated_dsl_local", validator_path)
        if spec is None or spec.loader is None:
            return [f"Build validation bootstrap failed: cannot load {validator_path}"]
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _run_build = module._run_build  # type: ignore[attr-defined]

    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="dsl_build_check_") as tmp:
        tmp_dir = Path(tmp)
        dsl_path = tmp_dir / "candidate.dsl.py"
        out_prefix = tmp_dir / "candidate"
        dsl_path.write_text(source, encoding="utf-8")
        try:
            _run_build(dsl_path=dsl_path, out_prefix=out_prefix, strict=bool(strict), emit_solvable=True)
        except Exception as exc:
            errors.append(f"Build validation failed: {type(exc).__name__}: {exc}")
    return errors


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tools-based PNG-to-DSL generator."
    )
    parser.add_argument("--image", required=True, help="Path to input PNG image")
    parser.add_argument("--problem-id", required=True, help="Problem id for template rendering")
    parser.add_argument("--out", required=True, help="Path to output problem.dsl.py draft")
    parser.add_argument("--provider", choices=("openai", "google"), default=None, help="LLM provider")
    parser.add_argument("--mode", choices=("api", "prompt"), default=None, help="Execution mode")
    parser.add_argument("--llm-output-file", default=None, help="Use pre-generated LLM output text file")
    parser.add_argument("--prompt-out", default=None, help="Write merged prompt bundle markdown")
    parser.add_argument("--model", default=None, help="Optional model name (unused in this skeleton)")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=DEFAULT_MAX_ATTEMPTS,
        help="Maximum regeneration attempts when generated DSL fails static validation.",
    )
    parser.add_argument(
        "--system-prompt",
        default=str(DEFAULT_SYSTEM_PROMPT),
        help="System prompt markdown path",
    )
    parser.add_argument(
        "--user-template",
        default=str(DEFAULT_USER_TEMPLATE),
        help="User prompt template markdown path",
    )
    parser.add_argument(
        "--rules-md",
        default=str(DEFAULT_RULES_MD),
        help="Optional markdown rules file path appended to system prompt when present.",
    )
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata only; do not write output")
    return parser.parse_args(argv)


def resolve_model_name(cli_model: str | None) -> str:
    return cli_model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


def call_llm_for_dsl(
    *,
    mode: str,
    llm_output_file: Path | None,
    prompt_out: Path | None,
    provider: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path,
) -> str:
    return run_llm_or_load_output(
        mode=mode,  # type: ignore[arg-type]
        llm_output_file=llm_output_file,
        prompt_out=prompt_out,
        provider=provider,  # type: ignore[arg-type]
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image_path=image_path,
        image_detail="high",
    )


def generate_dsl_from_png(
    *,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    provider: str | None = None,
    mode: str | None = None,
    llm_output_file: Path | None = None,
    prompt_out: Path | None = None,
    model: str | None = None,
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT,
    user_template_path: Path = DEFAULT_USER_TEMPLATE,
    rules_md_path: Path = DEFAULT_RULES_MD,
    force: bool = False,
    dry_run: bool = False,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
) -> dict[str, str]:
    resolved_provider = resolve_provider(provider)
    resolved_mode = resolve_mode(mode)
    resolved_model = resolve_model_name(model) if resolved_provider == "openai" else (model or os.getenv("GOOGLE_MODEL") or "gemini-2.5-flash")
    if resolved_provider == "google" and user_template_path == DEFAULT_USER_TEMPLATE and DEFAULT_USER_TEMPLATE_STRICT.exists():
        user_template_path = DEFAULT_USER_TEMPLATE_STRICT

    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt path does not exist: {system_prompt_path}")
    if not user_template_path.exists():
        raise FileNotFoundError(f"User template path does not exist: {user_template_path}")

    system_prompt = read_text_utf8(system_prompt_path)
    if rules_md_path.exists():
        system_prompt = f"{system_prompt}\n\n# Generation Rules\n\n{read_text_utf8(rules_md_path)}"
    system_prompt = f"{system_prompt}\n\n# Current DSL Schema Snapshot\n\n{DSL_SCHEMA_HINT}"
    user_template = read_text_utf8(user_template_path)
    rendered_user_prompt = render_user_prompt(user_template, problem_id)

    if dry_run:
        return {
            "image": str(image_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "model": resolved_model,
            "system_prompt": str(system_prompt_path),
            "user_template": str(user_template_path),
            "rules_md": str(rules_md_path),
        }

    ensure_output_writable(out_path, force=bool(force))
    load_dotenv_if_available()

    attempts = max(1, int(max_attempts))
    prompt_text = rendered_user_prompt
    dsl_text = ""
    validation_errors: list[str] = []

    for attempt in range(1, attempts + 1):
        raw_text = call_llm_for_dsl(
            mode=resolved_mode,
            llm_output_file=llm_output_file,
            prompt_out=prompt_out,
            provider=resolved_provider,
            model=resolved_model,
            system_prompt=system_prompt,
            user_prompt=prompt_text,
            image_path=image_path,
        )
        dsl_text = _synchronize_answer_values(
            _normalize_solvable_schema_fields(
                _sanitize_semantic_and_region_refs(
                    _normalize_legacy_slot_kwargs(strip_markdown_code_fence(raw_text))
                )
            )
        )
        dsl_text = _normalize_answer_alignment_block(dsl_text)
        validation_errors = _detect_text_corruption(dsl_text)
        if validation_errors:
            prompt_text = rendered_user_prompt + _render_retry_feedback(attempt=attempt + 1, errors=validation_errors)
            continue
        validation_errors = validate_dsl_source(dsl_text)
        if not validation_errors:
            validation_errors = validate_dsl_buildable(dsl_text, strict=True)
        if not validation_errors:
            break
        prompt_text = rendered_user_prompt + _render_retry_feedback(attempt=attempt + 1, errors=validation_errors)

    if validation_errors:
        raise ValueError(
            "Generated DSL did not pass static validation after "
            f"{attempts} attempts: {'; '.join(validation_errors)}"
        )

    out_path.write_text(dsl_text, encoding="utf-8")
    return {
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "provider": resolved_provider,
        "mode": resolved_mode,
        "model": resolved_model,
        "system_prompt": str(system_prompt_path),
        "user_template": str(user_template_path),
        "rules_md": str(rules_md_path),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    load_dotenv_if_available()

    image_path = Path(args.image)
    out_path = Path(args.out)
    system_prompt_path = Path(args.system_prompt)
    user_template_path = Path(args.user_template)
    rules_md_path = Path(args.rules_md)

    result = generate_dsl_from_png(
        image_path=image_path,
        problem_id=args.problem_id,
        out_path=out_path,
        provider=args.provider,
        mode=args.mode,
        llm_output_file=Path(args.llm_output_file) if args.llm_output_file else None,
        prompt_out=Path(args.prompt_out) if args.prompt_out else None,
        model=args.model,
        system_prompt_path=system_prompt_path,
        user_template_path=user_template_path,
        rules_md_path=rules_md_path,
        force=bool(args.force),
        dry_run=bool(args.dry_run),
        max_attempts=max(1, int(args.max_attempts)),
    )
    if args.dry_run:
        print(f"image={result['image']}")
        print(f"problem_id={result['problem_id']}")
        print(f"out={result['out']}")
        print(f"model={result['model']}")
        print(f"system_prompt={result['system_prompt']}")
        print(f"user_template={result['user_template']}")
        print(f"rules_md={result['rules_md']}")
        return 0

    print(f"Wrote DSL draft: {result['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
