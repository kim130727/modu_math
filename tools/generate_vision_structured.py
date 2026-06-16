from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - project dependency, kept for direct script resilience
    Draft202012Validator = None  # type: ignore[assignment]

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


SCHEMA_ID = "modu.vision_structured.v1"
DEFAULT_SCHEMA_PATH = Path("schema/vision/vision_structured.v1.json")

SYSTEM_PROMPT = """You are a structured vision analysis assistant for Korean math worksheet authoring.
Your task is to convert a worksheet image into a compact JSON object for later Python DSL generation.

Hard rules:
1) Output JSON only. No Markdown, no code fences, no explanation outside JSON.
2) Never solve the math problem.
3) Never fill blank answer slots with inferred answers.
4) Preserve visible Korean text exactly as shown whenever possible.
5) Separate visible facts from uncertain or inferred structure.
6) Use normalized coordinates from 0 to 1 for every bbox: x, y, w, h.
7) Include size/layout details for boxes, blanks, tables, fraction slots, diagrams, arrows, choices, and spatial groups.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a structured JSON vision draft sidecar from PNG or SVG."
    )
    parser.add_argument("--image", required=True, help="Path to input image (.png or .svg)")
    parser.add_argument("--problem-id", required=True, help="Problem id to reference in prompt")
    parser.add_argument("--out", required=True, help="Path to output vision_structured.json file")
    parser.add_argument("--vision-draft", default=None, help="Optional existing vision_draft.md for cross-check context")
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
    parser.add_argument(
        "--schema",
        default=str(DEFAULT_SCHEMA_PATH),
        help="JSON schema path for output validation.",
    )
    return parser.parse_args(argv)


def ensure_output_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing output: {path} (pass --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def read_image_size(image_path: Path) -> tuple[float, float]:
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        header = image_path.read_bytes()[:24]
        if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Invalid PNG header: {image_path}")
        width, height = struct.unpack(">II", header[16:24])
        return float(width), float(height)
    if suffix == ".svg":
        text = image_path.read_text(encoding="utf-8-sig")
        view_box = re.search(r"viewBox=[\"']\s*[-.\d]+\s+[-.\d]+\s+([.\d]+)\s+([.\d]+)\s*[\"']", text)
        if view_box:
            return float(view_box.group(1)), float(view_box.group(2))
        width = re.search(r"\bwidth=[\"']([.\d]+)", text)
        height = re.search(r"\bheight=[\"']([.\d]+)", text)
        if width and height:
            return float(width.group(1)), float(height.group(1))
        raise ValueError(f"Could not determine SVG size: {image_path}")
    raise ValueError("Only .png or .svg is supported for --image.")


def build_user_prompt(
    *,
    problem_id: str,
    image_path: Path,
    width_px: float,
    height_px: float,
    vision_draft_text: str | None,
) -> str:
    draft_block = ""
    if vision_draft_text:
        draft_block = f"""

Existing natural-language vision draft for cross-check. Use the image as the source of truth if it conflicts:
<vision_draft>
{vision_draft_text}
</vision_draft>
"""
    return f"""Problem ID: {problem_id}
Image path: {image_path}
Measured image size: width={width_px:g}px, height={height_px:g}px

