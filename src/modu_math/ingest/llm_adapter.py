from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_DOTENV_PATH = Path(__file__).resolve().parents[3] / ".env"


@dataclass(frozen=True)
class VisionAnalysis:
    problem_type_guess: str
    language: str
    template_hints: tuple[str, ...]
    text_lines: tuple[str, ...]
    detected_objects: tuple[str, ...]
    notes: tuple[str, ...]


class OpenAIVisionAdapter:
    """Thin OpenAI Responses API adapter for PNG classification signals."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gpt-5.4-mini",
        detail: str = "high",
        max_output_tokens: int = 1800,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._detail = detail
        self._max_output_tokens = max_output_tokens

    def analyze_png(
        self,
        *,
        image_path: Path,
        problem_id: str,
        ocr_lines: tuple[str, ...] = (),
    ) -> VisionAnalysis:
        prompt = _build_prompt(problem_id=problem_id, ocr_lines=ocr_lines)
        payload = {
            "model": self._model,
            "max_output_tokens": self._max_output_tokens,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": _image_to_data_url(image_path), "detail": self._detail},
                    ],
                }
            ],
        }
        response = _post_responses_api(api_key=self._api_key, payload=payload)
        raw_text = _extract_output_text(response)
        parsed = _extract_json_object(raw_text)
        return _parse_analysis(parsed)


def resolve_api_key_from_env_or_dotenv(
    *,
    env_name: str = "OPENAI_API_KEY",
    dotenv_path: Path = DEFAULT_DOTENV_PATH,
) -> str | None:
    api_key = os.getenv(env_name)
    if api_key:
        return api_key
    if not dotenv_path.exists():
        return None

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key != env_name:
            continue
        resolved = value.strip().strip('"').strip("'")
        return resolved or None
    return None


def _build_prompt(*, problem_id: str, ocr_lines: tuple[str, ...]) -> str:
    return (
        "You classify one math worksheet image for contract-first DSL generation.\n"
        "Return only one JSON object with keys:\n"
        "{\n"
        '  "problem_type_guess": "string",\n'
        '  "language": "ko|en|mixed|unknown",\n'
        '  "template_hints": ["string"],\n'
        '  "text_lines": ["string"],\n'
        '  "detected_objects": ["cube|triangle|circle|grid|fraction_area_model|arrow|label_slot|diagram_template"],\n'
        '  "notes": ["string"]\n'
        "}\n"
        "Guidelines:\n"
        "- Focus on high-level educational objects, not primitive drawing elements.\n"
        "- If uncertain, provide best-effort values.\n"
        "- Keep text_lines short and close to visible text.\n"
        f"- problem_id: {problem_id}\n"
        f"- optional_ocr_lines: {json.dumps(list(ocr_lines), ensure_ascii=False)}\n"
    )


def _image_to_data_url(image_path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(image_path))
    if not mime:
        mime = "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _post_responses_api(*, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        "https://api.openai.com/v1/responses",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API HTTP error {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"OpenAI API network error: {exc}") from exc


def _extract_output_text(response: dict[str, Any]) -> str:
    output_text = response.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text

    chunks: list[str] = []
    output = response.get("output")
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    chunks.append(part["text"])
    text = "\n".join(chunks).strip()
    if text:
        return text
    raise ValueError("Could not find textual output in API response.")


def _extract_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < 0 or end <= start:
            raise
        payload = json.loads(text[start : end + 1])

    if not isinstance(payload, dict):
        raise ValueError("Model output must decode to one JSON object.")
    return payload


def _parse_analysis(payload: dict[str, Any]) -> VisionAnalysis:
    return VisionAnalysis(
        problem_type_guess=_coerce_str(payload.get("problem_type_guess"), "generic"),
        language=_coerce_str(payload.get("language"), "unknown"),
        template_hints=_coerce_str_tuple(payload.get("template_hints")),
        text_lines=_coerce_str_tuple(payload.get("text_lines")),
        detected_objects=_normalize_object_names(_coerce_str_tuple(payload.get("detected_objects"))),
        notes=_coerce_str_tuple(payload.get("notes")),
    )


def _coerce_str(value: Any, default: str) -> str:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped:
            return stripped
    return default


def _coerce_str_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    out: list[str] = []
    for item in value:
        if not isinstance(item, str):
            continue
        stripped = item.strip()
        if stripped:
            out.append(stripped)
    return tuple(out)


def _normalize_object_names(items: tuple[str, ...]) -> tuple[str, ...]:
    allowed = {
        "cube",
        "triangle",
        "circle",
        "grid",
        "fraction_area_model",
        "arrow",
        "label_slot",
        "diagram_template",
    }
    normalized: list[str] = []
    seen: set[str] = set()
    for item in items:
        lowered = item.strip().lower()
        if lowered in allowed and lowered not in seen:
            normalized.append(lowered)
            seen.add(lowered)
    return tuple(normalized)

