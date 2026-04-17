from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


@dataclass
class OcrBox:
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float


@dataclass
class OcrPreprocessResult:
    available: bool
    text_lines: list[str]
    boxes: list[OcrBox]
    tags: list[str]
    error: str = ""


def _korean_char_count(text: str) -> int:
    return len(re.findall(r"[가-힣]", text))


def _ascii_alnum_count(text: str) -> int:
    return len(re.findall(r"[0-9A-Za-z]", text))


def _normalize_line_for_math_ocr(line: str) -> str:
    s = " ".join(line.split())
    # OCR 노이즈를 수학 문제 문맥에서 자주 나오는 형태로 보정
    replacements = {
        " OF ": " 0분 ",
        " OF": " 0분",
        "@초": "0초",
        "@+O+O": "0+0+0",
        "|7<": "17×",
        "x": "×",
        "X": "×",
        "~": "÷",
        "&=": "=",
        "LEP AY": "나타냅니까",
    }
    for src, dst in replacements.items():
        s = s.replace(src, dst)
    return s.strip()


def _result_quality_score(lines: list[str], boxes: list[OcrBox]) -> float:
    joined = " ".join(lines)
    korean = _korean_char_count(joined)
    alnum = _ascii_alnum_count(joined)
    box_bonus = min(len(boxes), 40)
    noise_penalty = joined.count("|") + joined.count("@")
    return (korean * 3.0) + (alnum * 0.8) + (len(lines) * 2.0) + (box_bonus * 0.2) - (noise_penalty * 1.5)


def _extract_tags_from_lines(lines: list[str], *, max_tags: int = 20) -> list[str]:
    seen: set[str] = set()
    tags: list[str] = []
    for line in lines:
        for token in _TOKEN_PATTERN.findall(line):
            lowered = token.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            tags.append(token)
            if len(tags) >= max_tags:
                return tags
    return tags


def _is_meaningful_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    korean = _korean_char_count(s)
    alnum = _ascii_alnum_count(s)
    has_operator = any(op in s for op in ["×", "÷", "+", "-", "="])
    if korean >= 3:
        return True
    if has_operator and alnum >= 2:
        return True
    if alnum >= 6:
        return True
    return False


def _clean_text_lines(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    for line in lines:
        normalized = _normalize_line_for_math_ocr(line)
        if _is_meaningful_line(normalized):
            cleaned.append(normalized)
    return cleaned


def _ensure_tesseract_command(pytesseract_module: Any) -> None:
    if os.name != "nt":
        return
    current_cmd = str(getattr(pytesseract_module.pytesseract, "tesseract_cmd", "") or "")
    needs_override = (not current_cmd) or (current_cmd == "tesseract" and shutil.which("tesseract") is None)
    if not needs_override:
        return
    for cmd_path in [
        Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
        Path("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"),
    ]:
        if cmd_path.exists():
            pytesseract_module.pytesseract.tesseract_cmd = str(cmd_path)
            return


def _make_tess_config_and_lang(local_tessdata: Path) -> tuple[str, str]:
    if local_tessdata.exists():
        config = f"--tessdata-dir {local_tessdata.resolve()}"
        if (local_tessdata / "kor.traineddata").exists():
            return config, "kor+eng"
        return config, "eng"
    return "", "eng"


def extract_ocr_features(image_path: str | Path) -> OcrPreprocessResult:
    try:
        from PIL import Image  # type: ignore[import-not-found]
        import pytesseract  # type: ignore[import-not-found]
    except Exception as exc:  # noqa: BLE001
        return OcrPreprocessResult(False, [], [], [], f"OCR dependency not available: {exc}")

    try:
        _ensure_tesseract_command(pytesseract)
        image = Image.open(Path(image_path)).convert("L")

        local_tessdata = Path("examples/problem/_rag/tessdata")
        tessdata_config, ocr_lang = _make_tess_config_and_lang(local_tessdata)

        candidates: list[tuple[list[str], list[OcrBox], float]] = []
        scales = [2, 3]
        thresholds = [160, 180, 200]
        psm_values = [6, 11]

        for scale in scales:
            resized = image.resize((image.width * scale, image.height * scale))
            variants = [resized]
            for th in thresholds:
                variants.append(resized.point(lambda p, t=th: 255 if p > t else 0))

            for variant in variants:
                for psm in psm_values:
                    config = f"{tessdata_config} --oem 1 --psm {psm}".strip()
                    raw_text = str(pytesseract.image_to_string(variant, lang=ocr_lang, config=config) or "")
                    text_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

                    data: dict[str, Any] = pytesseract.image_to_data(
                        variant,
                        lang=ocr_lang,
                        config=config,
                        output_type=pytesseract.Output.DICT,
                    )
                    boxes: list[OcrBox] = []
                    for idx, text in enumerate(data.get("text", [])):
                        token = str(text).strip()
                        if not token:
                            continue
                        left = int((int(data.get("left", [0])[idx] or 0)) / scale)
                        top = int((int(data.get("top", [0])[idx] or 0)) / scale)
                        width = int((int(data.get("width", [0])[idx] or 0)) / scale)
                        height = int((int(data.get("height", [0])[idx] or 0)) / scale)
                        try:
                            conf = float(data.get("conf", [0])[idx] or 0)
                        except Exception:  # noqa: BLE001
                            conf = 0.0
                        boxes.append(OcrBox(token, left, top, width, height, conf))

                    cleaned_lines = _clean_text_lines(text_lines)
                    score = _result_quality_score(cleaned_lines or text_lines, boxes)
                    candidates.append((cleaned_lines or text_lines, boxes, score))

        if not candidates:
            return OcrPreprocessResult(True, [], [], [])

        candidates.sort(key=lambda row: row[2], reverse=True)
        best_lines, best_boxes, _ = candidates[0]
        return OcrPreprocessResult(
            available=True,
            text_lines=best_lines,
            boxes=best_boxes,
            tags=_extract_tags_from_lines(best_lines),
        )
    except Exception as exc:  # noqa: BLE001
        return OcrPreprocessResult(False, [], [], [], str(exc))


def merge_ocr_result_into_meta(input_meta: dict[str, Any], ocr_result: OcrPreprocessResult) -> dict[str, Any]:
    merged = dict(input_meta)
    merged["ocr_available"] = ocr_result.available
    if ocr_result.error:
        merged["ocr_error"] = ocr_result.error
    if not ocr_result.available:
        return merged

    existing_tags = list(merged.get("tags") or [])
    seen = {str(tag).lower() for tag in existing_tags}
    for tag in ocr_result.tags:
        lowered = str(tag).lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        existing_tags.append(tag)

    merged["tags"] = existing_tags
    merged["ocr_text_lines"] = ocr_result.text_lines
    merged["ocr_boxes"] = [
        {
            "text": box.text,
            "x": box.x,
            "y": box.y,
            "width": box.width,
            "height": box.height,
            "confidence": box.confidence,
        }
        for box in ocr_result.boxes
    ]
    return merged
