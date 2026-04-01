"""Page-level raw extraction from PDF."""

from __future__ import annotations

from pathlib import Path

import pdfplumber

from math_problem_pipeline.models.raw_models import BBox, RawTextBlock, RawVisualBlock, SourcePage


def extract_pages(pdf_path: Path, document_id: str) -> list[SourcePage]:
    """Extract text/visual blocks for each page.

    TODO: Improve visual extraction precision for curves and grouped paths.
    """
    pages: list[SourcePage] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_id = f"{document_id}_p{i:04d}"
            text_blocks = _extract_text_blocks(page_id, page)
            visual_blocks = _extract_visual_blocks(page_id, page)
            pages.append(
                SourcePage(
                    page_id=page_id,
                    document_id=document_id,
                    source_pdf=str(pdf_path),
                    page_number=i,
                    width=float(page.width),
                    height=float(page.height),
                    text_blocks=text_blocks,
                    visual_blocks=visual_blocks,
                )
            )
    return pages


def _extract_text_blocks(page_id: str, page: pdfplumber.page.Page) -> list[RawTextBlock]:
    words = page.extract_words() or []
    blocks: list[RawTextBlock] = []
    for idx, word in enumerate(words, start=1):
        block_id = f"{page_id}_tb{idx:04d}"
        blocks.append(
            RawTextBlock(
                block_id=block_id,
                text=word.get("text", ""),
                bbox=BBox(
                    x0=float(word.get("x0", 0.0)),
                    y0=float(word.get("top", 0.0)),
                    x1=float(word.get("x1", 0.0)),
                    y1=float(word.get("bottom", 0.0)),
                ),
            )
        )
    return blocks


def _extract_visual_blocks(page_id: str, page: pdfplumber.page.Page) -> list[RawVisualBlock]:
    visuals: list[RawVisualBlock] = []

    for idx, rect in enumerate(page.rects or [], start=1):
        visuals.append(
            RawVisualBlock(
                block_id=f"{page_id}_vb_rect_{idx:04d}",
                kind="rect",
                bbox=BBox(
                    x0=float(rect.get("x0", 0.0)),
                    y0=float(rect.get("top", 0.0)),
                    x1=float(rect.get("x1", 0.0)),
                    y1=float(rect.get("bottom", 0.0)),
                ),
                payload={"linewidth": rect.get("linewidth")},
            )
        )

    for idx, line in enumerate(page.lines or [], start=1):
        x0 = float(line.get("x0", 0.0))
        y0 = float(line.get("top", 0.0))
        x1 = float(line.get("x1", x0))
        y1 = float(line.get("bottom", y0))
        visuals.append(
            RawVisualBlock(
                block_id=f"{page_id}_vb_line_{idx:04d}",
                kind="line",
                bbox=BBox(x0=min(x0, x1), y0=min(y0, y1), x1=max(x0, x1), y1=max(y0, y1)),
                payload={"x0": x0, "y0": y0, "x1": x1, "y1": y1},
            )
        )

    return visuals
