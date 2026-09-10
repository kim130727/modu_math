from __future__ import annotations

from modu_math.dsl import (
    Arrow,
    BlankSlot,
    Canvas,
    ChoiceSlot,
    Circle,
    CircleSlot,
    Constraint,
    Cube,
    DiagramTemplate,
    FractionAreaModel,
    Grid,
    Group,
    ImageSlot,
    LabelSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    ShapeObject,
    TextBoxSlot,
    TextSlot,
    Triangle,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=960,
        height=480,
        coordinate_mode="logical",
    )
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=("slot.question", "slot.inserted.image.1"),
        ),
        Region(
            id="region.diagram",
            role="diagram",
            flow="absolute",
            slot_ids=("slot.label.a", "slot.label.b"),
        ),
        Region(
            id="region.choice",
            role="choice",
            flow="absolute",
            slot_ids=("slot.choice.1", "slot.choice.2"),
        ),
        Region(
            id="region.answer",
            role="answer",
            flow="absolute",
            slot_ids=(),
        ),
    )
    slots = (
        TextBoxSlot(
            id="slot.question",
            prompt="",
            text=(
                "បន្ទាប់ពីបំពេញទឹកក្នុងដប ក និង ខ ពេញហើយ ទឹកត្រូវបានចាក់ទៅក្នុងធុងដែលមានរាង "
                "និងទំហំដូចគ្នា។ ប្រៀបធៀបចំណុះរបស់ដប ក និង ខ តាមកម្ពស់ទឹកដែលបង្ហាញក្នុងរូប "
                "ហើយជ្រើសពាក្យត្រឹមត្រូវ។"
            ),
            style_role="question",
            x=66.684,
            y=17.307,
            width=825.55,
            height=158,
            font_size=30,
            line_height=1.25,
            fill="#111827",
        ),
        TextBoxSlot(
            id="slot.label.a",
            prompt=None,
            text="ក",
            style_role="body",
            x=118.359,
            y=176.832,
            width=48.067,
            height=46,
            font_size=30,
            line_height=1.25,
            fill="#111827",
            semantic_role="symbol_label",
        ),
        TextBoxSlot(
            id="slot.label.b",
            prompt=None,
            text="ខ",
            style_role="body",
            x=685.632,
            y=194.047,
            width=51.512,
            height=46,
            font_size=30,
            line_height=1.25,
            fill="#111827",
            semantic_role="symbol_label",
        ),
        TextSlot(
            id="slot.choice.1",
            prompt="",
            text="(1) ដបដែលទឹកចាក់ផ្ទេរមានកម្ពស់ខ្ពស់ជាងគឺ (ដប ក, ដប ខ)។",
            style_role="question",
            x=36,
            y=402,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.choice.2",
            prompt="",
            text="(2) ដបដែលមានចំណុះច្រើនជាងគឺ (ដប ក, ដប ខ)។",
            style_role="question",
            x=36,
            y=448,
            font_size=28,
            fill="#111111",
        ),
        ImageSlot(
            id="slot.inserted.image.1",
            prompt="",
            href="data:image/png;base64,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",
            x=230,
            y=148,
            width=460,
            height=205,
            preserve_aspect_ratio="xMidYMid meet",
        ),
    )
    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="S3_elem_3_008745",
        title="ការប្រៀបធៀបចំណុះ",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()

PROBLEM_ID = "S3_elem_3_008745"

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_elem_3_008745",
    "problem_type": "비교",
    "metadata": {
        "language": "ko",
        "question": "ប្រៀបធៀបចំណុះរបស់ដប ក និង ខ។",
        "instruction": "ជ្រើសពាក្យត្រឹមត្រូវ។",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle.ga", "type": "물병", "label": "ដប ក"},
            {"id": "obj.bottle.na", "type": "물병", "label": "ដប ខ"},
            {
                "id": "obj.container.left",
                "type": "그릇",
                "label": "ធុងខាងឆ្វេង",
                "same_shape_as": "obj.container.right",
                "same_size_as": "obj.container.right",
            },
            {
                "id": "obj.container.right",
                "type": "그릇",
                "label": "ធុងខាងស្តាំ",
                "same_shape_as": "obj.container.left",
                "same_size_as": "obj.container.left",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.bottle.ga",
                    "obj.bottle.na",
                    "obj.container.left",
                    "obj.container.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.height", "rel.compare.capacity"],
            },
            "plan": {
                "method": "same_container_height_comparison",
                "description": "같은 모양과 크기의 그릇에 옮겨 담은 물의 높이를 비교하여 들이의 많고 "
                "적음을 판단한다.",
            },
            "execute": {
                "expected_operations": ["compare_water_heights", "infer_capacity_relation"]
            },
            "review": {"check_methods": ["same_container_rule_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["가 물병", "나 물병"],
        "choice_groups": [
            {"label": "(1)번 문제", "choices": ["가 물병", "나 물병"]},
            {"label": "(2)번 문제", "choices": ["가 물병", "나 물병"]},
        ],
        "answer_key": ["나 물병", "나 물병"],
        "target": {
            "type": "multiple_choice_group",
            "description": "옮겨 담은 물의 높이가 더 높은 것과 들이가 더 많은 것",
        },
        "value": "나 물병, 나 물병",
        "unit": "",
    },
}

SEMANTIC = SEMANTIC_OVERRIDE

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_elem_3_008745",
    "problem_type": "비교",
    "inputs": {
        "total_ticks": 2,
        "target_label": "가 물병, 나 물병",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle.ga", "value": {"label": "가 물병"}},
        {"ref": "obj.bottle.na", "value": {"label": "나 물병"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_group"},
    "method": "same_container_rule_check",
    "plan": [
        "ប្រៀបធៀបកម្ពស់ទឹកដែលចាក់ទៅក្នុងធុងមានរាងនិងទំហំដូចគ្នា។",
        "សន្និដ្ឋានថាដែលមានកម្រិតទឹកខ្ពស់ជាង មានចំណុះច្រើនជាង។",
    ],
    "steps": [
        {"id": "step.1", "expr": "그림에서 오른쪽 그릇의 물 높이가 더 높다", "value": "나 물병"},
        {
            "id": "step.2",
            "expr": "같은 그릇에서는 물 높이가 더 높은 쪽의 들이가 더 많다",
            "value": "나 물병",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "같은 모양과 크기의 그릇 비교인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답 선택이 그림의 높이 비교와 일치하는지 확인",
            "expected": "나 물병",
            "actual": "나 물병",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": ["가 물병", "나 물병"],
        "choice_groups": [
            {"label": "(1)번 문제", "choices": ["가 물병", "나 물병"]},
            {"label": "(2)번 문제", "choices": ["가 물병", "나 물병"]},
        ],
        "answer_key": ["나 물병", "나 물병"],
        "target": {
            "type": "multiple_choice_group",
            "description": "옮겨 담은 물의 높이가 더 높은 것과 들이가 더 많은 것",
        },
        "value": "나 물병, 나 물병",
        "unit": "",
    },
}

SEMANTIC_ANSWER = SOLVABLE.get("answer")
