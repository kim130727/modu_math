"""HWPX loading helpers."""

from __future__ import annotations

from pathlib import Path
import re
import zipfile

from math_problem_pipeline.models.raw_models import SourceDocument


def open_hwpx_document(hwpx_path: Path) -> SourceDocument:
    """Read high-level metadata from a HWPX file."""
    section_count = 0
    with zipfile.ZipFile(hwpx_path, "r") as zf:
        names = zf.namelist()
        # Count actual page sections only (exclude header.xml and other non-page XML files).
        section_count = len([n for n in names if re.fullmatch(r"Contents/section\d+\.xml", n)])
        if section_count == 0:
            section_count = len([n for n in names if n.startswith("Contents/") and n.endswith(".xml")])

    return SourceDocument(
        document_id=hwpx_path.stem,
        source_path=str(hwpx_path),
        page_count=max(section_count, 1),
        metadata={"format": "hwpx", "section_count": section_count},
    )