from __future__ import annotations

import json
from difflib import unified_diff
from pathlib import Path
from typing import Any

from modu_semantic.ir import Circle, Formula, Line, Polygon, Rect, Text
from modu_semantic.problem import Problem


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    return float(value)


def build_problem_from_semantic(semantic_data: dict[str, Any]) -> tuple[Problem, list[str]]:
    render = semantic_data.get("render", {})
    canvas = render.get("canvas", {})

    problem = Problem(
        width=to_float(canvas.get("width"), 0.0),
        height=to_float(canvas.get("height"), 0.0),
        background=str(canvas.get("background", "#F6F6F6")),
        problem_id=str(semantic_data.get("problem_id", "custom")),
        problem_type=str(semantic_data.get("problem_type", "custom")),
    )

    warnings: list[str] = []
    elements = sorted(render.get("elements", []), key=lambda e: e.get("z_index", 0))

    for index, el in enumerate(elements):
        etype = el.get("type")
        element_id = el.get("id") or f"auto_{index}_{etype}"
        common = {
            "id": str(element_id),
            "group": el.get("group"),
            "z_index": int(el.get("z_index", 0)),
            "anchor": el.get("anchor", "start"),
            "alignment": el.get("alignment", "left"),
            "semantic_role": el.get("semantic_role"),
            "stroke": el.get("stroke"),
            "stroke_width": el.get("stroke_width"),
            "fill": el.get("fill"),
            "font_family": el.get("font_family", "Malgun Gothic"),
            "font_size": el.get("font_size"),
            "font_weight": el.get("font_weight", "normal"),
        }

        if etype == "rect":
            problem.add(
                Rect(
                    **common,
                    x=to_float(el.get("x")),
                    y=to_float(el.get("y")),
                    width=to_float(el.get("width")),
                    height=to_float(el.get("height")),
                    rx=el.get("rx"),
                    ry=el.get("ry"),
                )
            )
        elif etype == "circle":
            problem.add(Circle(**common, x=to_float(el.get("x")), y=to_float(el.get("y")), r=to_float(el.get("r"))))
        elif etype == "line":
            problem.add(
                Line(
                    **common,
                    x1=to_float(el.get("x1")),
                    y1=to_float(el.get("y1")),
                    x2=to_float(el.get("x2")),
                    y2=to_float(el.get("y2")),
                )
            )
        elif etype == "polygon":
            problem.add(Polygon(**common, points=[tuple(p) for p in el.get("points", [])]))
        elif etype == "text":
            problem.add(Text(**common, x=to_float(el.get("x")), y=to_float(el.get("y")), text=str(el.get("text", ""))))
        elif etype == "formula":
            expr = el.get("expr")
            if expr is None and "text" in el:
                expr = el.get("text")
            problem.add(
                Formula(**common, x=to_float(el.get("x")), y=to_float(el.get("y")), expr=str(expr or ""))
            )
        else:
            warnings.append(f"Unsupported element type skipped: {etype} (id={element_id})")

    return problem, warnings


def flatten_json(data: Any, path: str = "$") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    if isinstance(data, dict):
        if not data:
            flat[path] = {}
            return flat
        for key, value in data.items():
            flat.update(flatten_json(value, f"{path}.{key}"))
        return flat

    if isinstance(data, list):
        if not data:
            flat[path] = []
            return flat
        for idx, value in enumerate(data):
            flat.update(flatten_json(value, f"{path}[{idx}]"))
        return flat

    flat[path] = data
    return flat


def compare_json_fields(reference: dict[str, Any], generated: dict[str, Any]) -> dict[str, Any]:
    ref_flat = flatten_json(reference)
    gen_flat = flatten_json(generated)
    all_paths = sorted(set(ref_flat.keys()) | set(gen_flat.keys()))

    rows: list[dict[str, Any]] = []
    same = 0
    different = 0
    missing_in_generated = 0
    missing_in_reference = 0

    for path in all_paths:
        ref_exists = path in ref_flat
        gen_exists = path in gen_flat

        if ref_exists and gen_exists:
            ref_val = ref_flat[path]
            gen_val = gen_flat[path]
            if ref_val == gen_val:
                status = "same"
                same += 1
            else:
                status = "different"
                different += 1
            rows.append({"path": path, "status": status, "reference": ref_val, "generated": gen_val})
            continue

        if ref_exists:
            missing_in_generated += 1
            rows.append(
                {"path": path, "status": "missing_in_generated", "reference": ref_flat[path], "generated": None}
            )
        else:
            missing_in_reference += 1
            rows.append(
                {"path": path, "status": "missing_in_reference", "reference": None, "generated": gen_flat[path]}
            )

    return {
        "summary": {
            "total_fields": len(all_paths),
            "same": same,
            "different": different,
            "missing_in_generated": missing_in_generated,
            "missing_in_reference": missing_in_reference,
        },
        "diffs": rows,
    }


