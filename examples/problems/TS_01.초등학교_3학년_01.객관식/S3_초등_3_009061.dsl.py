from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009061",
        title="도형을 보고 알맞은 말을 선택하세요",
        canvas=Canvas(width=760, height=210, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.no",
                    "slot.q1",
                    "slot.shape.line",
                    "slot.shape.left_mark",
                    "slot.shape.left_point",
                    "slot.shape.right_point",
                    "slot.choice",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.no",
                prompt="",
                text="100.",
                style_role="question",
                x=10.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="도형을 보고 알맞은 말을 선택하세요.",
                style_role="question",
                x=70.0,
                y=26.0,
                font_size=28,
            ),
            LineSlot(id="slot.shape.line", prompt="", x1=95.0, y1=76.0, x2=280.0, y2=76.0),
            TextSlot(
                id="slot.shape.left_mark",
                prompt="",
                text="ㄷ",
                style_role="diagram",
                x=89.0,
                y=68.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.shape.left_point", prompt="", cx=96.0, cy=76.0, r=3.2, fill="#222222"
            ),
            CircleSlot(
                id="slot.shape.right_point", prompt="", cx=280.0, cy=76.0, r=3.2, fill="#222222"
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 선분 ㅅ o , 반직선 ㅅ o , 직선 ㅅ o )",
                style_role="question",
                x=330.0,
                y=82.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009061",
    "problem_type": "도형_선의종류_선택",
    "metadata": {
        "language": "ko",
        "question": "도형을 보고 알맞은 말을 선택하세요.",
        "instruction": "도형의 종류를 보고 알맞은 말을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape", "type": "line_shape", "label_options": ["선분", "반직선", "직선"]}
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.shape"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.classify_shape"],
            },
            "plan": {
                "method": "도형의 끝 표시를 보고 종류를 판단한다",
                "description": "도형의 양 끝 표시를 확인하여 선분, 반직선, 직선 중 알맞은 말을 고른다.",
            },
            "execute": {"expected_operations": ["ends_observation", "shape_classification"]},
            "review": {"check_methods": ["label_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "shape_name", "description": "도형의 이름"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009061",
    "problem_type": "도형_선의종류_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "도형의 이름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.shape", "value": {"label_options": ["선분", "반직선", "직선"]}}],
    "target": {"ref": "answer.target", "type": "shape_name"},
    "method": "도형 분류",
    "plan": ["도형의 끝 표시를 보고 종류를 판단한다.", "보기 중 알맞은 말을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "도형의 양 끝 표시를 확인한다", "value": "양 끝이 표시된 선"},
        {"id": "step.2", "expr": "보기와 비교하여 도형의 종류를 고른다", "value": "선분"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분은 두 점을 이은 선과 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "shape_name", "description": "도형의 이름"},
        "value": 0,
        "unit": "",
    },
}
