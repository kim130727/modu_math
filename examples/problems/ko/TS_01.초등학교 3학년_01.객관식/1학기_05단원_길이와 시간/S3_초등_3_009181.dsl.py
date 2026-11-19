"""ModuMath Problem DSL: 거리 어림하기 - 약 1 km 500 m (S3_초등_3_009181)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009181"
PROBLEM_TITLE = "학교에서 약 1 km 500 m 떨어진 장소 선택하기"

ANSWER = {
    "type": "choice",
    "value": "시청",
    "unit": "",
    "answer_index": 2,
    "values": ["시청"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "문구점", "value": "문구점"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "도서관", "value": "도서관"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "시청", "value": "시청"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "시청",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_distance_estimation",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "05단원_길이와 시간",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "place.school", "type": "place", "label": "학교", "distance_m": 0},
            {"id": "place.stationery", "type": "place", "label": "문구점", "distance_m": 500},
            {"id": "place.library", "type": "place", "label": "도서관", "distance_m": 1000},
            {"id": "place.city_hall", "type": "place", "label": "시청", "distance_m": 1500},
        ],
        "relations": [
            {
                "id": "relation.distance_1km_500m",
                "type": "approx_distance",
                "from_id": "place.school",
                "to_id": "place.city_hall",
            }
        ],
    },
    "answer": ANSWER,
}


def _map_slots() -> tuple:
    bg = RectSlot(id="slot.diagram.map_bg", prompt="", x=315, y=88, width=256, height=195, fill="#d9ead3", stroke="none", stroke_width=0)
    road_main = RectSlot(id="slot.diagram.road_main", prompt="", x=440, y=108, width=16, height=175, fill="#ffffff", stroke="none", stroke_width=0)
    road_branch = PathSlot(id="slot.diagram.road_branch", prompt="", d="M 444 226 L 325 283 L 345 283 L 452 232 Z", fill="#ffffff", stroke="none", stroke_width=0)
    arc_500 = PathSlot(id="slot.diagram.arc_500", prompt="", d="M 448 122 Q 422 152, 448 182", fill="none", stroke="#38bdf8", stroke_width=1.4, stroke_dasharray="3,3")
    label_500 = TextSlot(id="slot.diagram.label_500", prompt="", text="약 500 m", x=402, y=152, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    dot_school = CircleSlot(id="slot.diagram.dot_school", prompt="", cx=448, cy=122, r=2.8, fill="#111827", stroke="#111827", stroke_width=1)
    dot_stat = CircleSlot(id="slot.diagram.dot_stat", prompt="", cx=448, cy=182, r=2.8, fill="#111827", stroke="#111827", stroke_width=1)
    dot_lib = CircleSlot(id="slot.diagram.dot_lib", prompt="", cx=448, cy=230, r=2.8, fill="#111827", stroke="#111827", stroke_width=1)
    dot_hall = CircleSlot(id="slot.diagram.dot_hall", prompt="", cx=396, cy=258, r=2.8, fill="#111827", stroke="#111827", stroke_width=1)

    icon_school = RectSlot(id="slot.diagram.icon_school", prompt="", x=425, y=94, width=46, height=22, fill="#fca5a5", stroke="#ef4444", stroke_width=1)
    lbl_school = TextSlot(id="slot.diagram.lbl_school", prompt="", text="학교", x=496, y=106, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    icon_stat = RectSlot(id="slot.diagram.icon_stat", prompt="", x=460, y=170, width=24, height=18, fill="#fdba74", stroke="#ea580c", stroke_width=1)
    lbl_stat = TextSlot(id="slot.diagram.lbl_stat", prompt="", text="문구점", x=512, y=180, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    icon_lib = RectSlot(id="slot.diagram.icon_lib", prompt="", x=460, y=218, width=28, height=20, fill="#fcd34d", stroke="#d97706", stroke_width=1)
    lbl_lib = TextSlot(id="slot.diagram.lbl_lib", prompt="", text="도서관", x=516, y=228, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    icon_hall = RectSlot(id="slot.diagram.icon_hall", prompt="", x=368, y=228, width=22, height=24, fill="#cbd5e1", stroke="#64748b", stroke_width=1)
    lbl_hall = TextSlot(id="slot.diagram.lbl_hall", prompt="", text="시청", x=379, y=216, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return (
        bg, road_main, road_branch, arc_500, label_500,
        dot_school, dot_stat, dot_lib, dot_hall,
        icon_school, lbl_school, icon_stat, lbl_stat, icon_lib, lbl_lib, icon_hall, lbl_hall,
    )


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="43. 학교에서 주변에 있는 장소까지의 거리를 어림해 보려고 합니다. 알맞은 장소를 선택하세요.",
        x=32,
        y=18,
        width=820,
        height=60,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    map_slots = _map_slots()
    line1 = TextSlot(id="slot.diagram.sent_1", prompt="", text="학교에서 약 1 km 500 m 떨어진 곳에 있는 장소는", x=443, y=310, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=268, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="문구점", x=320, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "문구점", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=366, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="도서관", x=416, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "도서관", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_2 = TextSlot(id="slot.choice.comma_2", prompt="", text=",", x=462, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="시청", x=505, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "시청", "group_id": "slot.choice.group", "include_in_submission": True})
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")입니다.", x=578, y=346, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (*map_slots, line1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=380, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.paren_l", "slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.comma_2", "slot.choice.option_2", "slot.choice.paren_r"),
            ),
        ),
        slots=(stem_slot, *diagram_slots, paren_l, opt_0, comma_1, opt_1, comma_2, opt_2, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "place.stationery", "value": "약 500 m"},
        {"ref": "place.library", "value": "문구점 거리의 약 2배"},
        {"ref": "place.city_hall", "value": "문구점 거리의 약 3배"},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "convert_km_to_m_and_estimate_distance",
    "steps": [
        {"id": "step.convert", "expr": "1 km 500 m = 1500 m", "value": 1500, "explanation": "1 km 500 m = 1500 m이므로 500 m의 세 배입니다."},
        {"id": "step.estimate", "expr": "500 * 3 = 1500", "value": "시청", "explanation": "학교에서 문구점까지의 거리의 약 세 배쯤 되는 곳에 위치한 시청이 약 1 km 500 m 떨어진 곳입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.km_to_m_conversion", "measurement.distance_estimation"],
        "errors": {
            "문구점": "measurement.wrong_distance_multiple",
            "도서관": "measurement.wrong_distance_multiple",
        },
    },
}
