from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from ..semantic.models.problem import SemanticProblem
from ..layout.models.canvas import LayoutCanvas
from ..layout.models.node import LayoutNode
from ..layout.diff import apply_layout_diff
from ..layout.validate import validate_layout_json
from ..adapters.json.layout_json import layout_to_layout_json
from ..adapters.json.renderer_json import layout_to_renderer
from ..renderer.validate import validate_renderer_json
from ..renderer.svg.render import render_svg
from ..adapters.json.semantic_json import problem_to_semantic_json
from ..semantic.validate import validate_semantic_json
from .validate_contracts import validate_contract_bundle

if TYPE_CHECKING:
    from ..editor.models.state import EditorState

def compile_problem_pipeline(
    problem: SemanticProblem, 
    canvas: LayoutCanvas, 
    nodes: list[LayoutNode], 
    out_prefix: str | Path,
    layout_patches: list[dict[str, Any]] | None = None,
    editor_state: Any | None = None,
    validate: bool = False,
    cross_layer_validate: bool | None = None,
    emit_semantic: bool = True,
) -> None:
    """
    Compile semantic/layout/renderer contracts and SVG artifact to disk.

    Validation policy:
    - semantic/layout/renderer contract validation always runs.
    - cross-layer validation is opt-in strict mode.
      - backward compatibility: `validate=True` enables strict mode.
      - explicit: `cross_layer_validate=True/False` overrides `validate`.
    """
    out_prefix = Path(out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    strict_cross_layer = bool(validate) if cross_layer_validate is None else bool(cross_layer_validate)
    
    semantic_json: dict[str, Any] | None = None
    if emit_semantic:
        # 1. Output semantic JSON
        semantic_json = problem_to_semantic_json(problem)
        validate_semantic_json(semantic_json)
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
    layout_json = layout_to_layout_json(str(problem.problem_id or ""), canvas, nodes)
    validate_layout_json(layout_json)
    layout_path = out_prefix.with_suffix(".layout.json")
    with open(layout_path, "w", encoding="utf-8") as f:
        json.dump(layout_json, f, ensure_ascii=False, indent=2)
        
    # 3. Output renderer JSON
    renderer_ast = layout_to_renderer(problem.problem_id, canvas, nodes)
    renderer_json = renderer_ast.to_dict()
    validate_renderer_json(renderer_json)
    if strict_cross_layer and semantic_json is not None:
        validate_contract_bundle(semantic_json, layout_json, renderer_json)
    renderer_path = out_prefix.with_suffix(".renderer.json")
    with open(renderer_path, "w", encoding="utf-8") as f:
        json.dump(renderer_json, f, ensure_ascii=False, indent=2)

    # 4. Output SVG (pure renderer -> SVG)
    svg_content = render_svg(renderer_ast)
    svg_path = out_prefix.with_suffix(".svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # 5. Optional Output Editor State
    if editor_state:
        editor_path = out_prefix.with_suffix(".editor_state.json")
        with open(editor_path, "w", encoding="utf-8") as f:
            json.dump(editor_state.to_dict(), f, ensure_ascii=False, indent=2)
