"""ModuMath Problem DSL: 각의 구성 요소에 대한 설명 고르기 (S3_초등_3_011944)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011944"
PROBLEM_TITLE = "각에 대한 잘못된 설명 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "ㄴ",
    "unit": "",
    "values": ["ㄴ", "㉡"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄴ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄴ",
            "diagnostics": [
                {
                    "id": "diag.confused_vertex_and_points",
                    "condition": "answer_in_ga_da",
                    "concept": "각의 꼭짓점과 변",
                    "reason": "반직선 위의 점 ㄴ, ㄹ까지 각의 꼭짓점으로 착각함",
                    "feedback": "각에서 두 반직선이 만나는 점 ㄷ만 각의 꼭짓점입니다. 따라서 각의 꼭짓점은 1개입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_angle_properties",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "02단원_평면도형",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "angle.nd_r", "type": "angle", "label": "각 ㄴㄷㄹ", "vertex": "점 ㄷ", "sides": ["반직선 ㄷㄴ", "반직선 ㄷㄹ"]},
            {"id": "statement.g", "type": "statement", "label": "ㄱ", "text": "점 ㄷ은 꼭짓점입니다.", "is_correct": True},
            {"id": "statement.n", "type": "statement", "label": "ㄴ", "text": "꼭짓점이 3개 있습니다.", "is_correct": False},
            {"id": "statement.d", "type": "statement", "label": "ㄷ", "text": "반직선 ㄷㄴ은 각의 변입니다.", "is_correct": True},
        ],
        "relations": [
            {
                "id": "relation.incorrect_statement",
                "type": "is_false_statement",
                "from_id": "statement.n",
                "to_id": "angle.nd_r",
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
        text="다음 도형을 보고 잘못 설명한 것을 찾아 기호를 쓰세요.",
        x=32,
        y=24,
        width=836,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    ray_up = LineSlot(
        id="slot.diagram.ray_up",
        prompt="",
        x1=515,
        y1=210,
        x2=410,
        y2=82,
        stroke="#111827",
        stroke_width=1.9,
    )

    ray_left = LineSlot(
        id="slot.diagram.ray_left",
        prompt="",
        x1=515,
        y1=210,
        x2=320,
        y2=210,
        stroke="#111827",
        stroke_width=1.9,
    )

    dot_n = CircleSlot(
        id="slot.diagram.dot_n",
        prompt="",
        cx=445,
        cy=125,
        r=3.8,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_d = CircleSlot(
        id="slot.diagram.dot_d",
        prompt="",
        cx=515,
        cy=210,
        r=3.8,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_r = CircleSlot(
        id="slot.diagram.dot_r",
        prompt="",
        cx=370,
        cy=210,
        r=3.8,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    label_n = TextBoxSlot(
        id="slot.diagram.label_n",
        prompt="",
        text="ㄴ",
        x=456,
        y=102,
        width=32,
        height=30,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )
    label_d = TextBoxSlot(
        id="slot.diagram.label_d",
        prompt="",
        text="ㄷ",
        x=526,
        y=194,
        width=32,
        height=30,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )
    label_r = TextBoxSlot(
        id="slot.diagram.label_r",
        prompt="",
        text="ㄹ",
        x=354,
        y=220,
        width=32,
        height=30,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    statement_box = RectSlot(
        id="slot.diagram.statement_box",
        prompt="",
        x=90,
        y=264,
        width=720,
        height=154,
        fill="#ffffff",
        stroke="#d885a3",
        stroke_width=2.0,
    )

    stmt_g = TextBoxSlot(
        id="slot.diagram.stmt_g",
        prompt="",
        text="㉠ 점 ㄷ은 꼭짓점입니다.",
        x=125,
        y=282,
        width=650,
        height=34,
        font_size=23,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )
    stmt_n = TextBoxSlot(
        id="slot.diagram.stmt_n",
        prompt="",
        text="㉡ 꼭짓점이 3개 있습니다.",
        x=125,
        y=324,
        width=650,
        height=34,
        font_size=23,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )
    stmt_d = TextBoxSlot(
        id="slot.diagram.stmt_d",
        prompt="",
        text="㉢ 반직선 ㄷㄴ은 각의 변입니다.",
        x=125,
        y=366,
        width=650,
        height=34,
        font_size=23,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=444,
        width=28,
        height=52,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=594,
        y=444,
        width=170,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 4,
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
            "max_font_size": 26,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=770,
        y=444,
        width=28,
        height=52,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        ray_up,
        ray_left,
        dot_n,
        dot_d,
        dot_r,
        label_n,
        label_d,
        label_r,
        statement_box,
        stmt_g,
        stmt_n,
        stmt_d,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=520,
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
