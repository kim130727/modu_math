from __future__ import annotations

from modu_math.layout.editor_overrides import apply_editor_overrides
from modu_math.pipeline.subproblem_projection import project_suffixed_subproblem


def test_project_suffixed_subproblem_keeps_matching_group_and_shifts_left() -> None:
    layout = {
        "regions": [
            {
                "id": "region.stem",
                "role": "stem",
                "slot_ids": ["slot.instruction", "slot.expr_1"],
            },
            {
                "id": "region.problems",
                "role": "diagram",
                "slot_ids": [
                    "slot.instruction",
                    "slot.label_1",
                    "slot.value_1",
                    "slot.label_2",
                    "slot.value_2",
                    "slot.answer_box_2",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.label_1",
                "kind": "text",
                "content": {"text": "(1)", "x": 20, "y": 40, "font_size": 20},
            },
            {
                "id": "slot.value_1",
                "kind": "text",
                "content": {"text": "123", "x": 50, "y": 40, "font_size": 20},
            },
            {
                "id": "slot.label_2",
                "kind": "text",
                "content": {"text": "(2)", "x": 145, "y": 40, "font_size": 20},
            },
            {
                "id": "slot.value_2",
                "kind": "text",
                "content": {"text": "456", "x": 175, "y": 40, "font_size": 20},
            },
            {
                "id": "slot.answer_box_2",
                "kind": "rect",
                "content": {"x": 170, "y": 50, "width": 20, "height": 20},
            },
            {"id": "answer.problem_1.a", "kind": "blank", "content": {}},
            {"id": "answer.problem_2.a", "kind": "blank", "content": {}},
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": ["slot.label_1", "slot.value_1"],
            },
            {
                "id": "group.problem_2",
                "member_ids": ["slot.label_2", "slot.value_2"],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [
                {"blank_id": "answer.problem_1.a", "value": 3},
                {"blank_id": "answer.problem_2.a", "value": 7},
            ],
            "value": [3, 7],
        }
    }
    solvable = {
        "answer": {
            "answer_key": [
                {"blank_id": "answer.problem_1.a", "value": 3},
                {"blank_id": "answer.problem_2.a", "value": 7},
            ],
            "value": [3, 7],
        },
        "steps": [
            {"id": "s1", "expr": "a", "value": {"ref": "answer.problem_1.a"}},
            {"id": "s2", "expr": "b", "value": {"ref": "answer.problem_2.a"}},
        ],
    }

    projected_layout, projected_semantic, projected_solvable, removed = (
        project_suffixed_subproblem(
            artifact_id="P3_1_01_00040_02163_2",
            template_id="P3_1_01_00040_02163",
            layout=layout,
            semantic=semantic,
            solvable=solvable,
        )
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.label_1" not in slot_ids
    assert "slot.label_2" in slot_ids
    assert "slot.answer_box_2" in slot_ids
    assert "answer.problem_2.a" in slot_ids
    assert "answer.problem_1.a" not in slot_ids
    assert removed >= {"slot.label_1", "slot.value_1", "answer.problem_1.a"}
    assert projected_layout["groups"] == [
        {"id": "group.problem_2", "member_ids": ["slot.label_2", "slot.value_2"]}
    ]
    shifted_label = next(
        slot for slot in projected_layout["slots"] if slot["id"] == "slot.label_2"
    )
    assert shifted_label["content"]["x"] == 20.0
    assert projected_semantic["answer"]["value"] == [7]
    assert projected_solvable is not None
    assert projected_solvable["answer"]["value"] == [7]
    assert [step["id"] for step in projected_solvable["steps"]] == ["s2"]


def test_project_suffixed_subproblem_uses_matching_region_without_groups() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.calculation.1",
                "role": "body",
                "slot_ids": ["slot.expr_1", "slot.submit_1"],
            },
            {
                "id": "region.calculation.2",
                "role": "body",
                "slot_ids": ["slot.expr_2", "slot.submit_2"],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {}},
            {"id": "slot.expr_1", "kind": "text", "content": {"x": 10, "y": 20}},
            {"id": "slot.expr_2", "kind": "text", "content": {"x": 110, "y": 20}},
            {
                "id": "slot.submit_1",
                "kind": "rect",
                "content": {
                    "x": 10,
                    "y": 60,
                    "width": 40,
                    "height": 20,
                    "interaction": {"type": "input", "role": "answer", "order": 0},
                },
            },
            {
                "id": "slot.submit_2",
                "kind": "rect",
                "content": {
                    "x": 110,
                    "y": 60,
                    "width": 40,
                    "height": 20,
                    "interaction": {"type": "input", "role": "answer", "order": 1},
                },
            },
        ],
        "groups": [],
        "reading_order": [
            "region.stem",
            "region.calculation.1",
            "slot.expr_1",
            "slot.submit_1",
            "region.calculation.2",
            "slot.expr_2",
            "slot.submit_2",
        ],
    }
    semantic = {
        "answer": {
            "value": [9, 50, 7, 90],
            "values": [
                {"value": 9, "target_ref": "answer.1.ones"},
                {"value": 50, "target_ref": "answer.1.tens"},
                {"value": 7, "target_ref": "answer.2.ones"},
                {"value": 90, "target_ref": "answer.2.tens"},
            ],
        },
        "steps": [
            {"id": "step.1", "result": "answer.1.ones"},
            {"id": "step.2", "result": "answer.2.ones"},
        ],
    }

    projected_layout, projected_semantic, _, removed = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_15595_2",
        template_id="P3_1_01_00040_15595",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.expr_1" not in slot_ids
    assert "slot.submit_1" not in slot_ids
    assert "slot.expr_2" in slot_ids
    assert "slot.submit_2" in slot_ids
    assert removed >= {"slot.expr_1", "slot.submit_1"}
    assert projected_semantic["answer"]["value"] == [7, 90]
    assert projected_semantic["answer"]["values"] == [
        {"value": 7, "target_ref": "answer.2.ones"},
        {"value": 90, "target_ref": "answer.2.tens"},
    ]
    assert projected_semantic["steps"] == [{"id": "step.2", "result": "answer.2.ones"}]


