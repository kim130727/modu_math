"""ModuMath Problem DSL: 사다리꼴에 대한 옳은 설명 찾기 (S3_초등_4_007549)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007549"
PROBLEM_TITLE = "사다리꼴에 대한 설명으로 옳은 것 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.confused_length_and_parallel",
                    "condition": "answer_equals_1",
                    "concept": "사다리꼴의 정의",
                    "reason": "변의 길이와 평행을 혼동함",
                    "feedback": "사다리꼴은 변의 길이와 상관없이 한 쌍의 마주 보는 변이 평행한 사각형입니다. 따라서 ②가 옳은 설명입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_trapezoid_definition",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "하",
    },
    "entities": {
        "opt_0": {"label": "① 한 쌍의 마주 보는 변의 길이가 같아.", "is_correct": False},
        "opt_1": {"label": "② 한 쌍의 마주 보는 변이 평행해.", "is_correct": True},
    },
    "relations": [
        {
            "type": "definition",
            "term": "사다리꼴",
            "correct_entity": "opt_1",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="92. 사다리꼴에 대한 설명으로 옳은 것을 찾아 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=136, y=144, width=258, height=106, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=492, y=144, width=258, height=106, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        CircleSlot(id="slot.diagram.puppy", prompt="", cx=265, cy=112, r=24, fill="#fed7aa", stroke="#c2410c", stroke_width=1.4),
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=156, y=156, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        TextBoxSlot(id="slot.diagram.t0", prompt="", text="한 쌍의 마주 보는\n변의 길이가 같아.", x=156, y=170, width=218, height=64, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),

        CircleSlot(id="slot.diagram.tiger", prompt="", cx=621, cy=112, r=24, fill="#fde047", stroke="#b45309", stroke_width=1.4),
        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=512, y=156, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        TextBoxSlot(id="slot.diagram.t1", prompt="", text="한 쌍의 마주 보는\n변이 평행해.", x=512, y=170, width=218, height=64, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=282, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, choice_0, choice_1, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "opt_0", "value": "한 쌍의 마주 보는 변의 길이가 같아."},
        {"ref": "opt_1", "value": "한 쌍의 마주 보는 변이 평행해."},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "사다리꼴에 대한 옳은 설명", "unit": ""},
    "method": "definition_matching",
    "steps": [
        {
            "id": "match_definition",
            "expr": "사다리꼴 = 한 쌍의 마주 보는 변이 평행한 사각형",
            "explanation": "변의 길이와 상관없이 사다리꼴은 한 쌍의 마주 보는 변이 평행합니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
