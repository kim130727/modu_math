"""Split source PDF into one-problem-per-file PDFs using segmented bboxes."""

from __future__ import annotations

from pathlib import Path

import pdfplumber

from math_problem_pipeline.extract.page_extractor import extract_pages
from math_problem_pipeline.extract.pdf_reader import open_pdf_document
from math_problem_pipeline.extract.problem_segmenter import regions_to_candidates, segment_page_to_regions
from math_problem_pipeline.utils.io import ensure_dir
from math_problem_pipeline.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


def split_pdf_into_problem_pdfs(
    pdf_path: Path,
    output_dir: Path,
    padding: float = 6.0,
    resolution: int = 220,
) -> list[Path]:
    """Split one PDF into per-problem cropped PDF files.

    Cropping is bbox-based from segmented candidates and exported as image-based
    single-page PDFs for quick visual verification.
    """
    doc = open_pdf_document(pdf_path)
    source_pages = extract_pages(pdf_path, doc.document_id)
    candidates = []
    for page in source_pages:
        regions = segment_page_to_regions(page)
        candidates.extend(regions_to_candidates(regions, page))

    ensure_dir(output_dir)
    written: list[Path] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for candidate in candidates:
            page = pdf.pages[candidate.page_number - 1]
            x0 = max(0.0, candidate.bbox.x0 - padding)
            y0 = max(0.0, candidate.bbox.y0 - padding)
            x1 = min(float(page.width), candidate.bbox.x1 + padding)
            y1 = min(float(page.height), candidate.bbox.y1 + padding)

            if x1 <= x0 or y1 <= y0:
                logger.warning("Skipping invalid bbox for %s", candidate.candidate_id)
                continue

            cropped = page.crop((x0, y0, x1, y1))
            img = cropped.to_image(resolution=resolution).original.convert("RGB")
            out_pdf = output_dir / f"{candidate.candidate_id}.pdf"
            img.save(out_pdf, "PDF", resolution=resolution)
            written.append(out_pdf)

    return written
