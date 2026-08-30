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
                "content": {
                    "choices": ["32", "42", "44", "46"],
                    "multiple_select": False,
                },
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
        "regions": [
            {
                "id": "region_diagram",
                "role": "diagram",
                "flow": "absolute",
                "slot_ids": ["slot_line"],
            }
        ],
        "slots": [
            {
                "id": "slot_line",
                "kind": "line",
                "prompt": "",
                "content": {
                    "x1": 10,
                    "y1": 20,
                    "x2": 90,
                    "y2": 20,
                    "transform": "rotate(30 50 20)",
                },
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)

    assert renderer["elements"][0]["attributes"]["transform"] == "rotate(30 50 20)"


def test_compile_renderer_preserves_answer_slot_metadata_without_type_conversion() -> (
    None
):
    layout = {
        "problem_id": "answer_slot_example_0001",
        "canvas": {"width": 200, "height": 120, "background": "#ffffff"},
        "regions": [
            {
                "id": "region_answer",
                "role": "answer",
                "flow": "absolute",
                "slot_ids": ["answer.final"],
            }
        ],
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


def test_compile_renderer_places_blank_after_text_box_bottom() -> None:
    layout = {
        "problem_id": "text_box_then_blank_example_0001",
        "canvas": {"width": 600, "height": 170, "background": "#ffffff"},
        "regions": [
            {
                "id": "region.stem",
                "role": "stem",
                "flow": "vertical",
                "slot_ids": ["slot.question", "slot.answer"],
            }
        ],
        "slots": [
            {
                "id": "slot.question",
                "kind": "text_box",
                "prompt": "",
                "content": {
                    "text": "동화책이 두 권 있습니다. 한 권은 230쪽이고 다른 한 권은 450쪽입니다.",
                    "x": 14,
                    "y": 20,
                    "width": 560,
                    "height": 144,
                    "font_size": 30,
                    "line_height": 1.45,
                },
            },
            {
                "id": "slot.answer",
                "kind": "blank",
                "prompt": "답",
                "content": {"placeholder": "쪽"},
            },
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    question = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.question.text"
    )
    blank = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.answer.blank"
    )
    question_bottom = (
        question["attributes"]["data-box-y"] + question["attributes"]["data-box-height"]
    )

    assert blank["attributes"]["y"] >= question_bottom + 12
    assert renderer["view_box"]["height"] == layout["canvas"]["height"]


def test_compile_renderer_preserves_canvas_view_box_when_content_overflows() -> None:
    layout = {
        "problem_id": "fixed_canvas_example_0001",
        "canvas": {"width": 400, "height": 120, "background": "#ffffff"},
        "regions": [
            {
                "id": "region.main",
                "role": "diagram",
                "flow": "absolute",
                "slot_ids": ["slot.low"],
            }
        ],
        "slots": [
            {
                "id": "slot.low",
                "kind": "rect",
                "prompt": "",
                "content": {
                    "x": 20,
                    "y": 100,
                    "width": 80,
                    "height": 40,
                    "fill": "none",
                    "stroke": "#111111",
                },
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)

    assert renderer["view_box"]["width"] == 400
    assert renderer["view_box"]["height"] == 120


def test_compile_renderer_uses_authored_blank_geometry() -> None:
    layout = {
        "problem_id": "sized_blank_example_0001",
        "canvas": {"width": 400, "height": 180, "background": "#ffffff"},
        "regions": [
            {
                "id": "region.answer",
                "role": "answer",
                "flow": "absolute",
                "slot_ids": ["slot.answer"],
            }
        ],
        "slots": [
            {
                "id": "slot.answer",
                "kind": "blank",
                "prompt": "",
                "content": {
                    "placeholder": "",
                    "x": 210,
                    "y": 94,
                    "width": 172,
                    "height": 58,
                    "fill": "#f8fafc",
                    "stroke": "#111827",
                    "stroke_width": 1.2,
                },
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    blank = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.answer.blank"
    )
    assert blank["attributes"]["x"] == 210.0
    assert blank["attributes"]["y"] == 94.0
    assert blank["attributes"]["width"] == 172.0
    assert blank["attributes"]["height"] == 58.0


def test_compile_renderer_skips_unplaced_contract_only_blank() -> None:
    layout = {
        "problem_id": "contract_only_blank_example_0001",
        "canvas": {"width": 320, "height": 180},
        "regions": [
            {
                "id": "region.diagram",
                "role": "diagram",
                "flow": "absolute",
                "slot_ids": ["slot.visible"],
            }
        ],
        "slots": [
            {
                "id": "slot.visible",
                "kind": "text",
                "content": {"text": "□", "x": 80, "y": 90, "font_size": 28},
            },
            {
                "id": "answer.contract",
                "kind": "blank",
                "content": {"answer_key": "7", "placeholder": ""},
            },
        ],
    }

    renderer = compile_renderer_json(layout)

    assert any(element["id"] == "slot.visible.text" for element in renderer["elements"])


def test_compile_renderer_uses_authored_blank_geometry() -> None:
    layout = {
        "problem_id": "sized_blank_example_0001",
        "canvas": {"width": 400, "height": 180, "background": "#ffffff"},
        "regions": [
            {
                "id": "region.answer",
                "role": "answer",
                "flow": "absolute",
                "slot_ids": ["slot.answer"],
            }
        ],
        "slots": [
            {
                "id": "slot.answer",
                "kind": "blank",
                "prompt": "",
                "content": {
                    "placeholder": "",
                    "x": 210,
                    "y": 94,
                    "width": 172,
                    "height": 58,
                    "fill": "#f8fafc",
                    "stroke": "#111827",
                    "stroke_width": 1.2,
                },
            }
        ],
        "diagrams": [],
    }

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    blank = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.answer.blank"
    )
    assert blank["attributes"]["x"] == 210.0
    assert blank["attributes"]["y"] == 94.0
    assert blank["attributes"]["width"] == 172.0
    assert blank["attributes"]["height"] == 58.0


def test_compile_renderer_skips_unplaced_contract_only_blank() -> None:
    layout = {
        "problem_id": "contract_only_blank_example_0001",
        "canvas": {"width": 320, "height": 180},
        "regions": [
            {
                "id": "region.diagram",
                "role": "diagram",
                "flow": "absolute",
                "slot_ids": ["slot.visible"],
            }
        ],
        "slots": [
            {
                "id": "slot.visible",
                "kind": "text",
                "content": {"text": "□", "x": 80, "y": 90, "font_size": 28},
            },
            {
                "id": "answer.contract",
                "kind": "blank",
                "content": {"answer_key": "7", "placeholder": ""},
            },
        ],
    }

    renderer = compile_renderer_json(layout)

    assert any(element["id"] == "slot.visible.text" for element in renderer["elements"])
    assert all(
        element["id"] != "answer.contract.blank" for element in renderer["elements"]
    )


def test_compile_renderer_keeps_region_blank_without_authored_geometry() -> None:
    layout = {
        "problem_id": "region_blank_example_0001",
        "canvas": {"width": 320, "height": 180},
        "regions": [
            {
                "id": "region.answer",
                "role": "answer",
                "flow": "vertical",
                "slot_ids": ["slot.answer"],
            }
        ],
        "slots": [
            {
                "id": "slot.answer",
                "kind": "blank",
                "content": {"answer_key": "7", "placeholder": ""},
            },
        ],
    }

    renderer = compile_renderer_json(layout)

    assert any(element["id"] == "slot.answer.blank" for element in renderer["elements"])


def test_apply_editor_overrides_preserves_text_slot_middle_anchor() -> None:
    from modu_math.layout.editor_overrides import (
        apply_editor_overrides,
        prune_editor_overrides,
    )

    layout = {
        "problem_id": "card_text_anchor_0001",
        "canvas": {"width": 500, "height": 220},
        "slots": [
            {
                "id": "slot.card1.text",
                "kind": "text",
                "content": {
                    "text": "1",
                    "x": 36,
                    "y": 72,
                    "font_size": 21,
                    "anchor": "middle",
                    "fill": "#111111",
                },
            }
        ],
    }

    overrides = {
        "version": 1,
        "slots": {
            "slot.card1.text": {
                "x": 78.132,
                "y": 76.105,
                "width": 24,
                "height": 34.25,
                "kind": "text_box",
            }
        },
    }

    pruned_overrides, _ = prune_editor_overrides(layout, overrides)
    applied_layout = apply_editor_overrides(layout, pruned_overrides)
    renderer = compile_renderer_json(applied_layout)

    slot_card1 = next(
        slot for slot in applied_layout["slots"] if slot["id"] == "slot.card1.text"
    )
    assert slot_card1["kind"] == "text"
    assert slot_card1["content"]["anchor"] == "middle"
    assert slot_card1["content"]["x"] == 90.132
    assert slot_card1["content"]["y"] == 97.105

    el = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.card1.text.text"
    )
    assert el["type"] == "text"
    assert el["attributes"]["text-anchor"] == "middle"
    assert el["attributes"]["x"] == 90.132
    assert el["attributes"]["y"] == 97.105


def test_apply_editor_overrides_keeps_center_dot_on_circle_center() -> None:
    from modu_math.layout.editor_overrides import apply_editor_overrides

    layout = {
        "problem_id": "circle_center_dot_0001",
        "canvas": {"width": 500, "height": 360},
        "slots": [
            {
                "id": "slot.diagram.top.circle",
                "kind": "circle",
                "content": {"cx": 478.0, "cy": 185.0, "r": 96.0},
            },
            {
                "id": "slot.diagram.top.center.dot",
                "kind": "text",
                "content": {
                    "text": "●",
                    "x": 473.0,
                    "y": 190.0,
                    "font_size": 12,
                    "anchor": "middle",
                    "fill": "#E11A86",
                },
            },
        ],
    }
    overrides = {
        "version": 1,
        "slots": {
            "slot.diagram.top.circle": {"cx": 337.0, "cy": 235.5},
            "slot.diagram.top.center.dot": {"x": 310.0, "y": 260.0},
        },
    }

    applied = apply_editor_overrides(layout, overrides)
    dot = next(
        slot
        for slot in applied["slots"]
        if slot["id"] == "slot.diagram.top.center.dot"
    )

    assert dot["content"]["x"] == 337.0
    assert dot["content"]["y"] == 239.5


def test_apply_editor_overrides_preserves_plain_text_slot_no_wrapping() -> None:
    from modu_math.layout.editor_overrides import (
        apply_editor_overrides,
        prune_editor_overrides,
    )
    from modu_math.renderer.svg.render import render_svg

    layout = {
        "problem_id": "question_text_no_wrap_0001",
        "canvas": {"width": 500, "height": 200},
        "slots": [
            {
                "id": "slot.qtext",
                "kind": "text",
                "content": {
                    "text": "계산 결과가 500보다 큰 것을 선택하세요.",
                    "x": 20,
                    "y": 35,
                    "font_size": 28,
                    "fill": "#111827",
                },
            }
        ],
    }

    overrides = {
        "version": 1,
        "slots": {
            "slot.qtext": {
                "height": 42,
                "kind": "text_box",
            }
        },
    }

    pruned_overrides, _ = prune_editor_overrides(layout, overrides)
    applied_layout = apply_editor_overrides(layout, pruned_overrides)
    renderer = compile_renderer_json(applied_layout)

    slot_qtext = next(
        slot for slot in applied_layout["slots"] if slot["id"] == "slot.qtext"
    )
    assert slot_qtext["kind"] == "text"
    assert "height" not in slot_qtext["content"]

    el = next(
        element
        for element in renderer["elements"]
        if element["id"] == "slot.qtext.text"
    )
    assert el["type"] == "text"

    svg = render_svg(renderer)
    assert "<tspan" not in svg
    assert "계산 결과가 500보다 큰 것을 선택하세요." in svg
