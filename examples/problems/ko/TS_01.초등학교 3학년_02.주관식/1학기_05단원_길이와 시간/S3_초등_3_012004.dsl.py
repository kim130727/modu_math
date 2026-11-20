"""ModuMath Problem DSL: 지도를 보고 어림한 거리의 장소 찾기 (S3_초등_3_012004)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012004"
PROBLEM_TITLE = "어림한 거리에 해당하는 장소 찾기"


ANSWER = {
    "type": "short_answer",
    "value": ["도서관", "학교, 우체국"],
    "unit": "",
    "values": ["도서관", "학교, 우체국"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_600",
            "slot_id": "slot.answer.input_600",
            "expected": "도서관",
        },
        {
            "id": "slot.answer.input_1000",
            "slot_id": "slot.answer.input_1000",
            "expected": "학교, 우체국",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_600",
            "value": "도서관",
            "diagnostics": [
                {
                    "id": "diag.distance_estimation_error_600",
                    "condition": "answer_not_equals_library",
                    "concept": "거리 어림하기",
                    "reason": "약 400 m 구간과 비교하여 약 600 m 떨어진 장소를 찾지 못함",
                    "feedback": "우리 집에서 병원까지가 약 400 m이므로, 그보다 조금 더 먼 약 600 m 떨어진 곳은 도서관입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_1000",
            "value": "학교, 우체국",
            "diagnostics": [
                {
                    "id": "diag.distance_estimation_error_1km",
                    "condition": "answer_not_equals_school_post",
                    "concept": "1 km = 1000 m 어림하기",
                    "reason": "1 km 거리에 있는 학교와 우체국을 모두 찾지 못함",
                    "feedback": "1 km는 1000 m로 약 400 m의 2배보다 조금 더 먼 거리입니다. 학교와 우체국이 약 1 km 떨어져 있습니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_distance_estimation_map",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "05단원_길이와 시간",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "place.home", "type": "location", "label": "우리 집"},
            {"id": "place.hospital", "type": "location", "label": "병원", "approx_distance_m": 400},
            {"id": "place.library", "type": "location", "label": "도서관", "approx_distance_m": 600},
            {"id": "place.school", "type": "location", "label": "학교", "approx_distance_m": 1000},
            {"id": "place.post_office", "type": "location", "label": "우체국", "approx_distance_m": 1000},
        ],
        "relations": [
            {
                "id": "relation.approx_600",
                "type": "approx_distance_from_home",
                "from_id": "place.home",
                "to_id": "place.library",
                "distance_m": 600,
            },
            {
                "id": "relation.approx_1km_school",
                "type": "approx_distance_from_home",
                "from_id": "place.home",
                "to_id": "place.school",
                "distance_m": 1000,
            },
            {
                "id": "relation.approx_1km_post",
                "type": "approx_distance_from_home",
                "from_id": "place.home",
                "to_id": "place.post_office",
                "distance_m": 1000,
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="우리집에서 약 600 m 떨어진 곳과 1 km 떨어진 곳에 있는 장소를 적어 보세요.",
        x=32,
        y=22,
        width=836,
        height=80,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    map_bg = RectSlot(
        id="slot.diagram.map_bg",
        prompt="",
        x=170,
        y=112,
        width=560,
        height=340,
        fill="#a3d977",
        stroke="#9ca3af",
        stroke_width=1.4,
    )

    # 주요 도로 (세로 도로 & 가로 도로)
    road_v1 = LineSlot(
        id="slot.diagram.road_v1",
        prompt="",
        x1=405,
        y1=112,
        x2=405,
        y2=452,
        stroke="#ffffff",
        stroke_width=12.0,
    )
    road_v2 = LineSlot(
        id="slot.diagram.road_v2",
        prompt="",
        x1=535,
        y1=112,
        x2=535,
        y2=452,
        stroke="#ffffff",
        stroke_width=12.0,
    )
    road_h1 = LineSlot(
        id="slot.diagram.road_h1",
        prompt="",
        x1=170,
        y1=200,
        x2=730,
        y2=200,
        stroke="#ffffff",
        stroke_width=12.0,
    )
    road_h2 = LineSlot(
        id="slot.diagram.road_h2",
        prompt="",
        x1=170,
        y1=325,
        x2=730,
        y2=325,
        stroke="#ffffff",
        stroke_width=12.0,
    )
    road_diag = LineSlot(
        id="slot.diagram.road_diag",
        prompt="",
        x1=355,
        y1=325,
        x2=410,
        y2=452,
        stroke="#ffffff",
        stroke_width=10.0,
    )

    # 기준 거리 호 (우리 집 -> 병원 앞 약 400 m)
    arc_400 = PathSlot(
        id="slot.diagram.arc_400",
        prompt="",
        d="M 535 152 Q 515 208 535 262",
        fill="none",
        stroke="#ec4899",
        stroke_width=1.8,
        stroke_dasharray="4 4",
    )
    badge_400_bg = RectSlot(
        id="slot.diagram.badge_400_bg",
        prompt="",
        x=470,
        y=192,
        width=92,
        height=24,
        fill="#ffffff",
        stroke="#d1d5db",
        stroke_width=1.0,
    )
    badge_400_text = TextBoxSlot(
        id="slot.diagram.badge_400_text",
        prompt="",
        text="약 400 m",
        x=470,
        y=192,
        width=92,
        height=24,
        font_size=14,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    # 장소 마커 & 이름
    home_box = RectSlot(
        id="slot.diagram.home_box",
        prompt="",
        x=505,
        y=120,
        width=60,
        height=30,
        fill="#fecaca",
        stroke="#dc2626",
        stroke_width=1.2,
    )
    home_label = TextBoxSlot(
        id="slot.diagram.home_label",
        prompt="",
        text="우리 집",
        x=568,
        y=124,
        width=70,
        height=24,
        font_size=15,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )
    dot_home = CircleSlot(id="slot.diagram.dot_home", prompt="", cx=535, cy=152, r=3.2, fill="#111827", stroke="#111827", stroke_width=1.0)

    hosp_box = RectSlot(
        id="slot.diagram.hosp_box",
        prompt="",
        x=560,
        y=248,
        width=60,
        height=30,
        fill="#fbcfe8",
        stroke="#db2777",
        stroke_width=1.2,
    )
    hosp_label = TextBoxSlot(
        id="slot.diagram.hosp_label",
        prompt="",
        text="병원",
        x=565,
        y=222,
        width=50,
        height=24,
        font_size=15,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    dot_hosp = CircleSlot(id="slot.diagram.dot_hosp", prompt="", cx=535, cy=262, r=3.2, fill="#111827", stroke="#111827", stroke_width=1.0)

    lib_box = RectSlot(
        id="slot.diagram.lib_box",
        prompt="",
        x=448,
        y=286,
        width=64,
        height=34,
        fill="#e0f2fe",
        stroke="#0284c7",
        stroke_width=1.2,
    )
    lib_label = TextBoxSlot(
        id="slot.diagram.lib_label",
        prompt="",
        text="도서관",
        x=448,
        y=322,
        width=64,
        height=24,
        font_size=15,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    dot_lib = CircleSlot(id="slot.diagram.dot_lib", prompt="", cx=535, cy=304, r=3.2, fill="#111827", stroke="#111827", stroke_width=1.0)

    school_box = RectSlot(
        id="slot.diagram.school_box",
        prompt="",
        x=255,
        y=366,
        width=76,
        height=34,
        fill="#ddd6fe",
        stroke="#7c3aed",
        stroke_width=1.2,
    )
    school_label = TextBoxSlot(
        id="slot.diagram.school_label",
        prompt="",
        text="학교",
        x=200,
        y=372,
        width=50,
        height=24,
        font_size=15,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="right",
        valign="middle",
    )
    dot_school = CircleSlot(id="slot.diagram.dot_school", prompt="", cx=340, cy=366, r=3.2, fill="#111827", stroke="#111827", stroke_width=1.0)

    post_box = RectSlot(
        id="slot.diagram.post_box",
        prompt="",
        x=495,
        y=404,
        width=60,
        height=34,
        fill="#fef3c7",
        stroke="#d97706",
        stroke_width=1.2,
    )
    post_label = TextBoxSlot(
        id="slot.diagram.post_label",
        prompt="",
        text="우체국",
        x=560,
        y=410,
        width=64,
        height=24,
        font_size=15,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )
    dot_post = CircleSlot(id="slot.diagram.dot_post", prompt="", cx=535, cy=400, r=3.2, fill="#111827", stroke="#111827", stroke_width=1.0)

    lbl_600 = TextBoxSlot(
        id="slot.answer.lbl_600",
        prompt="",
        text="약 600 m :",
        x=180,
        y=476,
        width=130,
        height=46,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    input_600 = RectSlot(
        id="slot.answer.input_600",
        prompt="",
        x=324,
        y=476,
        width=360,
        height=46,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 20,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "text",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 24,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    lbl_1000 = TextBoxSlot(
        id="slot.answer.lbl_1000",
        prompt="",
        text="약 1 km :",
        x=180,
        y=534,
        width=130,
        height=46,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    input_1000 = RectSlot(
        id="slot.answer.input_1000",
        prompt="",
        x=324,
        y=534,
        width=360,
        height=46,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 25,
            "include_in_submission": True,
            "order": 1,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "text",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 24,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    slots = (
        stem_slot,
        map_bg,
        road_v1,
        road_v2,
        road_h1,
        road_h2,
        road_diag,
        arc_400,
        badge_400_bg,
        badge_400_text,
        home_box,
        home_label,
        dot_home,
        hosp_box,
        hosp_label,
        dot_hosp,
        lib_box,
        lib_label,
        dot_lib,
        school_box,
        school_label,
        dot_school,
        post_box,
        post_label,
        dot_post,
        lbl_600,
        input_600,
        lbl_1000,
        input_1000,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=604,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=tuple(slot.id for slot in slots),
            ),
        ),
        slots=slots,
    )


PROBLEM_TEMPLATE = build_problem_template()
