"""ModuMath Problem DSL: 그림그래프에서 가장 많이/적게 팔린 음식 순서 선택하기 (S3_초등_3_008891)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008891"
PROBLEM_TITLE = "그림그래프를 보고 가장 많이 팔린 음식과 가장 적게 팔린 음식 순서 선택하기"

ANSWER = {
    "type": "choice",
    "value": "②",
    "unit": "",
    "answer_index": 1,
    "values": ["②"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "①", "value": "①"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "②", "value": "②"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "③", "value": "③"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "④", "value": "④"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_1", "value": "②"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_picture_graph_extremes",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "food.kimchi", "type": "picture_graph_col", "label": "김치찌개", "value": 320},
            {"id": "food.bibim", "type": "picture_graph_col", "label": "비빔밥", "value": 210},
            {"id": "food.mandu", "type": "picture_graph_col", "label": "만둣국", "value": 230},
            {"id": "food.doenjang", "type": "picture_graph_col", "label": "된장찌개", "value": 150},
        ],
        "relations": [
            {"id": "relation.max", "type": "has_max_count", "from_id": "food.kimchi", "to_id": "value.320"},
            {"id": "relation.min", "type": "has_min_count", "from_id": "food.doenjang", "to_id": "value.150"},
        ],
    },
    "answer": ANSWER,
}


def _bowl_slot(slot_id: str, cx: float, cy: float, large: bool) -> PathSlot:
    w = 22 if large else 14
    h = 16 if large else 10
    d = f"M {cx - w} {cy - h/2} L {cx + w} {cy - h/2} Q {cx + w*0.8} {cy + h}, {cx} {cy + h} Q {cx - w*0.8} {cy + h}, {cx - w} {cy - h/2} Z"
    return PathSlot(id=slot_id, prompt="", d=d, fill="#67e8f9", stroke="#0e7490", stroke_width=1.2)


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="55. 어느 음식점에서 일주일 동안 팔린 음식의 수를 그림그래프로 나타내었습니다. 일주일 동안 가장 많이 팔린 음식과 가장 적게 팔린 음식을 순서대로 나열한 것을 고르세요.",
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

    graph_title = TextSlot(id="slot.diagram.graph_title", prompt="", text="일주일 동안 팔린 음식의 수", x=443, y=104, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.graph_table",
        x=213,
        y=124,
        col_widths=(115, 115, 115, 115),
        row_heights=(150, 56),
        cells=(
            ("", "", "", ""),
            ("김치찌개", "비빔밥", "만둣국", "된장찌개"),
        ),
        font_size=18,
        stroke="#a8a29e",
    )

    col_counts = [(3, 2), (2, 1), (2, 3), (1, 5)]
    bowl_slots = []
    for c_idx, (hundreds, tens) in enumerate(col_counts):
        cx = 270 + c_idx * 115
        y_cur = 252
        for h in range(hundreds):
            bowl_slots.append(_bowl_slot(f"slot.diagram.big_{c_idx}_{h}", cx, y_cur, True))
            y_cur -= 28
        for t in range(tens):
            bowl_slots.append(_bowl_slot(f"slot.diagram.small_{c_idx}_{t}", cx, y_cur, False))
            y_cur -= 18

    leg_big = _bowl_slot("slot.diagram.legend_big", 440, 348, True)
    leg_big_txt = TextSlot(id="slot.diagram.legend_big_txt", prompt="", text="100그릇", x=505, y=352, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    leg_small = _bowl_slot("slot.diagram.legend_small", 585, 350, False)
    leg_small_txt = TextSlot(id="slot.diagram.legend_small_txt", prompt="", text="10그릇", x=638, y=352, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="① 된장찌개, 비빔밥", x=40, y=396, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="② 김치찌개, 된장찌개", x=450, y=396, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="③ 된장찌개, 김치찌개", x=40, y=434, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="④ 김치찌개, 비빔밥", x=450, y=434, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "④", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = (graph_title, *tbl, *bowl_slots, leg_big, leg_big_txt, leg_small, leg_small_txt)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=470, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2", "slot.choice.option_3")),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, opt_1, opt_2, opt_3),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "food.kimchi", "value": 320},
        {"ref": "food.bibim", "value": 210},
        {"ref": "food.mandu", "value": 230},
        {"ref": "food.doenjang", "value": 150},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "find_max_and_min_in_picture_graph",
    "steps": [
        {"id": "step.order", "expr": "320 > 230 > 210 > 150", "value": "②", "explanation": "김치찌개(320) > 만둣국(230) > 비빔밥(210) > 된장찌개(150)이므로 가장 많이 팔린 음식은 김치찌개, 가장 적게 팔린 음식은 된장찌개(②)입니다."}
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.picture_graph_interpretation"],
        "errors": {
            "③": "data.reversed_max_and_min_order",
            "④": "data.counted_total_icons_ignoring_scale",
        },
    },
}