def test_project_suffixed_subproblem_rebinds_stray_submit_to_target_box() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.calculation.1",
                "role": "body",
                "slot_ids": [
                    "slot.calculation.1.top",
                    "slot.calculation.1.box.ones",
                    "slot.calculation.1.box.tens",
                    "slot.calculation.1.line",
                    "konva.copied_submit",
                ],
            },
            {
                "id": "region.calculation.2",
                "role": "body",
                "slot_ids": ["slot.calculation.2.top"],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.calculation.1.top",
                "kind": "text",
                "content": {"text": "217", "x": 117, "y": 78, "font_size": 24},
            },
            {
                "id": "slot.calculation.1.box.ones",
                "kind": "rect",
                "content": {"x": 129, "y": 157, "width": 28, "height": 27},
            },
            {
                "id": "slot.calculation.1.box.tens",
                "kind": "rect",
                "content": {"x": 114, "y": 198, "width": 43, "height": 27},
            },
            {
                "id": "slot.calculation.1.line",
                "kind": "line",
                "content": {"x1": 69, "y1": 143, "x2": 161, "y2": 143},
            },
            {
                "id": "slot.calculation.2.top",
                "kind": "text",
                "content": {"text": "438", "x": 330, "y": 78, "font_size": 24},
            },
            {
                "id": "konva.copied_submit",
                "kind": "rect",
                "content": {
                    "x": 331,
                    "y": 156,
                    "width": 20,
                    "height": 27,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                        "value_type": "digit",
                        "max_length": 1,
                    },
                    "input_style": {"font_size_mode": "auto"},
                },
            },
        ],
        "groups": [],
    }
    semantic = {
        "answer": {
            "value": [9, 50, 7],
            "values": [
                {"value": 9, "target_ref": "answer.1.ones"},
                {"value": 50, "target_ref": "answer.1.tens"},
                {"value": 7, "target_ref": "answer.2.ones"},
            ],
        }
    }

    projected_layout, _, _, removed = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_15598_1",
        template_id="P3_1_01_00040_15598",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_by_id = {slot["id"]: slot for slot in projected_layout["slots"]}
    assert "konva.copied_submit" not in slot_by_id
    assert "konva.copied_submit" in removed
    interaction = slot_by_id["slot.calculation.1.box.ones"]["content"]["interaction"]
    assert interaction["role"] == "answer"
    assert interaction["order"] == 0
    assert "interaction" not in slot_by_id["slot.calculation.1.box.tens"]["content"]


