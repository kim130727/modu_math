"""Typer CLI for PDF -> semantic JSON -> Manim pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import TypeAdapter

from math_problem_pipeline.compare.debug_report import build_schema_refinement_report, write_report
from math_problem_pipeline.extract.page_extractor import extract_pages
from math_problem_pipeline.extract.pdf_reader import open_pdf_document
from math_problem_pipeline.extract.problem_segmenter import regions_to_candidates, segment_page_to_regions
from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.raw_models import SourcePage
from math_problem_pipeline.models.semantic_models import SemanticProblem
from math_problem_pipeline.normalize.semantic_builder import candidate_to_extracted, extracted_to_semantic
from math_problem_pipeline.render.manim_renderer import render_problem_to_png
from math_problem_pipeline.utils.io import ensure_dir, list_json_files, read_json, write_json
from math_problem_pipeline.utils.logging_utils import setup_logger

app = typer.Typer(help="Math problem pipeline CLI")
logger = setup_logger(__name__)
semantic_adapter = TypeAdapter(SemanticProblem)


@app.command("parse-pdf")
def parse_pdf(
    pdf_path: Path = typer.Argument(..., help="Input PDF path"),
    output_dir: Path = typer.Option(Path("output/raw/pages"), help="Raw page JSON output dir"),
) -> None:
    """Read a PDF and save page-level raw extraction."""
    doc = open_pdf_document(pdf_path)
    pages = extract_pages(pdf_path, doc.document_id)

    ensure_dir(output_dir)
    for page in pages:
        page_path = output_dir / f"{page.page_id}.json"
        write_json(page_path, page.model_dump())

    logger.info("Saved %d raw pages to %s", len(pages), output_dir)


@app.command("segment-problems")
def segment_problems(
    raw_pages_dir: Path = typer.Option(Path("output/raw/pages"), help="Raw page JSON directory"),
    output_dir: Path = typer.Option(Path("output/raw/problems"), help="Problem candidate output dir"),
) -> None:
    """Segment raw page extractions into problem candidates."""
    ensure_dir(output_dir)
    page_files = list_json_files(raw_pages_dir)
    total = 0

    for page_file in page_files:
        page = SourcePage.model_validate(read_json(page_file))
        regions = segment_page_to_regions(page)
        candidates = regions_to_candidates(regions, page)

        for candidate in candidates:
            out = output_dir / f"{candidate.candidate_id}.raw.json"
            write_json(out, candidate.model_dump())
            total += 1

    logger.info("Saved %d problem candidates to %s", total, output_dir)


@app.command("build-semantic")
def build_semantic(
    raw_problem_dir: Path = typer.Option(Path("output/raw/problems"), help="Raw problem JSON directory"),
    output_dir: Path = typer.Option(Path("output/semantic"), help="Semantic JSON output directory"),
) -> None:
    """Build semantic JSON from problem candidates."""
    ensure_dir(output_dir)
    raw_files = list_json_files(raw_problem_dir)

    for raw_file in raw_files:
        candidate = ProblemCandidate.model_validate(read_json(raw_file))
        extracted = candidate_to_extracted(candidate)
        semantic = extracted_to_semantic(extracted)
        out = output_dir / f"{semantic.problem_id}.semantic.json"
        write_json(out, semantic.model_dump())

    logger.info("Built %d semantic problems to %s", len(raw_files), output_dir)


@app.command("render-problem")
def render_problem(
    semantic_json: Path = typer.Argument(..., help="Semantic JSON file path"),
    output_dir: Path = typer.Option(Path("output/renders"), help="PNG output directory"),
    manim_media_dir: Path = typer.Option(Path("output/renders/.manim"), help="Manim temp media root"),
) -> None:
    """Render one semantic problem into static PNG."""
    ensure_dir(output_dir)
    semantic = semantic_adapter.validate_python(read_json(semantic_json))
    out_png = output_dir / f"{semantic.problem_id}.render.png"
    meta = render_problem_to_png(semantic, out_png, manim_media_dir)
    logger.info("Render result: %s", meta)


@app.command("render-all")
def render_all(
    semantic_dir: Path = typer.Option(Path("output/semantic"), help="Semantic JSON directory"),
    output_dir: Path = typer.Option(Path("output/renders"), help="PNG output directory"),
    manim_media_dir: Path = typer.Option(Path("output/renders/.manim"), help="Manim temp media root"),
) -> None:
    """Render all semantic problems in a folder."""
    ensure_dir(output_dir)
    files = list_json_files(semantic_dir)
    success = 0

    for f in files:
        semantic = semantic_adapter.validate_python(read_json(f))
        out_png = output_dir / f"{semantic.problem_id}.render.png"
        meta = render_problem_to_png(semantic, out_png, manim_media_dir)
        if meta.get("rendered"):
            success += 1

    logger.info("Rendered %d/%d problems", success, len(files))


@app.command("debug-compare")
def debug_compare(
    semantic_dir: Path = typer.Option(Path("output/semantic"), help="Semantic JSON directory"),
    raw_problem_dir: Path = typer.Option(Path("output/raw/problems"), help="Raw problem JSON directory"),
    render_dir: Path = typer.Option(Path("output/renders"), help="Render output directory"),
    report_dir: Path = typer.Option(Path("output/reports"), help="Report output directory"),
) -> None:
    """Generate schema refinement report JSONs."""
    ensure_dir(report_dir)

    semantic_files = list_json_files(semantic_dir)
    count = 0
    for semantic_file in semantic_files:
        semantic = semantic_adapter.validate_python(read_json(semantic_file))
        raw_path = raw_problem_dir / f"{semantic.problem_id}.raw.json"
        if not raw_path.exists():
            logger.warning("Missing raw problem for %s", semantic.problem_id)
            continue

        candidate = ProblemCandidate.model_validate(read_json(raw_path))
        render_png = render_dir / f"{semantic.problem_id}.render.png"
        render_meta = {
            "rendered": render_png.exists(),
            "output_png": str(render_png) if render_png.exists() else None,
            "used_fields": ["question_text", "type", "render_hint"],
        }

        report = build_schema_refinement_report(candidate, semantic, render_meta)
        report_path = report_dir / f"{semantic.problem_id}.report.json"
        write_report(report, report_path)
        count += 1

    logger.info("Wrote %d reports to %s", count, report_dir)


@app.command("bootstrap-samples")
def bootstrap_samples(
    output_dir: Path = typer.Option(Path("input/sample_semantic"), help="Sample semantic JSON output directory"),
) -> None:
    """Write built-in sample semantic JSONs for the six target problem types."""
    from math_problem_pipeline.samples import write_sample_semantics

    write_sample_semantics(output_dir)
    logger.info("Wrote sample semantic JSON files to %s", output_dir)


def main(argv: Optional[list[str]] = None) -> int:
    app(standalone_mode=False, args=argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
