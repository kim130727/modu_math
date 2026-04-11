from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _parse_label_indices(raw: str) -> dict[str, int]:
    # Example: "A:0,B:3,C:7,D:9"
    out: dict[str, int] = {}
    if not raw.strip():
        return out
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if ":" not in token:
            raise ValueError(f"Invalid label mapping token: {token!r}. Use LABEL:INDEX.")
        label, idx = token.split(":", 1)
        label = label.strip()
        if not label:
            raise ValueError(f"Empty label in token: {token!r}")
        out[label] = int(idx.strip())
    return out


def _load_point_map(
    *,
    point_map_json: Path | None,
    cv_json: Path | None,
    label_indices: dict[str, int],
) -> dict[str, tuple[float, float]]:
    if point_map_json is not None:
        payload = json.loads(point_map_json.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("--point-map-json must be a JSON object.")
        out: dict[str, tuple[float, float]] = {}
        for k, v in payload.items():
            if not isinstance(v, (list, tuple)) or len(v) != 2:
                continue
            out[str(k)] = (float(v[0]), float(v[1]))
        return out

    if cv_json is None:
        raise ValueError("Either --point-map-json or --cv-json must be provided.")
    if not label_indices:
        raise ValueError("When using --cv-json, you must provide --label-indices.")

    payload = json.loads(cv_json.read_text(encoding="utf-8"))
    intersections = payload.get("intersections", [])
    if not isinstance(intersections, list):
        raise ValueError("cv-json has invalid 'intersections' format.")

    out: dict[str, tuple[float, float]] = {}
    for label, idx in label_indices.items():
        if idx < 0 or idx >= len(intersections):
            raise ValueError(f"Intersection index out of range for label {label}: {idx}")
        pt = intersections[idx]
        if not isinstance(pt, dict) or "x" not in pt or "y" not in pt:
            raise ValueError(f"Invalid intersection record at index {idx}")
        out[label] = (float(pt["x"]), float(pt["y"]))
    return out


def _patch_point_dict_entries(content: str, label: str, x: float, y: float) -> str:
    # Patches entries like: "A": (123.0, 456.0) or 'A': (123.0, 456.0)
    pat = re.compile(
        rf"((['\"])({re.escape(label)})\2\s*:\s*)\(\s*[-+]?\d+(?:\.\d+)?\s*,\s*[-+]?\d+(?:\.\d+)?\s*\)"
    )
    return pat.sub(rf"\1({x:.6f}, {y:.6f})", content)


def _patch_lowercase_tuple_assign(content: str, label: str, x: float, y: float) -> str:
    # Patches variable assignments like: a = (123.0, 456.0)
    var = label.lower()
    pat = re.compile(
        rf"(^\s*{re.escape(var)}\s*=\s*)\(\s*[-+]?\d+(?:\.\d+)?\s*,\s*[-+]?\d+(?:\.\d+)?\s*\)",
        re.MULTILINE,
    )
    return pat.sub(rf"\1({x:.6f}, {y:.6f})", content)


def apply_point_map_to_generated(content: str, point_map: dict[str, tuple[float, float]]) -> str:
    patched = content
    for label, (x, y) in point_map.items():
        patched = _patch_point_dict_entries(patched, label, x, y)
        patched = _patch_lowercase_tuple_assign(patched, label, x, y)
    return patched


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply labeled point map to a generated geometry Python file.")
    parser.add_argument("--generated-py", required=True, help="Path to target generated.py")
    parser.add_argument(
        "--point-map-json",
        default=None,
        help="Optional JSON object: {\"A\": [x, y], \"B\": [x, y], ...}",
    )
    parser.add_argument(
        "--cv-json",
        default=None,
        help="Optional cv-json from geometry_cv_refine.py (uses intersections[]).",
    )
    parser.add_argument(
        "--label-indices",
        default="",
        help='Mapping from labels to intersections index, e.g. "A:0,B:3,C:7,D:9".',
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Write result to --generated-py directly. If omitted, writes <name>.patched.py",
    )
    args = parser.parse_args(argv)

    generated_py = Path(args.generated_py)
    if not generated_py.exists():
        raise FileNotFoundError(f"Generated file not found: {generated_py}")

    point_map_json = Path(args.point_map_json) if args.point_map_json else None
    cv_json = Path(args.cv_json) if args.cv_json else None
    labels = _parse_label_indices(args.label_indices)
    point_map = _load_point_map(point_map_json=point_map_json, cv_json=cv_json, label_indices=labels)
    if not point_map:
        raise ValueError("No usable points found.")

    original = generated_py.read_text(encoding="utf-8")
    patched = apply_point_map_to_generated(original, point_map)

    if args.in_place:
        out_path = generated_py
    else:
        out_path = generated_py.with_name(f"{generated_py.stem}.patched{generated_py.suffix}")

    out_path.write_text(patched, encoding="utf-8")
    print(f"patched: {out_path}")
    print(f"points: {sorted(point_map.keys())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
