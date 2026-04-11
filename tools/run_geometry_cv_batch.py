from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from modu_semantic.semantic_json_builder import make_answer_svg

from cv_pointmap_to_generated import apply_point_map_to_generated
from geometry_cv_refine import detect_geometry, write_overlay


def _build_answer_svg(folder: Path, problem_id: str) -> None:
    svg_path = folder / f"{problem_id}.svg"
    semantic_path = folder / f"{problem_id}.semantic.json"
    answer_svg_path = folder / f"{problem_id}.answer.svg"
    if not svg_path.exists() or not semantic_path.exists():
        return
    svg_text = svg_path.read_text(encoding="utf-8")
    semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
    answer_svg_path.write_text(make_answer_svg(svg_text, semantic, font_size=56), encoding="utf-8")


def _run_generated_py(folder: Path, problem_id: str) -> tuple[bool, str]:
    generated = folder / f"{problem_id}.generated.py"
    if not generated.exists():
        return False, f"missing generated.py: {generated}"
    proc = subprocess.run(
        [sys.executable, str(generated)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout).strip()
        return False, message or f"exit code {proc.returncode}"
    return True, ""


def _sanitize_generated_py(folder: Path, problem_id: str) -> tuple[bool, str]:
    generated = folder / f"{problem_id}.generated.py"
    if not generated.exists():
        return False, f"missing generated.py: {generated}"
    text = generated.read_text(encoding="utf-8")
    patterns = [
        r"^\s*font_family\s*=.*,\r?\n",
        r"^\s*font_weight\s*=.*,\r?\n",
        r"^\s*anchor\s*=.*,\r?\n",
        r"^\s*alignment\s*=.*,\r?\n",
        r"^\s*group\s*=.*,\r?\n",
        r"^\s*z_index\s*=.*,\r?\n",
    ]
    patched = text
    for pat in patterns:
        patched = re.sub(pat, "", patched, flags=re.MULTILINE)
    if patched != text:
        generated.write_text(patched, encoding="utf-8")
        return True, "sanitized unsupported kwargs"
    return True, "no changes"


def _dedupe_generated_add_blocks(folder: Path, problem_id: str) -> tuple[bool, str]:
    generated = folder / f"{problem_id}.generated.py"
    if not generated.exists():
        return False, f"missing generated.py: {generated}"

    text = generated.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    chunks: list[tuple[str, str | None, list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "p.add(" not in line:
            chunks.append(("raw", None, [line]))
            i += 1
            continue

        block: list[str] = [line]
        depth = line.count("(") - line.count(")")
        i += 1
        while i < len(lines) and depth > 0:
            cur = lines[i]
            block.append(cur)
            depth += cur.count("(") - cur.count(")")
            i += 1

        block_text = "".join(block)
        m = re.search(r'id\s*=\s*"([^"]+)"', block_text)
        elem_id = m.group(1) if m else None
        chunks.append(("add", elem_id, block))

    last_idx_by_id: dict[str, int] = {}
    for idx, (kind, elem_id, _block) in enumerate(chunks):
        if kind == "add" and elem_id:
            last_idx_by_id[elem_id] = idx

    removed = 0
    out_lines: list[str] = []
    for idx, (kind, elem_id, block) in enumerate(chunks):
        if kind == "add" and elem_id:
            if last_idx_by_id.get(elem_id) != idx:
                removed += 1
                continue
        out_lines.extend(block)

    patched = "".join(out_lines)
    if patched != text:
        generated.write_text(patched, encoding="utf-8")
        return True, f"deduped add blocks: {removed}"
    return True, "no duplicate add blocks"


def _apply_point_map_if_exists(folder: Path, problem_id: str, mapping_dir: Path) -> tuple[bool, str]:
    generated = folder / f"{problem_id}.generated.py"
    if not generated.exists():
        return False, "generated.py not found"

    mapping_path = mapping_dir / f"{problem_id}.json"
    if not mapping_path.exists():
        return False, "mapping not found"

    payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return False, f"invalid mapping json: {mapping_path}"

    points: dict[str, tuple[float, float]] = {}
    for key, value in payload.items():
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            continue
        points[str(key)] = (float(value[0]), float(value[1]))
    if not points:
        return False, "mapping has no usable points"

    original = generated.read_text(encoding="utf-8")
    patched = apply_point_map_to_generated(original, points)
    generated.write_text(patched, encoding="utf-8")
    return True, f"patched with {len(points)} points"


def _run_one(
    folder: Path,
    problem_id: str,
    *,
    mapping_dir: Path,
    do_detect: bool,
    do_patch: bool,
    do_execute: bool,
    do_answer: bool,
) -> dict[str, Any]:
    result: dict[str, Any] = {"problem_id": problem_id, "folder": str(folder)}

    img = folder / "img_diagram.png"
    cv_json = folder / "img_diagram.cv.json"
    cv_overlay = folder / "img_diagram.cv.overlay.png"

    if do_detect:
        if img.exists():
            try:
                data = detect_geometry(img)
                cv_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                write_overlay(img, data, cv_overlay)
                result["cv_detect"] = "ok"
                result["cv_lines"] = len(data.get("lines", []))
                result["cv_intersections"] = len(data.get("intersections", []))
            except Exception as exc:  # noqa: BLE001
                result["cv_detect"] = f"error: {exc}"
        else:
            result["cv_detect"] = "skip: no img_diagram.png"

    if do_patch:
        ok, msg = _apply_point_map_if_exists(folder, problem_id, mapping_dir)
        result["patch"] = "ok" if ok else f"skip: {msg}"

    if do_execute:
        san_ok, san_msg = _sanitize_generated_py(folder, problem_id)
        result["sanitize"] = "ok" if san_ok else f"error: {san_msg}"
        dedupe_ok, dedupe_msg = _dedupe_generated_add_blocks(folder, problem_id)
        result["dedupe"] = "ok" if dedupe_ok else f"error: {dedupe_msg}"
        result["dedupe_detail"] = dedupe_msg
        ok, msg = _run_generated_py(folder, problem_id)
        result["execute"] = "ok" if ok else f"error: {msg}"
    else:
        result["execute"] = "skip"

    if do_answer:
        try:
            _build_answer_svg(folder, problem_id)
            result["answer_svg"] = "ok"
        except Exception as exc:  # noqa: BLE001
            result["answer_svg"] = f"error: {exc}"

    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Batch geometry cv refine + generated.py execute pipeline.")
    parser.add_argument("--root", default="examples/problem/_semantic_build/geometry3k")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--mapping-dir", default="examples/problem/_semantic_build/geometry3k/_point_maps")
    parser.add_argument("--no-detect", action="store_true")
    parser.add_argument("--no-patch", action="store_true")
    parser.add_argument("--no-execute", action="store_true")
    parser.add_argument("--no-answer", action="store_true")
    parser.add_argument("--report", default=None, help="Optional output report path.")
    args = parser.parse_args(argv)

    root = Path(args.root)
    mapping_dir = Path(args.mapping_dir)

    results: list[dict[str, Any]] = []
    for pid in range(args.start, args.end + 1):
        name = f"{pid:04d}"
        folder = root / name
        if not folder.exists():
            results.append({"problem_id": name, "status": "skip: folder not found"})
            continue
        results.append(
            _run_one(
                folder,
                name,
                mapping_dir=mapping_dir,
                do_detect=not args.no_detect,
                do_patch=not args.no_patch,
                do_execute=not args.no_execute,
                do_answer=not args.no_answer,
            )
        )

    ok_count = sum(1 for r in results if r.get("execute") == "ok")
    payload = {
        "range": {"start": args.start, "end": args.end},
        "root": str(root),
        "mapping_dir": str(mapping_dir),
        "summary": {"total": len(results), "execute_ok": ok_count},
        "results": results,
    }

    if args.report:
        report_path = Path(args.report)
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = root / f"cv_batch_report_{args.start}_{args.end}_{stamp}.json"
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"report: {report_path}")
    print(f"execute_ok: {ok_count}/{len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
