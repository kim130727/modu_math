"""ModuMath Problem DSL: 이등변삼각형 선택하기 (S3_초등_4_007359)"""

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


PROBLEM_ID = "S3_초등_4_007359"
PROBLEM_TITLE = "모눈종이 위에서 이등변삼각형 선택하기"

ANSWER = {
    "value": "나",
    "answer_index": 1,
    "unit": "",
    "values": ["나"],
    "choices": [
        "가",
        "나",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "나",
            "diagnostics": [
                {
                    "id": "diag.chose_scalene",
                    "condition": "answer_equals_ga",
                    "concept": "이등변삼각형의 뜻",
                    "reason": "두 변의 길이가 다른 직각삼각형(가)을 선택함",
                    "feedback": "삼각형 가는 가로 5칸, 세로 6칸으로 세 변의 길이가 모두 다릅니다. 두 변의 길이가 같은 삼각형 나를 선택해 보세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_isosceles_triangle",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "tri_ga": {"label": "가", "is_isosceles": False},
        "tri_na": {"label": "나", "is_isosceles": True},
    },
    "relations": [
        {
            "type": "classification",
            "property": "two_equal_sides",
            "correct_entity": "tri_na",
            "distractor": "tri_ga",
        }
    ],
}


def _add_grid(slots: list, prefix: str, gx: int, gy: int, cols: int, rows: int, step: int) -> None:
    w = cols * step
    h = rows * step
    slots.append(RectSlot(id=f"slot.diagram.{prefix}_bg", prompt="", x=gx, y=gy, width=w, height=h, fill="#ffffff", stroke="#7dd3fc", stroke_width=1.0))
    for c in range(1, cols):
        x = gx + c * step
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_vc_{c}", prompt="", x1=x, y1=gy, x2=x, y2=gy + h, stroke="#7dd3fc", stroke_width=0.9, stroke_dasharray="3,3"))
    for r in range(1, rows):
        y = gy + r * step
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_hr_{r}", prompt="", x1=gx, y1=y, x2=gx + w, y2=y, stroke="#7dd3fc", stroke_width=0.9, stroke_dasharray="3,3"))


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="32. 이등변삼각형을 선택해 보세요.",
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

    diagram_slots = []
    gx, gy, step = 158, 84, 30
    _add_grid(diagram_slots, "grid", gx, gy, 19, 8, step)

    # 삼각형 가: (gx+2*step, gy+1*step), (gx+2*step, gy+7*step), (gx+7*step, gy+7*step)
    diagram_slots.append(PolygonSlot(
        id="slot.diagram.tri_ga",
        prompt="",
        points=[
            (gx + 2 * step, gy + 1 * step),
            (gx + 2 * step, gy + 7 * step),
            (gx + 7 * step, gy + 7 * step),
        ],
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    ))
    diagram_slots.append(TextSlot(id="slot.diagram.label_ga", prompt="", text="가", x=gx + 3 * step + 6, y=gy + 5 * step, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    # 삼각형 나: 밑변 5칸, 꼭짓점 중앙 (이등변삼각형)
    diagram_slots.append(PolygonSlot(
        id="slot.diagram.tri_na",
        prompt="",
        points=[
            (gx + 13.5 * step, gy + 1 * step),
            (gx + 11 * step, gy + 7 * step),
            (gx + 16 * step, gy + 7 * step),
        ],
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    ))
    diagram_slots.append(TextSlot(id="slot.diagram.label_na", prompt="", text="나", x=gx + 13.5 * step, y=gy + 5 * step, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=268, y=344, width=140, height=48, fill="#f3f4f6", stroke="#9ca3af", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "가", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_text", prompt="", text="가", x=338, y=356, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=478, y=344, width=140, height=48, fill="#f3f4f6", stroke="#9ca3af", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "나", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_text", prompt="", text="나", x=548, y=356, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=416, coordinate_mode="logical"),
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
        {"ref": "tri_ga", "value": "가로 5칸, 세로 6칸인 직각삼각형"},
        {"ref": "tri_na", "value": "두 변의 길이가 같은 삼각형"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "이등변삼각형", "unit": ""},
    "method": "triangle_classification",
    "steps": [
        {
            "id": "find_isosceles",
            "expr": "두 변의 길이가 같은 삼각형 = 나",
            "explanation": "두 변의 길이가 같은 삼각형이 이등변삼각형이므로 나입니다.",
            "value": "나",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
