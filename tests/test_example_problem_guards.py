from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType

from modu_math.dsl import ProblemTemplate, compile_problem_template_to_layout
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"example_problem_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load DSL module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _slot_by_id(layout: dict, slot_id: str) -> dict:
    for slot in layout.get("slots", []):
        if slot.get("id") == slot_id:
            return slot
    raise AssertionError(f"Missing layout slot: {slot_id}")


def _path_numbers(d: str) -> list[float]:
    return [float(value) for value in re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", d)]


def test_circle_area_0001_radius_helper_path_keeps_semantic_id_and_position() -> None:
    module = _load_module(Path("examples/problems/초6_2_원의넓이_0001.dsl.py"))
    problem = getattr(module, "PROBLEM_TEMPLATE")
    assert isinstance(problem, ProblemTemplate)

    layout = compile_problem_template_to_layout(problem)
    slot_ids = {slot["id"] for slot in layout["slots"]}
    assert "slot.radius_10_arc" in slot_ids
    assert "konva_1783766230573_paste_122425_0" not in slot_ids

    radius_line = _slot_by_id(layout, "slot.radius_10_line")["content"]
    radius_arc = _slot_by_id(layout, "slot.radius_10_arc")["content"]
    x1 = float(radius_line["x1"])
    y1 = float(radius_line["y1"])
    y2 = float(radius_line["y2"])
    nums = _path_numbers(radius_arc["d"])
    assert len(nums) == 6
    start_x, start_y, control_x, _control_y, end_x, end_y = nums

    top_y, bottom_y = sorted([y1, y2])
    assert abs(start_x - x1) <= 25
    assert abs(end_x - x1) <= 25
    assert top_y - 5 <= start_y <= top_y + 20
    assert bottom_y - 20 <= end_y <= bottom_y + 5
    assert control_x > x1

    svg = render_svg(compile_renderer_json(layout))
    assert 'id="slot.radius_10_arc.path"' in svg
    assert "konva_1783766230573_paste_122425_0" not in svg
