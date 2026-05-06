from __future__ import annotations

import argparse
import base64
import mimetypes
import os
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
        description="Generate problem.dsl.py from refined_draft.md (optionally with PNG verification)."
    )
    parser.add_argument("--draft", required=True, help="Path to refined_draft.md")
    parser.add_argument("--image", default=None, help="Optional path to original PNG for visible-detail verification")
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


def build_user_prompt(*, problem_id: str, refined_draft_text: str, include_image: bool) -> str:
    verify_note = (
        "원본 이미지는 보이는 사실 검증용이다."
        if include_image
        else "원본 이미지가 없으므로 draft 기반으로 작성하되 불확실성은 TODO 주석으로 남긴다."
    )
    return f"""Problem ID: {problem_id}

Generate Python DSL code for modu_math.

Primary source rule:
- `refined_draft.md` is the primary interpretation source.
- {verify_note}
- If draft and image conflict, prefer visible evidence from the image.

Safety and authoring rules:
- Output Python code only.
- Do not output JSON.
- Do not solve inferred answers and do not render inferred answers inside blanks unless printed in the image.
- Preserve TODO comments for uncertain parts.
- Keep structure faithful to visible layout: boxes, blanks, arrows, tables, fraction slots, diagrams, and spacing groups.
- Use current DSL signatures and avoid legacy kwargs.

Refined draft content:
<refined_draft>
{refined_draft_text}
</refined_draft>
"""


def call_openai_for_dsl(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path | None = None,
) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    user_content: list[dict[str, str]] = [{"type": "input_text", "text": user_prompt}]
    if image_path is not None:
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
    image_path: Path | None,
    problem_id: str,
    out_path: Path,
    model: str | None = None,
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT,
    rules_md_path: Path = DEFAULT_RULES_MD,
    force: bool = False,
    dry_run: bool = False,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
) -> dict[str, str]:
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft path does not exist: {draft_path}")
    if image_path is not None and not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt path does not exist: {system_prompt_path}")

    resolved_model = resolve_model_name(model)
    refined_draft_text = read_text_utf8(draft_path)
    system_prompt = read_text_utf8(system_prompt_path)
    if rules_md_path.exists():
        system_prompt = f"{system_prompt}\n\n# Generation Rules\n\n{read_text_utf8(rules_md_path)}"

    rendered_user_prompt = build_user_prompt(
        problem_id=problem_id,
        refined_draft_text=refined_draft_text,
        include_image=image_path is not None,
    )

    if dry_run:
        result = {
            "draft": str(draft_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "model": resolved_model,
            "system_prompt": str(system_prompt_path),
            "rules_md": str(rules_md_path),
            "has_image": str(image_path is not None),
        }
        if image_path is not None:
            result["image"] = str(image_path)
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
    result = {
        "draft": str(draft_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "model": resolved_model,
        "system_prompt": str(system_prompt_path),
        "rules_md": str(rules_md_path),
    }
    if image_path is not None:
        result["image"] = str(image_path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    result = generate_dsl_from_refined_draft(
        draft_path=Path(args.draft),
        image_path=Path(args.image) if args.image else None,
        problem_id=args.problem_id,
        out_path=Path(args.out),
        model=args.model,
        system_prompt_path=Path(args.system_prompt),
        rules_md_path=Path(args.rules_md),
        force=bool(args.force),
        dry_run=bool(args.dry_run),
        max_attempts=max(1, int(args.max_attempts)),
    )
    if args.dry_run:
        for key in ("draft", "image", "problem_id", "out", "model", "system_prompt", "rules_md", "has_image"):
            if key in result:
                print(f"{key}={result[key]}")
        return 0

    print(f"Wrote DSL draft: {result['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
