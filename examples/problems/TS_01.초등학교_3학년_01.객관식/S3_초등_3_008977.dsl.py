from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008977",
        title="각인지 판별하기",
        canvas=Canvas(width=760, height=312, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.stem",
                    "slot.choice.o",
                    "slot.stem.part2",
                    "slot.choice.x",
                    "slot.stem.tail",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.upper",
                    "slot.diagram.lower",
                    "slot.diagram.anchor",
                    "slot.ui.left",
                    "slot.ui.center",
                ),
            ),
            Region(id="region.footer", role="answer_and_explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.qbox", prompt="", x=14.0, y=15.0, width=10.0, height=10.0),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="12.",
                style_role="question",
                x=30.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem",
                prompt="",
                text="각이면",
                style_role="question",
                x=67.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.o",
                prompt="",
                text="○",
                style_role="question",
                x=148.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.part2",
                prompt="",
                text=", 각이 아니면",
                style_role="question",
                x=178.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.x",
                prompt="",
                text="×",
                style_role="question",
                x=302.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.tail",
                prompt="",
                text="를 선택하세요.",
                style_role="question",
                x=331.0,
                y=26.0,
                font_size=28,
            ),
            LineSlot(id="slot.diagram.upper", prompt="", x1=383.0, y1=88.0, x2=505.0, y2=41.0),
            LineSlot(id="slot.diagram.lower", prompt="", x1=384.0, y1=109.0, x2=511.0, y2=117.0),
            CircleSlot(
                id="slot.diagram.anchor", prompt="", cx=384.0, cy=96.0, r=2.5, fill="#222222"
            ),
            CircleSlot(id="slot.ui.left", prompt="", cx=34.0, cy=136.0, r=8.0, fill="none"),
            TextSlot(
                id="slot.ui.center",
                prompt="",
                text="○",
                style_role="question",
                x=28.0,
                y=142.0,
                font_size=18,
            ),
            CircleSlot(id="slot.ui.right", prompt="", cx=412.0, cy=136.0, r=8.0, fill="none"),
            TextSlot(
                id="slot.ui.right.x",
                prompt="",
                text="×",
                style_role="question",
                x=405.0,
                y=142.0,
                font_size=18,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008977",
    "problem_type": "geometry_identification",
    "metadata": {
        "language": "ko",
        "question": "각인지 판별하는 문제",
        "instruction": "각이면 ○, 각이 아니면 ×를 선택한다.",
        "points": 1,
    },
    "domain": {
        "objects": [
            {"id": "obj.figure", "type": "shape", "description": "두 반직선처럼 보이는 도형"},
            {
                "id": "obj.angle_definition",
                "type": "definition",
                "description": "한 점에서 그은 두 반직선으로 이루어진 도형",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure", "obj.angle_definition"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.classify"],
            },
            "plan": {
                "method": "definition_check",
                "description": "그림이 각의 정의에 맞는지 판별한다.",
            },
            "execute": {
                "expected_operations": [
                    "inspect_figure",
                    "compare_with_definition",
                    "select_symbol",
                ]
            },
            "review": {"check_methods": ["definition_match_check", "choice_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "각이 아니면 선택할 기호"},
        "value": "×",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008977",
    "problem_type": "geometry_identification",
    "inputs": {
        "total_ticks": 1,
        "target_label": "×",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.figure", "value": {"description": "두 반직선처럼 보이는 도형"}},
        {
            "ref": "obj.angle_definition",
            "value": {"description": "한 점에서 그은 두 반직선으로 이루어진 도형"},
        },
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "definition_check",
    "plan": ["그림이 각의 정의에 맞는지 확인합니다.", "정의에 맞지 않으면 ×를 선택합니다."],
    "steps": [
        {"id": "step.1", "expr": "그림 판별", "value": "각이 아님"},
        {"id": "step.2", "expr": "선택 기호", "value": "×"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "각의 정의와 그림이 일치하는가",
            "expected": False,
            "actual": False,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택 기호가 정답과 일치하는가",
            "expected": "×",
            "actual": "×",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "각이 아니면 선택할 기호"},
        "value": "×",
        "unit": "",
    },
}
