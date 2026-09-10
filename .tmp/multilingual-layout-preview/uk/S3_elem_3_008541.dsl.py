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
        width=940,
        height=394,
        coordinate_mode="logical",
    )
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=(
                "slot.q1",
                "slot.box",
                "slot.expr1",
                "slot.expr2",
                "slot.expr3",
                "slot.opt1",
                "slot.opt2",
                "slot.opt3",
                "slot.opt4",
            ),
        ),
    )
    slots = (
        TextSlot(
            id="slot.q1",
            prompt="",
            text="Виберіть варіант, де результати розташовані від найбільшого до найменшого.",
            style_role="question",
            x=105.018,
            y=76,
            font_size=28,
            fill="#111111",
        ),
        RectSlot(
            id="slot.box",
            prompt="",
            x=101.019,
            y=120,
            width=765,
            height=78,
            stroke="#FBE7C4",
            stroke_width=1,
            fill="#FBE7C4",
        ),
        TextSlot(
            id="slot.expr1",
            prompt="",
            text="А. 397 × 6",
            style_role="body",
            x=201.019,
            y=170,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.expr2",
            prompt="",
            text="Б. 549 × 4",
            style_role="body",
            x=411.019,
            y=170,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.expr3",
            prompt="",
            text="В. 456 × 5",
            style_role="body",
            x=641.019,
            y=170,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.opt1",
            prompt="",
            text="① А Б В",
            style_role="body",
            x=161.019,
            y=260,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.opt2",
            prompt="",
            text="② А В Б",
            style_role="body",
            x=531.019,
            y=260,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.opt3",
            prompt="",
            text="③ Б В А",
            style_role="body",
            x=161.019,
            y=320,
            font_size=28,
            fill="#111111",
        ),
        TextSlot(
            id="slot.opt4",
            prompt="",
            text="④ В Б А",
            style_role="body",
            x=531.019,
            y=315,
            font_size=28,
            fill="#111111",
        ),
    )
    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="S3_elem_3_008541",
        title="Виберіть варіант, де результати розташовані від найбільшого до найменшого",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()

PROBLEM_ID = "S3_elem_3_008541"

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_elem_3_008541",
    "problem_type": "multiple_choice_ordering",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
        "instruction": "보기에서 계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.a", "type": "expression", "label": "А", "operation": "397 × 6"},
            {"id": "obj.b", "type": "expression", "label": "Б", "operation": "549 × 4"},
            {"id": "obj.c", "type": "expression", "label": "В", "operation": "456 × 5"},
            {"id": "obj.option2", "type": "choice", "label": "②", "sequence": ["А", "В", "Б"]},
        ],
        "relations": [
            {"id": "rel.order", "type": "descending_order", "from_id": "obj.a", "to_id": "obj.b"}
        ],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
}

SEMANTIC = SEMANTIC_OVERRIDE

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": "S3_elem_3_008541",
    "problem_type": "multiple_choice_ordering",
    "inputs": {
        "total_ticks": 3,
        "target_label": "보기 번호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"label": "А", "expr": "397 × 6"}},
        {"ref": "obj.b", "value": {"label": "Б", "expr": "549 × 4"}},
        {"ref": "obj.c", "value": {"label": "В", "expr": "456 × 5"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_number"},
    "method": "compare_results_descending",
    "plan": [
        "Обчисліть кожний добуток і порівняйте результати від найбільшого до найменшого.",
        "Знайдіть номер варіанта з таким самим порядком порівняння.",
    ],
    "steps": [
        {"id": "step.1", "expr": "397 × 6", "value": 2382},
        {"id": "step.2", "expr": "549 × 4", "value": 2196},
        {"id": "step.3", "expr": "456 × 5", "value": 2280},
        {"id": "step.4", "expr": "2382 > 2280 > 2196", "value": "А, В, Б"},
        {"id": "step.5", "expr": "보기 대조", "value": "②"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "2382 > 2280 > 2196",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 ②의 순서",
            "expected": "А, В, Б",
            "actual": "А, В, Б",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
    "understanding": {
        "summary": "Compute three multiplication expressions and choose the option that "
        "orders their results from greatest to least.",
        "facts": [
            {
                "ref": "obj.a",
                "label": "expression A",
                "value": "397 x 6",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "obj.b",
                "label": "expression B",
                "value": "549 x 4",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "obj.c",
                "label": "expression C",
                "value": "456 x 5",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {"ref": "answer.target", "label": "choice number for descending order", "unit": ""}
        ],
        "relation": {
            "type": "compare_products_descending",
            "statement": "The products are 2382, 2196, and 2280, so the "
            "descending order is A, C, B.",
            "symbolic": "397 x 6 > 456 x 5 > 549 x 4",
            "uses": ["obj.a", "obj.b", "obj.c"],
            "result": "answer.target",
        },
        "diagnostic_questions": [
            {
                "id": "understand.compute_a",
                "type": "multiple_choice",
                "prompt": "What is 397 x 6?",
                "choices": [
                    {"id": "choice.1", "label": "choices", "text": "choices"},
                    {"id": "choice.2", "label": "2196", "text": "2196"},
                    {"id": "choice.3", "label": "2280", "text": "2280"},
                    {"id": "choice.4", "label": "2382", "text": "2382"},
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.order",
                "type": "multiple_choice",
                "prompt": "Which order is greatest to least?",
                "choices": [
                    {"id": "choice.1", "label": "choices", "text": "choices"},
                    {"id": "choice.2", "label": "A, B, C", "text": "A, B, C"},
                    {"id": "choice.3", "label": "A, C, B", "text": "A, C, B"},
                    {"id": "choice.4", "label": "C, A, B", "text": "C, A, B"},
                ],
                "answer_index": 1,
            },
        ],
    },
}

SEMANTIC_ANSWER = SOLVABLE.get("answer")
