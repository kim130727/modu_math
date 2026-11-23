"""ModuMath Problem DSL: 이등변삼각형 모두 찾기 (S3_초등_4_007362)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007362"
PROBLEM_TITLE = "이등변삼각형을 모두 찾아 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "① 가, 나",
        "② 가, 다",
        "③ 나, 라",
        "④ 다, 라",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.missed_isosceles",
                    "condition": "answer_not_2",
                    "concept": "이등변삼각형의 성질",
                    "reason": "두 변의 길이가 같은 삼각형 가와 다를 정확히 찾지 못함",
                    "feedback": "정삼각형(가)도 두 변의 길이가 같으므로 이등변삼각형에 포함됩니다. 두 변의 길이가 같은 삼각형은 가와 다입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_find_all_isosceles",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "중",
    },
    "entities": {
        "ga": {"label": "가", "is_isosceles": True},
        "na": {"label": "나", "is_isosceles": False},
        "da": {"label": "다", "is_isosceles": True},
        "ra": {"label": "라", "is_isosceles": False},
    },
    "relations": [
        {
            "type": "multi_classification",
            "property": "isosceles",
            "correct_entities": ["ga", "da"],
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="37. 이등변삼각형을 모두 찾아 선택해 보세요.",
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

    diagram_slots = [
        RectSlot(id="slot.diagram.green_box", prompt="", x=118, y=82, width=650, height=144, fill="#ffffff", stroke="#22c55e", stroke_width=2.0),
        PolygonSlot(id="slot.diagram.ga", prompt="", points=[(150, 102), (242, 102), (196, 198)], fill="none", stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_ga", prompt="", text="가", x=196, y=126, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.na", prompt="", points=[(396, 114), (254, 192), (452, 192)], fill="none", stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_na", prompt="", text="나", x=374, y=156, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.da", prompt="", points=[(476, 152), (636, 104), (636, 200)], fill="none", stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_da", prompt="", text="다", x=594, y=144, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.ra", prompt="", points=[(668, 104), (668, 200), (744, 200)], fill="none", stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.lbl_ra", prompt="", text="라", x=694, y=168, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    opts = ["① 가, 나", "② 가, 다", "③ 나, 라", "④ 다, 라"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 108 + idx * 176
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=252,
                width=148,
                height=48,
                fill="#f8fafc",
                stroke="#94a3b8",
                stroke_width=1.5,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label.split(" ")[0],
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(
            TextSlot(
                id=f"slot.diagram.opt_text_{idx}",
                prompt="",
                text=label,
                x=cx + 74,
                y=264,
                font_size=18,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
            )
        )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=330, coordinate_mode="logical"),
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
        {"ref": "ga", "value": "두 변의 길이가 같은 삼각형"},
        {"ref": "na", "value": "세 변의 길이가 다른 삼각형"},
        {"ref": "da", "value": "두 변의 길이가 같은 삼각형"},
        {"ref": "ra", "value": "세 변의 길이가 다른 직각삼각형"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "이등변삼각형 모두 찾기", "unit": ""},
    "method": "triangle_classification",
    "steps": [
        {
            "id": "find_all",
            "expr": "이등변삼각형 = 가, 다",
            "explanation": "두 변의 길이가 같은 삼각형은 가와 다입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
