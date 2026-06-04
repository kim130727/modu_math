from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008651",
        title="컴퍼스를 3 cm가 되도록 벌린 것을 찾아 선택해 보세요",
        canvas=Canvas(width=940.0, height=460.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.prefix",
                    "slot.q.text",
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.answer_choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.prefix",
                prompt="",
                text="□ 24.",
                style_role="question",
                x=12.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="컴퍼스를 3 cm가 되도록 벌린 것을 찾아 선택해 보세요.",
                style_role="question",
                x=78.0,
                y=34.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice1", prompt="", x=214.0, y=56.0, width=102.0, height=146.0
            ),
            RectSlot(
                id="slot.choice2", prompt="", x=462.0, y=56.0, width=102.0, height=146.0
            ),
            RectSlot(
                id="slot.choice3", prompt="", x=694.0, y=56.0, width=102.0, height=146.0
            ),
            RectSlot(
                id="slot.answer_choice",
                prompt="",
                x=58.0,
                y=228.0,
                width=102.0,
                height=146.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008651",
    "problem_type": "visual_selection",
    "metadata": {
        "language": "ko",
        "question": "컴퍼스를 3 cm가 되도록 벌린 것을 찾아 선택해 보세요.",
        "instruction": "조건에 맞는 컴퍼스 그림을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.compass", "type": "compass"},
            {"id": "obj.ruler", "type": "ruler"},
            {"id": "obj.length", "type": "length", "value": 3, "unit": "cm"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.length", "obj.compass", "obj.ruler"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.fit_gap"],
            },
            "plan": {
                "method": "visual_match",
                "description": "자의 0과 3 눈금에 맞는 컴퍼스 벌림 상태를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_with_ruler_marks",
                    "select_matching_compass",
                ]
            },
            "review": {"check_methods": ["condition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_compass",
            "description": "3 cm가 되도록 벌린 컴퍼스 그림",
        },
        "value": 1,
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
        {"ref": "obj.length", "value": 3, "unit": "cm"},
        {"ref": "obj.ruler", "value": {"marks": [0, 1, 2, 3]}},
    ],
    "target": {"ref": "answer.target", "type": "selected_compass"},
    "method": "visual_match",
    "plan": [
        "자의 0 눈금과 3 눈금에 맞는 벌림 상태를 찾는다.",
        "조건에 맞는 컴퍼스 그림을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "침을 0에 맞춤", "value": True},
        {"id": "step.2", "expr": "연필심을 3에 맞춤", "value": True},
        {
            "id": "step.3",
            "expr": "3 cm 조건과 일치하는 그림 선택",
            "value": "정답 그림",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "0과 3 눈금에 맞는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_compass",
            "description": "3 cm가 되도록 벌린 컴퍼스 그림",
        },
        "value": 1,
        "unit": "",
    },
}