Return exactly one JSON object with this top-level shape:
{{
  "schema": "{SCHEMA_ID}",
  "problem_id": "{problem_id}",
  "source_image": {{
    "path": "{image_path}",
    "width_px": {width_px:g},
    "height_px": {height_px:g},
    "coordinate_system": "normalized_0_1"
  }},
  "visible_text": [
    {{"id": "text.1", "text": "visible text exactly", "bbox": {{"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}}, "confidence": "high"}}
  ],
  "elements": [
    {{"id": "el.1", "type": "text", "text": "optional", "bbox": {{"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}}, "details": "size, alignment, nearby elements", "confidence": "high"}}
  ],
  "groups": [
    {{"id": "group.1", "role": "stem", "element_ids": ["el.1"], "bbox": {{"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}}, "details": "spatial grouping"}}
  ],
  "math_structure": {{
    "equations": [],
    "blanks": [],
    "choices": [],
    "tables": [],
    "diagrams": []
  }},
  "dsl_hints": [],
  "uncertain": []
}}

Detailed instructions:
- Use normalized coordinates. x/y are top-left; w/h are width/height.
- Keep coordinates approximate but useful for DSL layout.
- For every visible text chunk, add a visible_text item and usually a matching text element.
- For blanks, include their visual size and whether they are answer slots, labels, or layout placeholders.
- For tables, describe rows, columns, borders, and filled cells.
- For fraction slots, describe numerator/denominator/bars and any blank boxes.
- For diagrams, describe shapes, labels, line/arrow direction, and relative spacing.
- Do not infer hidden answers. If a blank is empty, keep it empty and mention it in math_structure.blanks.
- Put uncertain OCR, ambiguous geometry, or low confidence layout facts in uncertain.
{draft_block}
"""


def strip_json_code_fence(raw: str) -> str:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    return text


def parse_json_output(raw: str) -> dict[str, Any]:
    text = strip_json_code_fence(raw)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        data = json.loads(text[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("Structured vision output must be a JSON object.")
    return data


def _bbox_zero() -> dict[str, float]:
    return {"x": 0.0, "y": 0.0, "w": 0.0, "h": 0.0}


def _normalize_bbox(value: object) -> dict[str, float]:
    if not isinstance(value, dict):
        return _bbox_zero()
    normalized: dict[str, float] = {}
    for key in ("x", "y", "w", "h"):
        raw = value.get(key, 0.0)
        try:
            number = float(raw)
        except (TypeError, ValueError):
            number = 0.0
        normalized[key] = min(1.0, max(0.0, number))
    return normalized


def normalize_payload(data: dict[str, Any], *, problem_id: str, image_path: Path, width_px: float, height_px: float) -> dict[str, Any]:
    data["schema"] = SCHEMA_ID
    data["problem_id"] = str(problem_id)
    data["source_image"] = {
        "path": str(image_path),
        "width_px": float(width_px),
        "height_px": float(height_px),
        "coordinate_system": "normalized_0_1",
    }

    visible_text = data.get("visible_text")
    if not isinstance(visible_text, list):
        visible_text = []
    normalized_text: list[dict[str, Any]] = []
    for idx, item in enumerate(visible_text, start=1):
        if not isinstance(item, dict):
            continue
        normalized_text.append(
            {
                "id": str(item.get("id") or f"text.{idx}"),
                "text": str(item.get("text") or ""),
                "bbox": _normalize_bbox(item.get("bbox")),
                "confidence": item.get("confidence") if item.get("confidence") in {"high", "medium", "low"} else "medium",
                **({"notes": str(item["notes"])} if "notes" in item else {}),
            }
        )
    data["visible_text"] = normalized_text

    elements = data.get("elements")
    if not isinstance(elements, list):
        elements = []
    allowed_types = {"text", "box", "blank", "table", "fraction", "diagram", "arrow", "choice", "line", "shape", "number_line", "other"}
    normalized_elements: list[dict[str, Any]] = []
    for idx, item in enumerate(elements, start=1):
        if not isinstance(item, dict):
            continue
        element_type = item.get("type")
        normalized_item: dict[str, Any] = {
            "id": str(item.get("id") or f"el.{idx}"),
            "type": element_type if element_type in allowed_types else "other",
            "bbox": _normalize_bbox(item.get("bbox")),
            "details": str(item.get("details") or ""),
            "confidence": item.get("confidence") if item.get("confidence") in {"high", "medium", "low"} else "medium",
        }
        if "text" in item:
            normalized_item["text"] = str(item.get("text") or "")
        if "style" in item:
            normalized_item["style"] = str(item.get("style") or "")
        normalized_elements.append(normalized_item)
    data["elements"] = normalized_elements

    groups = data.get("groups")
    if not isinstance(groups, list):
        groups = []
    normalized_groups: list[dict[str, Any]] = []
    for idx, item in enumerate(groups, start=1):
        if not isinstance(item, dict):
            continue
        raw_ids = item.get("element_ids")
        element_ids = [str(x) for x in raw_ids] if isinstance(raw_ids, list) else []
        normalized_groups.append(
            {
                "id": str(item.get("id") or f"group.{idx}"),
                "role": str(item.get("role") or "unknown"),
                "element_ids": element_ids,
                "bbox": _normalize_bbox(item.get("bbox")),
                "details": str(item.get("details") or ""),
            }
        )
    data["groups"] = normalized_groups

    if not isinstance(data.get("math_structure"), dict):
        data["math_structure"] = {}
    for key in ("equations", "blanks", "choices", "tables", "diagrams"):
        if not isinstance(data["math_structure"].get(key), list):
            data["math_structure"][key] = []
    data["dsl_hints"] = [str(x) for x in data.get("dsl_hints", [])] if isinstance(data.get("dsl_hints"), list) else []
    data["uncertain"] = [str(x) for x in data.get("uncertain", [])] if isinstance(data.get("uncertain"), list) else []
    return data


def validate_payload(data: dict[str, Any], schema_path: Path) -> None:
    if Draft202012Validator is None:
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda err: list(err.path))
    if errors:
        formatted = "; ".join(f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}" for err in errors[:8])
        raise ValueError(f"Structured vision JSON failed schema validation: {formatted}")


def generate_vision_structured(
    *,
    image_path: Path,
    problem_id: str,
    out_path: Path,
    vision_draft_path: Path | None = None,
    provider: str | None = None,
    mode: str | None = None,
    llm_output_file: Path | None = None,
    prompt_out: Path | None = None,
    model: str | None = None,
    force: bool = False,
    detail: str = "low",
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> dict[str, str]:
    if not image_path.exists():
        raise FileNotFoundError(f"Image path does not exist: {image_path}")
    if vision_draft_path is not None and not vision_draft_path.exists():
        raise FileNotFoundError(f"Vision draft path does not exist: {vision_draft_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema path does not exist: {schema_path}")

    ensure_output_writable(out_path, force=bool(force))
    width_px, height_px = read_image_size(image_path)
    vision_draft_text = vision_draft_path.read_text(encoding="utf-8-sig") if vision_draft_path is not None else None

    load_dotenv_if_available()
    resolved_mode = resolve_mode(mode)
    resolved_provider = resolve_provider(provider)
    resolved_model = resolve_model_name(resolved_provider, model)
    user_prompt = build_user_prompt(
        problem_id=problem_id,
        image_path=image_path,
        width_px=width_px,
        height_px=height_px,
        vision_draft_text=vision_draft_text,
    )

    extra_user_texts: list[str] = []
    image_for_request: Path | None = image_path
    if image_path.suffix.lower() == ".svg":
        extra_user_texts.append(
            "Use the following SVG source as the visual input.\n<svg_source>\n"
            + image_path.read_text(encoding="utf-8-sig")
            + "\n</svg_source>"
        )
        image_for_request = None

    raw_text = run_llm_or_load_output(
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
    if raw_text is None:
        return {
            "image": str(image_path),
            "problem_id": problem_id,
            "out": str(out_path),
            "provider": resolved_provider,
            "mode": resolved_mode,
            "model": resolved_model,
            "detail": detail,
            "prompt_only": "true",
            "message": "Prompt bundle written. Add --llm-output-file later to generate structured vision JSON.",
        }

    payload = normalize_payload(
        parse_json_output(raw_text),
        problem_id=problem_id,
        image_path=image_path,
        width_px=width_px,
        height_px=height_px,
    )
    validate_payload(payload, schema_path=schema_path)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "image": str(image_path),
        "problem_id": problem_id,
        "out": str(out_path),
        "provider": resolved_provider,
        "mode": resolved_mode,
        "model": resolved_model,
        "detail": detail,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = generate_vision_structured(
        image_path=Path(args.image),
        problem_id=args.problem_id,
        out_path=Path(args.out),
        vision_draft_path=Path(args.vision_draft) if args.vision_draft else None,
        provider=args.provider,
        mode=args.mode,
        llm_output_file=Path(args.llm_output_file) if args.llm_output_file else None,
        prompt_out=Path(args.prompt_out) if args.prompt_out else None,
        model=args.model,
        force=bool(args.force),
        detail=args.detail,
        schema_path=Path(args.schema),
    )
    if result.get("prompt_only") == "true":
        print(result["message"])
        if args.prompt_out:
            print(f"Wrote prompt bundle: {args.prompt_out}")
        return 0
    print(f"Wrote structured vision JSON: {result['out']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
