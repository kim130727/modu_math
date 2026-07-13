from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    Group,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    PathSlot,
)

PROBLEM_ID = "រង្វង់_ឆកោនទៀងទាត់_ផលខុសគ្នាបរិមាត្រ_០០១"
PROBLEM_TITLE = "ផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=700,
            height=420,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.hexagon",
                    "slot.diameter_line",
                    "slot.center_point",
                    "slot.label_30",
                    "konva_1783767050396_paste_321289_0",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                text="ក្នុងរូបខាងស្តាំ តើផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់ស្មើប៉ុន្មានសង់ទីម៉ែត្រ? (តម្លៃ π: 3.14)",
                prompt="សំណួរដែលសួររកផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់",
                semantic_role="question",
                x=15,
                y=18,
                width=656,
                height=63,
                font_size=22,
                line_height=1.25,
                fill="#111111",
                align="left",
            ),
            # រង្វង់៖ អង្កត់ផ្ចិត 30cm កាំ 15cm
            CircleSlot(
                id="slot.circle",
                prompt="រង្វង់ដែលមានអង្កត់ផ្ចិត 30cm",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # ឆកោនទៀងទាត់ចារឹកក្នុងរង្វង់
            # ផ្ចិត (565, 225), កាំ 100px
            # កំពូល៖ 0°, 60°, 120°, 180°, 240°, 300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="ឆកោនទៀងទាត់ចារឹកក្នុងរង្វង់",
                points=(
                    (436, 264),
                    (386, 177.4),
                    (286, 177.4),
                    (236, 264),
                    (286, 350.6),
                    (386, 350.6),
                ),
                fill="none",
                stroke="#202020",
                stroke_width=2,
            ),
            # អង្កត់ផ្ចិតដែលភ្ជាប់កំពូលទល់មុខគ្នានៃឆកោនទៀងទាត់
            LineSlot(
                id="slot.diameter_line",
                prompt="អង្កត់ផ្ចិតរង្វង់ 30cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="ផ្ចិតរង្វង់",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="សញ្ញាបង្ហាញប្រវែងអង្កត់ផ្ចិត",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="ផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់",
                answer_key="4.2cm",
                placeholder="ចម្លើយ",
            ),
            PathSlot(
                id="konva_1783767050396_paste_321289_0",
                prompt="",
                d="M 234 267 Q 336.5 207 439 267",
                fill="none",
                stroke="#555555",
                stroke_width=1.8,
                stroke_dasharray="6 5",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.diagram.circle_hexagon",
                role="diagram_block",
                member_ids=(
                    "slot.circle",
                    "slot.hexagon",
                    "slot.diameter_line",
                    "slot.center_point",
                    "slot.label_30",
                    "konva_1783767050396_paste_321289_0",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "circle",
            "regular-hexagon",
            "circumference",
            "perimeter",
            "inscribed-polygon",
            "elementary-math",
            "schema-compliant",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_perimeter_difference",
    "metadata": {
        "language": "km",
        "question": (
            "ក្នុងរូបខាងស្តាំ តើផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់ស្មើប៉ុន្មានសង់ទីម៉ែត្រ? "
            "(តម្លៃ π: 3.14)"
        ),
        "instruction": (
            "រកកាំពីអង្កត់ផ្ចិតរង្វង់ ហើយប្រើការពិតថាប្រវែងជ្រុងមួយនៃឆកោនទៀងទាត់ដែលចារឹកក្នុងរង្វង់ "
            "ស្មើនឹងកាំរង្វង់។"
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "រង្វង់",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "ឆកោនទៀងទាត់",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "ផ្ចិតរង្វង់",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "អង្កត់ផ្ចិតរង្វង់",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "តម្លៃ π",
                "value": 3.14,
            },
        ],
        "relations": [
            {
                "id": "rel.hexagon_inscribed",
                "type": "inscribed_in",
                "from_id": "obj.hexagon",
                "to_id": "obj.circle",
            },
            {
                "id": "rel.hexagon_side_equals_radius",
                "type": "side_length_equals_radius",
                "from_id": "obj.hexagon",
                "to_id": "obj.circle",
                "equation": "s = r",
            },
            {
                "id": "rel.diameter_measure",
                "type": "diameter_measure",
                "from_id": "obj.circle",
                "to_id": "measure.diameter",
                "equation": "d = 30",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "slot.answer",
                "type": "number",
                "value": 4.2,
                "unit": "cm",
            }
        ],
        "choices": [],
        "answer_key": "4.2cm",
        "target": {
            "type": "perimeter_difference",
            "description": "តម្លៃដែលបានពីការដកបរិមាត្រឆកោនទៀងទាត់ចេញពីបរិមាត្ររង្វង់",
        },
        "value": 4.2,
        "unit": "cm",
    },
}


