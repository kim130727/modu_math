from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008991",
        title="직사각형 판별",
        canvas=Canvas(width=660, height=370, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q_num",
                    "slot.q_instr",
                    "slot.shape_right",
                    "slot.mark_x",
                    "slot.mark_dot",
                    "slot.answer_circle",
                ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.rect_explain",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="29.",
                style_role="question",
                x=18.0,
                y=33.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_instr",
                prompt="",
                text="직사각형이면 ○, 직사각형이 아니면 ×를 선택하세요.",
                style_role="question",
                x=74.0,
                y=33.0,
                font_size=28,
            ),
            RectSlot(id="slot.shape_right", prompt="", x=412.0, y=40.0, width=75.0, height=90.0),
            TextSlot(
                id="slot.mark_x",
                prompt="",
                text="×",
                style_role="label",
                x=449.0,
                y=140.0,
                font_size=28,
            ),
            CircleSlot(id="slot.mark_dot", prompt="", cx=34.0, cy=145.0, r=6.0, fill="#FFFFFF"),
            CircleSlot(
                id="slot.answer_circle", prompt="", cx=72.0, cy=183.0, r=10.0, fill="#FFFFFF"
            ),
            RectSlot(id="slot.rect_explain", prompt="", x=52.0, y=212.0, width=74.0, height=90.0),
            LineSlot(id="slot.rect_explain.lt1", prompt="", x1=52.0, y1=212.0, x2=61.0, y2=212.0),
            LineSlot(id="slot.rect_explain.lt2", prompt="", x1=52.0, y1=212.0, x2=52.0, y2=221.0),
            LineSlot(id="slot.rect_explain.rt1", prompt="", x1=126.0, y1=212.0, x2=117.0, y2=212.0),
            LineSlot(id="slot.rect_explain.rt2", prompt="", x1=126.0, y1=212.0, x2=126.0, y2=221.0),
            LineSlot(id="slot.rect_explain.lb1", prompt="", x1=52.0, y1=302.0, x2=61.0, y2=302.0),
            LineSlot(id="slot.rect_explain.lb2", prompt="", x1=52.0, y1=302.0, x2=52.0, y2=293.0),
            LineSlot(id="slot.rect_explain.rb1", prompt="", x1=126.0, y1=302.0, x2=117.0, y2=302.0),
            LineSlot(id="slot.rect_explain.rb2", prompt="", x1=126.0, y1=302.0, x2=126.0, y2=293.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008991",
    "problem_type": "도형_판별",
    "metadata": {
        "language": "ko",
        "question": "직사각형이면 ○, 직사각형이 아니면 ×를 선택하는 문제",
        "instruction": "직사각형인지 판별하여 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape_right", "type": "quadrilateral", "property": "rectangle_test_shape"},
            {"id": "obj.rect_explain", "type": "quadrilateral", "property": "rectangle_example"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.shape_right", "obj.rect_explain"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.definition"],
            },
            "plan": {
                "method": "definition_check",
                "description": "직사각형의 정의에 맞는지 확인하여 선택 기호를 정한다.",
            },
            "execute": {
                "expected_operations": ["shape_property_check", "match_definition", "select_symbol"]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection_symbol",
            "description": "직사각형이면 ○, 직사각형이 아니면 × 중 선택",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008991",
    "problem_type": "도형_판별",
    "inputs": {
        "total_ticks": 1,
        "target_label": "selection_symbol",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.shape_right",
            "value": {"type": "quadrilateral", "property": "rectangle_test_shape"},
        },
        {
            "ref": "obj.rect_explain",
            "value": {"type": "quadrilateral", "property": "rectangle_example"},
        },
    ],
    "target": {"ref": "answer.target", "type": "selection_symbol"},
    "method": "definition_check",
    "plan": ["도형이 직사각형의 정의에 맞는지 확인한다.", "판별 결과에 따라 ○ 또는 ×를 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "직사각형의 정의 확인", "value": "네 각이 모두 직각인 사각형"},
        {"id": "step.2", "expr": "판별 대상 도형의 성질 확인", "value": "TODO"},
        {"id": "step.3", "expr": "선택 기호 결정", "value": "TODO"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의와 판별 결과가 일치하는지 확인",
            "expected": "일치",
            "actual": "TODO",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection_symbol",
            "description": "직사각형이면 ○, 직사각형이 아니면 × 중 선택",
        },
        "value": 0,
        "unit": "",
    },
}
