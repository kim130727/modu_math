"""Page-level raw extraction from HWPX."""

from __future__ import annotations

from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

from math_problem_pipeline.models.raw_models import BBox, RawTextBlock, SourcePage


STYLE_TOKENS = {
    "HWPUNIT",
    "LEFT_ONLY",
    "SHOW_ALL",
    "WIDELY",
    "CONTINUOUS",
    "EACH_COLUMN",
    "DIGIT",
    "SOLID",
    "BOTH",
    "HORIZONTAL",
}


def extract_pages_from_hwpx(hwpx_path: Path, document_id: str) -> list[SourcePage]:
    """Extract text blocks from HWPX section XML parts."""
    pages: list[SourcePage] = []

    with zipfile.ZipFile(hwpx_path, "r") as zf:
        section_names = sorted(
            n for n in zf.namelist() if re.fullmatch(r"Contents/section\d+\.xml", n)
        )
        if not section_names:
            section_names = sorted(
                n for n in zf.namelist() if n.startswith("Contents/") and n.endswith(".xml")
            )

        if not section_names:
            return [
                SourcePage(
                    page_id=f"{document_id}_p0001",
                    document_id=document_id,
                    source_path=str(hwpx_path),
                    page_number=1,
                    width=595.0,
                    height=842.0,
                    text_blocks=[],
                    visual_blocks=[],
                )
            ]

        for page_no, section_name in enumerate(section_names, start=1):
            page_id = f"{document_id}_p{page_no:04d}"
            xml_data = zf.read(section_name)
            lines = _extract_text_lines(xml_data)
            text_blocks = _lines_to_blocks(page_id, lines)

            pages.append(
                SourcePage(
                    page_id=page_id,
                    document_id=document_id,
                    source_path=str(hwpx_path),
                    page_number=page_no,
                    width=595.0,
                    height=842.0,
                    text_blocks=text_blocks,
                    visual_blocks=[],
                )
            )

    return pages


def _extract_text_lines(xml_data: bytes) -> list[str]:
    root = ET.fromstring(xml_data)
    lines: list[str] = []

    for elem in root.iter():
        if elem.text is None:
            continue
        tag = elem.tag.lower()
        if not (tag.endswith("t") or tag.endswith("text") or tag.endswith("p")):
            continue
        text = _normalize_text(elem.text)
        if _is_meaningful(text):
            lines.append(text)

    deduped: list[str] = []
    prev = None
    for line in lines:
        if line == prev:
            continue
        deduped.append(line)
        prev = line
    return deduped


def _lines_to_blocks(page_id: str, lines: list[str]) -> list[RawTextBlock]:
    blocks: list[RawTextBlock] = []
    y = 72.0
    step = 18.0
    for idx, line in enumerate(lines, start=1):
        text = " ".join(line.split())
        if not text:
            continue
        x0 = 42.0
        x1 = min(560.0, x0 + max(60.0, min(500.0, len(text) * 7.2)))
        y0 = y
        y1 = y + 13.0
        blocks.append(
            RawTextBlock(
                block_id=f"{page_id}_tb{idx:04d}",
                text=text,
                bbox=BBox(x0=x0, y0=y0, x1=x1, y1=y1),
            )
        )
        y += step
        if y > 800:
            break
    return blocks


def _normalize_text(text: str) -> str:
    t = " ".join(text.split())
    if not t:
        return ""
    repaired = _repair_mojibake_cp949_utf8(t)
    if _hangul_score(repaired) > _hangul_score(t):
        return repaired
    return t


def _repair_mojibake_cp949_utf8(text: str) -> str:
    try:
        return text.encode("cp949").decode("utf-8")
    except Exception:
        return text


def _hangul_score(text: str) -> int:
    return sum(1 for ch in text if "가" <= ch <= "힣")


def _is_meaningful(text: str) -> bool:
    if not text or (len(text) == 1 and text in {"(", ")", "*", ",", "."}):
        return False
    if re.fullmatch(r"[\W_]+", text):
        return False

    upper = text.upper()
    if upper in STYLE_TOKENS:
        return False
    if re.fullmatch(r"[A-Z0-9_#\.\-\s]+", text) and len(text) <= 24:
        return False

    return True