def test_project_suffixed_subproblem_rebinds_overlapping_submit_to_target_box() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.calculation.2",
                "role": "body",
                "slot_ids": [
                    "slot.calculation.2.top",
                    "slot.calculation.2.box.ones",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.calculation.2.top",
                "kind": "text",
                "content": {"text": "125", "x": 317, "y": 78, "font_size": 24},
            },
            {
                "id": "slot.calculation.2.box.ones",
                "kind": "rect",
                "content": {"x": 329, "y": 157, "width": 28, "height": 27},
            },
            {
                "id": "konva.overlapping_submit",
                "kind": "rect",
                "content": {
                    "x": 331,
                    "y": 156,
                    "width": 20,
                    "height": 27,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                    },
                },
            },
        ],
        "groups": [],
    }
    semantic = {
        "answer": {
            "value": [9, 7],
            "values": [
                {"value": 9, "target_ref": "answer.1.ones"},
                {"value": 7, "target_ref": "answer.2.ones"},
            ],
        }
    }

    projected_layout, _, _, removed = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_15598_2",
        template_id="P3_1_01_00040_15598",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_by_id = {slot["id"]: slot for slot in projected_layout["slots"]}
    assert "konva.overlapping_submit" not in slot_by_id
    assert "konva.overlapping_submit" in removed
    interaction = slot_by_id["slot.calculation.2.box.ones"]["content"]["interaction"]
    assert interaction["role"] == "answer"
    assert interaction["order"] == 0


def test_project_suffixed_subproblem_drops_other_index_line_even_when_spatially_near() -> (
    None
):
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.calculation.1",
                "role": "body",
                "slot_ids": ["slot.calculation.1.line"],
            },
            {
                "id": "region.calculation.2",
                "role": "body",
                "slot_ids": [
                    "slot.calculation.2.top",
                    "slot.calculation.2.line",
                    "slot.calculation.2.answer",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 20, "y": 0}},
            {
                "id": "slot.calculation.1.line",
                "kind": "line",
                "content": {"x1": 72, "y1": 142, "x2": 162, "y2": 142},
            },
            {
                "id": "slot.calculation.2.top",
                "kind": "text",
                "content": {"text": "394", "x": 90, "y": 90, "font_size": 24},
            },
            {
                "id": "slot.calculation.2.line",
                "kind": "line",
                "content": {"x1": 72, "y1": 155, "x2": 215, "y2": 155},
            },
            {
                "id": "slot.calculation.2.answer",
                "kind": "rect",
                "content": {
                    "x": 100,
                    "y": 175,
                    "width": 80,
                    "height": 30,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 1,
                    },
                },
            },
        ],
        "groups": [],
    }
    semantic = {
        "answer": {
            "value": [395, 599],
            "values": [
                {"value": 395, "target_ref": "answer.calculation_1"},
                {"value": 599, "target_ref": "answer.calculation_2"},
            ],
        }
    }

    projected_layout, _, _, removed = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_15595_2",
        template_id="P3_1_01_00040_15595",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.calculation.1.line" not in slot_ids
    assert "slot.calculation.2.line" in slot_ids
    assert "slot.calculation.1.line" in removed


