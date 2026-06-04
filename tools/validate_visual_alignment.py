from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _norm(s: str) -> str:
    s = s.replace(" ", "")
    s = re.sub(r"\s+", "", s)
    return s.strip()


def _extract_backtick_texts(vision_text: str) -> list[str]:
    return [m.strip() for m in re.findall(r"`([^`]+)`", vision_text) if m.strip()]


def _collect_layout_texts(layout: dict) -> list[str]:
    out: list[str] = []
    for slot in layout.get("slots", []):
        if slot.get("kind") != "text":
            continue
        content = slot.get("content", {})
        text = content.get("text")
        if isinstance(text, str) and text.strip():
            out.append(text.strip())
    return out


def _collect_shape_counts(layout: dict) -> dict[str, int]:
    counts = {"rect": 0, "line": 0, "circle": 0, "path": 0, "polygon": 0}
    for slot in layout.get("slots", []):
        k = slot.get("kind")
        if k in counts:
            counts[k] += 1
    return counts


def main() -> int:
    p = argparse.ArgumentParser(description="Validate visual alignment between vision_draft and generated layout json.")
    p.add_argument("--vision-draft", required=True)
    p.add_argument("--layout-json", required=True)
    p.add_argument("--report", required=False)
    p.add_argument("--min-text-hit-ratio", type=float, default=0.55)
    args = p.parse_args()

    vision_path = Path(args.vision_draft)
    layout_path = Path(args.layout_json)
    if not vision_path.exists():
        raise SystemExit(f"vision draft not found: {vision_path}")
    if not layout_path.exists():
        raise SystemExit(f"layout json not found: {layout_path}")

    vision = _read(vision_path)
    layout = json.loads(_read(layout_path))

    expected_texts = _extract_backtick_texts(vision)
    layout_texts = _collect_layout_texts(layout)
    layout_texts_norm = [_norm(t) for t in layout_texts]

    matched: list[str] = []
    missing: list[str] = []
    for t in expected_texts:
        nt = _norm(t)
        ok = any((nt in lt) or (lt in nt) for lt in layout_texts_norm)
        if ok:
            matched.append(t)
        else:
            missing.append(t)

    hit_ratio = 1.0 if not expected_texts else len(matched) / len(expected_texts)

    shapes = _collect_shape_counts(layout)
    notes: list[str] = []
    if "박스" in vision and shapes["rect"] < 1:
        notes.append("Vision mentions box but no rect slot detected.")
    if ("가로줄" in vision or "가로선" in vision) and shapes["line"] < 1:
        notes.append("Vision mentions horizontal line but no line slot detected.")

    ok = hit_ratio >= args.min_text_hit_ratio and not notes
    report = {
        "ok": ok,
        "vision_draft": str(vision_path),
        "layout_json": str(layout_path),
        "text_hit_ratio": hit_ratio,
        "expected_text_count": len(expected_texts),
        "matched_text_count": len(matched),
        "missing_texts": missing[:40],
        "shape_counts": shapes,
        "notes": notes,
    }

    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not ok:
        print(f"Visual alignment failed: hit_ratio={hit_ratio:.2f}, notes={len(notes)}")
        return 2
    print(f"Visual alignment ok: hit_ratio={hit_ratio:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

