from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_00469"
PROBLEM_TITLE = "두 가족이 캔 고구마의 수"


ANSWER = {
    "value": 507,
    "unit": "개",
    "values": [507],
    "choices": [],
    "blanks": [
        {
            "id": "konva_1785063642549_rect_11081",
            "slot_id": "konva_1785063642549_rect_11081",
            "expected": 507,
        },
    ],
    "answer_key": [
        {
            "slot_id": "konva_1785063642549_rect_11081",
            "value": 507,
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "person.sanghyeon", "type": "person", "label": "상현"},
            {"id": "person.yongjin", "type": "person", "label": "용진"},
            {
                "id": "group.sanghyeon_family",
                "type": "family",
                "label": "상현이네 가족",
            },
            {
                "id": "group.yongjin_family",
                "type": "family",
                "label": "용진이네 가족",
            },
            {
                "id": "object.sweet_potato",
                "type": "countable_object",
                "label": "고구마",
                "unit": "개",
            },
            {
                "id": "quantity.sanghyeon_family_sweet_potatoes",
                "type": "quantity",
                "label": "상현이네 가족이 캔 고구마 수",
                "value": 259,
                "unit": "개",
            },
            {
                "id": "quantity.yongjin_family_sweet_potatoes",
                "type": "quantity",
                "label": "용진이네 가족이 캔 고구마 수",
                "value": 248,
                "unit": "개",
            },
            {
                "id": "quantity.total_sweet_potatoes",
                "type": "quantity",
                "label": "두 가족이 캔 고구마 수",
                "value": 507,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.sanghyeon_belongs_to_family",
                "type": "member_of",
                "from_id": "person.sanghyeon",
                "to_id": "group.sanghyeon_family",
            },
            {
                "id": "relation.yongjin_belongs_to_family",
                "type": "member_of",
                "from_id": "person.yongjin",
                "to_id": "group.yongjin_family",
            },
            {
                "id": "relation.sanghyeon_family_collected",
                "type": "collected",
                "from_id": "group.sanghyeon_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.sanghyeon_family_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_family_collected",
                "type": "collected",
                "from_id": "group.yongjin_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.yongjin_family_sweet_potatoes",
            },
            {
                "id": "relation.sanghyeon_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.sanghyeon_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.yongjin_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "given": [
        {
            "id": "sanghyeon_family_count",
            "ref": "quantity.sanghyeon_family_sweet_potatoes",
            "value": 259,
            "unit": "개",
            "label": "상현이네 가족이 캔 고구마 수",
        },
        {
            "id": "yongjin_family_count",
            "ref": "quantity.yongjin_family_sweet_potatoes",
            "value": 248,
            "unit": "개",
            "label": "용진이네 가족이 캔 고구마 수",
        },
    ],
    "target": {
        "id": "total_sweet_potatoes",
        "ref": "quantity.total_sweet_potatoes",
        "type": "number",
        "unit": "개",
        "label": "두 가족이 캔 고구마 수",
    },
    "method": "add_parts",
    "plan": [
        "상현이네 가족이 캔 고구마 수를 확인한다.",
        "용진이네 가족이 캔 고구마 수를 확인한다.",
        "두 수를 더해 전체 고구마 수를 구한다.",
    ],
    "steps": [
        {
            "id": "step.add_counts",
            "goal": "두 가족이 캔 고구마 수를 모두 구한다.",
            "expr": "259 + 248",
            "value": 507,
            "explanation": "전체 고구마 수를 구해야 하므로 259와 248을 더한다.",
        },
    ],
    "checks": [
        "507 - 248 = 259",
        "507 - 259 = 248",
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["add.part_part_whole", "add.three_digit"],
        "errors": {
            "497": "execute.add_carry",
            "259": "plan.copy_one_part",
            "248": "plan.copy_one_part",
        },
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                    "slot.expression",
                    "konva_1785063642549_rect_11081",
                    "konva_1785063642549_text_21880",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=32,
                y=24,
                width=836,
                height=92,
                text=(
                    "지난 일요일 상현이네와 용진이네 가족은 주말 농장에 갔습니다. "
                    "고구마를 상현이네는 259개, 용진이네는 248개 캤습니다. "
                    "이 두 가족이 캔 고구마는 모두 몇 개입니까?"
                ),
                font_size=24,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=124,
                y=146,
                width=340,
                height=42,
                text="259 + 248 =",
                font_size=30,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="right",
                valign="middle",
            ),
            RectSlot(
                id="konva_1785063642549_rect_11081",
                prompt="",
                x=486,
                y=145,
                width=112,
                height=44,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
                interaction={
                    "type": "input",
                    "role": "answer",
                    "value_type": "integer",
                    "max_length": 3,
                    "include_in_submission": True,
                    "order": 0,
                    "group_id": "final_answer",
                    "auto_advance": False,
                    "keyboard": "number",
                },
                input_style={
                    "font_size_mode": "auto",
                    "font_size_adjust": 0,
                    "min_font_size": 14,
                    "max_font_size": 52,
                    "font_weight": 700,
                    "horizontal_align": "center",
                    "vertical_align": "middle",
                    "padding": 6,
                    "text_color": "#222222",
                },
            ),
            TextBoxSlot(
                id="konva_1785063642549_text_21880",
                prompt="",
                text="개",
                x=614,
                y=145,
                font_size=30,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#111827",
                width=60,
                height=44,
                align="left",
                valign="middle",
                line_height=1.25,
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
