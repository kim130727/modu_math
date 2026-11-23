"""ModuMath Problem DSL: 사다리꼴이 되도록 선 긋기 (S3_초등_4_007547)"""

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


PROBLEM_ID = "S3_초등_4_007547"
PROBLEM_TITLE = "사각형에서 잘라 내면 사다리꼴이 되도록 선을 그은 것 선택하기"

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
                    "id": "diag.not_parallel_cut",
                    "condition": "answer_equals_2",
                    "concept": "사다리꼴의 성질",
                    "reason": "마주 보는 변이 평행하지 않게 자른 ②를 선택함",
                    "feedback": "한 쌍의 마주 보는 변이 평행하도록 잘라 내야 사다리꼴이 됩니다. 오른쪽 변과 평행하게 세로선을 그은 ①을 선택하세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_trapezoid_cut",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "중",
    },
    "entities": {
        "cut_0": {"label": "①", "forms_trapezoid": True},
        "cut_1": {"label": "②", "forms_trapezoid": False},
    },
    "relations": [
        {
            "type": "geometric_cut",
            "target_shape": "사다리꼴",
            "correct_entity": "cut_0",
            "distractor": "cut_1",
        }
    ],
}


def _add_grid(slots: list, prefix: str, gx: int, gy: int, cols: int, rows: int, step: int) -> None:
    w = cols * step
    h = rows * step
    slots.append(RectSlot(id=f"slot.diagram.{prefix}_bg", prompt="", x=gx, y=gy, width=w, height=h, fill="#ffffff", stroke="#7dd3fc", stroke_width=0.9))
    for c in range(1, cols):
        x = gx + c * step
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_vc_{c}", prompt="", x1=x, y1=gy, x2=x, y2=gy + h, stroke="#7dd3fc", stroke_width=0.8, stroke_dasharray="3,3"))
    for r in range(1, rows):
        y = gy + r * step
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_hr_{r}", prompt="", x1=gx, y1=y, x2=gx + w, y2=y, stroke="#7dd3fc", stroke_width=0.8, stroke_dasharray="3,3"))


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="89. 사각형에서 어느 부분을 잘라 내면 사다리꼴이 되는지 <보기>와 같이 선을 그은 것을 선택하세요.",
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
        RectSlot(id="slot.diagram.ex_box", prompt="", x=38, y=96, width=236, height=192, fill="#ffffff", stroke="#6b7280", stroke_width=1.4),
        TextSlot(id="slot.diagram.ex_lbl", prompt="", text="<보기>", x=54, y=108, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left"),
    ]
    step = 22
    _add_grid(diagram_slots, "ex", 68, 146, 8, 6, step)
    diagram_slots.append(PolygonSlot(id="slot.diagram.ex_poly", prompt="", points=[(90, 190), (200, 168), (222, 256), (90, 256)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(LineSlot(id="slot.diagram.ex_cut", prompt="", x1=90, y1=190, x2=206, y2=190, stroke="#ec4899", stroke_width=2.0))

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=316, y=110, width=246, height=176, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=598, y=110, width=246, height=176, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=336, y=120, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_grid(diagram_slots, "c0", 350, 138, 8, 6, step)
    diagram_slots.append(PolygonSlot(id="slot.diagram.c0_poly", prompt="", points=[(372, 160), (504, 160), (504, 248), (416, 226)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(LineSlot(id="slot.diagram.c0_cut", prompt="", x1=416, y1=160, x2=416, y2=226, stroke="#ec4899", stroke_width=2.0))

    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=618, y=120, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_grid(diagram_slots, "c1", 632, 138, 8, 6, step)
    diagram_slots.append(PolygonSlot(id="slot.diagram.c1_poly", prompt="", points=[(654, 160), (786, 160), (786, 248), (698, 226)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(LineSlot(id="slot.diagram.c1_cut", prompt="", x1=786, y1=160, x2=698, y2=226, stroke="#ec4899", stroke_width=2.0))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=312, coordinate_mode="logical"),
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
        {"ref": "cut_0", "value": "오른쪽 변과 평행하게 자른 선"},
        {"ref": "cut_1", "value": "대각선으로 자른 선"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "사다리꼴이 되는 선", "unit": ""},
    "method": "parallel_check",
    "steps": [
        {
            "id": "find_parallel_cut",
            "expr": "①의 자른 선과 오른쪽 변이 서로 평행",
            "explanation": "한 쌍의 마주 보는 변이 평행하도록 잘라 낸 것은 ①입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
