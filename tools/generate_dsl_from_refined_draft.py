from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import re
import tempfile
from pathlib import Path

try:
    from tools.generate_dsl_from_png import (
        DEFAULT_MAX_ATTEMPTS,
        DEFAULT_MODEL,
        DEFAULT_RULES_MD,
        DEFAULT_SYSTEM_PROMPT,
        _detect_text_corruption,
        _extract_response_text,
        _normalize_legacy_slot_kwargs,
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
        DEFAULT_MODEL,
        DEFAULT_RULES_MD,
        DEFAULT_SYSTEM_PROMPT,
        _detect_text_corruption,
        _extract_response_text,
        _normalize_legacy_slot_kwargs,
        _render_retry_feedback,
        read_text_utf8,
        resolve_model_name,
        strip_markdown_code_fence,
        validate_dsl_buildable,
        validate_dsl_source,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate problem.dsl.py from refined_draft.md (image-verified)."
    )
    parser.add_argument("--draft", required=True, help="Path to refined_draft.md")
    parser.add_argument("--image", required=True, help="Path to original image (PNG or SVG) for verification")
    parser.add_argument("--problem-id", required=True, help="Problem id for prompt context")
    parser.add_argument("--out", required=True, help="Path to output problem.dsl.py")
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
    return parser.parse_args(argv)


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def encode_image_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "image/png"
    return f"data:{mime_type};base64,{encode_image_base64(path)}"


def build_user_prompt(*, problem_id: str, refined_draft_text: str) -> str:
    return f"""Problem ID: {problem_id}

Generate Python DSL code for modu_math.

Primary source rule:
- `refined_draft.md` is the primary interpretation source.
- The image is used only to verify visible details.
- If draft and image conflict, prefer visible evidence from the image.

Safety and authoring rules:
- Output Python code only.
- Do not output JSON.
- `SEMANTIC_OVERRIDE` and `SOLVABLE` are mandatory.
- `SEMANTIC_OVERRIDE` must be concise domain/answer-centric semantics, not slot-by-slot mirror listing.
- `SOLVABLE` must include: schema, problem_id, problem_type, inputs, plan, steps, checks, answer.
- Do not solve inferred answers and do not render inferred answers inside blanks unless printed in the image.
- Preserve TODO comments for uncertain parts.
- Keep structure faithful to visible layout: boxes, blanks, arrows, tables, fraction slots, diagrams, and spacing groups.
- Use current DSL signatures and avoid legacy kwargs.
- Preserve original visible text faithfully. Do not rewrite, paraphrase, translate, or normalize visible source text.

Refined draft content:
<refined_draft>
{refined_draft_text}
</refined_draft>
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


def call_openai_for_dsl(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path,
) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    user_content: list[dict[str, str]] = [{"type": "input_text", "text": user_prompt}]
    if image_path.suffix.lower() == ".svg":
        svg_text = image_path.read_text(encoding="utf-8-sig")
        user_content.append(
            {
                "type": "input_text",
                "text": (
                    "Use the following SVG source as the visual input for verification.\n"
                    "<svg_source>\n"
                    f"{svg_text}\n"
                    "</svg_source>"
                ),
            }
        )
    else:
        user_content.append({"type": "input_image", "image_url": image_to_data_url(image_path), "detail": "high"})

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": user_content},
        ],
    )
    return _extract_response_text(response)


def generate_dsl_from_refined_draft(
    *,
    draft_path: Path,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    model: str | None = None,
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT,
    rules_md_path: Path = DEFAULT_RULES_MD,
    force: bool = False,
    dry_run: bool = False,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    max_line_diff_ratio: float = 1.0,
    min_text_match_ratio: float = 0.65,
) -> dict[str, str]:
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft path does not exist: {draft_path}")
    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt path does not exist: {system_prompt_path}")

    resolved_model = resolve_model_name(model)
    refined_draft_text = read_text_utf8(draft_path)
    system_prompt = read_text_utf8(system_prompt_path)
    if rules_md_path.exists():
        system_prompt = f"{system_prompt}\n\n# Generation Rules\n\n{read_text_utf8(rules_md_path)}"

    rendered_user_prompt = build_user_prompt(problem_id=problem_id, refined_draft_text=refined_draft_text)
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
        }
        if reference_svg is not None:
            result["reference_svg"] = str(reference_svg)
        return result

    ensure_output_writable(out_path, force=bool(force))

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None
    if load_dotenv is not None:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")

    attempts = max(1, int(max_attempts))
    prompt_text = rendered_user_prompt
    dsl_text = ""
    validation_errors: list[str] = []

    for attempt in range(1, attempts + 1):
        raw_text = call_openai_for_dsl(
            api_key=api_key,
            model=resolved_model,
            system_prompt=system_prompt,
            user_prompt=prompt_text,
            image_path=image_path,
        )
        dsl_text = _normalize_legacy_slot_kwargs(strip_markdown_code_fence(raw_text))

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
        "model": resolved_model,
        "system_prompt": str(system_prompt_path),
        "rules_md": str(rules_md_path),
        "has_reference_svg": str(reference_svg is not None),
    }
    if reference_svg is not None:
        result["reference_svg"] = str(reference_svg)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    result = generate_dsl_from_refined_draft(
        draft_path=Path(args.draft),
        image_path=Path(args.image),
        problem_id=args.problem_id,
        out_path=Path(args.out),
        model=args.model,
        system_prompt_path=Path(args.system_prompt),
        rules_md_path=Path(args.rules_md),
        force=bool(args.force),
        dry_run=bool(args.dry_run),
        max_attempts=max(1, int(args.max_attempts)),
        max_line_diff_ratio=float(args.max_line_diff_ratio),
        min_text_match_ratio=float(args.min_text_match_ratio),
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
        ):
            if key in result:
                print(f"{key}={result[key]}")
        return 0

    print(f"Wrote DSL draft: {result['out']}")
    if result.get("has_reference_svg") == "True":
        print(f"Reference SVG used for diff check: {result['reference_svg']}")
    else:
        print("Reference SVG not found. Diff check skipped (build validation only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
