"""ModuMath Problem DSL: 그림그래프에서 가장 많은 요일 찾기 (S3_초등_3_008888)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008888"
PROBLEM_TITLE = "그림그래프를 보고 도서관을 이용한 학생 수가 가장 많은 요일 선택하기"

ANSWER = {
    "type": "choice",
    "value": "수요일",
    "unit": "",
    "answer_index": 2,
    "values": ["수요일"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "월요일", "value": "월요일"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "화요일", "value": "화요일"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "수요일", "value": "수요일"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "목요일", "value": "목요일"},
        {"id": "slot.choice.option_4", "slot_id": "slot.choice.option_4", "text": "금요일", "value": "금요일"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_2", "value": "수요일"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_picture_graph_max",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "day.mon", "type": "picture_graph_row", "label": "월요일", "tens": 3, "ones": 2, "value": 32},
            {"id": "day.tue", "type": "picture_graph_row", "label": "화요일", "tens": 2, "ones": 4, "value": 24},
            {"id": "day.wed", "type": "picture_graph_row", "label": "수요일", "tens": 4, "ones": 1, "value": 41},
            {"id": "day.thu", "type": "picture_graph_row", "label": "목요일", "tens": 2, "ones": 1, "value": 21},
            {"id": "day.fri", "type": "picture_graph_row", "label": "금요일", "tens": 1, "ones": 5, "value": 15},
        ],
        "relations": [
            {
                "id": "relation.maximum",
                "type": "has_max_count",
                "from_id": "day.wed",
                "to_id": "value.41",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="52. 지애가 요일별로 도서관을 이용한 학생 수를 그림으로 나타내어 그래프를 만들었습니다. 그래프를 보고 알맞은 말을 선택하세요.",
        x=32,
        y=16,
        width=820,
        height=60,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    graph_title = TextSlot(id="slot.diagram.graph_title", prompt="", text="도서관을 이용한 학생 수", x=375, y=90, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.graph_table",
        x=165,
        y=110,
        col_widths=(95, 330),
        row_heights=(34, 42, 42, 42, 42, 42),
        cells=(
            ("요일", "학생 수"),
            ("월요일", ""),
            ("화요일", ""),
            ("수요일", ""),
            ("목요일", ""),
            ("금요일", ""),
        ),
        font_size=18,
        stroke="#65a30d",
    )

    # 요일별 그림 (큰 원 = 10명, 작은 원 = 1명)
    row_counts = [(3, 2), (2, 4), (4, 1), (2, 1), (1, 5)]
    icon_slots = []
    for r_idx, (tens, ones) in enumerate(row_counts):
        cy = 165 + r_idx * 42
        x_cur = 290
        for t in range(tens):
            icon_slots.append(CircleSlot(id=f"slot.diagram.big_{r_idx}_{t}", prompt="", cx=x_cur, cy=cy, r=14, fill="#fde047", stroke="#ca8a04", stroke_width=1.2))
            x_cur += 34
        for o in range(ones):
            icon_slots.append(CircleSlot(id=f"slot.diagram.small_{r_idx}_{o}", prompt="", cx=x_cur, cy=cy, r=8, fill="#fde047", stroke="#ca8a04", stroke_width=1.0))
            x_cur += 22

    # 범례
    leg_big = CircleSlot(id="slot.diagram.legend_big", prompt="", cx=655, cy=290, r=14, fill="#fde047", stroke="#ca8a04", stroke_width=1.2)
    leg_big_txt = TextSlot(id="slot.diagram.legend_big_txt", prompt="", text="10명", x=695, y=290, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    leg_small = CircleSlot(id="slot.diagram.legend_small", prompt="", cx=655, cy=332, r=8, fill="#fde047", stroke="#ca8a04", stroke_width=1.0)
    leg_small_txt = TextSlot(id="slot.diagram.legend_small_txt", prompt="", text="1명", x=690, y=332, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    sent_1 = TextSlot(id="slot.diagram.sent_1", prompt="", text="도서관을 이용한 학생 수가 가장 많은 요일은", x=443, y=378, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=150, y=414, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    days = ("월요일", "화요일", "수요일", "목요일", "금요일")
    choice_slots = []
    comma_slots = []
    choice_ids = ["slot.choice.paren_l"]
    for i, d_name in enumerate(days):
        cx = 205 + i * 105
        opt = TextSlot(
            id=f"slot.choice.option_{i}",
            prompt="",
            text=d_name,
            x=cx,
            y=414,
            font_size=21,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            interaction={"type": "choice", "role": "answer", "choice_index": i, "value": d_name, "group_id": "slot.choice.group", "include_in_submission": True},
        )
        choice_slots.append(opt)
        choice_ids.append(opt.id)
        if i < 4:
            comma = TextSlot(id=f"slot.choice.comma_{i + 1}", prompt="", text=",", x=cx + 52, y=414, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
            comma_slots.append(comma)
            choice_ids.append(comma.id)
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")입니다.", x=712, y=414, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_ids.append("slot.choice.paren_r")

    diagram_slots = (graph_title, *tbl, *icon_slots, leg_big, leg_big_txt, leg_small, leg_small_txt, sent_1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=455, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(choice_ids)),
        ),
        slots=(stem_slot, *diagram_slots, paren_l, *choice_slots, *comma_slots, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "day.mon", "value": 32},
        {"ref": "day.tue", "value": 24},
        {"ref": "day.wed", "value": 41},
        {"ref": "day.thu", "value": 21},
        {"ref": "day.fri", "value": 15},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "read_picture_graph_max",
    "steps": [
        {
            "id": "step.find_max",
            "expr": "max(32, 24, 41, 21, 15) == 41",
            "value": "수요일",
            "explanation": "10명을 나타내는 큰 그림의 수가 4개로 가장 많은 수요일(41명)이 학생 수가 가장 많은 요일입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.picture_graph_interpretation"],
        "errors": {
            "화요일": "data.counted_total_icons_ignoring_scale",
            "금요일": "data.counted_total_icons_ignoring_scale",
        },
    },
}