# Editor-build compatibility payload. The visual layout above is authored; this
# block keeps generated ids and answer/solvable shapes aligned with schemas.
PROBLEM_ID = "ថ្នាក់ទី៦_២_ផ្ទៃក្រឡារង្វង់_០០០២"
PROBLEM_TEMPLATE = build_problem_template()

ANSWER = {
    "blanks": [
        {
            "id": "slot.answer",
            "type": "number",
            "value": 4.2,
            "unit": "cm",
        }
    ],
    "choices": [],
    "answer_key": [
        {
            "blank_id": "slot.answer",
            "value": 4.2,
            "unit": "cm",
        }
    ],
    "target": {
        "type": "perimeter_difference",
        "description": "តម្លៃដែលបានពីការដកបរិមាត្រឆកោនទៀងទាត់ចេញពីបរិមាត្ររង្វង់",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_perimeter_difference",
    "inputs": {
        "diameter": 30,
        "pi": 3.14,
        "polygon_sides": 6,
        "target_label": "ផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់",
        "unit": "cm",
    },
    "given": [
        {"ref": "measure.diameter", "value": {"length": 30, "unit": "cm"}},
        {"ref": "const.pi", "value": 3.14},
        {"ref": "rel.hexagon_inscribed", "value": True},
        {"ref": "rel.hexagon_side_equals_radius", "value": True},
    ],
    "target": {
        "ref": "answer.target",
        "type": "perimeter_difference",
    },
    "method": "compare_circle_and_inscribed_hexagon_perimeters",
    "plan": [
        "ចែកអង្កត់ផ្ចិតរង្វង់ 30cm នឹង 2 ដើម្បីរកកាំ 15cm។",
        "ជ្រុងមួយនៃឆកោនទៀងទាត់ដែលចារឹកក្នុងរង្វង់ស្មើនឹងកាំរង្វង់ ដូច្នេះវាមានប្រវែង 15cm។",
        "គណនាបរិមាត្ររង្វង់ និងបរិមាត្រឆកោនទៀងទាត់ដោយឡែកពីគ្នា។",
        "ដកបរិមាត្រឆកោនទៀងទាត់ចេញពីបរិមាត្ររង្វង់ ដើម្បីរកផលខុសគ្នា។",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "30 ÷ 2",
            "value": {"result": 15, "meaning": "កាំរង្វង់", "unit": "cm"},
            "explanation": "បើចែកអង្កត់ផ្ចិត 30cm នឹង 2 នោះកាំស្មើ 15cm។",
        },
        {
            "id": "step.2",
            "expr": "ជ្រុងមួយនៃឆកោនទៀងទាត់ = កាំរង្វង់",
            "value": {"result": 15, "meaning": "ជ្រុងមួយនៃឆកោនទៀងទាត់", "unit": "cm"},
            "explanation": "ជ្រុងមួយនៃឆកោនទៀងទាត់ដែលចារឹកក្នុងរង្វង់ស្មើនឹងកាំរង្វង់។",
        },
        {
            "id": "step.3",
            "expr": "30 × 3.14",
            "value": {"result": 94.2, "meaning": "បរិមាត្ររង្វង់", "unit": "cm"},
            "explanation": "បរិមាត្ររង្វង់គឺអង្កត់ផ្ចិតគុណនឹងតម្លៃ π ដូច្នេះស្មើ 94.2cm។",
        },
        {
            "id": "step.4",
            "expr": "15 × 6",
            "value": {"result": 90, "meaning": "បរិមាត្រឆកោនទៀងទាត់", "unit": "cm"},
            "explanation": "ឆកោនទៀងទាត់មាន 6 ជ្រុង ដូច្នេះបរិមាត្ររបស់វាស្មើ 90cm។",
        },
        {
            "id": "step.5",
            "expr": "94.2 - 90",
            "value": {
                "result": 4.2,
                "meaning": "ផលខុសគ្នារវាងបរិមាត្ររង្វង់ និងឆកោនទៀងទាត់",
                "unit": "cm",
            },
            "explanation": "ដកបរិមាត្រឆកោនទៀងទាត់ 90cm ចេញពីបរិមាត្ររង្វង់ 94.2cm នោះបាន 4.2cm។",
        },
    ],
    "checks": [
        {"id": "check.1", "expr": "15 × 2", "expected": 30, "actual": 30, "pass": True},
        {"id": "check.2", "expr": "15 × 6", "expected": 90, "actual": 90, "pass": True},
        {"id": "check.3", "expr": "30 × 3.14", "expected": 94.2, "actual": 94.2, "pass": True},
        {"id": "check.4", "expr": "94.2 - 90", "expected": 4.2, "actual": 4.2, "pass": True},
    ],
    "answer": ANSWER,
}
