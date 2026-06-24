from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008988",
        title="직각삼각형 판별",
        canvas=Canvas(width=720, height=270, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4", "slot.q5"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.tri.1", "slot.tri.2", "slot.tri.3", "slot.tri.mark"),
            ),
            Region(
                id="region.footer", role="footer", flow="absolute", slot_ids=("slot.mark.circle",)
            ),
        ),
        slots=(
            RectSlot(id="slot.qbox", prompt="", x=10.0, y=16.0, width=12.0, height=12.0),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="26.",
                style_role="question",
                x=34.0,
                y=25.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="직각삼각형이면",
                style_role="question",
                x=70.0,
                y=25.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="○",
                style_role="question",
                x=227.0,
                y=25.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text=", 직각삼각형이 아니면",
                style_role="question",
                x=252.0,
                y=25.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="×",
                style_role="question",
                x=446.0,
                y=25.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q6",
                prompt="",
                text="를 선택하세요.",
                style_role="question",
                x=470.0,
                y=25.0,
                font_size=28,
            ),
            LineSlot(id="slot.tri.1", prompt="", x1=438.0, y1=43.0, x2=386.0, y2=113.0),
            LineSlot(id="slot.tri.2", prompt="", x1=438.0, y1=43.0, x2=492.0, y2=113.0),
            LineSlot(id="slot.tri.3", prompt="", x1=386.0, y1=113.0, x2=492.0, y2=113.0),
            TextSlot(
                id="slot.tri.mark",
                prompt="",
                text="×",
                style_role="annotation",
                x=426.0,
                y=123.0,
                font_size=28,
            ),
            CircleSlot(id="slot.mark.circle", prompt="", cx=24.0, cy=120.0, r=7.0, fill="#ffffff"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("도형판별", "직각삼각형", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008988",
    "problem_type": "shape_judgment",
    "metadata": {
        "language": "ko",
        "question": "직각삼각형 여부를 보고 ○ 또는 ×를 선택하는 문제",
        "instruction": "직각삼각형이면 ○, 직각삼각형이 아니면 ×를 선택하세요.",
    },
    "domain": {
        "objects": [{"id": "obj.triangle", "type": "triangle"}],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.triangle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.judge_right_triangle"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "삼각형이 직각삼각형인지 여부를 보고 선택 기호를 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_triangle_shape",
                    "check_right_angle_presence",
                    "select_symbol",
                ]
            },
            "review": {"check_methods": ["definition_check", "symbol_selection_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection_symbol",
            "description": "직각삼각형 여부에 따라 선택하는 기호",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008988",
    "problem_type": "shape_judgment",
    "inputs": {
        "total_ticks": 1,
        "target_label": "선택 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.triangle", "value": {"type": "triangle"}}],
    "target": {"ref": "answer.target", "type": "selection_symbol"},
    "plan": "삼각형의 직각 여부를 보고 선택 기호를 판단한다.",
    "steps": [{"id": "step.1", "expr": "삼각형의 직각 여부 확인", "value": "uncertain"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "직각삼각형 판별 기준과 일치하는지 확인",
            "expected": "right_triangle_classification",
            "actual": "uncertain",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection_symbol",
            "description": "직각삼각형 여부에 따라 선택하는 기호",
        },
        "value": 0,
        "unit": "",
    },
}
