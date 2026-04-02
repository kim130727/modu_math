"""Heuristic image structure analyzer for semantic pre-structuring.

This MVP focuses on layout decomposition (text/diagram/table/choice-like blocks)
without external OCR/model dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass
class Region:
    x: int
    y: int
    w: int
    h: int
    kind: str
    score: float


def analyze_image_structure(image_path: Path) -> dict:
    with Image.open(image_path) as im:
        rgb = im.convert("RGB")
        gray = np.asarray(rgb.convert("L"), dtype=np.uint8)

    h, w = gray.shape
    if h <= 1 or w <= 1:
        return {
            "version": "mvp-1",
            "image_size": {"width": int(w), "height": int(h)},
            "regions": [],
            "summary": {
                "region_count": 0,
                "has_choice_like_layout": False,
                "has_diagram_like_region": False,
                "has_table_like_region": False,
                "estimated_problem_layout": "unknown",
            },
        }

    # Robust threshold from bright percentile to separate ink from paper.
    bright = float(np.percentile(gray, 85))
    thr = min(245.0, max(170.0, bright - 25.0))
    ink = gray < thr

    # Horizontal projection and smoothing.
    row_density = ink.mean(axis=1)
    kernel = np.ones(9, dtype=np.float32) / 9.0
    row_smooth = np.convolve(row_density, kernel, mode="same")

    row_thr = max(0.008, float(np.percentile(row_smooth, 55) * 0.7))
    active_rows = row_smooth > row_thr
    row_runs = _runs_from_bool(active_rows, min_len=max(4, h // 200), merge_gap=max(4, h // 250))

    regions: list[Region] = []
    for y0, y1 in row_runs:
        band = ink[y0 : y1 + 1, :]
        col_density = band.mean(axis=0)
        col_smooth = np.convolve(col_density, np.ones(7, dtype=np.float32) / 7.0, mode="same")
        col_thr = max(0.01, float(np.percentile(col_smooth, 50) * 0.8))
        active_cols = col_smooth > col_thr
        col_runs = _runs_from_bool(active_cols, min_len=max(8, w // 220), merge_gap=max(6, w // 260))

        for x0, x1 in col_runs:
            ww = x1 - x0 + 1
            hh = y1 - y0 + 1
            if ww * hh < max(120, (w * h) // 1400):
                continue

            patch = ink[y0 : y1 + 1, x0 : x1 + 1]
            kind, score = _classify_patch(patch, w, h)
            regions.append(Region(x=x0, y=y0, w=ww, h=hh, kind=kind, score=score))

    regions = _merge_similar_regions(regions, w, h)
    regions = sorted(regions, key=lambda r: (r.y, r.x))

    kinds = [r.kind for r in regions]
    has_choices = _detect_choice_like(regions, w)
    has_diagram = "diagram_like" in kinds
    has_table = "table_like" in kinds

    if has_choices and has_diagram:
        layout = "mixed_text_choices_diagram"
    elif has_choices:
        layout = "text_with_choices"
    elif has_diagram:
        layout = "text_with_diagram"
    elif has_table:
        layout = "table_or_chart"
    elif regions:
        layout = "text_dominant"
    else:
        layout = "unknown"

    return {
        "version": "mvp-1",
        "image_size": {"width": int(w), "height": int(h)},
        "regions": [
            {
                "bbox": {
                    "x": int(r.x),
                    "y": int(r.y),
                    "width": int(r.w),
                    "height": int(r.h),
                },
                "bbox_norm": {
                    "x": round(r.x / w, 5),
                    "y": round(r.y / h, 5),
                    "width": round(r.w / w, 5),
                    "height": round(r.h / h, 5),
                },
                "kind": r.kind,
                "confidence": round(float(r.score), 4),
            }
            for r in regions
        ],
        "summary": {
            "region_count": len(regions),
            "has_choice_like_layout": bool(has_choices),
            "has_diagram_like_region": bool(has_diagram),
            "has_table_like_region": bool(has_table),
            "estimated_problem_layout": layout,
        },
    }


def _runs_from_bool(mask: np.ndarray, min_len: int, merge_gap: int) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    n = int(mask.shape[0])
    i = 0
    while i < n:
        if not bool(mask[i]):
            i += 1
            continue
        j = i
        while j + 1 < n and bool(mask[j + 1]):
            j += 1
        if (j - i + 1) >= min_len:
            runs.append((i, j))
        i = j + 1

    if not runs:
        return runs

    merged = [runs[0]]
    for s, e in runs[1:]:
        ps, pe = merged[-1]
        if s - pe <= merge_gap:
            merged[-1] = (ps, e)
        else:
            merged.append((s, e))
    return merged


def _classify_patch(patch: np.ndarray, full_w: int, full_h: int) -> tuple[str, float]:
    ph, pw = patch.shape
    area_ratio = (pw * ph) / max(1.0, full_w * full_h)
    ink_ratio = float(patch.mean())
    aspect = pw / max(1.0, ph)

    gx = np.abs(np.diff(patch.astype(np.int16), axis=1)).mean() if pw > 1 else 0.0
    gy = np.abs(np.diff(patch.astype(np.int16), axis=0)).mean() if ph > 1 else 0.0
    edge_density = float((gx + gy) / 2.0)

    row_var = float(patch.mean(axis=1).var()) if ph > 1 else 0.0
    col_var = float(patch.mean(axis=0).var()) if pw > 1 else 0.0

    # table-like: broader area + strong line regularity.
    if area_ratio > 0.04 and (row_var > 0.015 and col_var > 0.015) and edge_density > 0.04:
        return "table_like", min(0.98, 0.55 + edge_density * 2.0)

    # diagram-like: dense ink and edge-rich but not a thin text strip.
    if ink_ratio > 0.08 and edge_density > 0.05 and ph > full_h * 0.07 and pw > full_w * 0.12:
        return "diagram_like", min(0.97, 0.5 + edge_density * 2.0)

    # choice-like: medium width compact blocks near left side often list entries.
    if pw < full_w * 0.55 and ph < full_h * 0.16 and aspect > 1.5 and ink_ratio < 0.22:
        return "choice_like", 0.65

    # default text block.
    if aspect >= 2.0 and ph < full_h * 0.18:
        return "text_block", 0.7

    return "other", 0.5


def _merge_similar_regions(regions: list[Region], full_w: int, full_h: int) -> list[Region]:
    if not regions:
        return regions

    regions = sorted(regions, key=lambda r: (r.y, r.x))
    out: list[Region] = []
    y_gap = max(6, full_h // 180)
    x_overlap_min = max(10, full_w // 30)

    for r in regions:
        if not out:
            out.append(r)
            continue
        p = out[-1]
        overlap = max(0, min(p.x + p.w, r.x + r.w) - max(p.x, r.x))
        close = abs(r.y - (p.y + p.h)) <= y_gap
        same_kind = p.kind == r.kind or {p.kind, r.kind} <= {"text_block", "choice_like"}

        if same_kind and close and overlap >= x_overlap_min:
            nx = min(p.x, r.x)
            ny = min(p.y, r.y)
            nr = max(p.x + p.w, r.x + r.w)
            nb = max(p.y + p.h, r.y + r.h)
            nk = p.kind if p.kind == r.kind else "text_block"
            ns = max(p.score, r.score)
            out[-1] = Region(x=nx, y=ny, w=nr - nx, h=nb - ny, kind=nk, score=ns)
        else:
            out.append(r)

    return out


def _detect_choice_like(regions: list[Region], full_w: int) -> bool:
    candidates = [r for r in regions if r.kind == "choice_like" and r.x < int(full_w * 0.35)]
    if len(candidates) >= 3:
        return True

    # fallback: repeated text blocks with similar widths in a vertical stack
    text_blocks = [r for r in regions if r.kind == "text_block" and r.w < int(full_w * 0.65)]
    if len(text_blocks) < 3:
        return False

    text_blocks = sorted(text_blocks, key=lambda r: r.y)
    streak = 1
    for i in range(1, len(text_blocks)):
        a = text_blocks[i - 1]
        b = text_blocks[i]
        similar_w = abs(a.w - b.w) <= max(12, int(full_w * 0.05))
        gap = b.y - (a.y + a.h)
        regular_gap = 0 <= gap <= max(24, int(full_w * 0.03))
        if similar_w and regular_gap:
            streak += 1
            if streak >= 3:
                return True
        else:
            streak = 1
    return False
