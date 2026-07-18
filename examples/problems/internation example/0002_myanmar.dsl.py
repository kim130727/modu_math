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

PROBLEM_ID = "စက်ဝိုင်းနှင့်ပုံမှန်ဆဋ္ဌဂံပတ်လည်အလျားကွာခြားချက်_၀၀၁"
PROBLEM_TITLE = "စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်"


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
                text="ညာဘက်ရှိ ပုံတွင် စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်သည် စင်တီမီတာ မည်မျှဖြစ်သနည်း။ (π တန်ဖိုး: 3.14)",
                prompt="စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်ကို မေးသော ပုစ္ဆာ",
                semantic_role="question",
                x=15,
                y=18,
                width=656,
                height=91,
                font_size=22,
                line_height=1.25,
                fill="#111111",
                align="left",
            ),
            # စက်ဝိုင်း: အချင်း 30cm၊ အချင်းဝက် 15cm
            CircleSlot(
                id="slot.circle",
                prompt="အချင်း 30cm ရှိသော စက်ဝိုင်း",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # စက်ဝိုင်းအတွင်း ထိစပ်ရေးဆွဲထားသော ပုံမှန်ဆဋ္ဌဂံ
            # ဗဟိုချက် (565, 225)၊ အချင်းဝက် 100px
            # ထောင့်မှတ်များ: 0°, 60°, 120°, 180°, 240°, 300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="စက်ဝိုင်းအတွင်း ထိစပ်ရေးဆွဲထားသော ပုံမှန်ဆဋ္ဌဂံ",
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
            # ပုံမှန်ဆဋ္ဌဂံ၏ မျက်နှာချင်းဆိုင် ထောင့်မှတ်နှစ်ခုကို ဆက်ထားသော အချင်း
            LineSlot(
                id="slot.diameter_line",
                prompt="စက်ဝိုင်း၏ အချင်း 30cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="စက်ဝိုင်း၏ ဗဟိုချက်",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="အချင်းအလျား ပြသချက်",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်",
                answer_key="4.2cm",
                placeholder="အဖြေ",
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
        "language": "my",
        "question": (
            "ညာဘက်ရှိ ပုံတွင် စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်သည် "
            "စင်တီမီတာ မည်မျှဖြစ်သနည်း။ (π တန်ဖိုး: 3.14)"
        ),
        "instruction": (
            "စက်ဝိုင်း၏ အချင်းမှ အချင်းဝက်ကို ရှာပြီး၊ စက်ဝိုင်းအတွင်း ထိစပ်ရေးဆွဲထားသော ပုံမှန်ဆဋ္ဌဂံ၏ "
            "အနားတစ်ဖက်၏ အလျားသည် စက်ဝိုင်း၏ အချင်းဝက်နှင့် တူညီသည်ကို အသုံးပြုပါ။"
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "စက်ဝိုင်း",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "ပုံမှန်ဆဋ္ဌဂံ",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "စက်ဝိုင်း၏ ဗဟိုချက်",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "စက်ဝိုင်း၏ အချင်း",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "π တန်ဖိုး",
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
            "description": "စက်ဝိုင်း၏ ပတ်လည်အလျားမှ ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျားကို နုတ်ထားသော တန်ဖိုး",
        },
        "value": 4.2,
        "unit": "cm",
    },
}