def test_project_suffixed_subproblem_promotes_text_blank_and_drops_nearby_rect() -> (
    None
):
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.problems",
                "role": "diagram",
                "slot_ids": [
                    "slot.instruction",
                    "slot.label_1",
                    "slot.blank_1_tens",
                    "slot.number_1_bottom_ones",
                    "konva.answer.box",
                ],
            },
        ],
        "slots": [
            {
                "id": "slot.instruction",
                "kind": "text_box",
                "content": {
                    "text": "다음 계산이 맞도록 □ 안에 알맞은 수를 써넣으시오.",
                    "x": 10,
                    "y": 0,
                    "width": 160,
                    "height": 20,
                    "font_size": 17,
                    "line_height": 1.2,
                },
            },
            {"id": "slot.label_1", "kind": "text", "content": {"x": 20, "y": 40}},
            {
                "id": "slot.blank_1_tens",
                "kind": "text",
                "content": {
                    "text": "□",
                    "x": 80,
                    "y": 70,
                    "font_size": 22,
                    "fill": "#111111",
                },
            },
            {
                "id": "slot.number_1_bottom_ones",
                "kind": "text",
                "content": {"text": "8", "x": 110, "y": 70},
            },
            {
                "id": "answer.problem_1.tens",
                "kind": "blank",
                "content": {},
            },
            {
                "id": "konva.answer.box",
                "kind": "rect",
                "content": {"x": 75, "y": 74, "width": 18, "height": 18},
            },
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": [
                    "slot.label_1",
                    "slot.blank_1_tens",
                    "slot.number_1_bottom_ones",
                ],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "answer.problem_1.tens", "value": 7}],
            "value": [7],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_02163_1",
        template_id="P3_1_01_00040_02163",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_by_id = {slot["id"]: slot for slot in projected_layout["slots"]}
    assert "konva.answer.box" not in slot_by_id
    assert slot_by_id["slot.blank_1_tens"]["kind"] == "rect"
    assert slot_by_id["slot.blank_1_tens"]["content"]["fill"] == "#ffffff"
    interaction = slot_by_id["slot.blank_1_tens"]["content"]["interaction"]
    assert interaction["role"] == "answer"
    assert interaction["answer_ref"] == "answer_key[0]"
    assert slot_by_id["slot.label_1"]["content"]["y"] > 40


