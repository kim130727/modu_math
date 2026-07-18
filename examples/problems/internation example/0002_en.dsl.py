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

PROBLEM_ID = "circle_hexagon_perimeter_difference_001"
PROBLEM_TITLE = "Difference between the circle's circumference and the regular hexagon's perimeter"


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
                text="In the figure on the right, what is the difference, in centimeters, between the circumference of the circle and the perimeter of the regular hexagon? (Use 3.14 for pi.)",
                prompt="A problem asking for the difference between the circumference of a circle and the perimeter of a regular hexagon",
                semantic_role="question",
                x=15,
                y=18,
                width=656,
                height=118,
                font_size=22,
                line_height=1.25,
                fill="#111111",
                align="left",
            ),
            # Circle: diameter 30 cm, radius 15 cm
            CircleSlot(
                id="slot.circle",
                prompt="A circle with a diameter of 30 cm",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # A regular hexagon inscribed in the circle
            # Center (565, 225), radius 100 px
            # Vertices: 0°, 60°, 120°, 180°, 240°, 300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="A regular hexagon inscribed in the circle",
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
            # A diameter connecting opposite vertices of the regular hexagon
            LineSlot(
                id="slot.diameter_line",
                prompt="The circle's diameter is 30 cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="Center of the circle",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="Diameter length label",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="Difference between the circle's circumference and the regular hexagon's perimeter",
                answer_key="4.2cm",
                placeholder="Answer",
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
        "language": "en",
        "question": (
            "In the figure on the right, what is the difference, in centimeters, "
            "between the circumference of the circle and the perimeter of the regular hexagon? "
            "(Use 3.14 for pi.)"
        ),
        "instruction": (
            "Find the radius from the circle's diameter, and use the fact that "
            "each side of a regular hexagon inscribed in a circle is equal to the circle's radius."
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "circle",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "regular hexagon",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "Center of the circle",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "diameter of the circle",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "pi",
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
            "description": "The circle's circumference minus the regular hexagon's perimeter",
        },
        "value": 4.2,
        "unit": "cm",
    },
}