# Editor-build compatibility payload. The visual layout above is authored; this
# block keeps generated ids and answer/solvable shapes aligned with schemas.
PROBLEM_ID = "အတန်း၆_၂_စက်ဝိုင်းဧရိယာ_၀၀၀၂"
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
        "description": "စက်ဝိုင်း၏ ပတ်လည်အလျားမှ ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျားကို နုတ်ထားသော တန်ဖိုး",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {'schema': 'modu.solvable.v1.2',
 'problem_id': 'အတန်း၆_၂_စက်ဝိုင်းဧရိယာ_၀၀၀၂',
 'problem_type': 'numeric_answer_perimeter_difference',
 'inputs': {'diameter': 30,
            'pi': 3.14,
            'polygon_sides': 6,
            'target_label': 'စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်',
            'unit': 'cm'},
 'given': [{'ref': 'measure.diameter', 'value': {'length': 30, 'unit': 'cm'}},
           {'ref': 'const.pi', 'value': 3.14},
           {'ref': 'rel.hexagon_inscribed', 'value': True},
           {'ref': 'rel.hexagon_side_equals_radius', 'value': True}],
 'target': {'ref': 'answer.target', 'type': 'perimeter_difference'},
 'method': 'compare_circle_and_inscribed_hexagon_perimeters',
 'plan': ['စက်ဝိုင်း၏ အချင်း 30cm ကို 2 ဖြင့်စား၍ အချင်းဝက် 15cm ကို ရှာပါ။',
          'စက်ဝိုင်းအတွင်း ထိစပ်ရေးဆွဲထားသော ပုံမှန်ဆဋ္ဌဂံ၏ အနားတစ်ဖက်သည် စက်ဝိုင်း၏ '
          'အချင်းဝက်နှင့် တူသောကြောင့် 15cm ဖြစ်သည်။',
          'စက်ဝိုင်း၏ ပတ်လည်အလျားနှင့် ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျားကို သီးခြားစီ ရှာပါ။',
          'စက်ဝိုင်း၏ ပတ်လည်အလျားမှ ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျားကို နုတ်၍ ကွာခြားချက်ကို ရှာပါ။'],
 'steps': [{'id': 'step.1',
            'expr': '30 ÷ 2',
            'value': {'result': 15, 'meaning': 'စက်ဝိုင်း၏ အချင်းဝက်', 'unit': 'cm'},
            'explanation': 'အချင်း 30cm ကို 2 ဖြင့်စားလျှင် အချင်းဝက်သည် 15cm ဖြစ်သည်။'},
           {'id': 'step.2',
            'expr': 'ပုံမှန်ဆဋ္ဌဂံ၏ အနားတစ်ဖက် = စက်ဝိုင်း၏ အချင်းဝက်',
            'value': {'result': 15, 'meaning': 'ပုံမှန်ဆဋ္ဌဂံ၏ အနားတစ်ဖက်', 'unit': 'cm'},
            'explanation': 'စက်ဝိုင်းအတွင်း ထိစပ်ရေးဆွဲထားသော ပုံမှန်ဆဋ္ဌဂံ၏ အနားတစ်ဖက်သည် '
                           'စက်ဝိုင်း၏ အချင်းဝက်နှင့် တူညီသည်။'},
           {'id': 'step.3',
            'expr': '30 × 3.14',
            'value': {'result': 94.2, 'meaning': 'စက်ဝိုင်း၏ ပတ်လည်အလျား', 'unit': 'cm'},
            'explanation': 'စက်ဝိုင်း၏ ပတ်လည်အလျားသည် အချင်းကို π တန်ဖိုးဖြင့် မြှောက်၍ 94.2cm '
                           'ဖြစ်သည်။'},
           {'id': 'step.4',
            'expr': '15 × 6',
            'value': {'result': 90, 'meaning': 'ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျား', 'unit': 'cm'},
            'explanation': 'ပုံမှန်ဆဋ္ဌဂံတွင် အနား 6 ဖက်ရှိသောကြောင့် ပတ်လည်အလျားသည် 90cm '
                           'ဖြစ်သည်။'},
           {'id': 'step.5',
            'expr': '94.2 - 90',
            'value': {'result': 4.2,
                      'meaning': 'စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက်',
                      'unit': 'cm'},
            'explanation': 'စက်ဝိုင်း၏ ပတ်လည်အလျား 94.2cm မှ ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျား 90cm ကို '
                           'နုတ်လျှင် 4.2cm ဖြစ်သည်။'}],
 'checks': [{'id': 'check.1', 'expr': '15 × 2', 'expected': 30, 'actual': 30, 'pass': True},
            {'id': 'check.2', 'expr': '15 × 6', 'expected': 90, 'actual': 90, 'pass': True},
            {'id': 'check.3', 'expr': '30 × 3.14', 'expected': 94.2, 'actual': 94.2, 'pass': True},
            {'id': 'check.4', 'expr': '94.2 - 90', 'expected': 4.2, 'actual': 4.2, 'pass': True}],
 'answer': {'blanks': [{'id': 'slot.answer', 'type': 'number', 'value': 4.2, 'unit': 'cm'}],
            'choices': [],
            'answer_key': [{'blank_id': 'slot.answer', 'value': 4.2, 'unit': 'cm'}],
            'target': {'type': 'perimeter_difference',
                       'description': 'စက်ဝိုင်း၏ ပတ်လည်အလျားမှ ပုံမှန်ဆဋ္ဌဂံ၏ ပတ်လည်အလျားကို '
                                      'နုတ်ထားသော တန်ဖိုး'},
            'value': 4.2,
            'unit': 'cm'},
 'understanding': {'summary': 'Find စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား ကွာခြားချက် '
                              'using the given information.',
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
                                 'label': 'စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ ပတ်လည်အလျား '
                                          'ကွာခြားချက်',
                                 'unit': 'cm',
                                 'source': 'unknown'}],
                   'relation': {'type': 'compare_circle_and_inscribed_hexagon_perimeters',
                                'statement': 'စက်ဝိုင်း၏ အချင်း 30cm ကို 2 ဖြင့်စား၍ အချင်းဝက် '
                                             '15cm ကို ရှာပါ။',
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
                                                         'စက်ဝိုင်းနှင့် ပုံမှန်ဆဋ္ဌဂံတို့၏ '
                                                         'ပတ်လည်အလျား ကွာခြားချက်'],
                                             'answer_index': 2}]}}