def test_project_suffixed_subproblem_matches_item_group_submit_rect_by_order() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.example",
                "role": "example",
                "slot_ids": [
                    "slot.example_box",
                    "slot.example_left_value",
                    "slot.example_right_value",
                ],
            },
            {
                "id": "region.diagram",
                "role": "diagram",
                "slot_ids": [
                    "slot.item_1_left_value",
                    "slot.item_2_left_value",
                    "slot.submit_1",
                    "slot.submit_2",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.example_box",
                "kind": "rect",
                "content": {"x": 20, "y": 30, "width": 80, "height": 50},
            },
            {
                "id": "slot.example_left_value",
                "kind": "text",
                "content": {"text": "25", "x": 40, "y": 50, "font_size": 15},
            },
            {
                "id": "slot.example_right_value",
                "kind": "text",
                "content": {"text": "28", "x": 70, "y": 50, "font_size": 15},
            },
            {
                "id": "slot.item_1_left_value",
                "kind": "text",
                "content": {"text": "236", "x": 60, "y": 100, "font_size": 15},
            },
            {"id": "slot.answer_1", "kind": "blank", "content": {}},
            {
                "id": "slot.item_2_left_value",
                "kind": "text",
                "content": {"text": "756", "x": 214, "y": 100, "font_size": 15},
            },
            {"id": "slot.answer_2", "kind": "blank", "content": {}},
            {
                "id": "slot.submit_1",
                "kind": "rect",
                "content": {
                    "x": 70,
                    "y": 130,
                    "width": 54,
                    "height": 29,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                    },
                },
            },
            {
                "id": "slot.submit_2",
                "kind": "rect",
                "content": {
                    "x": 224,
                    "y": 130,
                    "width": 54,
                    "height": 29,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 1,
                    },
                },
            },
        ],
        "groups": [
            {
                "id": "group.example",
                "role": "addition_rule_example",
                "member_ids": [
                    "slot.example_box",
                    "slot.example_left_value",
                    "slot.example_right_value",
                ],
            },
            {
                "id": "group.item_1",
                "member_ids": ["slot.item_1_left_value", "slot.answer_1"],
            },
            {
                "id": "group.item_2",
                "member_ids": ["slot.item_2_left_value", "slot.answer_2"],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [
                {"blank_id": "slot.answer_1", "value": 701},
                {"blank_id": "slot.answer_2", "value": 1305},
            ],
            "value": [701, 1305],
        }
    }

    projected_layout, projected_semantic, _, _ = project_suffixed_subproblem(
        artifact_id="ko/P3_1_01_00040_02164_2.dsl.py",
        template_id="P3_1_01_00040_02164",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.submit_1" not in slot_ids
    assert "slot.submit_2" in slot_ids
    assert "slot.answer_1" not in slot_ids
    assert "slot.answer_2" in slot_ids
    assert "slot.example_box" in slot_ids
    assert "slot.example_left_value" in slot_ids
    assert {region["id"] for region in projected_layout["regions"]} == {
        "region.stem",
        "region.example",
        "region.diagram",
    }
    assert {group["id"] for group in projected_layout["groups"]} == {
        "group.example",
        "group.item_2",
    }
    example_box = next(
        slot for slot in projected_layout["slots"] if slot["id"] == "slot.example_box"
    )
    assert example_box["content"]["x"] == 20
    assert projected_semantic["answer"]["value"] == [1305]


def test_project_suffixed_subproblem_preserves_moved_promoted_blank_rect() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.problems",
                "role": "diagram",
                "slot_ids": ["slot.blank_1_tens", "slot.number_1_bottom_ones"],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.blank_1_tens",
                "kind": "text",
                "content": {
                    "text": "□",
                    "x": 91.0,
                    "y": 82.0,
                    "width": 18.0,
                    "height": 18.0,
                    "font_size": 22,
                    "fill": "#ffffff",
                    "stroke": "#111827",
                    "stroke_width": 1.2,
                },
            },
            {
                "id": "slot.number_1_bottom_ones",
                "kind": "text",
                "content": {"text": "8", "x": 120, "y": 100, "font_size": 22},
            },
            {"id": "answer.problem_1.tens", "kind": "blank", "content": {}},
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": ["slot.blank_1_tens", "slot.number_1_bottom_ones"],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "answer.problem_1.tens", "value": 7}],
            "value": [7],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="ko/P3_1_01_00040_02163_1.dsl.py",
        template_id="P3_1_01_00040_02163",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    blank = next(
        slot for slot in projected_layout["slots"] if slot["id"] == "slot.blank_1_tens"
    )
    assert blank["kind"] == "rect"
    assert blank["content"]["x"] == 91.0
    assert blank["content"]["y"] == 82.0
    assert blank["content"]["width"] == 18.0
    assert blank["content"]["height"] == 18.0


def test_project_suffixed_subproblem_keeps_spatial_answer_input_with_wrong_order() -> (
    None
):
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.problems",
                "role": "diagram",
                "slot_ids": [
                    "slot.addend_1",
                    "slot.line_1",
                    "slot.answer_input_1",
                    "slot.addend_2",
                    "slot.line_2",
                    "slot.answer_input_2",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.addend_1",
                "kind": "text",
                "content": {"text": "235", "x": 40, "y": 60, "font_size": 20},
            },
            {
                "id": "slot.line_1",
                "kind": "line",
                "content": {"x1": 35, "y1": 90, "x2": 100, "y2": 90},
            },
            {
                "id": "slot.answer_input_1",
                "kind": "rect",
                "content": {
                    "x": 40,
                    "y": 108,
                    "width": 60,
                    "height": 28,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                    },
                },
            },
            {
                "id": "slot.addend_2",
                "kind": "text",
                "content": {"text": "529", "x": 160, "y": 60, "font_size": 20},
            },
            {
                "id": "slot.line_2",
                "kind": "line",
                "content": {"x1": 150, "y1": 90, "x2": 215, "y2": 90},
            },
            {"id": "slot.answer_2", "kind": "blank", "content": {}},
            {
                "id": "slot.answer_input_2",
                "kind": "rect",
                "content": {
                    "x": 155,
                    "y": 108,
                    "width": 60,
                    "height": 28,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                    },
                },
            },
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": ["slot.addend_1", "slot.line_1"],
            },
            {
                "id": "group.problem_2",
                "member_ids": ["slot.addend_2", "slot.line_2", "slot.answer_2"],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "slot.answer_2", "value": 1427}],
            "value": [1427],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_02162_2",
        template_id="P3_1_01_00040_02162",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.answer_input_1" not in slot_ids
    assert "slot.answer_input_2" in slot_ids
    assert "slot.answer_2" in slot_ids


