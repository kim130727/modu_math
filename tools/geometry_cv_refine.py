from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

try:
    import cv2
except ModuleNotFoundError as exc:  # pragma: no cover
    cv2 = None
    _CV2_IMPORT_ERROR = exc
else:
    _CV2_IMPORT_ERROR = None


def _segment_length(seg: tuple[int, int, int, int]) -> float:
    x1, y1, x2, y2 = seg
    return math.hypot(x2 - x1, y2 - y1)


def _line_angle_deg(seg: tuple[int, int, int, int]) -> float:
    x1, y1, x2, y2 = seg
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if angle < 0:
        angle += 180.0
    return angle


def _intersection(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
) -> tuple[float, float] | None:
    x1, y1, x2, y2 = a
    x3, y3, x4, y4 = b
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-8:
        return None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den

    # Segment-only intersection to avoid far-away infinite-line intersections.
    def _in_range(v: float, a0: float, a1: float, pad: float = 2.0) -> bool:
        lo, hi = (a0, a1) if a0 <= a1 else (a1, a0)
        return (lo - pad) <= v <= (hi + pad)

    if not (_in_range(px, x1, x2) and _in_range(py, y1, y2) and _in_range(px, x3, x4) and _in_range(py, y3, y4)):
        return None
    return (px, py)


def _within_image(pt: tuple[float, float], w: int, h: int, pad: float = 4.0) -> bool:
    x, y = pt
    return -pad <= x <= (w + pad) and -pad <= y <= (h + pad)


def _dedupe_points(points: list[tuple[float, float]], eps: float = 6.0) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for p in points:
        if not any(math.hypot(p[0] - q[0], p[1] - q[1]) <= eps for q in out):
            out.append(p)
    return out


def _dedupe_segments(
    segments: list[tuple[int, int, int, int]],
    *,
    angle_eps: float = 3.5,
    mid_eps: float = 40.0,
) -> list[tuple[int, int, int, int]]:
    kept: list[tuple[int, int, int, int]] = []
    for seg in sorted(segments, key=_segment_length, reverse=True):
        x1, y1, x2, y2 = seg
        ang = _line_angle_deg(seg)
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        duplicate = False
        for ref in kept:
            rx1, ry1, rx2, ry2 = ref
            rang = _line_angle_deg(ref)
            diff = abs(ang - rang)
            diff = min(diff, 180.0 - diff)
            rmx = (rx1 + rx2) / 2.0
            rmy = (ry1 + ry2) / 2.0
            md = math.hypot(mx - rmx, my - rmy)
            if diff <= angle_eps and md <= mid_eps:
                duplicate = True
                break
        if not duplicate:
            kept.append(seg)
    return kept


