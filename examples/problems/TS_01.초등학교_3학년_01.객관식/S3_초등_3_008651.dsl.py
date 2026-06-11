from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, compass_on_ruler_slots


def build_problem_template() -> ProblemTemplate:
    choice1 = compass_on_ruler_slots(
        "slot.choice1",
        x=198.0,
        y=181.0,
        unit_width=31.0,
        needle_mark=0.0,
        pencil_mark=2.3,
        hinge_offset_x=34.0,
        hinge_y_offset=-95.0,
        scale=0.95,
    )
    choice2 = compass_on_ruler_slots(
        "slot.choice2",
        x=438.0,
        y=181.0,
        unit_width=31.0,
        needle_mark=-0.3,
        pencil_mark=3.0,
        hinge_offset_x=32.0,
        hinge_y_offset=-95.0,
        scale=0.95,
    )
    choice3 = compass_on_ruler_slots(
        "slot.choice3",
        x=678.0,
        y=181.0,
        unit_width=31.0,
        needle_mark=0.0,
        pencil_mark=3.0,
        hinge_offset_x=43.0,
        hinge_y_offset=-95.0,
        scale=0.95,
    )
    answer = compass_on_ruler_slots(
        "slot.answer.diagram",
        x=61.0,
        y=355.0,
        unit_width=31.0,
        needle_mark=0.0,
        pencil_mark=3.0,
        hinge_offset_x=48.0,
        hinge_y_offset=-95.0,
        scale=0.95,
    )

    return ProblemTemplate(
        id="S3_초등_3_008651",
        title="컴퍼스를 3 cm가 되도록 벌린 것 찾기",
        canvas=Canvas(width=940, height=460, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.prefix", "slot.q.text"),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=tuple(slot.id for slot in (*choice1, *choice2, *choice3)),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer.label", *(slot.id for slot in answer), "slot.explanation.label", "slot.explanation.text1", "slot.explanation.text2"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.prefix",
                prompt="",
                text="□ 24.",
                style_role="question",
                x=14.0,
                y=31.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="컴퍼스를 3 cm가 되도록 벌린 것을 찾아 선택해 보세요.",
                style_role="question",
                x=72.0,
                y=31.0,
                font_size=24,
            ),
            *choice1,
            *choice2,
            *choice3,
            TextSlot(
                id="slot.answer.label",
                prompt="",
                text="(정답)",
                style_role="answer",
                x=14.0,
                y=314.0,
                font_size=17,
            ),
            *answer,
            TextSlot(
                id="slot.explanation.label",
                prompt="",
                text="(해설)",
                style_role="explanation",
                x=14.0,
                y=421.0,
                font_size=17,
            ),
            TextSlot(
                id="slot.explanation.text1",
                prompt="",
                text="컴퍼스의 침을 자의 눈금 0에 맞추고 연필심을 자의 눈금 3에 오도록 컴퍼스를 벌",
                style_role="explanation",
                x=61.0,
                y=421.0,
                font_size=23,
            ),
            TextSlot(
                id="slot.explanation.text2",
                prompt="",
                text="린 것을 찾습니다.",
                style_role="explanation",
                x=36.0,
                y=452.0,
                font_size=23,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "compass", "ruler", "length"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008651",
    "problem_type": "visual_selection",
    "metadata": {
        "language": "ko",
        "question": "컴퍼스를 3 cm가 되도록 벌린 것을 찾아 선택해 보세요.",
        "instruction": "컴퍼스의 침과 연필심 사이가 3 cm인 그림을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.compass", "type": "compass"},
            {"id": "obj.ruler", "type": "ruler"},
            {"id": "obj.length", "type": "length", "value": 3, "unit": "cm"},
        ],
        "relations": [
            {
                "id": "rel.target_gap",
                "type": "distance_equals",
                "from_id": "obj.compass",
                "to_id": "obj.length",
                "description": "컴퍼스의 침과 연필심 사이의 거리가 3 cm이다.",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.length", "obj.compass", "obj.ruler"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.target_gap"],
            },
            "plan": {
                "method": "visual_match",
                "description": "자의 0 눈금과 3 눈금에 각각 컴퍼스의 침과 연필심이 맞는 그림을 찾는다.",
            },
            "execute": {"expected_operations": ["compare_with_ruler_marks", "select_matching_compass"]},
            "review": {"check_methods": ["condition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008651",
    "problem_type": "visual_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "3 cm",
        "target_ticks": 3,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [
        {"ref": "obj.length", "value": {"amount": 3, "unit": "cm"}},
        {"ref": "obj.ruler", "value": {"marks": [0, 1, 2, 3]}},
    ],
    "target": {"ref": "answer.target", "type": "selected_compass"},
    "method": "visual_match",
    "plan": [
        "컴퍼스의 침이 자의 눈금 0에 있는지 확인한다.",
        "연필심이 자의 눈금 3에 오도록 벌어진 그림을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "침을 0 눈금에 맞춤", "value": True},
        {"id": "step.2", "expr": "연필심을 3 눈금에 맞춤", "value": True},
        {"id": "step.3", "expr": "3 cm 조건과 일치하는 그림 선택", "value": 3},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "침과 연필심 사이가 3 cm인가?",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": 3,
        "unit": "",
    },
}
