"""PDF loading helpers."""

from __future__ import annotations

from pathlib import Path

import pdfplumber

from math_problem_pipeline.models.raw_models import SourceDocument


def open_pdf_document(pdf_path: Path) -> SourceDocument:
    """Read high-level metadata from a PDF file."""
    with pdfplumber.open(str(pdf_path)) as pdf:
        page_count = len(pdf.pages)
        metadata = pdf.metadata or {}

    return SourceDocument(
        document_id=pdf_path.stem,
        source_pdf=str(pdf_path),
        page_count=page_count,
        metadata=metadata,
    )
