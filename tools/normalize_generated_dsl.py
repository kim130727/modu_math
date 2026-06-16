from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


DSL_IMPORT_LINE = (
    "from modu_math.dsl import Canvas, CircleSlot, LineSlot, PathSlot, PolygonSlot, "
    "ProblemTemplate, RectSlot, Region, TextBoxSlot, TextSlot"
)


def _to_node(value: object) -> ast.AST:
    return ast.parse(repr(value), mode="eval").body


def _literal(node: ast.AST | None) -> object | None:
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def write_report(path: Path, dsl_path: Path, errors: list[str]) -> None:
    payload = {
        "dsl_path": str(dsl_path),
        "ok": False,
        "errors": errors,
        "stage": "normalize_generated_dsl",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize generated DSL before validation.")
    parser.add_argument("--dsl", required=True, help="Path to *.dsl.py")
    parser.add_argument("--failure-report", required=False, help="Path to write failure report json")
    args = parser.parse_args()

    dsl_path = Path(args.dsl)
    if not dsl_path.exists():
        raise SystemExit(f"DSL not found: {dsl_path}")

    src = dsl_path.read_text(encoding="utf-8")
    changed = False

    if "from modu_math import ProblemTemplate" in src:
        src = src.replace("from modu_math import ProblemTemplate", DSL_IMPORT_LINE)
        changed = True

    dict_shape_errors: list[str] = []

    # Normalize Region kwargs: drop unsupported name, map kind->role.
    try:
        tree = ast.parse(src)
    except SyntaxError:
        tree = None
    if tree is not None:
        class _Fixer(ast.NodeTransformer):
            def visit_Call(self, node: ast.Call) -> ast.AST:  # noqa: N802
                self.generic_visit(node)
                if not isinstance(node.func, ast.Name):
                    return node

                func = node.func.id
                kw_map = {kw.arg: kw for kw in node.keywords if kw.arg}

                if func == "ProblemTemplate":
                    # canvas={...} -> Canvas(...)
                    if "canvas" in kw_map:
                        cval = kw_map["canvas"].value
                        lit = _literal(cval)
                        if isinstance(lit, dict):
                            width = lit.get("width", 760)
                            height = lit.get("height", 420)
                            mode = lit.get("coordinate_mode", "logical")
                            kw_map["canvas"].value = ast.Call(
                                func=ast.Name(id="Canvas", ctx=ast.Load()),
                                args=[],
                                keywords=[
                                    ast.keyword(arg="width", value=_to_node(width)),
                                    ast.keyword(arg="height", value=_to_node(height)),
                                    ast.keyword(arg="coordinate_mode", value=_to_node(mode)),
                                ],
                            )

                if func == "Region":
                    # normalize region signature: id, role, flow, slot_ids
                    if "name" in kw_map and "id" not in kw_map:
                        kw_map["name"].arg = "id"
                    if "kind" in kw_map and "role" not in kw_map:
                        kw_map["kind"].arg = "role"
                    if "type" in kw_map and "role" not in kw_map:
                        kw_map["type"].arg = "role"
                    if "id" not in kw_map:
                        node.keywords.append(ast.keyword(arg="id", value=_to_node("region.auto")))
                    if "role" not in kw_map:
                        node.keywords.append(ast.keyword(arg="role", value=_to_node("diagram")))
                    if "flow" not in kw_map:
                        node.keywords.append(ast.keyword(arg="flow", value=_to_node("absolute")))
                    if "slot_ids" not in kw_map:
                        node.keywords.append(ast.keyword(arg="slot_ids", value=_to_node(tuple())))
                    allowed = {"id", "role", "flow", "slot_ids"}
                    node.keywords = [kw for kw in node.keywords if kw.arg in allowed]

                if func.endswith("Slot"):
                    # normalize common legacy kwargs while preserving text content
                    if "name" in kw_map and "id" not in kw_map:
                        kw_map["name"].arg = "id"
                    if "w" in kw_map and "width" not in kw_map:
                        kw_map["w"].arg = "width"
                    if "h" in kw_map and "height" not in kw_map:
                        kw_map["h"].arg = "height"
                    if func == "CircleSlot":
                        if "x" in kw_map and "cx" not in kw_map:
                            kw_map["x"].arg = "cx"
                        if "y" in kw_map and "cy" not in kw_map:
                            kw_map["y"].arg = "cy"
                    if func == "PathSlot" and "path" in kw_map and "d" not in kw_map:
                        kw_map["path"].arg = "d"
                    if func == "TextSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        if "text" not in kw_map:
                            node.keywords.append(ast.keyword(arg="text", value=_to_node("")))
                        if "style_role" not in kw_map:
                            node.keywords.append(ast.keyword(arg="style_role", value=_to_node("diagram")))
                        allowed = {"id", "prompt", "text", "style_role", "x", "y", "font_size", "font_family", "anchor", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "TextBoxSlot":
                        allowed = {"id", "prompt", "text", "style_role", "x", "y", "width", "height", "font_size", "font_family", "align", "valign", "line_height", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "RectSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        allowed = {"id", "prompt", "x", "y", "width", "height", "stroke", "stroke_width", "rx", "ry", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "LineSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        allowed = {"id", "prompt", "x1", "y1", "x2", "y2", "stroke", "stroke_width", "stroke_dasharray", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "CircleSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        allowed = {"id", "prompt", "cx", "cy", "r", "stroke", "stroke_width", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "PolygonSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        allowed = {"id", "prompt", "points", "x", "y", "stroke", "stroke_width", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                    elif func == "PathSlot":
                        if "prompt" not in kw_map:
                            node.keywords.append(ast.keyword(arg="prompt", value=_to_node("")))
                        allowed = {"id", "prompt", "d", "x", "y", "stroke", "stroke_width", "stroke_dasharray", "fill", "semantic_role"}
                        node.keywords = [kw for kw in node.keywords if kw.arg in allowed]
                return node
        new_tree = _Fixer().visit(tree)
        ast.fix_missing_locations(new_tree)
        new_src = ast.unparse(new_tree) + "\n"
        if new_src != src:
            src = new_src
            changed = True

    if changed:
        dsl_path.write_text(src, encoding="utf-8", newline="\n")
        print(f"Normalized imports: {dsl_path}")

    if dict_shape_errors:
        if args.failure_report:
            write_report(Path(args.failure_report), dsl_path, dict_shape_errors)
            print(f"Wrote normalize failure report: {args.failure_report}")
        for err in dict_shape_errors:
            print(f"- {err}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
