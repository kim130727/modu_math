from __future__ import annotations

import argparse
import base64
import mimetypes
import os
import logging
import asyncio
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-5.4-mini"

SYSTEM_PROMPT = """You are a Korean math worksheet vision-to-DSL planning assistant.
You rewrite a raw vision draft markdown into a cleaner, DSL-friendly refined draft markdown.

Hard rules:
1) Output markdown text only (never JSON).
2) Do not generate Python DSL code.
3) Do not solve the problem unless an answer is visibly printed in the source.
4) Do not fill blank answers with inferred values.
5) Separate visible facts, inferred mathematical meaning, rendering/layout hints, DSL component hints, and TODO/uncertain items.
6) If an equation transformation chain is present, explain step-by-step what changed at each equality.
7) If a transformation like a/b ÷ n -> a/(b×n) appears, explicitly include this sentence:
   "나누기 n은 분모의 ×n으로 반영된다."
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refine vision_draft.md into a cleaner DSL-ready refined_draft.md."
    )
    parser.add_argument("--vision-draft", required=True, help="Path to input vision_draft.md")
    parser.add_argument("--problem-id", required=True, help="Problem id for prompt context")
    parser.add_argument("--out", required=True, help="Path to output refined_draft.md")
    parser.add_argument("--image", default=None, help="Optional path to original PNG for cross-check")
    parser.add_argument("--model", default=None, help="Optional model override")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing --out file")
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


def build_user_prompt(problem_id: str, vision_draft_text: str, has_image: bool) -> str:
    image_note = (
        "원본 PNG가 함께 제공되므로, 초안과 이미지가 다르면 이미지 기준으로 교정하세요."
        if has_image
        else "원본 PNG 없이 텍스트 초안만 제공되므로, 불확실성은 명시적으로 남기세요."
    )
    return f"""문제 ID: {problem_id}

아래 raw vision draft를 DSL 작성에 더 직접적으로 쓸 수 있는 refined draft로 다시 작성하세요.
{image_note}

반드시 마크다운으로 작성하고, 아래 섹션 헤더를 그대로 포함하세요:

[문제 개요]
[원본에 보이는 요소]
[수식/관계 구조]
[등호별 변환 의미]
[빈칸 정책]
[반복 패턴]
[DSL 작성 힌트]
[semantic/solvable 힌트]
[주의 및 TODO]

작성 규칙:
- JSON 금지, Python DSL 코드 출력 금지.
- 정답 추론 금지. 단, 원본에 정답이 인쇄되어 '보이는 경우'에만 관찰 사실로 언급 가능.
- 빈칸에는 추론값을 넣지 말고 빈칸으로 유지한다는 정책을 분명히 써주세요.
- "보이는 사실"과 "추론되는 수학적 의미"를 분리해서 쓰세요.
- 렌더링/레이아웃 힌트(정렬, 간격, 그룹, 박스, 표, 화살표, 분수 슬롯)를 구체적으로 쓰세요.
- 등호 연쇄 변형이 있으면 각 단계의 변화 내용을 설명하세요.
- a/b ÷ n -> a/(b×n) 류 변환이 보이면 정확히 다음 문장을 포함하세요:
  "나누기 n은 분모의 ×n으로 반영된다."
- 불확실한 항목은 TODO로 남기고 단정하지 마세요.

--- RAW VISION DRAFT START ---
{vision_draft_text}
--- RAW VISION DRAFT END ---
"""


async def refine_vision_draft(
    *,
    vision_draft_path: Path,
    problem_id: str,
    out_path: Path,
    image_path: Path | None = None,
    model: str | None = None,
    force: bool = False,
) -> dict[str, str]:
    if not vision_draft_path.exists():
        raise FileNotFoundError(f"Vision draft path does not exist: {vision_draft_path}")
    if image_path is not None and not image_path.exists():
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
        from openai import AsyncOpenAI
    except ImportError as exc:
        raise ImportError("openai package is required. Install with: pip install openai") from exc

    vision_draft_text = vision_draft_path.read_text(encoding="utf-8-sig")
    user_prompt = build_user_prompt(
        problem_id=problem_id,
        vision_draft_text=vision_draft_text,
        has_image=image_path is not None,
    )
    resolved_model = resolve_model_name(model)

    user_content: list[dict[str, str]] = [{"type": "input_text", "text": user_prompt}]
    if image_path is not None:
        user_content.append({"type": "input_image", "image_url": image_to_data_url(image_path), "detail": "high"})

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
    client = AsyncOpenAI(api_key=api_key)
    response = await client.responses.create(
        model=resolved_model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": SYSTEM_PROMPT}]},
            {"role": "user", "content": user_content},
        ],
    )
    refined_text = _extract_response_text(response)
    out_path.write_text(refined_text.rstrip() + "\n", encoding="utf-8")

    result = {
        "vision_draft": str(vision_draft_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "model": resolved_model,
        "refined_text": refined_text,
    }
    if image_path is not None:
        result["image"] = str(image_path)
    return result


async def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = await refine_vision_draft(
        vision_draft_path=Path(args.vision_draft),
        problem_id=args.problem_id,
        out_path=Path(args.out),
        image_path=Path(args.image) if args.image else None,
        model=args.model,
        force=bool(args.force),
    )
    logger.info(f"Wrote refined draft: {result['out']}")
    logger.debug(result["refined_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
