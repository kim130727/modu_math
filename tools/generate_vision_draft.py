from __future__ import annotations

import argparse
import base64
import mimetypes
from pathlib import Path

try:
    from tools.llm_client import (
        load_dotenv_if_available,
        resolve_model_name,
        resolve_mode,
        resolve_provider,
        run_llm_or_load_output,
    )
except ImportError:
    from llm_client import load_dotenv_if_available, resolve_model_name, resolve_mode, resolve_provider, run_llm_or_load_output

SYSTEM_PROMPT = """You are a vision analysis assistant for Korean math worksheet authoring.
Your task is to produce a Snippai-style Korean natural-language draft that helps a human or another tool write Python DSL later.

Hard rules:
1) Never solve the math problem.
2) Never fill blank answer slots with inferred answers.
3) Separate visible facts from inferred meaning.
4) Describe layout and structure precisely: boxes, blanks, arrows, tables, fraction slots, diagrams, alignment, and spatial grouping.
5) If equation transformation steps are shown, explain what changed at each equality step.
6) Output must be Markdown text in Korean, not JSON.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Korean vision draft markdown from PNG or SVG before DSL generation."
    )
    parser.add_argument("--image", required=True, help="Path to input image (.png or .svg)")
    parser.add_argument("--problem-id", required=True, help="Problem id to reference in prompt")
    parser.add_argument("--out", required=True, help="Path to output markdown file")
    parser.add_argument("--provider", choices=("openai", "google"), default=None, help="LLM provider")
    parser.add_argument("--mode", choices=("api", "prompt"), default=None, help="Execution mode")
    parser.add_argument("--llm-output-file", default=None, help="Use pre-generated LLM output text file")
    parser.add_argument("--prompt-out", default=None, help="Write merged prompt bundle markdown")
    parser.add_argument("--model", default=None, help="Optional model override")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
    parser.add_argument(
        "--detail",
        choices=("low", "high", "auto"),
        default="low",
        help="Vision detail level for input_image",
    )
    return parser.parse_args(argv)


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def image_to_data_url(image_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type:
        mime_type = "image/png"
    b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{b64}"


def build_user_prompt(problem_id: str) -> str:
    return f"""문제 ID: {problem_id}

입력 시각 자료를 보고, Python DSL 작성 전에 사용할 '시각 분석 초안'을 한국어 마크다운으로 작성하세요.
반드시 아래 섹션 헤더를 모두 포함하세요:

[전체적인 구성]
[보이는 텍스트]
[반복되는 시각 패턴]
[수식 단계] (해당될 때)
[등호별 변환 의미] (해당될 때)
[세부 내용]
[Python DSL 작성 힌트]
[주의할 점]
[불확실한 부분]

추가 지침:
- 문제를 풀지 마세요.
- 빈칸에 들어갈 답을 추론해서 채우지 마세요.
- 보이는 사실과 추론 의미를 구분해서 쓰세요.
- 박스, 빈칸, 화살표, 표, 분수 슬롯, 도형, 배치를 구체적으로 설명하세요.
- 등호가 여러 번 이어진 변형식이 보이면, 각 단계에서 무엇이 바뀌었는지 설명하세요.
- 불확실한 부분은 단정하지 말고 명시하세요.
- 결과는 JSON이 아닌 마크다운 텍스트로만 출력하세요.
"""


def build_svg_payload(svg_path: Path) -> str:
    return svg_path.read_text(encoding="utf-8-sig")


def generate_vision_draft(
    *,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    provider: str | None = None,
    mode: str | None = None,
    llm_output_file: Path | None = None,
    prompt_out: Path | None = None,
    model: str | None = None,
    force: bool = False,
    detail: str = "high",
) -> dict[str, str]:
    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")

    suffix = image_path.suffix.lower()
    if suffix not in (".png", ".svg"):
        raise ValueError("Only .png or .svg is supported for --image.")

    ensure_output_writable(out_path, force=bool(force))

    load_dotenv_if_available()
    resolved_mode = resolve_mode(mode)
    resolved_provider = resolve_provider(provider)
    resolved_model = resolve_model_name(resolved_provider, model)
    user_prompt = build_user_prompt(problem_id)

    extra_user_texts: list[str] = []
    image_for_request: Path | None = image_path
    if suffix == ".svg":
        svg_text = build_svg_payload(image_path)
        extra_user_texts.append(
            "Use the following SVG source as the visual input.\n<svg_source>\n" + svg_text + "\n</svg_source>"
        )
        image_for_request = None

    draft_text = run_llm_or_load_output(
        mode=resolved_mode,
        llm_output_file=llm_output_file,
        prompt_out=prompt_out,
        provider=resolved_provider,
        model=resolved_model,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=image_for_request,
        image_detail=detail,
        extra_user_texts=extra_user_texts,
    )
    if draft_text is None:
        return {
            "image": str(image_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "provider": resolved_provider,
            "mode": resolved_mode,
            "model": resolved_model,
            "detail": detail,
            "prompt_only": "true",
            "message": "Prompt bundle written. Add --llm-output-file later to generate vision draft.",
        }

    out_path.write_text(draft_text.rstrip() + "\n", encoding="utf-8")

    return {
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "provider": resolved_provider,
        "mode": resolved_mode,
        "model": resolved_model,
        "detail": detail,
        "draft_text": draft_text,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    result = generate_vision_draft(
        image_path=Path(args.image),
        problem_id=args.problem_id,
        out_path=Path(args.out),
        provider=args.provider,
        mode=args.mode,
        llm_output_file=Path(args.llm_output_file) if args.llm_output_file else None,
        prompt_out=Path(args.prompt_out) if args.prompt_out else None,
        model=args.model,
        force=bool(args.force),
        detail=args.detail,
    )

    if result.get("prompt_only") == "true":
        print(result["message"])
        if args.prompt_out:
            print(f"Wrote prompt bundle: {args.prompt_out}")
        return 0

    print(f"Wrote vision draft: {result['out']}")
    try:
        print(result["draft_text"])
    except UnicodeEncodeError:
        print("(vision draft text omitted due to console encoding)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
