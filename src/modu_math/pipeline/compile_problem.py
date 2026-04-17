from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..semantic.models.problem import SemanticProblem
from ..semantic.validate import load_and_validate
from ..layout.models.canvas import LayoutCanvas
from ..layout.models.node import LayoutNode
from ..layout.diff import apply_layout_diff
from ..editor.models.state import EditorState
from ..renderer.svg.render import render_svg
from ..adapters.json.semantic_json import problem_to_semantic_json

def compile_problem_pipeline(
    problem: SemanticProblem, 
    canvas: LayoutCanvas, 
    nodes: list[LayoutNode], 
    out_prefix: str | Path,
    layout_patches: list[dict[str, Any]] | None = None,
    editor_state: EditorState | None = None
) -> None:
    """End-to-end pipeline to compile a problem and save standard outputs."""
    out_prefix = Path(out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Output semantic JSON
    semantic_json = problem_to_semantic_json(problem)
    semantic_path = out_prefix.with_suffix(".semantic.json")
    with open(semantic_path, "w", encoding="utf-8") as f:
        json.dump(semantic_json, f, ensure_ascii=False, indent=2)

    # Apply layout patches if provided before exporting layout and SVG
    if layout_patches:
        apply_layout_diff(nodes, layout_patches)
        
        # Optionally save the layout diff for debugging or persistence
        diff_json = {
            "problem_id": problem.problem_id,
            "patches": layout_patches
        }
        diff_path = out_prefix.with_suffix(".layout.diff.json")
        with open(diff_path, "w", encoding="utf-8") as f:
            json.dump(diff_json, f, ensure_ascii=False, indent=2)

    # 2. Output layout JSON
    layout_json = {
        "problem_id": problem.problem_id,
        "canvas": canvas.to_dict(),
        "nodes": [n.to_dict() for n in nodes]
    }
    layout_path = out_prefix.with_suffix(".layout.json")
    with open(layout_path, "w", encoding="utf-8") as f:
        json.dump(layout_json, f, ensure_ascii=False, indent=2)
        
    # 3. Output SVG
    svg_content = render_svg(canvas, nodes)
    svg_path = out_prefix.with_suffix(".svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # 4. Optional Output Editor State
    if editor_state:
        editor_path = out_prefix.with_suffix(".editor_state.json")
        with open(editor_path, "w", encoding="utf-8") as f:
            json.dump(editor_state.to_dict(), f, ensure_ascii=False, indent=2)
