"""ModuMath Problem DSL: 그림그래프에서 다 농장보다 생산량이 적은 농장 모두 선택하기 (S3_초등_3_008890)"""

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


PROBLEM_ID = "S3_초등_3_008890"
PROBLEM_TITLE = "그림그래프를 보고 기준보다 생산량이 적은 농장 모두 선택하기"

ANSWER = {
    "type": "multi_choice",
    "value": ["나 농장", "마 농장"],
    "unit": "",
    "values": ["나 농장", "마 농장"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "가 농장", "value": "가 농장"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "나 농장", "value": "나 농장"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "다 농장", "value": "다 농장"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "라 농장", "value": "라 농장"},
        {"id": "slot.choice.option_4", "slot_id": "slot.choice.option_4", "text": "마 농장", "value": "마 농장"},
    ],
    "answer_key": [
        {"slot_id": "slot.choice.option_1", "value": "나 농장"},
        {"slot_id": "slot.choice.option_4", "value": "마 농장"},
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_select_picture_graph_comparison",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "farm.ga", "type": "picture_graph_row", "label": "가 농장", "value": 31},
            {"id": "farm.na", "type": "picture_graph_row", "label": "나 농장", "value": 14},
            {"id": "farm.da", "type": "picture_graph_row", "label": "다 농장", "value": 23},
            {"id": "farm.ra", "type": "picture_graph_row", "label": "라 농장", "value": 42},
            {"id": "farm.ma", "type": "picture_graph_row", "label": "마 농장", "value": 20},
        ],
        "relations": [
            {"id": "relation.less_na", "type": "less_than", "from_id": "farm.na", "to_id": "farm.da"},
            {"id": "relation.less_ma", "type": "less_than", "from_id": "farm.ma", "to_id": "farm.da"},
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="54. 진아네 마을의 농장에서 하루 동안 생산한 토마토의 양을 조사하여 그림그래프로 나타내었습니다. 토마토 생산량이 다 농장보다 적은 농장을 모두 선택해 보세요.",
        x=32,
        y=16,
        width=820,
        height=76,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    graph_title = TextSlot(id="slot.diagram.graph_title", prompt="", text="농장별 토마토 생산량", x=375, y=102, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.graph_table",
        x=165,
        y=122,
        col_widths=(82, 330),
        row_heights=(34, 42, 42, 42, 42, 42),
        cells=(
            ("농장", "토마토 생산량"),
            ("가", ""),
            ("나", ""),
            ("다", ""),
            ("라", ""),
            ("마", ""),
        ),
        font_size=18,
        stroke="#65a30d",
    )

    row_counts = [(3, 1), (1, 4), (2, 3), (4, 2), (2, 0)]
    icon_slots = []
    for r_idx, (tens, ones) in enumerate(row_counts):
        cy = 177 + r_idx * 42
        x_cur = 285
        for t in range(tens):
            icon_slots.append(CircleSlot(id=f"slot.diagram.big_{r_idx}_{t}", prompt="", cx=x_cur, cy=cy, r=14, fill="#ef4444", stroke="#b91c1c", stroke_width=1.2))
            x_cur += 34
        for o in range(ones):
            icon_slots.append(CircleSlot(id=f"slot.diagram.small_{r_idx}_{o}", prompt="", cx=x_cur, cy=cy, r=8, fill="#ef4444", stroke="#b91c1c", stroke_width=1.0))
            x_cur += 22

    leg_big = CircleSlot(id="slot.diagram.legend_big", prompt="", cx=635, cy=300, r=14, fill="#ef4444", stroke="#b91c1c", stroke_width=1.2)
    leg_big_txt = TextSlot(id="slot.diagram.legend_big_txt", prompt="", text="10상자", x=685, y=300, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    leg_small = CircleSlot(id="slot.diagram.legend_small", prompt="", cx=635, cy=342, r=8, fill="#ef4444", stroke="#b91c1c", stroke_width=1.0)
    leg_small_txt = TextSlot(id="slot.diagram.legend_small_txt", prompt="", text="1상자", x=680, y=342, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=285, y=396, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    farms = ("가 농장", "나 농장", "다 농장", "라 농장", "마 농장")
    choice_slots = []
    comma_slots = []
    choice_ids = ["slot.choice.paren_l"]
    for i, f_name in enumerate(farms):
        cx = 340 + i * 112
        opt = TextSlot(
            id=f"slot.choice.option_{i}",
            prompt="",
            text=f_name,
            x=cx,
            y=396,
            font_size=20,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            interaction={"type": "choice", "role": "answer", "choice_index": i, "value": f_name, "group_id": "slot.choice.group", "multi_select": True, "include_in_submission": True},
        )
        choice_slots.append(opt)
        choice_ids.append(opt.id)
        if i < 4:
            comma = TextSlot(id=f"slot.choice.comma_{i + 1}", prompt="", text=",", x=cx + 56, y=396, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
            comma_slots.append(comma)
            choice_ids.append(comma.id)
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=844, y=396, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_ids.append("slot.choice.paren_r")

    diagram_slots = (graph_title, *tbl, *icon_slots, leg_big, leg_big_txt, leg_small, leg_small_txt)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=435, coordinate_mode="logical"),
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
        {"ref": "farm.ga", "value": 31},
        {"ref": "farm.na", "value": 14},
        {"ref": "farm.da", "value": 23},
        {"ref": "farm.ra", "value": 42},
        {"ref": "farm.ma", "value": 20},
    ],
    "target": {"ref": "answer.values", "type": "choice_list"},
    "method": "read_picture_graph_and_filter_less_than",
    "steps": [
        {"id": "step.read_da", "expr": "2 * 10 + 3 * 1", "value": 23, "explanation": "다 농장의 생산량은 23상자입니다."},
        {"id": "step.filter", "expr": "production < 23", "value": ["나 농장", "마 농장"], "explanation": "나 농장(14상자)과 마 농장(20상자)이 다 농장(23상자)보다 적습니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.picture_graph_comparison"],
        "errors": {
            "가 농장": "data.chose_greater_than_target",
        },
    },
}
