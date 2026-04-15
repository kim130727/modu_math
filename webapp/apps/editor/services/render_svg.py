from __future__ import annotations

from typing import Any

from modu_semantic.semantic_json_builder import build_problem_from_semantic_dict, make_answer_svg


def render_preview_svg(semantic: dict[str, Any]) -> str:
    problem = build_problem_from_semantic_dict(semantic, validate_input=False)
    svg = problem.to_svg()
    return make_answer_svg(svg, semantic, font_size=42)

