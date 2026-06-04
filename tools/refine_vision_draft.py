from __future__ import annotations

import argparse
import logging
import asyncio
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        help="Vision detail level for optional image cross-check.",
    )
    return parser.parse_args(argv)


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


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
    provider: str | None = None,
    mode: str | None = None,
    llm_output_file: Path | None = None,
    prompt_out: Path | None = None,
    model: str | None = None,
    force: bool = False,
    detail: str = "low",
) -> dict[str, str]:
    if not vision_draft_path.exists():
        raise FileNotFoundError(f"Vision draft path does not exist: {vision_draft_path}")
    if image_path is not None and not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")

    ensure_output_writable(out_path, force=bool(force))

    load_dotenv_if_available()

    vision_draft_text = vision_draft_path.read_text(encoding="utf-8-sig")
    user_prompt = build_user_prompt(
        problem_id=problem_id,
        vision_draft_text=vision_draft_text,
        has_image=image_path is not None,
    )
    resolved_mode = resolve_mode(mode)
    resolved_provider = resolve_provider(provider)
    resolved_model = resolve_model_name(resolved_provider, model)

    refined_text = run_llm_or_load_output(
        mode=resolved_mode,
        llm_output_file=llm_output_file,
        prompt_out=prompt_out,
        provider=resolved_provider,
        model=resolved_model,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=image_path,
        image_detail=detail,
    )
    if refined_text is None:
        result = {
            "vision_draft": str(vision_draft_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "provider": resolved_provider,
            "mode": resolved_mode,
            "model": resolved_model,
            "prompt_only": "true",
            "message": "Prompt bundle written. Add --llm-output-file later to generate refined draft.",
        }
        if image_path is not None:
            result["image"] = str(image_path)
        return result

    out_path.write_text(refined_text.rstrip() + "\n", encoding="utf-8")

    result = {
        "vision_draft": str(vision_draft_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "provider": resolved_provider,
        "mode": resolved_mode,
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
        provider=args.provider,
        mode=args.mode,
        llm_output_file=Path(args.llm_output_file) if args.llm_output_file else None,
        prompt_out=Path(args.prompt_out) if args.prompt_out else None,
        model=args.model,
        force=bool(args.force),
        detail=args.detail,
    )
    if result.get("prompt_only") == "true":
        logger.info(result["message"])
        if args.prompt_out:
            logger.info(f"Wrote prompt bundle: {args.prompt_out}")
        return 0

    logger.info(f"Wrote refined draft: {result['out']}")
    logger.debug(result["refined_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
