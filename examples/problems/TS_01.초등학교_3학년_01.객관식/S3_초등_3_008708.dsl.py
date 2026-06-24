from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008708",
        title="원의 지름",
        canvas=Canvas(width=960, height=620, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                ),
            ),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.top.circle", "slot.top.diameter", "slot.top.dot1", "slot.top.dot2"),
            ),
            Region(id="region.diagram.bottom", role="diagram", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="    원의 지름을 그림과 같이 그렸습니다. 바르게 그렸으면 ○,",
                style_role="question",
                x=30,
                y=65,
                font_size=30,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="틀리게 그렸으면 ×표를 선택하세요.",
                style_role="question",
                x=30,
                y=120,
                font_size=30,
            ),
            CircleSlot(
                id="slot.top.circle",
                prompt="",
                cx=415,
                cy=305,
                r=150,
                fill="none",
                stroke="#222222",
            ),
            LineSlot(
                id="slot.top.diameter", prompt="", x1=265, y1=305, x2=570, y2=305, stroke="#222222"
            ),
            CircleSlot(
                id="slot.top.dot1", prompt="", cx=420, cy=285, r=5, fill="none", stroke="#666666"
            ),
            CircleSlot(id="slot.top.dot2", prompt="", cx=417, cy=305, r=5, fill="#ff3aa7"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008708",
    "problem_type": "ox_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 지름을 그림과 같이 그렸습니다. 바르게 그렸으면 ○, 틀리게 그렸으면 ×표를 선택하세요.",
        "instruction": "원의 지름이 바르게 그려졌는지 판단하는 문제이다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.top_circle", "type": "circle"},
            {"id": "obj.bottom_circle", "type": "circle"},
            {"id": "obj.diameter_line", "type": "line", "role": "diameter_candidate"},
            {"id": "obj.center_marks", "type": "mark_group"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.top_circle", "obj.diameter_line"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.evaluate_diameter"],
            },
            "plan": {
                "method": "correctness_judgment",
                "description": "그림의 지름 표현이 바른지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_circle_and_line",
                    "compare_with_diameter_condition",
                ]
            },
            "review": {"check_methods": ["visual_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "바르게 그렸으면 ○, 틀리게 그렸으면 ×"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008708",
    "problem_type": "ox_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "○/×",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.top_circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter_line", "value": {"type": "line", "role": "diameter_candidate"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "correctness_judgment",
    "plan": ["원과 선의 관계를 관찰한다.", "지름으로 그린 표현이 바른지 판단한다."],
    "steps": [
        {"id": "step.1", "expr": "원과 수평선의 배치 관찰", "value": "관찰됨"},
        {"id": "step.2", "expr": "지름 표현의 정오 판정", "value": "미확정"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택 기호는 ○ 또는 ×여야 함",
            "expected": "○/×",
            "actual": "○/×",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "바르게 그렸으면 ○, 틀리게 그렸으면 ×"},
        "value": 0,
        "unit": "",
    },
}
