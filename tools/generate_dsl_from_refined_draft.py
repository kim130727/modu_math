from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from tools.generate_dsl_from_png import (
        DEFAULT_MAX_ATTEMPTS,
        DEFAULT_RULES_MD,
        DEFAULT_SYSTEM_PROMPT,
        _detect_text_corruption,
        _normalize_solvable_schema_fields,
        _synchronize_answer_values,
        _normalize_legacy_slot_kwargs,
        _sanitize_semantic_and_region_refs,
        _render_retry_feedback,
        read_text_utf8,
        resolve_model_name,
        strip_markdown_code_fence,
        validate_dsl_buildable,
        validate_dsl_source,
    )
except ImportError:
    from generate_dsl_from_png import (
        DEFAULT_MAX_ATTEMPTS,
        DEFAULT_RULES_MD,
        DEFAULT_SYSTEM_PROMPT,
        _detect_text_corruption,
        _normalize_solvable_schema_fields,
        _synchronize_answer_values,
        _normalize_legacy_slot_kwargs,
        _sanitize_semantic_and_region_refs,
        _render_retry_feedback,
        read_text_utf8,
        resolve_model_name,
        strip_markdown_code_fence,
        validate_dsl_buildable,
        validate_dsl_source,
    )

try:
    from tools.llm_client import (
        load_dotenv_if_available,
        resolve_mode,
        resolve_provider,
        run_llm_or_load_output,
    )