def test_project_suffixed_subproblem_prefers_ordered_submit_over_spatial_duplicate() -> (
    None
):
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.diagram",
                "role": "diagram",
                "slot_ids": [
                    "slot.item_2_left_value",
                    "slot.answer_2",
                    "slot.spatial_duplicate",
                    "slot.ordered_submit_2",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.item_2_left_value",
                "kind": "text",
                "content": {"text": "756", "x": 214, "y": 100, "font_size": 15},
            },
            {"id": "slot.answer_2", "kind": "blank", "content": {}},
            {
                "id": "slot.spatial_duplicate",
                "kind": "rect",
                "content": {
                    "x": 218,
                    "y": 118,
                    "width": 54,
                    "height": 29,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 0,
                    },
                },
            },
            {
                "id": "slot.ordered_submit_2",
                "kind": "rect",
                "content": {
                    "x": 370,
                    "y": 118,
                    "width": 54,
                    "height": 29,
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                        "order": 1,
                    },
                },
            },
        ],
        "groups": [
            {
                "id": "group.item_2",
                "member_ids": ["slot.item_2_left_value", "slot.answer_2"],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "slot.answer_2", "value": 1305}],
            "value": [1305],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_02164_2",
        template_id="P3_1_01_00040_02164",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.spatial_duplicate" not in slot_ids
    assert "slot.ordered_submit_2" in slot_ids


def test_project_suffixed_subproblem_preserves_editor_moved_text_blank_rect() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.problems",
                "role": "diagram",
                "slot_ids": [
                    "slot.blank_1_tens",
                    "slot.number_1_answer_rest",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.blank_1_tens",
                "kind": "text",
                "content": {"text": "□", "x": 80, "y": 70, "font_size": 22},
            },
            {
                "id": "slot.number_1_answer_rest",
                "kind": "text",
                "content": {"text": "3  1", "x": 130, "y": 100, "font_size": 22},
            },
            {"id": "answer.problem_1.tens", "kind": "blank", "content": {}},
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": ["slot.blank_1_tens", "slot.number_1_answer_rest"],
            },
        ],
    }
    overrides = {
        "slots": {
            "slot.blank_1_tens": {"x": 158.72, "y": 82.516},
            "slot.number_1_answer_rest": {"y": 137.987},
        }
    }
    layout = apply_editor_overrides(layout, overrides)
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "answer.problem_1.tens", "value": 7}],
            "value": [7],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_02163_1",
        template_id="P3_1_01_00040_02163",
        layout=layout,
        semantic=semantic,
        solvable=None,
        protected_slot_ids=set(overrides["slots"]),
    )

    slot_by_id = {slot["id"]: slot for slot in projected_layout["slots"]}
    assert slot_by_id["slot.blank_1_tens"]["kind"] == "rect"
    assert slot_by_id["slot.blank_1_tens"]["content"]["x"] == 158.72
    assert slot_by_id["slot.blank_1_tens"]["content"]["y"] == 82.516
    assert slot_by_id["slot.number_1_answer_rest"]["content"]["y"] == 137.987