# Editor-build compatibility payload. The visual layout above is authored; this
# block keeps generated ids and answer/solvable shapes aligned with schemas.
PROBLEM_ID = "grade6_circle_hexagon_perimeter_difference_0002"
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
        "description": "The circle's circumference minus the regular hexagon's perimeter",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {'schema': 'modu.solvable.v1.2',
 'problem_id': 'grade6_circle_hexagon_perimeter_difference_0002',
 'problem_type': 'numeric_answer_perimeter_difference',
 'inputs': {'diameter': 30,
            'pi': 3.14,
            'polygon_sides': 6,
            'target_label': "Difference between the circle's circumference and the regular "
                            "hexagon's perimeter",
            'unit': 'cm'},
 'given': [{'ref': 'measure.diameter', 'value': {'length': 30, 'unit': 'cm'}},
           {'ref': 'const.pi', 'value': 3.14},
           {'ref': 'rel.hexagon_inscribed', 'value': True},
           {'ref': 'rel.hexagon_side_equals_radius', 'value': True}],
 'target': {'ref': 'answer.target', 'type': 'perimeter_difference'},
 'method': 'compare_circle_and_inscribed_hexagon_perimeters',
 'plan': ['Divide the 30 cm diameter by 2 to find the 15 cm radius.',
          "Each side of a regular hexagon inscribed in a circle equals the circle's radius, so it "
          'is 15 cm.',
          "Find the circle's circumference and the regular hexagon's perimeter.",
          "Subtract the regular hexagon's perimeter from the circle's circumference."],
 'steps': [{'id': 'step.1',
            'expr': '30 ÷ 2',
            'value': {'result': 15, 'meaning': 'radius of the circle', 'unit': 'cm'},
            'explanation': 'Dividing the 30 cm diameter by 2 gives a radius of 15 cm.'},
           {'id': 'step.2',
            'expr': 'one side of the regular hexagon = radius of the circle',
            'value': {'result': 15, 'meaning': 'one side of the regular hexagon', 'unit': 'cm'},
            'explanation': 'Each side of a regular hexagon inscribed in a circle equals the '
                           "circle's radius."},
           {'id': 'step.3',
            'expr': '30 × 3.14',
            'value': {'result': 94.2, 'meaning': 'circumference of the circle', 'unit': 'cm'},
            'explanation': "The circle's circumference is 94.2 cm because the diameter is "
                           'multiplied by pi.'},
           {'id': 'step.4',
            'expr': '15 × 6',
            'value': {'result': 90, 'meaning': 'perimeter of the regular hexagon', 'unit': 'cm'},
            'explanation': 'A regular hexagon has 6 sides, so its perimeter is 90 cm.'},
           {'id': 'step.5',
            'expr': '94.2 - 90',
            'value': {'result': 4.2,
                      'meaning': "Difference between the circle's circumference and the regular "
                                 "hexagon's perimeter",
                      'unit': 'cm'},
            'explanation': "Subtracting the regular hexagon's perimeter of 90 cm from the circle's "
                           'circumference of 94.2 cm gives 4.2 cm.'}],
 'checks': [{'id': 'check.1', 'expr': '15 × 2', 'expected': 30, 'actual': 30, 'pass': True},
            {'id': 'check.2', 'expr': '15 × 6', 'expected': 90, 'actual': 90, 'pass': True},
            {'id': 'check.3', 'expr': '30 × 3.14', 'expected': 94.2, 'actual': 94.2, 'pass': True},
            {'id': 'check.4', 'expr': '94.2 - 90', 'expected': 4.2, 'actual': 4.2, 'pass': True}],
 'answer': {'blanks': [{'id': 'slot.answer', 'type': 'number', 'value': 4.2, 'unit': 'cm'}],
            'choices': [],
            'answer_key': [{'blank_id': 'slot.answer', 'value': 4.2, 'unit': 'cm'}],
            'target': {'type': 'perimeter_difference',
                       'description': "The circle's circumference minus the regular hexagon's "
                                      'perimeter'},
            'value': 4.2,
            'unit': 'cm'},
 'understanding': {'summary': "Find Difference between the circle's circumference and the regular "
                              "hexagon's perimeter using the given information.",
                   'facts': [{'ref': 'measure.diameter',
                              'label': 'diameter',
                              'value': 30,
                              'unit': 'cm',
                              'source': 'explicit'},
                             {'ref': 'const.pi',
                              'label': 'pi',
                              'value': 3.14,
                              'unit': 'cm',
                              'source': 'explicit'},
                             {'ref': 'rel.hexagon_inscribed',
                              'label': 'hexagon inscribed',
                              'value': True,
                              'unit': 'cm',
                              'source': 'explicit'},
                             {'ref': 'rel.hexagon_side_equals_radius',
                              'label': 'hexagon side equals radius',
                              'value': True,
                              'unit': 'cm',
                              'source': 'explicit'}],
                   'unknowns': [{'ref': 'answer.target',
                                 'label': "Difference between the circle's circumference and the "
                                          "regular hexagon's perimeter",
                                 'unit': 'cm',
                                 'source': 'unknown'}],
                   'relation': {'type': 'compare_circle_and_inscribed_hexagon_perimeters',
                                'statement': 'Divide the 30 cm diameter by 2 to find the 15 cm '
                                             'radius.',
                                'symbolic': '30 ÷ 2',
                                'uses': ['measure.diameter',
                                         'const.pi',
                                         'rel.hexagon_inscribed',
                                         'rel.hexagon_side_equals_radius'],
                                'result': 'answer.target'},
                   'diagnostic_questions': [{'id': 'understand.target',
                                             'type': 'multiple_choice',
                                             'prompt': 'What should we find?',
                                             'choices': ['diameter',
                                                         'pi',
                                                         "Difference between the circle's "
                                                         "circumference and the regular hexagon's "
                                                         'perimeter'],
                                             'answer_index': 2}]}}
