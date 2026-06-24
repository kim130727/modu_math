from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009021",
        title="반직선을 읽는 방법",
        canvas=Canvas(width=850.0, height=520.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.choice_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.box.bg", "slot.c1", "slot.c2", "slot.c3", "slot.choice"),
            ),
            Region(id="region.answer_explanation", role="supporting", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="59. 반직선을 읽는 방법에 대한 설명으로 옳은 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=24.0,
                y=36.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box.bg",
                prompt="",
                x=92.0,
                y=75.0,
                width=708.0,
                height=133.0,
                fill="#DCD8F1",
            ),
            TextSlot(
                id="slot.c1",
                prompt="",
                text="㉠ 반직선은 두 점 중 어느 점을 먼저 읽어도 상관없습니다.",
                style_role="body",
                x=115.0,
                y=107.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.c2",
                prompt="",
                text="㉡ 반직선 ㄴㄱ은 반직선 ㄴㄱ이라고 읽을 수 있습니다.",
                style_role="body",
                x=115.0,
                y=143.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.c3",
                prompt="",
                text="㉢ 반직선은 반드시 시작점을 먼저 읽습니다.",
                style_role="body",
                x=115.0,
                y=179.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( ㉠ , ㉡ , ㉢ )",
                style_role="body",
                x=639.0,
                y=255.0,
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
    "problem_id": "S3_초등_3_009021",
    "problem_type": "multiple_choice_concept",
    "metadata": {
        "language": "ko",
        "question": "반직선을 읽는 방법에 대한 설명으로 옳은 것을 찾는 문제",
        "instruction": "옳은 설명을 고르기",
        "points": 0,
    },
    "domain": {
        "objects": [
            {"id": "obj.railway_concept", "type": "concept", "name": "반직선"},
            {
                "id": "obj.statement.a",
                "type": "statement",
                "name": "두 점 중 어느 점을 먼저 읽어도 상관없다",
            },
            {
                "id": "obj.statement.b",
                "type": "statement",
                "name": "반직선 ㄴㄱ은 반직선 ㄴㄱ이라고 읽을 수 있다",
            },
            {
                "id": "obj.statement.c",
                "type": "statement",
                "name": "반직선은 반드시 시작점을 먼저 읽는다",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.statement.a", "obj.statement.b", "obj.statement.c"],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "statement_verification",
                "description": "각 설명이 반직선의 읽는 방법에 맞는지 판단한다.",
            },
            "execute": {"expected_operations": ["compare_statements", "select_true_statement"]},
            "review": {"check_methods": ["consistency_with_definition"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "옳은 설명의 기호"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009021",
    "problem_type": "multiple_choice_concept",
    "inputs": {
        "total_ticks": 3,
        "target_label": "옳은 설명의 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.statement.a", "value": "두 점 중 어느 점을 먼저 읽어도 상관없다"},
        {"ref": "obj.statement.b", "value": "반직선 ㄴㄱ은 반직선 ㄴㄱ이라고 읽을 수 있다"},
        {"ref": "obj.statement.c", "value": "반직선은 반드시 시작점을 먼저 읽는다"},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "statement_verification",
    "plan": ["각 문장을 반직선의 읽는 방법과 비교한다.", "옳은 문장을 기호로 고른다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "㉠: 반직선은 두 점 중 어느 점을 먼저 읽어도 되는가?",
            "value": False,
        },
        {"id": "step.2", "expr": "㉡: 반직선 ㄴㄱ을 ㄴㄱ으로 읽는 것이 맞는가?", "value": False},
        {"id": "step.3", "expr": "㉢: 반직선은 시작점을 먼저 읽는가?", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "옳은 문항이 ㉢인지 확인",
            "expected": "㉢",
            "actual": "㉢",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "옳은 설명의 기호"},
        "value": 3,
        "unit": "",
    },
}
