"""ModuMath Problem DSL: 선분 찾아 기호 쓰기 (S3_초등_3_011942)"""

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


PROBLEM_ID = "S3_초등_3_011942"
PROBLEM_TITLE = "선분 찾아 기호 쓰기"


ANSWER = {
    "type": "short_answer",
    "value": "ㄷ",
    "unit": "",
    "values": ["ㄷ", "㉢"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄷ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄷ",
            "diagnostics": [
                {
                    "id": "diag.curved_line_selected",
                    "condition": "answer_in_ga_na",
                    "concept": "선분의 정의",
                    "reason": "굽은 선인 ㄱ 또는 ㄴ을 선택함",
                    "feedback": "선분은 두 점을 곧게 이은 선입니다. 휘어지지 않고 곧게 뻗은 선을 찾아보세요.",
                },
                {
                    "id": "diag.bent_line_selected",
                    "condition": "answer_equals_ra",
                    "concept": "선분의 정의",
                    "reason": "중간에 꺾인 선 ㄹ을 선분으로 착각함",
                    "feedback": "ㄹ은 중간에서 한 번 꺾인 선입니다. 두 점을 한 번에 곧게 이은 선을 찾아보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_line_classification",
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
            {"id": "point.left", "type": "point", "label": "왼쪽 점"},
            {"id": "point.right", "type": "point", "label": "오른쪽 점"},
            {"id": "line.giyeok", "type": "curved_line", "label": "ㄱ", "is_straight": False},
            {"id": "line.nieun", "type": "curved_line", "label": "ㄴ", "is_straight": False},
            {"id": "line.digeut", "type": "line_segment", "label": "ㄷ", "is_straight": True},
            {"id": "line.rieul", "type": "polyline", "label": "ㄹ", "is_straight": False},
        ],
        "relations": [
            {
                "id": "relation.target_segment",
                "type": "is_line_segment",
                "from_id": "line.digeut",
                "to_id": "concept.line_segment",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _badge_slots(prefix: str, label: str, cx: float, cy: float) -> tuple[CircleSlot, TextBoxSlot]:
    circle = CircleSlot(
        id=f"slot.diagram.{prefix}_badge",
        prompt="",
        cx=cx,
        cy=cy,
        r=14.0,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
    )
    text = TextBoxSlot(
        id=f"slot.diagram.{prefix}_label",
        prompt="",
        text=label,
        x=cx - 14,
        y=cy - 14,
        width=28,
        height=28,
        font_size=17,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    return circle, text


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="선분을 찾아 기호를 쓰세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    line_g = PathSlot(
        id="slot.diagram.line_g",
        prompt="",
        d="M 200 225 Q 450 55 700 225",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    line_n = PathSlot(
        id="slot.diagram.line_n",
        prompt="",
        d="M 200 225 C 295 140, 385 185, 470 210 C 545 232, 595 170, 700 225",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    line_d = LineSlot(
        id="slot.diagram.line_d",
        prompt="",
        x1=200,
        y1=225,
        x2=700,
        y2=225,
        stroke="#111827",
        stroke_width=1.8,
    )
    line_r = PathSlot(
        id="slot.diagram.line_r",
        prompt="",
        d="M 200 225 L 450 285 L 700 225",
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )

    dot_left = CircleSlot(
        id="slot.diagram.dot_left",
        prompt="",
        cx=200,
        cy=225,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_right = CircleSlot(
        id="slot.diagram.dot_right",
        prompt="",
        cx=700,
        cy=225,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    badge_g_c, badge_g_t = _badge_slots("g", "ㄱ", 450, 108)
    badge_n_c, badge_n_t = _badge_slots("n", "ㄴ", 450, 178)
    badge_d_c, badge_d_t = _badge_slots("d", "ㄷ", 450, 248)
    badge_r_c, badge_r_t = _badge_slots("r", "ㄹ", 450, 314)

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=356,
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
        y=356,
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
        y=356,
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
        line_g,
        line_n,
        line_d,
        line_r,
        dot_left,
        dot_right,
        badge_g_c,
        badge_g_t,
        badge_n_c,
        badge_n_t,
        badge_d_c,
        badge_d_t,
        badge_r_c,
        badge_r_t,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=430,
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
