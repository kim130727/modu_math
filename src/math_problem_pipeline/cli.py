"""Typer CLI for conservative HWPX -> raw -> semantic -> render pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import TypeAdapter

from math_problem_pipeline.compare.debug_report import build_schema_refinement_report, write_report
from math_problem_pipeline.extract.hwpx_extractor import extract_images_from_hwpx, extract_pages_from_hwpx
from math_problem_pipeline.extract.hwpx_reader import open_hwpx_document
from math_problem_pipeline.extract.problem_segmenter import (
    filter_obvious_non_problems,
    regions_to_candidates,
    segment_page_to_regions,
)
from math_problem_pipeline.models.problem_models import ProblemCandidate
from math_problem_pipeline.models.raw_models import SourcePage
from math_problem_pipeline.models.semantic_models import SemanticProblem
from math_problem_pipeline.normalize.semantic_builder import candidate_to_extracted, extracted_to_semantic
from math_problem_pipeline.normalize.validators import validate_candidate
from math_problem_pipeline.render.manim_renderer import render_problem_to_png
from math_problem_pipeline.render.svg_renderer import render_problem_to_svg
from math_problem_pipeline.utils.io import ensure_dir, list_json_files, read_json, write_json
from math_problem_pipeline.utils.logging_utils import setup_logger

app = typer.Typer(help="Math problem pipeline CLI")
logger = setup_logger(__name__)
semantic_adapter = TypeAdapter(SemanticProblem)


def _write_candidate_bundle(
    candidate: ProblemCandidate,
    flat_dir: Path,
    bundle_root: Path,
) -> None:
    """Write legacy flat raw.json and new per-problem bundle (raw.json only)."""
    write_json(flat_dir / f"{candidate.candidate_id}.raw.json", candidate.model_dump())

    bundle_dir = ensure_dir(bundle_root / candidate.candidate_id)
    write_json(bundle_dir / "raw.json", candidate.model_dump())


def _list_raw_candidate_files(raw_problem_dir: Path) -> list[Path]:
    """Support both flat *.raw.json and bundle */raw.json."""
    flat = list_json_files(raw_problem_dir)
    bundled = sorted(p for p in raw_problem_dir.glob("*/raw.json") if p.is_file())

    by_id: dict[str, Path] = {}
    for p in flat:
        by_id[p.stem.replace(".raw", "")] = p
    for p in bundled:
        candidate_id = p.parent.name
        by_id.setdefault(candidate_id, p)
    return sorted(by_id.values())


def _resolve_raw_candidate_path(raw_problem_dir: Path, problem_id: str) -> Path | None:
    flat = raw_problem_dir / f"{problem_id}.raw.json"
    if flat.exists():
        return flat
    bundled = raw_problem_dir / problem_id / "raw.json"
    if bundled.exists():
        return bundled
    return None


@app.command("parse-hwpx")
def parse_hwpx(
    hwpx_path: Path = typer.Argument(..., help="Input HWPX path"),
    output_dir: Path = typer.Option(Path("output/raw/pages"), help="Raw page JSON output dir"),
    images_dir: Path = typer.Option(Path("output/raw/images"), help="Raw image output dir"),
) -> None:
    """Stage 1: extract pages and image assets from HWPX."""
    doc = open_hwpx_document(hwpx_path)
    image_ids = extract_images_from_hwpx(hwpx_path, images_dir, doc.document_id)
    pages = extract_pages_from_hwpx(hwpx_path, doc.document_id, page_image_ids=image_ids)

    ensure_dir(output_dir)
    for page in pages:
        page_path = output_dir / f"{page.page_id}.json"
        write_json(page_path, page.model_dump())

    logger.info("Saved %d raw pages to %s (images=%d in %s)", len(pages), output_dir, len(image_ids), images_dir)


@app.command("segment-problems")
def segment_problems(
    raw_pages_dir: Path = typer.Option(Path("output/raw/pages"), help="Raw page JSON directory"),
    output_dir: Path = typer.Option(Path("output/raw/problems"), help="Problem candidate output dir"),
    rejected_output_dir: Path = typer.Option(Path("output/raw/rejected"), help="Rejected candidate output dir"),
) -> None:
    """Stages 2~4: segment -> candidate -> filter/reject obvious non-problems."""
    ensure_dir(output_dir)
    ensure_dir(rejected_output_dir)
    page_files = list_json_files(raw_pages_dir)
    accepted_total = 0
    rejected_total = 0

    for page_file in page_files:
        page = SourcePage.model_validate(read_json(page_file))
        regions = segment_page_to_regions(page)
        candidates = regions_to_candidates(regions, page)
        accepted, rejected = filter_obvious_non_problems(candidates)

        for candidate in accepted:
            _write_candidate_bundle(candidate, output_dir, output_dir)
            accepted_total += 1

        for candidate in rejected:
            _write_candidate_bundle(candidate, rejected_output_dir, rejected_output_dir)
            rejected_total += 1

    logger.info("Saved accepted=%d rejected=%d candidates", accepted_total, rejected_total)


@app.command("build-semantic")
def build_semantic(
    raw_problem_dir: Path = typer.Option(Path("output/raw/problems"), help="Raw problem JSON directory"),
    output_dir: Path = typer.Option(Path("output/semantic"), help="Semantic JSON output directory"),
    rejected_output_dir: Path = typer.Option(Path("output/semantic_rejected"), help="Rejected semantic output directory"),
) -> None:
    """Stages 5~7: classify conservatively -> build minimal semantic -> validate."""
    ensure_dir(output_dir)
    ensure_dir(rejected_output_dir)
    raw_files = _list_raw_candidate_files(raw_problem_dir)

    rejected = 0
    for raw_file in raw_files:
        candidate = ProblemCandidate.model_validate(read_json(raw_file))
        candidate.warnings.extend(validate_candidate(candidate))
        candidate.warnings = sorted(set(candidate.warnings))
        extracted = candidate_to_extracted(candidate)
        semantic = extracted_to_semantic(extracted)

        if semantic.type == "rejected_candidate":
            out = rejected_output_dir / f"{semantic.problem_id}.semantic.json"
            rejected += 1
        else:
            out = output_dir / f"{semantic.problem_id}.semantic.json"
        write_json(out, semantic.model_dump())

    logger.info("Built %d semantic problems (%d rejected)", len(raw_files), rejected)


@app.command("render-problem")
def render_problem(
    semantic_json: Path = typer.Argument(..., help="Semantic JSON file path"),
    output_dir: Path = typer.Option(Path("output/renders"), help="PNG output directory"),
    manim_media_dir: Path = typer.Option(Path("output/renders/.manim"), help="Manim temp media root"),
) -> None:
    """Render one semantic problem into static PNG (with scene-level fallback safety)."""
    ensure_dir(output_dir)
    semantic = semantic_adapter.validate_python(read_json(semantic_json))
    out_png = output_dir / f"{semantic.problem_id}.render.png"
    meta = render_problem_to_png(semantic, out_png, manim_media_dir)
    logger.info("Render result: %s", meta)


@app.command("render-svg")
def render_svg(
    semantic_json: Path = typer.Argument(..., help="Semantic JSON file path"),
    output_dir: Path = typer.Option(Path("output/svg"), help="SVG output directory"),
) -> None:
    """Render one semantic problem into standalone SVG for visual validation."""
    ensure_dir(output_dir)
    semantic = semantic_adapter.validate_python(read_json(semantic_json))
    out_svg = output_dir / f"{semantic.problem_id}.render.svg"
    meta = render_problem_to_svg(semantic, out_svg)
    logger.info("SVG render result: %s", meta)


@app.command("render-svg-all")
def render_svg_all(
    semantic_dir: Path = typer.Option(Path("output/semantic"), help="Semantic JSON directory"),
    output_dir: Path = typer.Option(Path("output/svg"), help="SVG output directory"),
) -> None:
    """Render all semantic problems into standalone SVG files."""
    ensure_dir(output_dir)
    files = list_json_files(semantic_dir)

    for f in files:
        semantic = semantic_adapter.validate_python(read_json(f))
        out_svg = output_dir / f"{semantic.problem_id}.render.svg"
        render_problem_to_svg(semantic, out_svg)

    logger.info("Rendered %d SVG files to %s", len(files), output_dir)


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
        raw_path = _resolve_raw_candidate_path(raw_problem_dir, semantic.problem_id)
        if raw_path is None:
            logger.warning("Missing raw problem for %s", semantic.problem_id)
            continue

        candidate = ProblemCandidate.model_validate(read_json(raw_path))
        render_png = render_dir / f"{semantic.problem_id}.render.png"
        render_meta = {
            "rendered": render_png.exists(),
            "output_png": str(render_png) if render_png.exists() else None,
            "used_fields": ["question_text", "type", "render_hint"],
            "fallback_render_used": "render_fallback" in " ".join(semantic.warnings),
        }

        report = build_schema_refinement_report(candidate, semantic, render_meta)
        report_path = report_dir / f"{semantic.problem_id}.report.json"
        write_report(report, report_path)
        count += 1

    logger.info("Wrote %d reports to %s", count, report_dir)


@app.command("run-pipeline")
def run_pipeline(
    hwpx_path: Path = typer.Argument(..., help="Input HWPX path"),
    output_root: Path = typer.Option(Path("output"), help="Root output directory"),
) -> None:
    """Single command conservative pipeline for HWPX."""
    raw_root = output_root / "raw"
    raw_pages_dir = raw_root / "pages"
    raw_images_dir = raw_root / "images"
    raw_problem_dir = raw_root / "problems"
    raw_rejected_dir = raw_root / "rejected"
    semantic_dir = output_root / "semantic"
    semantic_rejected_dir = output_root / "semantic_rejected"
    svg_dir = output_root / "svg"
    report_dir = output_root / "reports"

    for d in [raw_pages_dir, raw_images_dir, raw_problem_dir, raw_rejected_dir, semantic_dir, semantic_rejected_dir, svg_dir, report_dir]:
        ensure_dir(d)

    doc = open_hwpx_document(hwpx_path)
    image_ids = extract_images_from_hwpx(hwpx_path, raw_images_dir, doc.document_id)
    pages = extract_pages_from_hwpx(hwpx_path, doc.document_id, page_image_ids=image_ids)

    all_accepted: list[ProblemCandidate] = []
    all_rejected: list[ProblemCandidate] = []

    for page in pages:
        write_json(raw_pages_dir / f"{page.page_id}.json", page.model_dump())
        regions = segment_page_to_regions(page)
        candidates = regions_to_candidates(regions, page)
        accepted, rejected = filter_obvious_non_problems(candidates)
        all_accepted.extend(accepted)
        all_rejected.extend(rejected)

    for c in all_accepted:
        _write_candidate_bundle(c, raw_problem_dir, raw_problem_dir)
    for c in all_rejected:
        _write_candidate_bundle(c, raw_rejected_dir, raw_rejected_dir)

    for cand in [*all_accepted, *all_rejected]:
        cand.warnings.extend(validate_candidate(cand))
        cand.warnings = sorted(set(cand.warnings))
        extracted = candidate_to_extracted(cand)
        semantic = extracted_to_semantic(extracted)

        if semantic.type == "rejected_candidate":
            sem_path = semantic_rejected_dir / f"{semantic.problem_id}.semantic.json"
            render_meta = {"rendered": False, "fallback_render_used": False, "reason": "rejected_candidate"}
        else:
            sem_path = semantic_dir / f"{semantic.problem_id}.semantic.json"
            render_meta = render_problem_to_svg(
                semantic,
                svg_dir / f"{semantic.problem_id}.render.svg",
            )

        write_json(sem_path, semantic.model_dump())
        report = build_schema_refinement_report(cand, semantic, render_meta)
        write_report(report, report_dir / f"{semantic.problem_id}.report.json")

    logger.info(
        "Pipeline done: pages=%d accepted=%d rejected=%d semantic=%d images=%d",
        len(pages),
        len(all_accepted),
        len(all_rejected),
        len(all_accepted) + len(all_rejected),
        len(image_ids),
    )


@app.command("bootstrap-samples")
def bootstrap_samples(
    output_dir: Path = typer.Option(Path("input/sample_semantic"), help="Sample semantic JSON output directory"),
) -> None:
    """Write built-in sample semantic JSONs for the target problem types."""
    from math_problem_pipeline.samples import write_sample_semantics

    write_sample_semantics(output_dir)
    logger.info("Wrote sample semantic JSON files to %s", output_dir)


def main(argv: Optional[list[str]] = None) -> int:
    app(standalone_mode=False, args=argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
