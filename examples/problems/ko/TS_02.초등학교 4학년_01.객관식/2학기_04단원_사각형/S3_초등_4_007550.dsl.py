"""ModuMath Problem DSL: 사다리꼴이 되는 자른 선 고르기 (S3_초등_4_007550)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007550"
PROBLEM_TITLE = "사각형에서 잘라 내면 사다리꼴이 되는 선의 기호 선택하기"

ANSWER = {
    "value": "ㄷ",
    "answer_index": 2,
    "unit": "",
    "values": ["ㄷ"],
    "choices": [
        "ㄱ",
        "ㄴ",
        "ㄷ",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "ㄷ",
            "diagnostics": [
                {
                    "id": "diag.wrong_cut_line",
                    "condition": "answer_not_digeut",
                    "concept": "사다리꼴의 성질",
                    "reason": "사각형의 위쪽 변과 평행하지 않은 선(ㄱ 또는 ㄴ)을 선택함",
                    "feedback": "한 쌍의 마주 보는 변이 평행하려면 위쪽 변과 평행한 가로선 ㄷ을 따라 잘라야 합니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_trapezoid_cut_line",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "중",
    },
    "entities": {
        "line_g": {"label": "ㄱ", "is_parallel": False},
        "line_n": {"label": "ㄴ", "is_parallel": False},
        "line_d": {"label": "ㄷ", "is_parallel": True},
    },
    "relations": [
        {
            "type": "parallel_line_match",
            "correct_entity": "line_d",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="93. 사각형에서 어느 선을 따라 잘라 내면 사다리꼴이 되는지 기호를 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        PolygonSlot(id="slot.diagram.quad", prompt="", points=[(344, 128), (546, 128), (484, 248), (344, 224)], fill="none", stroke="#111827", stroke_width=2.0),
        LineSlot(id="slot.diagram.cut_g", prompt="", x1=332, y1=114, x2=454, y2=258, stroke="#ec4899", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_g", prompt="", text="ㄱ", x=322, y=94, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        LineSlot(id="slot.diagram.cut_n", prompt="", x1=426, y1=110, x2=498, y2=264, stroke="#ec4899", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_n", prompt="", text="ㄴ", x=422, y=88, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        LineSlot(id="slot.diagram.cut_d", prompt="", x1=316, y1=224, x2=562, y2=224, stroke="#ec4899", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_d", prompt="", text="ㄷ", x=582, y=214, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    opts = ["ㄱ", "ㄴ", "ㄷ"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 218 + idx * 165
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=286,
                width=120,
                height=46,
                fill="#f8fafc",
                stroke="#94a3b8",
                stroke_width=1.5,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label,
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_text_{idx}", prompt="", text=label, x=cx + 60, y=297, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=356, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, *choice_slots, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "line_g", "value": "대각선 ㄱ"},
        {"ref": "line_n", "value": "대각선 ㄴ"},
        {"ref": "line_d", "value": "위쪽 변과 평행한 선 ㄷ"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "사다리꼴이 되는 선", "unit": ""},
    "method": "parallel_check",
    "steps": [
        {
            "id": "find_parallel",
            "expr": "선 ㄷ ∥ 위쪽 변",
            "explanation": "한 쌍의 마주 보는 변이 평행하려면 ㄷ을 따라 잘라야 합니다.",
            "value": "ㄷ",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
