from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import re
from pathlib import Path


DEFAULT_SYSTEM_PROMPT = Path("prompts/dsl_agent_system.md")
DEFAULT_USER_TEMPLATE = Path("prompts/dsl_agent_user_template.md")
DEFAULT_MODEL = "gpt-5.4-mini"


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_user_prompt(template: str, problem_id: str) -> str:
    return template.replace("{{problem_id}}", problem_id).replace("{problem_id}", problem_id)


def encode_image_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def strip_markdown_code_fence(text: str) -> str:
    match = re.search(r"```(?:python|py)?\s*\n(?P<code>[\s\S]*?)\n```", text, flags=re.IGNORECASE)
    if match:
        return match.group("code").strip()
    return text


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
    parser.add_argument("--model", default=None, help="Optional model name (unused in this skeleton)")
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
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata only; do not write output")
    return parser.parse_args(argv)


def resolve_model_name(cli_model: str | None) -> str:
    return cli_model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


def _extract_response_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    output = getattr(response, "output", None)
    if isinstance(output, list):
        chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if not isinstance(content, list):
                continue
            for part in content:
                part_type = getattr(part, "type", None)
                part_text = getattr(part, "text", None)
                if part_type == "output_text" and isinstance(part_text, str):
                    chunks.append(part_text)
        merged = "\n".join(chunks).strip()
        if merged:
            return merged

    raise ValueError("Could not extract text output from OpenAI response.")


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

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type:
        mime_type = "image/png"
    image_data_url = f"data:{mime_type};base64,{encode_image_base64(image_path)}"

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": image_data_url, "detail": "high"},
                ],
            },
        ],
    )
    return _extract_response_text(response)


def generate_dsl_from_png(
    *,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    model: str | None = None,
    system_prompt_path: Path = DEFAULT_SYSTEM_PROMPT,
    user_template_path: Path = DEFAULT_USER_TEMPLATE,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, str]:
    resolved_model = resolve_model_name(model)

    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if not system_prompt_path.exists():
        raise FileNotFoundError(f"System prompt path does not exist: {system_prompt_path}")
    if not user_template_path.exists():
        raise FileNotFoundError(f"User template path does not exist: {user_template_path}")

    system_prompt = read_text_utf8(system_prompt_path)
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
        }

    ensure_output_writable(out_path, force=bool(force))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")

    raw_text = call_openai_for_dsl(
        api_key=api_key,
        model=resolved_model,
        system_prompt=system_prompt,
        user_prompt=rendered_user_prompt,
        image_path=image_path,
    )
    dsl_text = strip_markdown_code_fence(raw_text)
    out_path.write_text(dsl_text, encoding="utf-8")
    return {
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "model": resolved_model,
        "system_prompt": str(system_prompt_path),
        "user_template": str(user_template_path),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None
    if load_dotenv is not None:
        load_dotenv()

    image_path = Path(args.image)
    out_path = Path(args.out)
    system_prompt_path = Path(args.system_prompt)
    user_template_path = Path(args.user_template)

    result = generate_dsl_from_png(
        image_path=image_path,
        problem_id=args.problem_id,
        out_path=out_path,
        model=args.model,
        system_prompt_path=system_prompt_path,
        user_template_path=user_template_path,
        force=bool(args.force),
        dry_run=bool(args.dry_run),
    )
    if args.dry_run:
        print(f"image={result['image']}")
        print(f"problem_id={result['problem_id']}")
        print(f"out={result['out']}")
        print(f"model={result['model']}")
        print(f"system_prompt={result['system_prompt']}")
        print(f"user_template={result['user_template']}")
        return 0

    print(f"Wrote DSL draft: {result['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
