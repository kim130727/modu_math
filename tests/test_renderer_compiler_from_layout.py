from __future__ import annotations

from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.validate import validate_renderer_json


def test_compile_renderer_from_multiple_choice_layout() -> None:
    layout = {
        "problem_id": "mcq_layout_example_0001",
        "canvas": {"width": 960, "height": 640, "background": "#ffffff"},
        "regions": [
            {"id": "region_stem", "role": "stem", "slot_ids": ["slot_stem"]},
            {"id": "region_choices", "role": "choices", "slot_ids": ["slot_choices"]},
        ],
        "slots": [
            {
                "id": "slot_stem",
                "kind": "text",
                "content": {"text": "What is 28 + 14?"},
            },
            {
                "id": "slot_choices",
                "kind": "choice",
                "prompt": "Select one answer.",
                "content": {"choices": ["32", "42", "44", "46"], "multiple_select": False},
            },
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    assert renderer["problem_id"] == "mcq_layout_example_0001"
    assert renderer["view_box"]["width"] == 960
    assert renderer["elements"][0]["id"] == "slot_stem.text"
    assert renderer["elements"][0]["type"] == "text"
    assert renderer["elements"][0]["refs"]["layout_slot_id"] == "slot_stem"


def test_compile_renderer_expands_cube_object_to_primitives() -> None:
    layout = {
        "problem_id": "diagram_cube_example_0001",
        "canvas": {"width": 1200, "height": 760, "background": "#ffffff"},
        "slots": [
            {
                "id": "slot_question",
                "kind": "text",
                "content": {"text": "How many edges does this cube have?"},
            }
        ],
        "diagrams": [
            {
                "id": "diagram_cube",
                "frame": {"x": 80, "y": 260, "width": 520, "height": 360},
                "objects": [
                    {
                        "id": "obj_cube_main",
                        "object_type": "cube",
                        "perspective": "isometric",
                    }
                ],
                "label_slots": [
                    {
                        "id": "diagram_label_front",
                        "kind": "label",
                        "content": {
                            "text": "front",
                            "target_object_id": "obj_cube_main",
                            "target_anchor": "right",
                        },
                    }
                ],
            }
        ],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    groups = [element for element in renderer["elements"] if element["type"] == "group"]
    assert len(groups) == 1

    cube_primitives = [
        child
        for child in groups[0]["elements"]
        if child.get("refs", {}).get("layout_object_id") == "obj_cube_main"
    ]
    assert len(cube_primitives) >= 12
    assert any(child["id"].endswith(".edge.connect.bl") for child in cube_primitives)
    assert all(child["type"] in {"line", "text"} for child in groups[0]["elements"])


def test_compile_renderer_preserves_slot_transform() -> None:
    layout = {
        "problem_id": "transform_example_0001",
        "canvas": {"width": 200, "height": 120, "background": "#ffffff"},
        "regions": [{"id": "region_diagram", "role": "diagram", "flow": "absolute", "slot_ids": ["slot_line"]}],
        "slots": [
            {
                "id": "slot_line",
                "kind": "line",
                "prompt": "",
                "content": {"x1": 10, "y1": 20, "x2": 90, "y2": 20, "transform": "rotate(30 50 20)"},
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)

    assert renderer["elements"][0]["attributes"]["transform"] == "rotate(30 50 20)"


def test_compile_renderer_preserves_answer_slot_metadata_without_type_conversion() -> None:
    layout = {
        "problem_id": "answer_slot_example_0001",
        "canvas": {"width": 200, "height": 120, "background": "#ffffff"},
        "regions": [{"id": "region_answer", "role": "answer", "flow": "absolute", "slot_ids": ["answer.final"]}],
        "slots": [
            {
                "id": "answer.final",
                "kind": "rect",
                "prompt": "",
                "content": {
                    "x": 10,
                    "y": 20,
                    "width": 80,
                    "height": 40,
                    "fill": "#ffffff",
                    "stroke": "#111111",
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "value_type": "integer",
                        "max_length": 3,
                        "include_in_submission": True,
                        "order": 0,
                        "group_id": "final_answer",
                        "auto_advance": False,
                        "keyboard": "number",
                    },
                    "input_style": {
                        "font_size_mode": "auto",
                        "font_size_adjust": 0,
                        "min_font_size": 14,
                        "max_font_size": 52,
                        "font_weight": 700,
                        "horizontal_align": "center",
                        "vertical_align": "middle",
                        "padding": 6,
                        "text_color": "#222222",
                    },
                },
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    element = renderer["elements"][0]
    assert element["type"] == "rect"
    assert element["interaction"]["type"] == "input"
    assert element["input_style"]["font_size_mode"] == "auto"

