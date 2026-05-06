from __future__ import annotations

import argparse
import base64
import mimetypes
import os
from pathlib import Path

DEFAULT_MODEL = "gpt-5.4-mini"

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
        description="Generate a Korean vision draft markdown from PNG before DSL generation."
    )
    parser.add_argument("--image", required=True, help="Path to input PNG image")
    parser.add_argument("--problem-id", required=True, help="Problem id to reference in prompt")
    parser.add_argument("--out", required=True, help="Path to output markdown file")
    parser.add_argument("--model", default=None, help="Optional model override")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
    parser.add_argument(
        "--detail",
        choices=("low", "high", "auto"),
        default="high",
        help="Vision detail level for input_image",
    )
    return parser.parse_args(argv)


def resolve_model_name(cli_model: str | None) -> str:
    return cli_model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL


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


def _extract_response_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    output = getattr(response, "output", None)
    if isinstance(output, list):
        chunks: list[str] = []
        for item in output:
            content = getattr(item, "content", None)
            if not isinstance(content, list):
                continue
            for part in content:
                if getattr(part, "type", None) == "output_text":
                    text = getattr(part, "text", None)
                    if isinstance(text, str):
                        chunks.append(text)
        merged = "\n".join(chunks).strip()
        if merged:
            return merged

    raise ValueError("Could not extract text output from OpenAI response.")


def build_user_prompt(problem_id: str) -> str:
    return f"""문제 ID: {problem_id}

아래 PNG 이미지를 보고, Python DSL 작성 전에 사용할 '시각 분석 초안'을 한국어 마크다운으로 작성하세요.
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


def generate_vision_draft(
    *,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    model: str | None = None,
    force: bool = False,
    detail: str = "high",
) -> dict[str, str]:
    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")

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

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    resolved_model = resolve_model_name(model)
    data_url = image_to_data_url(image_path)
    user_prompt = build_user_prompt(problem_id)

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=resolved_model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": data_url, "detail": detail},
                ],
            },
        ],
    )
    draft_text = _extract_response_text(response)
    out_path.write_text(draft_text.rstrip() + "\n", encoding="utf-8")

    return {
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
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
        model=args.model,
        force=bool(args.force),
        detail=args.detail,
    )

    print(f"Wrote vision draft: {result['out']}")
    print(result["draft_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
