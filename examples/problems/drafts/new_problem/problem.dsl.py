from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextBoxSlot

PROBLEM_ID = "new_problem"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title="new_problem",
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("konva_1783748388763_text_23300",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="konva_1783748388763_text_23300",
                prompt="",
                text="안녕하세요",
                x=80.917,
                y=59.296,
                font_size=30,
                fill="#111827",
                width=168,
                height=46,
                align="left",
                line_height=1.25,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("draft",),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "metadata": {
        "language": "ko",
        "question": "",
        "instruction": "",
    },
    "domain": {
        "objects": [],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": "",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "inputs": {
        "target_label": "",
        "unit": "",
        "quantities": {},
        "conditions": [],
    },
    "given": [],
    "target": {
        "ref": "answer.value",
        "type": "unknown",
    },
    "method": "",
    "plan": [],
    "steps": [],
    "checks": [],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": "",
        "unit": "",
    },
}