def test_project_suffixed_subproblem_does_not_translate_protected_path_offsets() -> (
    None
):
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.diagram",
                "role": "diagram",
                "slot_ids": [
                    "slot.item_1_value",
                    "slot.item_2_path",
                    "slot.item_2_value",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {
                "id": "slot.item_1_value",
                "kind": "text",
                "content": {"text": "1", "x": 20, "y": 60, "font_size": 15},
            },
            {
                "id": "slot.item_2_path",
                "kind": "path",
                "content": {
                    "d": "M 280 160 L 378 160",
                    "x": 0.0,
                    "y": 0.0,
                    "fill": "none",
                    "stroke": "#111111",
                },
            },
            {
                "id": "slot.item_2_value",
                "kind": "text",
                "content": {"text": "2", "x": 300, "y": 60, "font_size": 15},
            },
            {"id": "slot.answer_2", "kind": "blank", "content": {}},
        ],
        "groups": [
            {"id": "group.item_1", "member_ids": ["slot.item_1_value"]},
            {
                "id": "group.item_2",
                "member_ids": [
                    "slot.item_2_path",
                    "slot.item_2_value",
                    "slot.answer_2",
                ],
            },
        ],
    }
    semantic = {
        "answer": {
            "answer_key": [{"blank_id": "slot.answer_2", "value": 2}],
            "value": [2],
        }
    }

    projected_layout, _, _, _ = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_02164_2",
        template_id="P3_1_01_00040_02164",
        layout=layout,
        semantic=semantic,
        solvable=None,
        protected_slot_ids={"slot.item_2_path", "slot.item_2_value"},
    )

    slot_by_id = {slot["id"]: slot for slot in projected_layout["slots"]}
    assert slot_by_id["slot.item_2_path"]["content"]["x"] == 0.0
    assert slot_by_id["slot.item_2_path"]["content"]["y"] == 0.0
    assert slot_by_id["slot.item_2_path"]["content"]["d"] == "M 280 160 L 378 160"
    assert slot_by_id["slot.item_2_value"]["content"]["x"] == 300


def test_project_suffixed_subproblem_preserves_multiple_submit_slots_in_subproblem() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.instruction"]},
            {
                "id": "region.calculation.2",
                "role": "body",
                "slot_ids": [
                    "slot.calculation.2.top",
                    "slot.calculation.2.box.ones",
                    "slot.calculation.2.box.tens",
                    "slot.calculation.2.box.hundreds",
                    "slot.calculation.2.box.total",
                ],
            },
        ],
        "slots": [
            {"id": "slot.instruction", "kind": "text", "content": {"x": 10, "y": 0}},
            {"id": "slot.calculation.2.top", "kind": "text", "content": {"text": "386", "x": 190, "y": 90}},
            {
                "id": "slot.calculation.2.box.ones",
                "kind": "rect",
                "content": {
                    "x": 202,
                    "y": 169,
                    "width": 28,
                    "height": 27,
                    "interaction": {"type": "input", "role": "answer", "order": 0},
                },
            },
            {
                "id": "slot.calculation.2.box.tens",
                "kind": "rect",
                "content": {
                    "x": 187,
                    "y": 210,
                    "width": 43,
                    "height": 27,
                    "interaction": {"type": "input", "role": "answer", "order": 1},
                },
            },
            {
                "id": "slot.calculation.2.box.hundreds",
                "kind": "rect",
                "content": {
                    "x": 172,
                    "y": 251,
                    "width": 58,
                    "height": 27,
                    "interaction": {"type": "input", "role": "answer", "order": 2},
                },
            },
            {
                "id": "slot.calculation.2.box.total",
                "kind": "rect",
                "content": {
                    "x": 172,
                    "y": 303,
                    "width": 58,
                    "height": 29,
                    "interaction": {"type": "input", "role": "answer", "order": 3},
                },
            },
        ],
        "groups": [],
    }
    semantic = {
        "answer": {
            "value": [7, 90, 500, 597],
            "values": [
                {"value": 7, "target_ref": "answer.2.ones"},
                {"value": 90, "target_ref": "answer.2.tens"},
                {"value": 500, "target_ref": "answer.2.hundreds"},
                {"value": 597, "target_ref": "answer.2.total"},
            ],
        }
    }

    projected_layout, projected_semantic, _, removed = project_suffixed_subproblem(
        artifact_id="P3_1_01_00040_15598_2",
        template_id="P3_1_01_00040_15598",
        layout=layout,
        semantic=semantic,
        solvable=None,
    )

    slot_ids = {slot["id"] for slot in projected_layout["slots"]}
    assert "slot.calculation.2.box.ones" in slot_ids
    assert "slot.calculation.2.box.tens" in slot_ids
    assert "slot.calculation.2.box.hundreds" in slot_ids
    assert "slot.calculation.2.box.total" in slot_ids
    assert not removed
    assert projected_semantic["answer"]["value"] == [7, 90, 500, 597]

