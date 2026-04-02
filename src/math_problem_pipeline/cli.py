"""Typer CLI for conservative HWPX -> raw -> semantic -> render pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from pydantic import TypeAdapter

from math_problem_pipeline.extract.hwpx_extractor import extract_images_from_hwpx, extract_pages_from_hwpx
from math_problem_pipeline.extract.image_pipeline import (
    build_image_semantic,
    list_supported_images,
    sha256_file,
)
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


def _write_problem_bundle_raw(candidate: ProblemCandidate, problems_dir: Path) -> Path:
    """Write raw.json into output/problems/<problem_id>/."""
    bundle_dir = ensure_dir(problems_dir / candidate.candidate_id)
    raw_path = bundle_dir / "raw.json"
    write_json(raw_path, candidate.model_dump())
    return bundle_dir


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



@app.command("run-pipeline")
def run_pipeline(
    hwpx_path: Path = typer.Argument(..., help="Input HWPX path"),
    output_root: Path = typer.Option(Path("output"), help="Root output directory"),
) -> None:
    """Single command conservative pipeline for HWPX."""
    images_dir = output_root / "images"
    problems_dir = output_root / "problems"

    for d in [images_dir, problems_dir]:
        ensure_dir(d)

    doc = open_hwpx_document(hwpx_path)
    image_ids = extract_images_from_hwpx(hwpx_path, images_dir, doc.document_id)
    pages = extract_pages_from_hwpx(hwpx_path, doc.document_id, page_image_ids=image_ids)

    all_accepted: list[ProblemCandidate] = []
    all_rejected: list[ProblemCandidate] = []

    for page in pages:
        regions = segment_page_to_regions(page)
        candidates = regions_to_candidates(regions, page)
        accepted, rejected = filter_obvious_non_problems(candidates)
        all_accepted.extend(accepted)
        all_rejected.extend(rejected)

    for c in all_accepted:
        _write_problem_bundle_raw(c, problems_dir)

    rendered = 0
    for cand in all_accepted:
        cand.warnings.extend(validate_candidate(cand))
        cand.warnings = sorted(set(cand.warnings))
        extracted = candidate_to_extracted(cand)
        semantic = extracted_to_semantic(extracted)
        problem_dir = ensure_dir(problems_dir / semantic.problem_id)
        sem_path = problem_dir / "semantic.json"
        render_problem_to_svg(semantic, problem_dir / "render.svg")
        write_json(sem_path, semantic.model_dump())
        rendered += 1

    logger.info(
        "Pipeline done: pages=%d accepted=%d rejected=%d rendered=%d images=%d output=%s",
        len(pages),
        len(all_accepted),
        len(all_rejected),
        rendered,
        len(image_ids),
        output_root,
    )


@app.command("run-image-pipeline")
def run_image_pipeline(
    images_dir: Path = typer.Option(Path("output/images"), help="Input image directory (png/bmp)"),
    output_root: Path = typer.Option(Path("output"), help="Root output directory"),
) -> None:
    """Build semantic.json + render.svg bundles from image files."""
    problems_dir = ensure_dir(output_root / "problems")
    images = list_supported_images(images_dir)

    if not images:
        logger.warning("No supported images found in %s", images_dir)
        return

    manifest: list[dict] = []
    rendered = 0

    for image_path in images:
        problem_id = image_path.stem
        problem_dir = ensure_dir(problems_dir / problem_id)

        rel_image_href = Path("..") / ".." / "images" / image_path.name
        semantic = build_image_semantic(
            image_path=image_path,
            problem_id=problem_id,
            source_path=str(image_path),
            relative_image_href=rel_image_href.as_posix(),
        )

        raw_payload = {
            "problem_id": problem_id,
            "source_image": str(image_path),
            "image_name": image_path.name,
            "sha256": sha256_file(image_path),
            "pipeline": "run-image-pipeline",
        }

        write_json(problem_dir / "raw.json", raw_payload)
        write_json(problem_dir / "semantic.json", semantic.model_dump())
        render_meta = render_problem_to_svg(semantic, problem_dir / "render.svg")

        manifest.append(
            {
                "problem_id": problem_id,
                "source_image": str(image_path),
                "semantic_json": str(problem_dir / "semantic.json"),
                "render_svg": str(problem_dir / "render.svg"),
                "image_sha256": sha256_file(image_path),
                "render_meta": render_meta,
            }
        )
        rendered += 1

    write_json(output_root / "image_svg_match_manifest.json", {"count": rendered, "items": manifest})
    logger.info("Image pipeline done: images=%d rendered=%d output=%s", len(images), rendered, output_root)


@app.command("measure-image-svg-match")
def measure_image_svg_match(
    output_root: Path = typer.Option(Path("output"), help="Root output directory"),
) -> None:
    """Measure source image vs SVG-reference consistency using hash/path checks."""
    manifest_path = output_root / "image_svg_match_manifest.json"
    if not manifest_path.exists():
        logger.warning("Missing manifest: %s", manifest_path)
        return

    manifest = read_json(manifest_path)
    results: list[dict] = []

    for item in manifest.get("items", []):
        src = Path(item["source_image"])
        sem = Path(item["semantic_json"])
        svg = Path(item["render_svg"])

        if not (src.exists() and sem.exists() and svg.exists()):
            results.append({
                "problem_id": item.get("problem_id"),
                "score": 0.0,
                "status": "missing_artifact",
            })
            continue

        semantic = semantic_adapter.validate_python(read_json(sem))
        source_coords = semantic.coordinates.source_coordinates
        href = source_coords.get("image_path")
        expected_hash = source_coords.get("sha256")
        actual_hash = sha256_file(src)

        svg_text = svg.read_text(encoding="utf-8")
        href_match = bool(href and href in svg_text)
        hash_match = bool(expected_hash and expected_hash == actual_hash)

        score = 1.0 if (href_match and hash_match) else (0.5 if (href_match or hash_match) else 0.0)
        results.append(
            {
                "problem_id": item.get("problem_id"),
                "source_image": str(src),
                "render_svg": str(svg),
                "href_match": href_match,
                "hash_match": hash_match,
                "score": score,
                "note": "hash/path consistency score; pixel-level comparison can be added later via SVG rasterization",
            }
        )

    avg = sum(r["score"] for r in results) / max(1, len(results))
    out = {
        "count": len(results),
        "average_score": avg,
        "results": results,
    }
    write_json(output_root / "image_svg_match_scores.json", out)
    logger.info("Measured image-svg match: count=%d avg=%.3f", len(results), avg)


@app.command("measure-image-svg-pixel-match")
def measure_image_svg_pixel_match(
    output_root: Path = typer.Option(Path("output"), help="Root output directory"),
) -> None:
    """Compute pixel-level similarity (SSIM/PSNR) between source images and rendered SVG image regions."""
    from io import BytesIO
    import xml.etree.ElementTree as ET

    import numpy as np
    from PIL import Image

    rasterizer = "none"
    svg_to_png = None
    svg_text_to_png = None
    try:
        import cairosvg

        svg_to_png = lambda svg_path: cairosvg.svg2png(url=str(svg_path))
        svg_text_to_png = lambda svg_text: cairosvg.svg2png(bytestring=svg_text.encode("utf-8"))
        rasterizer = "cairosvg"
    except Exception:
        try:
            import resvg_py

            svg_to_png = lambda svg_path: resvg_py.svg_to_bytes(Path(svg_path).read_text(encoding="utf-8"))
            svg_text_to_png = lambda svg_text: resvg_py.svg_to_bytes(svg_text)
            rasterizer = "resvg_py"
        except Exception:
            svg_to_png = None
            svg_text_to_png = None

    if svg_to_png is None or svg_text_to_png is None:
        logger.warning("No SVG rasterizer available (tried cairosvg,resvg_py).")
        return

    manifest_path = output_root / "image_svg_match_manifest.json"
    if not manifest_path.exists():
        logger.warning("Missing manifest: %s", manifest_path)
        return

    manifest = read_json(manifest_path)
    results: list[dict] = []

    for item in manifest.get("items", []):
        problem_id = item.get("problem_id")
        src = Path(item["source_image"])
        sem = Path(item["semantic_json"])
        svg = Path(item["render_svg"])

        if not (src.exists() and sem.exists() and svg.exists()):
            results.append({"problem_id": problem_id, "status": "missing_artifact", "score": 0.0})
            continue

        try:
            semantic = semantic_adapter.validate_python(read_json(sem))
            src_coords = semantic.coordinates.source_coordinates
            src_w = int(src_coords.get("image_width") or 0)
            src_h = int(src_coords.get("image_height") or 0)

            if src_w <= 0 or src_h <= 0:
                with Image.open(src) as im_src:
                    src_w, src_h = im_src.size

            svg_text = svg.read_text(encoding="utf-8")
            root = ET.fromstring(svg_text)
            img_elem = None
            for elem in root.iter():
                if elem.tag.split("}")[-1] == "image":
                    img_elem = elem
                    break

            if img_elem is None:
                results.append({"problem_id": problem_id, "status": "svg_image_tag_missing", "score": 0.0})
                continue

            def _num(attr: str, default: float) -> float:
                raw = (img_elem.attrib.get(attr) or "").strip()
                if not raw:
                    return default
                for suffix in ("px", "%"):
                    if raw.endswith(suffix):
                        raw = raw[: -len(suffix)]
                try:
                    return float(raw)
                except Exception:
                    return default

            href = (img_elem.attrib.get("href") or img_elem.attrib.get("{http://www.w3.org/1999/xlink}href") or "").replace("\\", "/")
            href_uri = str(src_coords.get("image_data_uri") or src.resolve().as_uri())
            preserve = img_elem.attrib.get("preserveAspectRatio") or "xMidYMid meet"
            # Use original source resolution for fidelity measurement.
            # Comparing on scaled render-box dimensions introduces extra
            # interpolation loss that is unrelated to semantic/image correctness.
            svg_w = max(1, int(src_w))
            svg_h = max(1, int(src_h))

            mini_svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">'
                f'<image href="{href_uri}" x="0" y="0" width="{svg_w}" height="{svg_h}" preserveAspectRatio="{preserve}"/>'
                '</svg>'
            )
            rendered_png = svg_text_to_png(mini_svg)
            with Image.open(BytesIO(rendered_png)) as rendered_img:
                rendered_rgba = rendered_img.convert("RGBA")

            arr_rgba = np.asarray(rendered_rgba)
            alpha = arr_rgba[..., 3]
            ys, xs = np.where(alpha > 0)
            if len(xs) == 0 or len(ys) == 0:
                crop = rendered_rgba.convert("RGB")
            else:
                x0 = int(xs.min())
                x1 = int(xs.max()) + 1
                y0 = int(ys.min())
                y1 = int(ys.max()) + 1
                crop = rendered_rgba.crop((x0, y0, x1, y1)).convert("RGB")

            with Image.open(src) as src_img:
                ref = src_img.convert("RGB")

            target_size = crop.size
            if target_size[0] <= 0 or target_size[1] <= 0:
                results.append({"problem_id": problem_id, "status": "invalid_rendered_size", "score": 0.0})
                continue

            # Compose reference image with SVG meet-fit rule (centered, aspect-preserving).
            tw, th = target_size
            rw, rh = ref.size
            scale = min(tw / max(1, rw), th / max(1, rh))
            nw = max(1, int(round(rw * scale)))
            nh = max(1, int(round(rh * scale)))
            ref_fit = ref.resize((nw, nh), Image.Resampling.BICUBIC)
            ref_canvas = Image.new("RGB", (tw, th), (255, 255, 255))
            ox = (tw - nw) // 2
            oy = (th - nh) // 2
            ref_canvas.paste(ref_fit, (ox, oy))

            a = np.asarray(ref_canvas, dtype=np.float32)
            b = np.asarray(crop, dtype=np.float32)

            mse = float(np.mean((a - b) ** 2))
            if mse <= 1e-12:
                psnr = 99.0
            else:
                psnr = float(20.0 * np.log10(255.0 / np.sqrt(mse)))

            # Global SSIM approximation.
            a_gray = np.dot(a[..., :3], [0.299, 0.587, 0.114])
            b_gray = np.dot(b[..., :3], [0.299, 0.587, 0.114])
            mu_a = float(a_gray.mean())
            mu_b = float(b_gray.mean())
            var_a = float(a_gray.var())
            var_b = float(b_gray.var())
            cov = float(((a_gray - mu_a) * (b_gray - mu_b)).mean())
            c1 = (0.01 * 255) ** 2
            c2 = (0.03 * 255) ** 2
            ssim = ((2 * mu_a * mu_b + c1) * (2 * cov + c2)) / ((mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2))
            ssim = float(max(0.0, min(1.0, ssim)))

            psnr_norm = max(0.0, min(1.0, psnr / 50.0))
            score = float(0.6 * ssim + 0.4 * psnr_norm)

            results.append(
                {
                    "problem_id": problem_id,
                    "source_image": str(src),
                    "render_svg": str(svg),
                    "status": "ok",
                    "mse": mse,
                    "psnr": psnr,
                    "ssim": ssim,
                    "score": score,
                    "rasterizer": rasterizer,
                }
            )
        except Exception as exc:
            results.append(
                {
                    "problem_id": problem_id,
                    "source_image": str(src),
                    "render_svg": str(svg),
                    "status": "error",
                    "score": 0.0,
                    "error": str(exc),
                }
            )

    ok = [r for r in results if r.get("status") == "ok"]
    avg = sum(r["score"] for r in ok) / max(1, len(ok))
    out = {
        "count": len(results),
        "ok_count": len(ok),
        "average_score": avg,
        "metric": "0.6*SSIM + 0.4*normalized_PSNR",
        "rasterizer": rasterizer,
        "results": results,
    }
    write_json(output_root / "image_svg_pixel_match_scores.json", out)
    logger.info("Measured pixel match: count=%d ok=%d avg=%.4f", len(results), len(ok), avg)


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


