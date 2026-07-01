from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008757",
        title="들이의 비교와 어림",
        canvas=Canvas(width=940, height=596, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.top.text", "slot.inserted.image.1", "slot.inserted.image.2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bottle.water.label",
                    "slot.diag.water_name",
                    "slot.diag.water_volume",
                    "slot.diag.soy_name",
                ),
            ),
            Region(
                id="region.choice1",
                role="stem",
                flow="absolute",
                slot_ids=("slot.choice1.text",),
            ),
            Region(
                id="region.choice2",
                role="stem",
                flow="absolute",
                slot_ids=("slot.choice2.arrow", "slot.choice2.text"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.top.text",
                prompt="",
                text="500 mL 생수병을 보고 들이를 어림해 보려고 합니다. 알맞은 것을 선택하세요.",
                style_role="question",
                x=38,
                y=61,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.bottle.water.label",
                prompt="",
                text="",
                style_role="diagram",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diag.water_name",
                prompt="",
                text="생수병",
                style_role="label",
                x=267,
                y=366,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diag.water_volume",
                prompt="",
                text="500 mL",
                style_role="label",
                x=258,
                y=408,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diag.soy_name",
                prompt="",
                text="간장병",
                style_role="label",
                x=609,
                y=361,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice1.text",
                prompt="",
                text="간장병의 들이는 500 mL 생수병의 들이보다 ( 많습니다 , 적습니다 ).",
                style_role="question",
                x=68,
                y=501,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice2.arrow",
                prompt="",
                text="→",
                style_role="question",
                x=211,
                y=541,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice2.text",
                prompt="",
                text="간장병의 들이는 약 ( 2 mL , 2 L )입니다.",
                style_role="question",
                x=246,
                y=542,
                font_size=28,
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=265,
                y=200,
                width=77,
                height=124,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.2",
                prompt="",
                href="data:image/png;base64,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",
                x=585,
                y=125,
                width=126,
                height=205,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008757",
    "problem_type": "들이_비교와_어림",
    "metadata": {
        "language": "ko",
        "question": "500 mL 생수병을 기준으로 간장병의 들이를 비교하고 알맞게 어림하는 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.water_bottle",
                "type": "container",
                "name": "생수병",
                "capacity_unit": "mL",
                "capacity_value": 500,
            },
            {"id": "obj.soy_bottle", "type": "container", "name": "간장병"},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_selection",
            "description": "간장병의 들이 비교 결과와 어림한 단위를 고른다",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008757",
    "problem_type": "들이_비교와_어림",
    "inputs": {
        "total_ticks": 0,
        "target_label": "간장병의 들이와 500 mL 생수병의 들이 비교",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "mL/L",
    },
    "given": [
        {
            "ref": "obj.water_bottle",
            "value": {"name": "생수병", "capacity_value": 500, "capacity_unit": "mL"},
        },
        {"ref": "obj.soy_bottle", "value": {"name": "간장병"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_selection"},
    "method": "compare_and_estimate",
    "plan": [
        "간장병의 들이가 500 mL 생수병보다 큰지 작은지를 읽는다.",
        "비교 결과에 맞는 문장을 고르고, 어림한 단위를 선택한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "간장병의 들이 ? 500 mL 생수병의 들이",
            "value": "more",
        },
        {
            "id": "step.2",
            "expr": "선택지 비교: (많습니다, 적습니다)",
            "value": "많습니다",
        },
        {"id": "step.3", "expr": "선택지 비교: (2 mL, 2 L)", "value": "2 L"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "비교 결과가 500 mL보다 큼과 일치하는가",
            "expected": "more",
            "actual": "more",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "어림 단위가 큰 들이에 맞는가",
            "expected": "2 L",
            "actual": "2 L",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_selection",
            "description": "간장병의 들이 비교 결과와 어림한 단위를 고른다",
        },
        "value": 2,
        "unit": "",
    },
}