def to_markdown_report(title: str, diff_result: dict[str, Any]) -> str:
    summary = diff_result["summary"]
    lines = [
        f"# {title}",
        "",
        "## Summary",
        f"- total_fields: {summary['total_fields']}",
        f"- same: {summary['same']}",
        f"- different: {summary['different']}",
        f"- missing_in_generated: {summary['missing_in_generated']}",
        f"- missing_in_reference: {summary['missing_in_reference']}",
        "",
        "## Field Diff (non-same)",
        "| path | status | reference | generated |",
        "|---|---|---|---|",
    ]

    for row in diff_result["diffs"]:
        if row["status"] == "same":
            continue
        reference = json.dumps(row["reference"], ensure_ascii=False)
        generated = json.dumps(row["generated"], ensure_ascii=False)
        lines.append(f"| `{row['path']}` | {row['status']} | `{reference}` | `{generated}` |")

    return "\n".join(lines) + "\n"


def svg_diff_report(reference_svg: str, generated_svg: str) -> str:
    diff_lines = list(
        unified_diff(
            reference_svg.splitlines(),
            generated_svg.splitlines(),
            fromfile="reference_semantic_final.svg",
            tofile="generated_semantic.svg",
            lineterm="",
        )
    )
    if not diff_lines:
        return "# SVG Diff Report\n\nNo differences.\n"
    return "# SVG Diff Report\n\n```diff\n" + "\n".join(diff_lines) + "\n```\n"


def run_problem_diff_report(problem_id: str) -> dict[str, Any]:
    base = Path(f"examples/problem/{problem_id}")
    target_root = Path(f"tests/problem/{problem_id}")
    out_dir = target_root / "generated"
    report_dir = target_root / "report"

    reference_semantic = load_json(base / "json/semantic_final/semantic_final.json")
    reference_layout = load_json(base / "json/layout_final/layout_final.json")
    reference_svg = (base / "svg/final/semantic_final.svg").read_text(encoding="utf-8")

    problem, warnings = build_problem_from_semantic(reference_semantic)

    generated_semantic = problem.to_semantic_json(validate=False)
    generated_layout = problem.to_layout_json()
    generated_svg = problem.to_svg()

    write_json(out_dir / f"{problem_id}.semantic.generated.json", generated_semantic)
    write_json(out_dir / f"{problem_id}.layout.generated.json", generated_layout)
    write_text(out_dir / f"{problem_id}.semantic.generated.svg", generated_svg)

    semantic_diff = compare_json_fields(reference_semantic, generated_semantic)
    layout_diff = compare_json_fields(reference_layout, generated_layout)

    write_json(report_dir / "semantic_diff.json", semantic_diff)
    write_json(report_dir / "layout_diff.json", layout_diff)
    write_text(report_dir / "semantic_diff.md", to_markdown_report("Semantic JSON Diff Report", semantic_diff))
    write_text(report_dir / "layout_diff.md", to_markdown_report("Layout JSON Diff Report", layout_diff))
    write_text(report_dir / "svg_diff.md", svg_diff_report(reference_svg, generated_svg))

    summary = {
        "warnings": warnings,
        "outputs": {
            "semantic": str(out_dir / f"{problem_id}.semantic.generated.json"),
            "layout": str(out_dir / f"{problem_id}.layout.generated.json"),
            "svg": str(out_dir / f"{problem_id}.semantic.generated.svg"),
        },
        "reports": {
            "semantic": str(report_dir / "semantic_diff.md"),
            "layout": str(report_dir / "layout_diff.md"),
            "svg": str(report_dir / "svg_diff.md"),
        },
        "summary": {
            "semantic": semantic_diff["summary"],
            "layout": layout_diff["summary"],
        },
    }
    write_json(report_dir / "run_summary.json", summary)
    return summary

