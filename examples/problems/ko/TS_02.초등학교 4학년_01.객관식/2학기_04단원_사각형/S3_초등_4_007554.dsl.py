"""ModuMath Problem DSL: 평행한 변이 1쌍 있는 사각형 찾기 (S3_초등_4_007554)"""

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


PROBLEM_ID = "S3_초등_4_007554"
PROBLEM_TITLE = "평행한 변이 1쌍 있는 사각형 선택하기"

ANSWER = {
    "value": "다",
    "answer_index": 2,
    "unit": "",
    "values": ["다"],
    "choices": [
        "가",
        "나",
        "다",
        "라",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "다",
            "diagnostics": [
                {
                    "id": "diag.chose_two_pairs",
                    "condition": "answer_not_da",
                    "concept": "평행한 변의 수에 따른 사각형 분류",
                    "reason": "평행한 변이 2쌍 있는 사각형(가, 나, 라)과 1쌍 있는 사각형(다)을 구분하지 못함",
                    "feedback": "가, 나, 라는 마주 보는 두 쌍의 변이 모두 평행합니다. 평행한 변이 1쌍만 있는 사각형은 다입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_parallel_pair_count",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "중",
    },
    "entities": {
        "ga": {"label": "가", "parallel_pairs": 2},
        "na": {"label": "나", "parallel_pairs": 2},
        "da": {"label": "다", "parallel_pairs": 1},
        "ra": {"label": "라", "parallel_pairs": 2},
    },
    "relations": [
        {
            "type": "classification",
            "property": "parallel_pairs == 1",
            "correct_entity": "da",
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
        text="99. 사각형을 평행한 변의 수에 따라 사각형을 분류하려고 합니다. 물음에 답하세요.\n(1) 평행한 변이 1쌍 있는 사각형을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=76,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = []
    gx, gy, step = 119, 108, 24
    _add_grid(diagram_slots, "grid", gx, gy, 27, 6, step)

    diagram_slots.append(PolygonSlot(id="slot.diagram.ga", prompt="", points=[(gx + 4 * step, gy + 1 * step), (gx + 7 * step, gy + 3 * step), (gx + 4 * step, gy + 5 * step), (gx + 1 * step, gy + 3 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_ga", prompt="", text="가", x=gx + 4 * step, y=gy + 2.7 * step, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.na", prompt="", points=[(gx + 11 * step, gy + 1 * step), (gx + 15 * step, gy + 1 * step), (gx + 13 * step, gy + 5 * step), (gx + 9 * step, gy + 5 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_na", prompt="", text="나", x=gx + 12 * step, y=gy + 2.7 * step, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.da", prompt="", points=[(gx + 17 * step, gy + 1 * step), (gx + 21 * step, gy + 1 * step), (gx + 21 * step, gy + 5 * step), (gx + 17 * step, gy + 4 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_da", prompt="", text="다", x=gx + 19 * step, y=gy + 2.5 * step, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.ra", prompt="", points=[(gx + 23 * step, gy + 1 * step), (gx + 26 * step, gy + 1 * step), (gx + 26 * step, gy + 5 * step), (gx + 23 * step, gy + 5 * step)], fill="none", stroke="#111827", stroke_width=1.8))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_ra", prompt="", text="라", x=gx + 24.5 * step, y=gy + 2.7 * step, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    opts = ["가", "나", "다", "라"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 166 + idx * 146
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=276,
                width=116,
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
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_text_{idx}", prompt="", text=label, x=cx + 58, y=287, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=348, coordinate_mode="logical"),
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
        {"ref": "ga", "value": "평행한 변 2쌍"},
        {"ref": "na", "value": "평행한 변 2쌍"},
        {"ref": "da", "value": "평행한 변 1쌍"},
        {"ref": "ra", "value": "평행한 변 2쌍"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "평행한 변이 1쌍 있는 사각형", "unit": ""},
    "method": "quadrilateral_classification",
    "steps": [
        {
            "id": "count_parallel_pairs",
            "expr": "평행한 변이 1쌍 있는 사각형 = 다",
            "explanation": "평행한 변이 1쌍 있는 사각형은 다입니다.",
            "value": "다",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
