"""ModuMath Problem DSL: 각도기로 그린 75° 이등변삼각형 찾기 (S3_초등_4_007366)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007366"
PROBLEM_TITLE = "두 각의 크기가 75°인 이등변삼각형 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.wrong_angle_reading",
                    "condition": "answer_equals_2",
                    "concept": "각도기로 이등변삼각형 그리기",
                    "reason": "70°로 그린 삼각형(②)을 선택함",
                    "feedback": "①은 각도기의 안쪽 눈금 75°에 맞추어 그렸고, ②는 70°에 맞추어 그렸습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_protractor_isosceles",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "중",
    },
    "entities": {
        "tri_0": {"label": "①", "base_angle": 75},
        "tri_1": {"label": "②", "base_angle": 70},
    },
    "relations": [
        {
            "type": "angle_match",
            "target_angle": 75,
            "correct_entity": "tri_0",
            "distractor": "tri_1",
        }
    ],
}


def _add_protractor_triangle(slots: list, prefix: str, cx: int, cy: int, r: int, deg: int) -> None:
    slots.append(PathSlot(id=f"slot.diagram.{prefix}_arc", prompt="", d=f"M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy} Z", fill="#e0f2fe", stroke="#38bdf8", stroke_width=1.4))
    slots.append(PathSlot(id=f"slot.diagram.{prefix}_inner", prompt="", d=f"M {cx - 28} {cy} A 28 28 0 0 1 {cx + 28} {cy}", fill="none", stroke="#38bdf8", stroke_width=1.0))
    for a in range(0, 181, 10):
        rad = math.radians(a)
        x1 = cx + (r - 12) * math.cos(rad)
        y1 = cy - (r - 12) * math.sin(rad)
        x2 = cx + r * math.cos(rad)
        y2 = cy - r * math.sin(rad)
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_t_{a}", prompt="", x1=x1, y1=y1, x2=x2, y2=y2, stroke="#0284c7", stroke_width=1.0))
        if a % 30 == 0:
            lx = cx + (r - 22) * math.cos(rad)
            ly = cy - (r - 22) * math.sin(rad) - 6
            slots.append(TextSlot(id=f"slot.diagram.{prefix}_lbl_{a}", prompt="", text=str(180 - a), x=lx, y=ly, font_size=10, font_family='"Noto Sans KR", sans-serif', fill="#0369a1", align="center"))

    # 밑변(중심 -> 오른쪽 0도 끝점)과 양 끝각이 deg인 이등변삼각형
    base_len = r - 12
    # 왼쪽 꼭짓점 (cx, cy), 오른쪽 꼭짓점 (cx + base_len, cy)
    # 윗 꼭짓점 x = cx + base_len / 2, y = cy - (base_len / 2) * tan(deg)
    rad_d = math.radians(deg)
    apex_x = cx + base_len / 2
    apex_y = cy - (base_len / 2) * math.tan(rad_d)
    slots.append(PolygonSlot(
        id=f"slot.diagram.{prefix}_tri",
        prompt="",
        points=[(cx, cy), (cx + base_len, cy), (apex_x, apex_y)],
        fill="none",
        stroke="#111827",
        stroke_width=2.2,
    ))


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="43. 다음 그림은 두 각의 크기가 같은 이등변삼각형을 그린 것입니다. 두 각의 크기가 75°인 삼각형을 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=48, y=96, width=376, height=256, fill="#ffffff", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=462, y=96, width=376, height=256, fill="#ffffff", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=68, y=108, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=482, y=108, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
    ]
    _add_protractor_triangle(diagram_slots, "p0", 236, 326, 128, 75)
    _add_protractor_triangle(diagram_slots, "p1", 650, 326, 128, 70)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=376, coordinate_mode="logical"),
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
        {"ref": "tri_0", "value": "양 끝 각이 75°인 이등변삼각형"},
        {"ref": "tri_1", "value": "양 끝 각이 70°인 이등변삼각형"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "두 각의 크기가 75°인 삼각형", "unit": ""},
    "method": "protractor_reading",
    "steps": [
        {
            "id": "read_protractor",
            "expr": "①의 각도기 눈금 = 75°",
            "explanation": "주어진 선분의 양 끝에 각각 75°인 각을 그린 삼각형은 ①입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
