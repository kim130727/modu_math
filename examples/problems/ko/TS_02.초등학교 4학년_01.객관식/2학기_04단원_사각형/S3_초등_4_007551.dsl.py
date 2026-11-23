"""ModuMath Problem DSL: 서로 다른 사다리꼴 2개 찾기 (S3_초등_4_007551)"""

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


PROBLEM_ID = "S3_초등_4_007551"
PROBLEM_TITLE = "모눈종이 위에서 서로 다른 사다리꼴 2개 찾아 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "① 1번, 3번",
        "② 1번, 2번",
        "③ 2번, 4번",
        "④ 3번, 4번",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.missed_trapezoids",
                    "condition": "answer_not_1",
                    "concept": "사다리꼴의 성질",
                    "reason": "평행한 변이 한 쌍이라도 있는 도형(1번, 3번)을 정확히 찾지 못함",
                    "feedback": "평행한 변이 한 쌍이라도 있는 사각형은 1번과 3번입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_find_two_trapezoids",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "중",
    },
    "entities": {
        "fig_1": {"label": "1번", "is_trapezoid": True},
        "fig_2": {"label": "2번", "is_trapezoid": False},
        "fig_3": {"label": "3번", "is_trapezoid": True},
        "fig_4": {"label": "4번", "is_trapezoid": False},
    },
    "relations": [
        {
            "type": "classification",
            "property": "at_least_one_parallel_pair",
            "correct_entities": ["fig_1", "fig_3"],
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
        text="94. 서로 다른 사다리꼴을 2개 찾아 선택하세요.",
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
    gx, gy, step = 119, 80, 24
    _add_grid(diagram_slots, "grid", gx, gy, 27, 6, step)

    diagram_slots.append(PolygonSlot(id="slot.diagram.f1", prompt="", points=[(gx + 3 * step, gy + 1 * step), (gx + 6 * step, gy + 1 * step), (gx + 8 * step, gy + 5 * step), (gx + 1 * step, gy + 5 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.l1", prompt="", text="1번", x=gx + 4.5 * step, y=gy + 6 * step + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.f2", prompt="", points=[(gx + 9 * step, gy + 0 * step), (gx + 15 * step, gy + 1.5 * step), (gx + 12 * step, gy + 5 * step), (gx + 9 * step, gy + 3.5 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.l2", prompt="", text="2번", x=gx + 12 * step, y=gy + 6 * step + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.f3", prompt="", points=[(gx + 16 * step, gy + 1 * step), (gx + 20 * step, gy + 1 * step), (gx + 22 * step, gy + 5 * step), (gx + 16 * step, gy + 5 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.l3", prompt="", text="3번", x=gx + 19 * step, y=gy + 6 * step + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.f4", prompt="", points=[(gx + 23 * step, gy + 1 * step), (gx + 27 * step, gy + 1 * step), (gx + 26 * step, gy + 5 * step), (gx + 23 * step, gy + 4 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.l4", prompt="", text="4번", x=gx + 25 * step, y=gy + 6 * step + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))

    opts = ["① 1번, 3번", "② 1번, 2번", "③ 2번, 4번", "④ 3번, 4번"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 108 + idx * 176
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=266,
                width=148,
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
                    "value": label.split(" ")[0],
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_text_{idx}", prompt="", text=label, x=cx + 74, y=277, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=340, coordinate_mode="logical"),
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
        {"ref": "fig_1", "value": "평행한 변이 1쌍 있는 사각형"},
        {"ref": "fig_2", "value": "평행한 변이 없는 사각형"},
        {"ref": "fig_3", "value": "평행한 변이 1쌍 있는 사각형"},
        {"ref": "fig_4", "value": "평행한 변이 없는 사각형"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "사다리꼴 2개", "unit": ""},
    "method": "quadrilateral_classification",
    "steps": [
        {
            "id": "find_trapezoids",
            "expr": "평행한 변이 있는 사각형 = 1번, 3번",
            "explanation": "평행한 변이 한 쌍이라도 있는 사각형은 1번과 3번입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
