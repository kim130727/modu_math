from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15475"
PROBLEM_TITLE = "동화책과 위인전의 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=960,
            height=260,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.table",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.table.outer",
                    "slot.table.v1",
                    "slot.table.v2",
                    "slot.table.v3",
                    "slot.table.v4",
                    "slot.table.h1",
                    "slot.table.r1c1",
                    "slot.table.r1c2",
                    "slot.table.r1c3",
                    "slot.table.r1c4",
                    "slot.table.r1c5",
                    "slot.table.r2c1",
                    "slot.table.r2c2",
                    "slot.table.r2c3",
                    "slot.table.r2c4",
                    "slot.table.r2c5",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text=(
                    "다음은 지희네 반 학급 문고의 책의 수를 조사한 것입니다. "
                    "동화책과 위인전을 더하면 모두 몇 권입니까?"
                ),
                style_role="question",
                x=30,
                y=28,
                font_size=24,
                fill="#111111",
            ),
            RectSlot(
                id="slot.table.outer",
                prompt="",
                x=30,
                y=80,
                width=600,
                height=90,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1,
            ),
            LineSlot(
                id="slot.table.v1",
                prompt="",
                x1=150,
                y1=80,
                x2=150,
                y2=170,
                stroke="#111827",
                stroke_width=1,
            ),
            LineSlot(
                id="slot.table.v2",
                prompt="",
                x1=270,
                y1=80,
                x2=270,
                y2=170,
                stroke="#111827",
                stroke_width=1,
            ),
            LineSlot(
                id="slot.table.v3",
                prompt="",
                x1=390,
                y1=80,
                x2=390,
                y2=170,
                stroke="#111827",
                stroke_width=1,
            ),
            LineSlot(
                id="slot.table.v4",
                prompt="",
                x1=510,
                y1=80,
                x2=510,
                y2=170,
                stroke="#111827",
                stroke_width=1,
            ),
            LineSlot(
                id="slot.table.h1",
                prompt="",
                x1=30,
                y1=125,
                x2=630,
                y2=125,
                stroke="#111827",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.table.r1c1",
                prompt="",
                text="책 종류",
                x=90,
                y=108,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r1c2",
                prompt="",
                text="위인전",
                x=210,
                y=108,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r1c3",
                prompt="",
                text="동화책",
                x=330,
                y=108,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r1c4",
                prompt="",
                text="그림책",
                x=450,
                y=108,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r1c5",
                prompt="",
                text="참고서",
                x=570,
                y=108,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r2c1",
                prompt="",
                text="수(권)",
                x=90,
                y=153,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r2c2",
                prompt="",
                text="324",
                x=210,
                y=153,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r2c3",
                prompt="",
                text="210",
                x=330,
                y=153,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r2c4",
                prompt="",
                text="103",
                x=450,
                y=153,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            TextSlot(
                id="slot.table.r2c5",
                prompt="",
                text="101",
                x=570,
                y=153,
                font_size=22,
                max_width=110,
                anchor="middle",
                style_role="table",
                fill="#111827",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="534",
                placeholder="권",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 534,
    "unit": "권",
    "target_ref": "quantity.biography_storybook_total",
    "derived_from": "step.add_target_books",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_table_addition_problem",
    "metadata": {
        "language": "ko-KR",
        "question": "동화책과 위인전을 더하면 모두 몇 권입니까?",
        "instruction": "표에서 필요한 두 수를 찾아 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "collection.class_library",
                "type": "book_collection",
                "label": "지희네 반 학급 문고",
            },
            {
                "id": "quantity.biography_count",
                "type": "quantity",
                "label": "위인전 수",
                "value": 324,
                "unit": "권",
            },
            {
                "id": "quantity.storybook_count",
                "type": "quantity",
                "label": "동화책 수",
                "value": 210,
                "unit": "권",
            },
            {
                "id": "quantity.picture_book_count",
                "type": "quantity",
                "label": "그림책 수",
                "value": 103,
                "unit": "권",
            },
            {
                "id": "quantity.reference_book_count",
                "type": "quantity",
                "label": "참고서 수",
                "value": 101,
                "unit": "권",
            },
            {
                "id": "quantity.biography_storybook_total",
                "type": "unknown_quantity",
                "label": "위인전과 동화책의 전체 수",
                "unit": "권",
            },
        ],
        "relations": [
            {
                "id": "relation.target_is_sum",
                "type": "sum_of",
                "subject": "quantity.biography_storybook_total",
                "objects": [
                    "quantity.biography_count",
                    "quantity.storybook_count",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.biography_count",
                    "quantity.storybook_count",
                    "quantity.picture_book_count",
                    "quantity.reference_book_count",
                ],
                "target_ref": "quantity.biography_storybook_total",
                "condition_refs": ["relation.target_is_sum"],
            },
            "plan": {
                "method": "select_table_values_and_add",
                "description": "표에서 위인전과 동화책의 수를 찾아 더합니다.",
            },
            "execute": {
                "expected_operations": ["addition"],
            },
            "review": {
                "check_methods": ["subtraction_check"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_table_addition_problem",
    "inputs": {
        "target_label": "위인전과 동화책의 전체 수",
        "unit": "권",
        "book_counts": {
            "biography": 324,
            "storybook": 210,
            "picture_book": 103,
            "reference_book": 101,
        },
    },
    "given": [
        {
            "ref": "quantity.biography_count",
            "value": {
                "count": 324,
                "unit": "권",
            },
        },
        {
            "ref": "quantity.storybook_count",
            "value": {
                "count": 210,
                "unit": "권",
            },
        },
        {
            "ref": "quantity.picture_book_count",
            "value": {
                "count": 103,
                "unit": "권",
            },
        },
        {
            "ref": "quantity.reference_book_count",
            "value": {
                "count": 101,
                "unit": "권",
            },
        },
    ],
    "target": {
        "ref": "quantity.biography_storybook_total",
        "type": "number",
    },
    "method": "표에서 위인전 수 324권과 동화책 수 210권을 찾아 두 수를 더합니다.",
    "understanding": {
        "summary": "표에서 위인전과 동화책의 수를 찾아 두 수의 합을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.biography_count",
                "label": "위인전 수",
                "value": 324,
                "unit": "권",
                "source": "explicit",
            },
            {
                "ref": "quantity.storybook_count",
                "label": "동화책 수",
                "value": 210,
                "unit": "권",
                "source": "explicit",
            },
            {
                "ref": "quantity.picture_book_count",
                "label": "그림책 수",
                "value": 103,
                "unit": "권",
                "source": "explicit",
            },
            {
                "ref": "quantity.reference_book_count",
                "label": "참고서 수",
                "value": 101,
                "unit": "권",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.biography_storybook_total",
                "label": "위인전과 동화책의 전체 수",
                "unit": "권",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "위인전 수와 동화책 수를 더하면 두 종류의 책 전체 수가 됩니다.",
            "symbolic": "324 + 210 = □",
            "uses": [
                "quantity.biography_count",
                "quantity.storybook_count",
            ],
            "result": "quantity.biography_storybook_total",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 더해야 하는 두 종류의 책은 무엇인가요?",
                "choices": [
                    "위인전과 동화책",
                    "동화책과 그림책",
                    "그림책과 참고서",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.values",
                "type": "multiple_choice",
                "prompt": "표에서 위인전과 동화책의 수를 바르게 찾은 것은 무엇인가요?",
                "choices": [
                    "위인전 324권, 동화책 210권",
                    "위인전 210권, 동화책 103권",
                    "위인전 103권, 동화책 101권",
                ],
                "answer_index": 0,
            },
        ],
    },
    "plan": [
        "표에서 위인전의 수 324권을 찾습니다.",
        "표에서 동화책의 수 210권을 찾습니다.",
        "두 종류의 책 수를 더합니다.",
    ],
    "steps": [
        {
            "id": "step.add_target_books",
            "expr": "324 + 210",
            "value": 534,
            "explanation": "동화책과 위인전을 모두 세어야 하므로 324와 210을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_storybooks",
            "expr": "534 - 210",
            "expected": 324,
            "actual": 324,
            "pass": True,
        },
        {
            "id": "check.subtract_biographies",
            "expr": "534 - 324",
            "expected": 210,
            "actual": 210,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