except ImportError:
    from llm_client import load_dotenv_if_available, resolve_mode, resolve_provider, run_llm_or_load_output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate problem.dsl.py from refined_draft.md (image-verified)."
    )
    parser.add_argument("--draft", required=True, help="Path to refined_draft.md")
    parser.add_argument("--image", required=True, help="Path to original image (PNG or SVG) for verification")
    parser.add_argument("--problem-id", required=True, help="Problem id for prompt context")
    parser.add_argument(
        "--source-problem-json",
        default=None,
        help="Optional original source problem JSON path (answer/explanation reference only).",
    )
    parser.add_argument(
        "--vision-structured",
        default=None,
        help="Optional structured vision JSON sidecar used as layout constraints for DSL generation.",
    )
    parser.add_argument("--out", required=True, help="Path to output problem.dsl.py")
    parser.add_argument("--provider", choices=("openai", "google"), default=None, help="LLM provider")
    parser.add_argument("--mode", choices=("api", "prompt"), default=None, help="Execution mode")
    parser.add_argument("--llm-output-file", default=None, help="Use pre-generated LLM output text file")
    parser.add_argument("--prompt-out", default=None, help="Write merged prompt bundle markdown")
    parser.add_argument("--model", default=None, help="Optional model name override")
    parser.add_argument("--system-prompt", default=str(DEFAULT_SYSTEM_PROMPT), help="System prompt markdown path")
    parser.add_argument(
        "--rules-md",
        default=str(DEFAULT_RULES_MD),
        help="Optional markdown rules file path appended to system prompt when present.",
    )
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata only; do not write output")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=DEFAULT_MAX_ATTEMPTS,
        help="Maximum regeneration attempts when generated DSL fails static validation.",
    )
    parser.add_argument(
        "--max-line-diff-ratio",
        type=float,
        default=1.0,
        help="Maximum allowed line-count diff ratio when SVG reference is available.",
    )
    parser.add_argument(
        "--min-text-match-ratio",
        type=float,
        default=0.65,
        help="Minimum required text match ratio when SVG reference is available.",
    )
    parser.add_argument(
        "--compact-prompt",
        action="store_true",
        help="Use a shorter prompt profile to reduce token usage/cost.",
    )
    parser.add_argument(
        "--max-draft-chars",
        type=int,
        default=3500,
        help="Maximum refined_draft characters to inject when --compact-prompt is enabled.",
    )
    parser.add_argument(
        "--image-detail",
        choices=("low", "high", "auto"),
        default="low",
        help="Vision detail level for the verification image during DSL generation.",
    )
    parser.add_argument(
        "--write-on-fail",
        action="store_true",
        help="Write the last generated DSL output even when validation fails.",
    )
    parser.add_argument(
        "--failure-report",
        default=None,
        help="Optional JSON report path to write validation failure reasons.",
    )
    return parser.parse_args(argv)


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def _extract_answer_explanation_refs(source_json_path: Path | None) -> list[str]:
    if source_json_path is None or not source_json_path.exists():
        return []
    try:
        data = json.loads(source_json_path.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    refs: list[str] = []
    key_hint = ("answer", "해설", "설명", "풀이", "solution", "explain")

    def walk(node: object, parent_key: str = "") -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                k_str = str(k)
                if any(h in k_str.lower() for h in key_hint):
                    if isinstance(v, (str, int, float, bool)):
                        refs.append(f"{k_str}: {v}")
                walk(v, k_str)
        elif isinstance(node, list):
            for item in node:
                walk(item, parent_key)
        elif isinstance(node, (str, int, float, bool)) and parent_key:
            if any(h in parent_key.lower() for h in key_hint):
                refs.append(f"{parent_key}: {node}")

    walk(data)
    seen: set[str] = set()
    out: list[str] = []
    for x in refs:
        s = re.sub(r"\s+", " ", str(x)).strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
        if len(out) >= 20:
            break
    return out


COMPACT_DSL_RULES = """Compact DSL generation rules:
- Output Python code only.
- Keep visible worksheet text exactly as shown.
- Use ProblemTemplate(id=..., title=..., canvas=..., regions=..., slots=...).
- Include SEMANTIC_OVERRIDE and SOLVABLE.
- SEMANTIC_OVERRIDE must include non-empty problem_id equal to the ProblemTemplate id.
- SEMANTIC_OVERRIDE: meaning-only (no coordinates/style mirrors).
- SOLVABLE must use schema "modu.solvable.v1.2".
- SOLVABLE: include schema/problem_id/problem_type/inputs/given/target/understanding/plan/steps/checks/answer.
- SOLVABLE.understanding should split facts, unknowns, relation, and small diagnostic questions for the student's first read.
- SEMANTIC_OVERRIDE["answer"] and SOLVABLE["answer"] must match for strict validation.
- Do not infer hidden answers into visible blanks.
- If uncertain, keep minimal valid structure and add TODO comments.
- Hard rule: never use dict/list literals for ProblemTemplate structural fields.
- Must use Canvas(...), regions=(Region(...), ...), slots=(TextSlot(...)/TextBoxSlot(...)/RectSlot(...), ...).
- Use TextBoxSlot only when a fixed PowerPoint-like text box is needed; keep ordinary labels as TextSlot.
- PathSlot, ImageSlot, ChoiceSlot, BlankSlot, LabelSlot, and modu_math.dsl helper slot factories are allowed when they match visible content.
- Hard rule: import from modu_math.dsl only. Do not use `from modu_math import ProblemTemplate`.
"""


def _compact_refined_draft_text(text: str, max_chars: int) -> str:
    normalized = text.strip()
    if len(normalized) <= max_chars:
        return normalized
    lines = [ln.rstrip() for ln in normalized.splitlines() if ln.strip()]
    selected: list[str] = []
    current = 0
    for ln in lines:
        if ln.startswith("[") and ln.endswith("]"):
            selected.append(ln)
            current += len(ln) + 1
            continue
        if ln.startswith("- ") or ln.startswith("* ") or ln[:2].isdigit():
            if current + len(ln) + 1 > max_chars:
                break
            selected.append(ln)
            current += len(ln) + 1
    compact = "\n".join(selected).strip()
    if compact and len(compact) <= max_chars:
        return compact
    return normalized[: max(0, max_chars)].rstrip() + "\n...(truncated for cost)"


def _read_vision_structured_json(path: Path | None, *, compact_prompt: bool) -> str | None:
    if path is None:
        return None
    if not path.exists():
        raise FileNotFoundError(f"Structured vision JSON path does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if compact_prompt:
        keep_keys = ("schema", "problem_id", "source_image", "elements", "groups", "math_structure", "dsl_hints", "uncertain")
        data = {key: data[key] for key in keep_keys if key in data}
    return json.dumps(data, ensure_ascii=False, indent=2)


def _render_vision_structured_block(vision_structured_text: str | None) -> str:
    if not vision_structured_text:
        return ""
    return f"""

Structured vision JSON layout constraints:
<vision_structured_json>
{vision_structured_text}
</vision_structured_json>

Use the structured vision JSON as layout evidence:
- Treat `source_image.width_px` and `source_image.height_px` as the measured source canvas size.
- Use `elements[].bbox` and `groups[].bbox` as approximate normalized layout constraints.
- Convert normalized bbox to DSL coordinates by multiplying x/w by canvas width and y/h by canvas height.
- Prefer `groups` for high-level regions and `elements` for individual slots.
- Use `visible_text` and element `text` only for visible worksheet text; never copy answer/explanation reference text into visible slots unless it is visibly printed.
- Keep layout coordinates, colors, and style details out of `SEMANTIC_OVERRIDE`.
- If structured JSON conflicts with visible image evidence, trust the image; if it conflicts only with the refined draft wording, prefer structured JSON for layout placement.
"""


def build_user_prompt(
    *,
    problem_id: str,
    refined_draft_text: str,
    source_answer_refs: list[str],
    compact_prompt: bool,
    vision_structured_text: str | None = None,
) -> str:
    source_block = ""
    if source_answer_refs:
        refs_text = "\n".join(f"- {item}" for item in source_answer_refs)
        source_block = (
            "\nSource problem JSON answer/explanation references (optional context):\n"
            "<source_problem_json_answer_explanation>\n"
            f"{refs_text}\n"
            "</source_problem_json_answer_explanation>\n"
        )
    vision_structured_block = _render_vision_structured_block(vision_structured_text)
    if compact_prompt:
        return f"""Problem ID: {problem_id}

Generate modu_math Python DSL from the refined draft, structured vision layout constraints, and image verification.

Rules:
- Output Python code only.
- Keep visible worksheet text exact.
- Include `SEMANTIC_OVERRIDE` and `SOLVABLE`.
- `SEMANTIC_OVERRIDE["problem_id"]` must exist and match `{problem_id}`.
- `SOLVABLE["schema"]` must be "modu.solvable.v1.2".
- `SOLVABLE["problem_id"]` must match `{problem_id}`.
- `SOLVABLE["understanding"]` should include summary, facts, unknowns, relation, and diagnostic questions before calculation steps.
- `SEMANTIC_OVERRIDE["answer"]` and `SOLVABLE["answer"]` must match for strict validation.
- Keep semantic meaning-focused, not renderer/layout mirrors.
- Do not infer blank answers unless visibly printed.
- Keep uncertain parts as TODO.
- If structured vision JSON is provided, use it as the primary layout constraint source.
- Convert normalized bbox values to canvas-relative DSL x/y/width/height coordinates.
- Do not mirror layout coordinates into semantic.
- Hard rule: never use dict/list literals for ProblemTemplate structural fields.
- Must use Canvas(...), regions=(Region(...), ...), slots=(TextSlot(...)/TextBoxSlot(...)/RectSlot(...), ...).
- Use TextBoxSlot only when a fixed PowerPoint-like text box is needed; keep ordinary labels as TextSlot.
- PathSlot, ImageSlot, ChoiceSlot, BlankSlot, LabelSlot, and modu_math.dsl helper slot factories are allowed when they match visible content.
- Hard rule: import from modu_math.dsl only. Do not use `from modu_math import ProblemTemplate`.

Refined draft:
<refined_draft>
{refined_draft_text}
</refined_draft>
{vision_structured_block}
{source_block}
"""
    return f"""Problem ID: {problem_id}

Generate Python DSL code for modu_math.

Primary source rule:
- `refined_draft.md` is the primary interpretation source.
- If `vision_structured.json` is provided, it is the primary layout constraint source.
- The image is used only to verify visible details.
- If draft and image conflict, prefer visible evidence from the image.
- If draft and structured JSON conflict on layout placement, prefer structured JSON unless image evidence says otherwise.

Safety and authoring rules:
- Output Python code only.
- Do not output JSON.
- `SEMANTIC_OVERRIDE` and `SOLVABLE` are mandatory.
- `SEMANTIC_OVERRIDE` must be concise domain/answer-centric semantics, not slot-by-slot mirror listing.
- `SOLVABLE["schema"]` must be "modu.solvable.v1.2".
- `ProblemTemplate.id`, `SEMANTIC_OVERRIDE["problem_id"]`, and `SOLVABLE["problem_id"]` must all match `{problem_id}`.
- `SEMANTIC_OVERRIDE["answer"]` and `SOLVABLE["answer"]` must match for strict validation.
- `SOLVABLE` must include: schema, problem_id, problem_type, inputs, given, target, understanding, plan, steps, checks, answer.
- `SOLVABLE["understanding"]` should help the student identify given facts, the unknown target, and the relation before calculation.
- Every `SOLVABLE.steps[]` item MUST include exactly these required keys at minimum: id (string), expr (string), value (any).
- Every `SOLVABLE.checks[]` item MUST include exactly these required keys at minimum: id (string), expr (string), expected, actual, pass (boolean).
- Never omit required SOLVABLE fields even if uncertain; use conservative placeholders rather than missing keys.
- Do not solve inferred answers and do not render inferred answers inside blanks unless printed in the image.
- Preserve TODO comments for uncertain parts.
- Keep structure faithful to visible layout: boxes, blanks, arrows, tables, fraction slots, diagrams, and spacing groups.
- Use current DSL signatures and avoid legacy kwargs.
- Preserve original visible text faithfully. Do not rewrite, paraphrase, translate, or normalize visible source text.
- If source JSON answer/explanation context is provided, use it only for `SEMANTIC_OVERRIDE` and `SOLVABLE`.
- Never copy source JSON answer/explanation text into layout slots, renderer-oriented text, or visible worksheet text.
- Use structured JSON normalized bboxes to plan canvas, regions, and slot positions.
- Prefer source image dimensions from structured JSON for `Canvas(width=..., height=...)` when available.
- Convert each bbox with `x_px=x*width_px`, `y_px=y*height_px`, `width_px=w*width_px`, `height_px=h*height_px`.
- Use `groups[].role` to create meaningful regions and `elements[].id`/`type` to create readable slot ids.
- Keep structured JSON coordinates and style hints in layout slots only, never in `SEMANTIC_OVERRIDE`.
- Hard rule: never use dict/list literals for ProblemTemplate structural fields.
- Must use Canvas(...), regions=(Region(...), ...), slots=(TextSlot(...)/TextBoxSlot(...)/RectSlot(...), ...).
- Use TextBoxSlot only when a fixed PowerPoint-like text box is needed; keep ordinary labels as TextSlot.
- PathSlot, ImageSlot, ChoiceSlot, BlankSlot, LabelSlot, and modu_math.dsl helper slot factories are allowed when they match visible content.
- Hard rule: import from modu_math.dsl only. Do not use `from modu_math import ProblemTemplate`.

Refined draft content:
<refined_draft>
{refined_draft_text}
</refined_draft>
{vision_structured_block}
{source_block}
"""


def _resolve_reference_svg(image_path: Path, draft_path: Path) -> Path | None:
    draft_dir = draft_path.parent
    answer_svgs = sorted(draft_dir.glob("*.answer.svg"))
    if answer_svgs:
        return answer_svgs[0]
    if image_path.suffix.lower() == ".svg":
        return image_path
    return None


def _extract_svg_text_tokens(svg_text: str) -> set[str]:
    tokens: set[str] = set()
    for raw in re.findall(r">([^<>]+)<", svg_text):
        s = re.sub(r"\s+", " ", raw).strip()
        if s and any(ch.isalnum() for ch in s):
            tokens.add(s)
    return tokens


def _count_svg_lines(svg_text: str) -> int:
    return len(re.findall(r"<line(\s|>)", svg_text))


def _compare_svg_quality(reference_svg: Path, generated_svg: Path) -> dict[str, float]:
    ref_text = reference_svg.read_text(encoding="utf-8", errors="ignore")
    gen_text = generated_svg.read_text(encoding="utf-8", errors="ignore")

    ref_lines = _count_svg_lines(ref_text)
    gen_lines = _count_svg_lines(gen_text)
    line_diff_ratio = abs(gen_lines - ref_lines) / max(1, ref_lines)

    ref_tokens = _extract_svg_text_tokens(ref_text)
    gen_tokens = _extract_svg_text_tokens(gen_text)
    text_match_ratio = 1.0 if not ref_tokens else len(ref_tokens & gen_tokens) / max(1, len(ref_tokens))

    return {
        "ref_lines": float(ref_lines),
        "gen_lines": float(gen_lines),
        "line_diff_ratio": line_diff_ratio,
        "text_match_ratio": text_match_ratio,
    }


def _extra_feedback_from_errors(errors: list[str]) -> str:
    joined = "\n".join(errors)
    lines: list[str] = []
    lines.append("\n[TARGETED FIX RULES]")
    lines.append("- Import every slot class you use from modu_math.dsl. Do not use undefined symbols.")
    lines.append("- If you use PathSlot, explicitly import PathSlot.")
    lines.append("- Prefer simple primitives (LineSlot/RectSlot/CircleSlot/TextSlot) unless complex paths are required.")
    lines.append("- Use TextBoxSlot only for fixed-size text boxes; otherwise use TextSlot.")
    lines.append("- Do not emit incomplete semantic relations.")
    lines.append("- For every relation in domain.relations, both from_id and to_id must be non-empty strings.")
    lines.append("- If relation endpoints are uncertain, omit that relation instead of emitting empty IDs.")
    lines.append("- Do not emit placeholder empty strings for IDs, labels, or required fields.")
    lines.append("- Keep output as a full valid Python DSL file, not partial patch text.")

    if "NameError: name 'PathSlot' is not defined" in joined:
        lines.append("- Detected PathSlot NameError: either import PathSlot or replace with LineSlot/PolygonSlot.")
    if "from_id must be a non-empty string" in joined or "to_id must be a non-empty string" in joined:
        lines.append("- Detected invalid relation endpoint IDs: remove invalid relations or set valid object IDs.")
    if "SVG diff threshold exceeded" in joined:
        lines.append("- Detected visual structure drift: do not simplify geometry.")
        lines.append("- Preserve segment granularity from source (keep short tick/cap/marker lines as separate primitives).")
        lines.append("- Keep option text chunking and line-break layout close to source.")
        lines.append("- Keep decorative/auxiliary lines if visible in source.")

    return "\n".join(lines) + "\n"


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
    image_detail: str,
) -> str:
    extra_user_texts: list[str] = []
    image_for_request: Path | None = image_path
    if image_path.suffix.lower() == ".svg":
        svg_text = image_path.read_text(encoding="utf-8-sig")
        extra_user_texts.append(
            "Use the following SVG source as the visual input for verification.\n<svg_source>\n"
            + svg_text
            + "\n</svg_source>"
        )
        image_for_request = None

    return run_llm_or_load_output(
        mode=mode,  # type: ignore[arg-type]
        llm_output_file=llm_output_file,
        prompt_out=prompt_out,
        provider=provider,  # type: ignore[arg-type]
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        image_path=image_for_request,
        image_detail=image_detail,
        extra_user_texts=extra_user_texts,
    )


def generate_dsl_from_refined_draft(
    *,
    draft_path: Path,
    image_path: Path,
    problem_id: str,
    source_problem_json_path: Path | None = None,
    vision_structured_path: Path | None = None,
    out_path: Path,
    provider: str | None = None,
    mode: str | None = None,
    llm_output_file: Path | None = None,
    prompt_out: Path | None = None,
    model: str | None = None,
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT,
    rules_md_path: Path = DEFAULT_RULES_MD,
    force: bool = False,
    dry_run: bool = False,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    max_line_diff_ratio: float = 1.0,
    min_text_match_ratio: float = 0.65,
    compact_prompt: bool = False,
    max_draft_chars: int = 3500,
    image_detail: str = "low",
    write_on_fail: bool = False,
    failure_report_path: Path | None = None,
) -> dict[str, str]:
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft path does not exist: {draft_path}")
    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt path does not exist: {system_prompt_path}")
    if vision_structured_path is not None and not vision_structured_path.exists():
        raise FileNotFoundError(f"Structured vision JSON path does not exist: {vision_structured_path}")

    resolved_provider = resolve_provider(provider)
    resolved_mode = resolve_mode(mode)
    resolved_model = resolve_model_name(model) if resolved_provider == "openai" else (model or os.getenv("GOOGLE_MODEL") or "gemini-2.5-flash")
    refined_draft_text = read_text_utf8(draft_path)
    if compact_prompt:
        refined_draft_text = _compact_refined_draft_text(refined_draft_text, max(500, int(max_draft_chars)))
    system_prompt = read_text_utf8(system_prompt_path)
    if compact_prompt:
        system_prompt = f"{system_prompt}\n\n# Generation Rules\n\n{COMPACT_DSL_RULES}"
    elif rules_md_path.exists():
        system_prompt = f"{system_prompt}\n\n# Generation Rules\n\n{read_text_utf8(rules_md_path)}"

    source_answer_refs = _extract_answer_explanation_refs(source_problem_json_path)
    vision_structured_text = _read_vision_structured_json(
        vision_structured_path,
        compact_prompt=compact_prompt,
    )
    rendered_user_prompt = build_user_prompt(
        problem_id=problem_id,
        refined_draft_text=refined_draft_text,
        source_answer_refs=source_answer_refs,
        compact_prompt=compact_prompt,
        vision_structured_text=vision_structured_text,
    )
    reference_svg = _resolve_reference_svg(image_path=image_path, draft_path=draft_path)

    if dry_run:
        result = {
            "draft": str(draft_path),
            "image": str(image_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "model": resolved_model,
            "system_prompt": str(system_prompt_path),
            "rules_md": str(rules_md_path),
            "has_reference_svg": str(reference_svg is not None),
            "has_vision_structured": str(vision_structured_path is not None),
        }
        if vision_structured_path is not None:
            result["vision_structured"] = str(vision_structured_path)
        if reference_svg is not None:
            result["reference_svg"] = str(reference_svg)
        return result

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
            image_detail=image_detail,
        )
        if raw_text is None:
            result = {
                "draft": str(draft_path),
                "image": str(image_path),
                "problem_id": problem_id,
                "out": str(out_path),
                "provider": resolved_provider,
                "mode": resolved_mode,
                "model": resolved_model,
                "system_prompt": str(system_prompt_path),
                "rules_md": str(rules_md_path),
                "has_reference_svg": str(reference_svg is not None),
                "has_vision_structured": str(vision_structured_path is not None),
                "prompt_only": "true",
                "message": "Prompt bundle written. Add --llm-output-file later to generate DSL.",
            }
            if vision_structured_path is not None:
                result["vision_structured"] = str(vision_structured_path)
            if reference_svg is not None:
                result["reference_svg"] = str(reference_svg)
            return result
        dsl_text = _synchronize_answer_values(
            _normalize_solvable_schema_fields(
                _sanitize_semantic_and_region_refs(
                    _normalize_legacy_slot_kwargs(strip_markdown_code_fence(raw_text))
                )
            )
        )

        validation_errors = _detect_text_corruption(dsl_text)
        if validation_errors:
            strict_text_feedback = (
                "\n\n[CRITICAL RETRY RULE]\n"
                "원문 텍스트 절대 변경 금지. 문제 문장/선택지/도형 라벨을 번역, 의역, 요약, 교정하지 말고 보이는 그대로 유지하라.\n"
            )
            prompt_text = rendered_user_prompt + strict_text_feedback + _render_retry_feedback(
                attempt=attempt + 1,
                errors=validation_errors,
            )
            continue

        validation_errors = validate_dsl_source(dsl_text)
        if not validation_errors:
            validation_errors = validate_dsl_buildable(dsl_text, strict=True)

        if not validation_errors and reference_svg is not None:
            try:
                with tempfile.TemporaryDirectory(prefix="refined_draft_svg_diff_") as tmp:
                    tmp_dir = Path(tmp)
                    tmp_dsl = tmp_dir / "candidate.dsl.py"
                    tmp_prefix = tmp_dir / "candidate"
                    tmp_dsl.write_text(dsl_text, encoding="utf-8")

                    try:
                        from tools.validate_generated_dsl import _run_build
                    except ImportError:
                        from validate_generated_dsl import _run_build

                    _run_build(
                        dsl_path=tmp_dsl,
                        out_prefix=tmp_prefix,
                        strict=True,
                        emit_solvable=False,
                    )
                    generated_svg = tmp_prefix.with_suffix(".svg")
                    metrics = _compare_svg_quality(reference_svg, generated_svg)
                    if (
                        metrics["line_diff_ratio"] > max_line_diff_ratio
                        or metrics["text_match_ratio"] < min_text_match_ratio
                    ):
                        validation_errors = [
                            (
                                "SVG diff threshold exceeded: "
                                f"line_diff_ratio={metrics['line_diff_ratio']:.3f} "
                                f"(max {max_line_diff_ratio:.3f}), "
                                f"text_match_ratio={metrics['text_match_ratio']:.3f} "
                                f"(min {min_text_match_ratio:.3f})."
                            )
                        ]
            except Exception as exc:  # noqa: BLE001
                validation_errors = [f"SVG diff check failed: {type(exc).__name__}: {exc}"]

        if not validation_errors:
            break

        strict_text_feedback = (
            "\n\n[CRITICAL RETRY RULE]\n"
            "원문 텍스트 절대 변경 금지. 문제 문장/선택지/도형 라벨을 번역, 의역, 요약, 교정하지 말고 보이는 그대로 유지하라.\n"
        )
        targeted_feedback = _extra_feedback_from_errors(validation_errors)
        prompt_text = rendered_user_prompt + strict_text_feedback + targeted_feedback + _render_retry_feedback(
            attempt=attempt + 1,
            errors=validation_errors,
        )

    if validation_errors:
        if failure_report_path is not None:
            failure_report_path.parent.mkdir(parents=True, exist_ok=True)
            failure_report = {
                "status": "validation_failed",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "problem_id": problem_id,
                "draft": str(draft_path),
                "image": str(image_path),
                "out": str(out_path),
                "vision_structured": str(vision_structured_path) if vision_structured_path is not None else None,
                "provider": resolved_provider,
                "mode": resolved_mode,
                "model": resolved_model,
                "max_attempts": attempts,
                "validation_errors": validation_errors,
            }
            failure_report_path.write_text(
                json.dumps(failure_report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        if write_on_fail and dsl_text.strip():
            out_path.write_text(dsl_text, encoding="utf-8")
            result = {
                "draft": str(draft_path),
                "image": str(image_path),
                "problem_id": problem_id,
                "out": str(out_path),
                "provider": resolved_provider,
                "mode": resolved_mode,
                "model": resolved_model,
                "system_prompt": str(system_prompt_path),
                "rules_md": str(rules_md_path),
                "has_reference_svg": str(reference_svg is not None),
                "has_vision_structured": str(vision_structured_path is not None),
                "status": "invalid_written",
                "validation_errors": "; ".join(validation_errors),
            }
            if failure_report_path is not None:
                result["failure_report"] = str(failure_report_path)
            return result
        raise ValueError(
            "Generated DSL did not pass static/diff validation after "
            f"{attempts} attempts: {'; '.join(validation_errors)}"
        )

    out_path.write_text(dsl_text, encoding="utf-8")
    result = {
        "draft": str(draft_path),
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "provider": resolved_provider,
        "mode": resolved_mode,
        "model": resolved_model,
        "system_prompt": str(system_prompt_path),
        "rules_md": str(rules_md_path),
        "has_reference_svg": str(reference_svg is not None),
        "has_source_problem_json": str(source_problem_json_path is not None and source_problem_json_path.exists()),
        "has_vision_structured": str(vision_structured_path is not None and vision_structured_path.exists()),
    }
    if vision_structured_path is not None:
        result["vision_structured"] = str(vision_structured_path)
    if reference_svg is not None:
        result["reference_svg"] = str(reference_svg)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    result = generate_dsl_from_refined_draft(
        draft_path=Path(args.draft),
        image_path=Path(args.image),
        problem_id=args.problem_id,
        source_problem_json_path=Path(args.source_problem_json) if args.source_problem_json else None,
        vision_structured_path=Path(args.vision_structured) if args.vision_structured else None,
        out_path=Path(args.out),
        provider=args.provider,
        mode=args.mode,
        llm_output_file=Path(args.llm_output_file) if args.llm_output_file else None,
        prompt_out=Path(args.prompt_out) if args.prompt_out else None,
        model=args.model,
        system_prompt_path=Path(args.system_prompt),
        rules_md_path=Path(args.rules_md),
        force=bool(args.force),
        dry_run=bool(args.dry_run),
        max_attempts=max(1, int(args.max_attempts)),
        max_line_diff_ratio=float(args.max_line_diff_ratio),
        min_text_match_ratio=float(args.min_text_match_ratio),
        compact_prompt=bool(args.compact_prompt),
        max_draft_chars=max(500, int(args.max_draft_chars)),
        image_detail=args.image_detail,
        write_on_fail=bool(args.write_on_fail),
        failure_report_path=Path(args.failure_report) if args.failure_report else None,
    )
    if args.dry_run:
        for key in (
            "draft",
            "image",
            "reference_svg",
            "problem_id",
            "out",
            "model",
            "system_prompt",
            "rules_md",
            "has_reference_svg",
            "has_vision_structured",
            "vision_structured",
        ):
            if key in result:
                print(f"{key}={result[key]}")
        return 0

    if result.get("prompt_only") == "true":
        print(result["message"])
        if args.prompt_out:
            print(f"Wrote prompt bundle: {args.prompt_out}")
        return 0

    print(f"Wrote DSL draft: {result['out']}")
    if result.get("status") == "invalid_written":
        print("Validation failed, but last DSL output was written due to --write-on-fail.")
        print(f"validation_errors={result.get('validation_errors','')}")
        if result.get("failure_report"):
            print(f"failure_report={result['failure_report']}")
    if result.get("has_reference_svg") == "True":
        print(f"Reference SVG used for diff check: {result['reference_svg']}")
    else:
        print("Reference SVG not found. Diff check skipped (build validation only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