def _clip_segment_to_circle(
    seg: tuple[int, int, int, int],
    circle: tuple[float, float, float],
    *,
    pad: float = 1.5,
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    x1, y1, x2, y2 = map(float, seg)
    cx, cy, r = circle
    rr = max(0.0, r + pad)

    dx = x2 - x1
    dy = y2 - y1
    fx = x1 - cx
    fy = y1 - cy

    a = dx * dx + dy * dy
    if a <= 1e-8:
        d2 = (x1 - cx) ** 2 + (y1 - cy) ** 2
        if d2 <= rr * rr:
            p = (int(round(x1)), int(round(y1)))
            return p, p
        return None

    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - rr * rr
    disc = b * b - 4.0 * a * c

    inside1 = (x1 - cx) ** 2 + (y1 - cy) ** 2 <= rr * rr
    inside2 = (x2 - cx) ** 2 + (y2 - cy) ** 2 <= rr * rr

    ts: list[float] = []
    if inside1:
        ts.append(0.0)
    if inside2:
        ts.append(1.0)

    if disc >= 0.0:
        root = math.sqrt(disc)
        t1 = (-b - root) / (2.0 * a)
        t2 = (-b + root) / (2.0 * a)
        if 0.0 <= t1 <= 1.0:
            ts.append(t1)
        if 0.0 <= t2 <= 1.0:
            ts.append(t2)

    if len(ts) < 2:
        return None

    ts = sorted(ts)
    t_start = ts[0]
    t_end = ts[-1]
    if t_end - t_start <= 1e-6:
        return None

    px1 = x1 + dx * t_start
    py1 = y1 + dy * t_start
    px2 = x1 + dx * t_end
    py2 = y1 + dy * t_end
    return (int(round(px1)), int(round(py1))), (int(round(px2)), int(round(py2)))


def detect_geometry(
    image_path: Path,
    *,
    canny1: int = 60,
    canny2: int = 160,
    hough_thresh: int = 45,
    min_line_len: int = 36,
    max_line_gap: int = 12,
    circle_dp: float = 1.3,
    circle_min_dist: int = 80,
    circle_param2: int = 40,
    circle_min_radius: int = 60,
    circle_max_radius: int = 0,
    max_circles: int = 2,
) -> dict[str, Any]:
    if cv2 is None:
        raise RuntimeError(
            "OpenCV (cv2) is not installed. Install it with: pip install opencv-python"
        ) from _CV2_IMPORT_ERROR
    bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, canny1, canny2)

    raw_lines = cv2.HoughLinesP(
        edges,
        rho=1.0,
        theta=np.pi / 180.0,
        threshold=hough_thresh,
        minLineLength=min_line_len,
        maxLineGap=max_line_gap,
    )
    segments: list[tuple[int, int, int, int]] = []
    if raw_lines is not None:
        for item in raw_lines:
            x1, y1, x2, y2 = item[0]
            seg = (int(x1), int(y1), int(x2), int(y2))
            if _segment_length(seg) >= min_line_len:
                segments.append(seg)

    # Keep a compact set of strongest lines by length.
    segments = sorted(segments, key=_segment_length, reverse=True)[:80]
    segments = _dedupe_segments(segments)
    segments = segments[:20]

    max_r = circle_max_radius if circle_max_radius > 0 else min(w, h) // 2
    circles_raw = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=circle_dp,
        minDist=circle_min_dist,
        param1=140,
        param2=circle_param2,
        minRadius=circle_min_radius,
        maxRadius=max_r,
    )
    circles: list[tuple[float, float, float]] = []
    if circles_raw is not None:
        for c in circles_raw[0]:
            circles.append((float(c[0]), float(c[1]), float(c[2])))
        circles = sorted(circles, key=lambda c: c[2], reverse=True)
        filtered: list[tuple[float, float, float]] = []
        for c in circles:
            cx, cy, r = c
            if any(math.hypot(cx - fx, cy - fy) < max(18.0, min(r, fr) * 0.45) for fx, fy, fr in filtered):
                continue
            filtered.append(c)
            if len(filtered) >= max_circles:
                break
        circles = filtered

    intersections: list[tuple[float, float]] = []
    right_angle_candidates: list[dict[str, Any]] = []
    for i in range(len(segments)):
        a = segments[i]
        ang_a = _line_angle_deg(a)
        for j in range(i + 1, len(segments)):
            b = segments[j]
            ang_b = _line_angle_deg(b)
            diff = abs(ang_a - ang_b)
            diff = min(diff, 180.0 - diff)
            p = _intersection(a, b)
            if p is None or not _within_image(p, w, h):
                continue
            intersections.append(p)
            if abs(diff - 90.0) <= 8.0:
                right_angle_candidates.append(
                    {
                        "point": [round(p[0], 3), round(p[1], 3)],
                        "angle_diff": round(diff, 3),
                        "line_i": i,
                        "line_j": j,
                    }
                )

    intersections = _dedupe_points(intersections, eps=8.0)

    return {
        "image": {"path": str(image_path), "width": w, "height": h},
        "lines": [
            {
                "id": idx,
                "x1": s[0],
                "y1": s[1],
                "x2": s[2],
                "y2": s[3],
                "length": round(_segment_length(s), 3),
                "angle_deg": round(_line_angle_deg(s), 3),
            }
            for idx, s in enumerate(segments)
        ],
        "circles": [
            {"id": idx, "cx": round(c[0], 3), "cy": round(c[1], 3), "r": round(c[2], 3)}
            for idx, c in enumerate(circles)
        ],
        "intersections": [{"x": round(x, 3), "y": round(y, 3)} for x, y in intersections],
        "right_angle_candidates": right_angle_candidates[:40],
    }


def write_overlay(
    image_path: Path,
    data: dict[str, Any],
    out_path: Path,
) -> None:
    if cv2 is None:
        return
    bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if bgr is None:
        return

    for circle in data.get("circles", []):
        c = (int(circle["cx"]), int(circle["cy"]))
        r = int(circle["r"])
        cv2.circle(bgr, c, r, (255, 120, 0), 2, cv2.LINE_AA)
        cv2.circle(bgr, c, 2, (255, 120, 0), -1, cv2.LINE_AA)

    main_circle: tuple[float, float, float] | None = None
    circles = data.get("circles", [])
    if isinstance(circles, list) and circles:
        first = circles[0]
        if isinstance(first, dict):
            main_circle = (float(first["cx"]), float(first["cy"]), float(first["r"]))

    for line in data.get("lines", []):
        seg = (int(line["x1"]), int(line["y1"]), int(line["x2"]), int(line["y2"]))
        if main_circle is not None:
            clipped = _clip_segment_to_circle(seg, main_circle)
            if clipped is None:
                continue
            p1, p2 = clipped
        else:
            p1 = (seg[0], seg[1])
            p2 = (seg[2], seg[3])
        cv2.line(bgr, p1, p2, (0, 160, 255), 2, cv2.LINE_AA)

    for p in data.get("intersections", []):
        c = (int(p["x"]), int(p["y"]))
        cv2.circle(bgr, c, 3, (0, 0, 255), -1, cv2.LINE_AA)

    for cand in data.get("right_angle_candidates", [])[:12]:
        x, y = cand["point"]
        c = (int(x), int(y))
        cv2.circle(bgr, c, 5, (255, 0, 255), 2, cv2.LINE_AA)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), bgr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect geometry primitives (lines/circles/intersections) with OpenCV.")
    parser.add_argument("--image", required=True, help="Input image path (png/jpg).")
    parser.add_argument("--out-json", default=None, help="Output JSON path. Defaults to <image>.cv.json")
    parser.add_argument("--out-overlay", default=None, help="Optional overlay preview image path.")
    args = parser.parse_args(argv)

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if cv2 is None:
        raise RuntimeError("OpenCV (cv2) is not installed. Install it with: pip install opencv-python")

    data = detect_geometry(image_path)

    out_json = Path(args.out_json) if args.out_json else image_path.with_suffix(".cv.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"cv json: {out_json}")

    if args.out_overlay:
        out_overlay = Path(args.out_overlay)
        write_overlay(image_path, data, out_overlay)
        print(f"overlay: {out_overlay}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
