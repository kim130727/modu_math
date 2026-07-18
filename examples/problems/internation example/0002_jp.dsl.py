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

PROBLEM_ID = "小6_円と正六角形の周りの長さの差_0002"
PROBLEM_TITLE = "円周と正六角形の周りの長さの差"


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
                    "konva_1783908403385_paste_1136183_0",
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
                text="右の図で、円周と正六角形の周りの長さの差は何cmですか。",
                prompt="円周と正六角形の周りの長さの差を求める問題",
                semantic_role="question",
                x=15,
                y=18,
                width=656,
                height=36,
                font_size=22,
                line_height=1.25,
                fill="#111111",
                align="left",
            ),
            # 円：直径30cm、半径15cm
            CircleSlot(
                id="slot.circle",
                prompt="直径が30cmの円",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # 円に内接する正六角形
            # 中心 (565, 225)、半径100px
            # 頂点：0°、60°、120°、180°、240°、300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="円に内接する正六角形",
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
            # 正六角形の向かい合う頂点を結ぶ直径
            LineSlot(
                id="slot.diameter_line",
                prompt="円の直径は30cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="円の中心",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="直径の長さの表示",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="円周と正六角形の周りの長さの差",
                answer_key="4.2cm",
                placeholder="答え",
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
            TextBoxSlot(
                id="konva_1783908403385_paste_1136183_0",
                prompt="",
                text="(円周率は3.14とします。）",
                x=14.008,
                y=54.006,
                font_size=22,
                fill="#111111",
                width=656,
                height=36,
                align="left",
                line_height=1.25,
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
        "language": "ja",
        "question": (
            "右の図で、円周と正六角形の周りの長さの差は" "何cmですか。" "（円周率は3.14とします。）"
        ),
        "instruction": (
            "円の直径から半径を求め、円に内接する正六角形の"
            "1辺の長さが円の半径と等しいことを利用します。"
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "円",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "正六角形",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "円の中心",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "円の直径",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "円周率",
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
            "description": "円周から正六角形の周りの長さを引いた値",
        },
        "value": 4.2,
        "unit": "cm",
    },
}


# エディタービルド互換用のデータです。上の図の配置は作成済みであり、この
# ブロックで生成IDとanswer/solvableの構造をスキーマに合わせます。
PROBLEM_ID = "小6_円と正六角形の周りの長さの差_0002"
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
        "description": "円周から正六角形の周りの長さを引いた値",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {'schema': 'modu.solvable.v1.2',
 'problem_id': '小6_円と正六角形の周りの長さの差_0002',
 'problem_type': 'numeric_answer_perimeter_difference',
 'inputs': {'diameter': 30,
            'pi': 3.14,
            'polygon_sides': 6,
            'target_label': '円周と正六角形の周りの長さの差',
            'unit': 'cm'},
 'given': [{'ref': 'measure.diameter', 'value': {'length': 30, 'unit': 'cm'}},
           {'ref': 'const.pi', 'value': 3.14},
           {'ref': 'rel.hexagon_inscribed', 'value': True},
           {'ref': 'rel.hexagon_side_equals_radius', 'value': True}],
 'target': {'ref': 'answer.target', 'type': 'perimeter_difference'},
 'method': 'compare_circle_and_inscribed_hexagon_perimeters',
 'plan': ['直径30cmを2で割って、半径15cmを求めます。',
          '円に内接する正六角形の1辺は円の半径と等しいので、15cmです。',
          '円周と正六角形の周りの長さをそれぞれ求めます。',
          '円周から正六角形の周りの長さを引きます。'],
 'steps': [{'id': 'step.1',
            'expr': '30 ÷ 2',
            'value': {'result': 15, 'meaning': '円の半径', 'unit': 'cm'},
            'explanation': '直径30cmを2で割ると、半径は15cmです。'},
           {'id': 'step.2',
            'expr': '正六角形の1辺 = 円の半径',
            'value': {'result': 15, 'meaning': '正六角形の1辺', 'unit': 'cm'},
            'explanation': '円に内接する正六角形の1辺は、円の半径と等しくなります。'},
           {'id': 'step.3',
            'expr': '30 × 3.14',
            'value': {'result': 94.2, 'meaning': '円周', 'unit': 'cm'},
            'explanation': '円周は、直径に円周率を掛けるので94.2cmです。'},
           {'id': 'step.4',
            'expr': '15 × 6',
            'value': {'result': 90, 'meaning': '正六角形の周りの長さ', 'unit': 'cm'},
            'explanation': '正六角形には辺が6本あるので、周りの長さは90cmです。'},
           {'id': 'step.5',
            'expr': '94.2 - 90',
            'value': {'result': 4.2, 'meaning': '円周と正六角形の周りの長さの差', 'unit': 'cm'},
            'explanation': '円周94.2cmから正六角形の周りの長さ90cmを引くと、4.2cmです。'}],
 'checks': [{'id': 'check.1', 'expr': '15 × 2', 'expected': 30, 'actual': 30, 'pass': True},
            {'id': 'check.2', 'expr': '15 × 6', 'expected': 90, 'actual': 90, 'pass': True},
            {'id': 'check.3', 'expr': '30 × 3.14', 'expected': 94.2, 'actual': 94.2, 'pass': True},
            {'id': 'check.4', 'expr': '94.2 - 90', 'expected': 4.2, 'actual': 4.2, 'pass': True}],
 'answer': {'blanks': [{'id': 'slot.answer', 'type': 'number', 'value': 4.2, 'unit': 'cm'}],
            'choices': [],
            'answer_key': [{'blank_id': 'slot.answer', 'value': 4.2, 'unit': 'cm'}],
            'target': {'type': 'perimeter_difference', 'description': '円周から正六角形の周りの長さを引いた値'},
            'value': 4.2,
            'unit': 'cm'},
 'understanding': {'summary': 'Find 円周と正六角形の周りの長さの差 using the given information.',
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
                                 'label': '円周と正六角形の周りの長さの差',
                                 'unit': 'cm',
                                 'source': 'unknown'}],
                   'relation': {'type': 'compare_circle_and_inscribed_hexagon_perimeters',
                                'statement': '直径30cmを2で割って、半径15cmを求めます。',
                                'symbolic': '30 ÷ 2',
                                'uses': ['measure.diameter',
                                         'const.pi',
                                         'rel.hexagon_inscribed',
                                         'rel.hexagon_side_equals_radius'],
                                'result': 'answer.target'},
                   'diagnostic_questions': [{'id': 'understand.target',
                                             'type': 'multiple_choice',
                                             'prompt': 'What should we find?',
                                             'choices': ['diameter', 'pi', '円周と正六角形の周りの長さの差'],
                                             'answer_index': 2}]}}
