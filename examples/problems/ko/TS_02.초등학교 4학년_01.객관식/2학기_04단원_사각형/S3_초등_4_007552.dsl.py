"""ModuMath Problem DSL: 정사각형과 사다리꼴의 관계 (S3_초등_4_007552)"""

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


PROBLEM_ID = "S3_초등_4_007552"
PROBLEM_TITLE = "주어진 정사각형을 보고 사다리꼴인지 알맞은 말 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "① 있습니다, 입니다",
        "② 있습니다, 아닙니다",
        "③ 없습니다, 입니다",
        "④ 없습니다, 아닙니다",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.square_is_trapezoid",
                    "condition": "answer_not_1",
                    "concept": "정사각형과 사다리꼴의 포함 관계",
                    "reason": "정사각형도 평행한 변이 있으므로 사다리꼴임을 놓침",
                    "feedback": "정사각형은 마주 보는 변이 평행하므로 평행한 변이 있습니다. 따라서 주어진 도형은 사다리꼴입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_square_as_trapezoid",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "중",
    },
    "entities": {
        "shape": {"label": "정사각형", "has_parallel_sides": True, "is_trapezoid": True},
    },
    "relations": [
        {
            "type": "inclusion",
            "subset": "정사각형",
            "superset": "사다리꼴",
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
        text="95. 다음 도형을 보고 알맞은 말을 선택하세요.",
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
    gx, gy, step = 335, 76, 24
    _add_grid(diagram_slots, "grid", gx, gy, 9, 6, step)
    diagram_slots.append(PolygonSlot(
        id="slot.diagram.square",
        prompt="",
        points=[(gx + 2 * step, gy + 1 * step), (gx + 6 * step, gy + 1 * step), (gx + 6 * step, gy + 5 * step), (gx + 2 * step, gy + 5 * step)],
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    ))
    diagram_slots.append(TextBoxSlot(
        id="slot.diagram.bullets",
        prompt="",
        text="• 평행한 변이 ( 있습니다 , 없습니다 ).\n• 주어진 도형은 사다리꼴(이)( 입니다 , 아닙니다 ).",
        x=72,
        y=236,
        width=740,
        height=68,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
        line_height=1.6,
    ))

    opts = [
        "① 있습니다, 입니다",
        "② 있습니다, 아닙니다",
        "③ 없습니다, 입니다",
        "④ 없습니다, 아닙니다",
    ]
    choice_slots = []
    for idx, label in enumerate(opts):
        col = idx % 2
        row = idx // 2
        cx = 118 + col * 340
        cy = 324 + row * 54
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=cy,
                width=310,
                height=42,
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
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_text_{idx}", prompt="", text=label, x=cx + 22, y=cy + 11, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=442, coordinate_mode="logical"),
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
    "given": [{"ref": "shape", "value": "정사각형"}],
    "target": {"ref": "slot.choice.option_0", "label": "알맞은 말", "unit": ""},
    "method": "quadrilateral_inclusion",
    "steps": [
        {
            "id": "check_trapezoid",
            "expr": "정사각형은 평행한 변이 있음 -> 사다리꼴임",
            "explanation": "정사각형은 평행한 변이 있으므로 사다리꼴입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
