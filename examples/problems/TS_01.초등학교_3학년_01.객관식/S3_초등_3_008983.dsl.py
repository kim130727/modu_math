from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008983",
        title="직각을 선택하세요",
        canvas=Canvas(width=850, height=398, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.num", "slot.title"),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.a",
                    "slot.opt1.b",
                    "slot.opt2.a",
                    "slot.opt2.b",
                    "slot.opt3.a",
                    "slot.opt3.b",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer.shape.a", "slot.answer.shape.b"),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.expl.shape.a", "slot.expl.shape.b", "slot.expl.square"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.num",
                prompt="",
                text="18.",
                style_role="question",
                x=16.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="직각을 선택하세요.",
                style_role="question",
                x=68.0,
                y=28.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt1.a", prompt="", x1=164.0, y1=49.0, x2=199.0, y2=107.0),
            LineSlot(id="slot.opt1.b", prompt="", x1=199.0, y1=107.0, x2=268.0, y2=107.0),
            LineSlot(id="slot.opt2.a", prompt="", x1=403.0, y1=46.0, x2=403.0, y2=107.0),
            LineSlot(id="slot.opt2.b", prompt="", x1=403.0, y1=107.0, x2=473.0, y2=107.0),
            LineSlot(id="slot.opt3.a", prompt="", x1=636.0, y1=85.0, x2=704.0, y2=47.0),
            LineSlot(id="slot.opt3.b", prompt="", x1=636.0, y1=85.0, x2=703.0, y2=109.0),
            LineSlot(id="slot.answer.shape.a", prompt="", x1=51.0, y1=128.0, x2=51.0, y2=206.0),
            LineSlot(id="slot.answer.shape.b", prompt="", x1=51.0, y1=206.0, x2=118.0, y2=206.0),
            LineSlot(id="slot.expl.shape.a", prompt="", x1=33.0, y1=325.0, x2=33.0, y2=361.0),
            LineSlot(id="slot.expl.shape.b", prompt="", x1=33.0, y1=361.0, x2=104.0, y2=361.0),
            RectSlot(id="slot.expl.square", prompt="", x=33.0, y=351.0, width=10.0, height=10.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008983",
    "problem_type": "angle_identification",
    "metadata": {
        "language": "ko",
        "question": "직각을 선택하세요.",
        "instruction": "보기에서 직각인 각을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.option_1", "type": "angle"},
            {"id": "obj.option_2", "type": "angle"},
            {"id": "obj.option_3", "type": "angle"},
            {"id": "obj.right_angle_example", "type": "angle", "property": "right_angle"},
            {"id": "obj.square_mark", "type": "marker", "property": "right_angle_marker"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.option_1", "obj.option_2", "obj.option_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_right_angle"],
            },
            "plan": {
                "method": "shape_matching",
                "description": "보기의 각 모양을 직각의 ㄴ자 형태와 비교한다.",
            },
            "execute": {"expected_operations": ["compare_angle_shapes", "match_right_angle_form"]},
            "review": {"check_methods": ["compare_with_right_angle_example"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "직각인 보기"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008983",
    "problem_type": "angle_identification",
    "inputs": {
        "total_ticks": 3,
        "target_label": "직각인 보기",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option_1", "value": {"type": "angle"}},
        {"ref": "obj.option_2", "value": {"type": "angle"}},
        {"ref": "obj.option_3", "value": {"type": "angle"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "shape_matching",
    "plan": ["보기 3개를 직각의 ㄴ자 형태와 비교한다.", "직각 표시가 필요한 각의 모양을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "보기의 각 모양을 직각 예시와 비교한다", "value": "비교"},
        {"id": "step.2", "expr": "ㄴ자 형태와 가장 잘 맞는 보기를 찾는다", "value": "판별"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "직각 예시와 동일한 ㄴ자 형태인지 확인",
            "expected": "직각 형태",
            "actual": "미확정",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "직각인 보기"},
        "value": 0,
        "unit": "",
    },
}
