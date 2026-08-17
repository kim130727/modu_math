from __future__ import annotations

from modu_math.layout.sanitizer import sanitize_layout


def test_sanitize_layout_enforces_answer_input_and_removes_deleted_refs() -> None:
    layout = {
        "regions": [
            {
                "id": "region.diagram",
                "role": "diagram",
                "slot_ids": ["slot.answer", "slot.deleted", "slot.missing"],
            }
        ],
        "slots": [
            {
                "id": "slot.answer",
                "kind": "rect",
                "content": {
                    "x": 10,
                    "y": 20,
                    "width": 18,
                    "height": 18,
                    "fill": "#111111",
                    "interaction": {"type": "input", "role": "answer"},
                },
            },
            {
                "id": "slot.deleted",
                "kind": "rect",
                "content": {"x": 30, "y": 20, "width": 18, "height": 18},
            },
        ],
        "groups": [
            {
                "id": "group.problem_1",
                "member_ids": ["slot.answer", "slot.deleted", "slot.missing"],
            }
        ],
        "reading_order": [
            "region.diagram",
            "slot.answer",
            "slot.deleted",
            "slot.missing",
        ],
    }

    sanitized = sanitize_layout(layout, deleted_slots={"slot.deleted"})

    assert [slot["id"] for slot in sanitized["slots"]] == ["slot.answer"]
    content = sanitized["slots"][0]["content"]
    assert content["fill"] == "#ffffff"
    assert content["stroke"] == "#111827"
    assert content["interaction"]["include_in_submission"] is True
    assert content["interaction"]["group_id"] == "final_answer"
    assert content["input_style"]["font_size_mode"] == "auto"
    assert sanitized["regions"][0]["slot_ids"] == ["slot.answer"]
    assert sanitized["groups"][0]["member_ids"] == ["slot.answer"]
    assert sanitized["reading_order"] == ["region.diagram", "slot.answer"]


def test_sanitize_layout_clamps_text_box_answer_inside_canvas() -> None:
    layout = {
        "canvas": {"width": 900, "height": 320},
        "regions": [
            {
                "id": "region.answer",
                "role": "answer",
                "slot_ids": ["slot.answer_text"],
            }
        ],
        "slots": [
            {
                "id": "slot.answer_text",
                "kind": "text_box",
                "content": {
                    "text": "(소방서, 주민센터)",
                    "x": 645.922,
                    "y": 253.293,
                    "width": 206.199,
                    "height": 78.0,
                    "fill": "#111827",
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "include_in_submission": True,
                    },
                },
            }
        ],
    }

    sanitized = sanitize_layout(layout)
    content = sanitized["slots"][0]["content"]

    assert content["fill"] == "#111827"
    assert content["y"] == 234.0
    assert content["height"] == 78.0
    assert content["input_style"]["height"] == 78.0


def test_sanitize_layout_separates_following_slots_from_long_top_text() -> None:
    layout = {
        "canvas": {"width": 850, "height": 260},
        "slots": [
            {
                "id": "slot.question",
                "kind": "text_box",
                "content": {
                    "text": "다음은 지희네 반 학급 문고의 책의 수를 조사한 것입니다.",
                    "x": 25.924,
                    "y": 22.169,
                    "width": 674.552,
                    "height": 121.0,
                },
            },
            {
                "id": "slot.table.outer",
                "kind": "rect",
                "content": {
                    "x": 25.82,
                    "y": 104.385,
                    "width": 600,
                    "height": 90,
                },
            },
            {
                "id": "slot.table.h1",
                "kind": "line",
                "content": {
                    "x1": 25.82,
                    "y1": 149.385,
                    "x2": 625.82,
                    "y2": 149.385,
                },
            },
            {
                "id": "slot.table.r1c1",
                "kind": "text",
                "content": {
                    "text": "책 종류",
                    "x": 85.82,
                    "y": 132.385,
                    "font_size": 22,
                    "max_width": 110,
                },
            },
            {
                "id": "slot.table.r2c1",
                "kind": "text",
                "content": {
                    "text": "수(권)",
                    "x": 85.82,
                    "y": 177.385,
                    "font_size": 22,
                    "max_width": 110,
                },
            },
            {
                "id": "slot.answer",
                "kind": "rect",
                "content": {
                    "x": 658.67,
                    "y": 196.067,
                    "width": 126.029,
                    "height": 44.355,
                    "interaction": {"type": "input", "role": "answer"},
                },
            },
        ],
    }

    sanitized = sanitize_layout(layout)
    by_id = {slot["id"]: slot for slot in sanitized["slots"]}

    assert by_id["slot.table.outer"]["content"]["y"] == 151.169
    assert by_id["slot.table.h1"]["content"]["y1"] == 196.169
    assert by_id["slot.table.r1c1"]["content"]["y"] == 179.169
    assert by_id["slot.table.r2c1"]["content"]["y"] == 224.169
    assert by_id["slot.answer"]["content"]["y"] == 196.067


def test_sanitize_layout_preserves_editor_moved_slot_near_top_text() -> None:
    layout = {
        "canvas": {"width": 960, "height": 500},
        "slots": [
            {
                "id": "slot.instruction",
                "kind": "text_box",
                "content": {
                    "text": "2, 4, 6의 숫자 카드를 한 번씩만 사용하여 세 자리 수를 만들려고 합니다.",
                    "x": 20.0,
                    "y": 12.0,
                    "width": 920.0,
                    "height": 134.557,
                    "font_size": 30,
                },
            },
            {
                "id": "slot.question1",
                "kind": "text_box",
                "content": {
                    "text": "(1) 숫자 카드를 이용하여 만들 수 있는 가장 큰 세 자리 수를 쓰시오.",
                    "x": 16.852,
                    "y": 121.508,
                    "width": 918.492,
                    "height": 83,
                    "font_size": 30,
                },
            },
        ],
    }

    sanitized = sanitize_layout(layout, protected_slot_ids={"slot.question1"})
    by_id = {slot["id"]: slot for slot in sanitized["slots"]}

    assert by_id["slot.question1"]["content"]["y"] == 121.508
