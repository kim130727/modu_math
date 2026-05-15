from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, fraction_slots


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=680,
        height=315,
        coordinate_mode="logical",
    )

    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=(
                "slot.l1.pre",
                "slot.l1.frac.num",
                "slot.l1.frac.bar",
                "slot.l1.frac.den",
                "slot.l1.post",
                "slot.l2.pre",
                "slot.l2.frac.num",
                "slot.l2.frac.bar",
                "slot.l2.frac.den",
                "slot.l2.post",
                "slot.l3",
                "slot.l4",
            ),
        ),
    )

    slots = (
        TextSlot(
            id="slot.l1.pre",
            prompt="",
            text="하트 모양 한 개를 만드는 데 철사가",
            style_role="body",
            x=4.0,
            y=52.0,
            font_size=35,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.l1.frac",
            numerator="3",
            denominator="16",
            x=556.0,
            numerator_y=26.0,
            bar_y=42.0,
            denominator_y=78.0,
            bar_width=44.0,
            font_size=35,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.0,
        ),
        TextSlot(
            id="slot.l1.post",
            prompt="",
            text="m",
            style_role="body",
            x=590.0,
            y=52.0,
            font_size=35,
            fill="#222222",
        ),
        TextSlot(
            id="slot.l2.pre",
            prompt="",
            text="필요합니다. 철사",
            style_role="body",
            x=4.0,
            y=143.0,
            font_size=35,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.l2.frac",
            numerator="15",
            denominator="16",
            x=292.0,
            numerator_y=111.0,
            bar_y=128.0,
            denominator_y=166.0,
            bar_width=58.0,
            font_size=35,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.0,
        ),
        TextSlot(
            id="slot.l2.post",
            prompt="",
            text="m로 만들 수 있는 하트",
            style_role="body",
            x=330.0,
            y=143.0,
            font_size=35,
            fill="#222222",
        ),
        TextSlot(
            id="slot.l3",
            prompt="",
            text="모양은 몇 개인지 풀이 과정을 쓰고 답을 구해",
            style_role="body",
            x=4.0,
            y=223.0,
            font_size=35,
            fill="#222222",
        ),
        TextSlot(
            id="slot.l4",
            prompt="",
            text="보시오.",
            style_role="body",
            x=4.0,
            y=299.0,
            font_size=35,
            fill="#222222",
        ),
    )

    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="msedge_ntxZ4waQ7n",
        title="",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_015',
    'problem_type': 'word_problem',
    'metadata': {   'language': 'ko',
                    'question': '철사 15/16 m로 만들 수 있는 하트 모양은 몇 개인지',
                    'instruction': '하트 모양 한 개를 만드는 데 철사가 3/16 m 필요합니다. 철사 15/16 m로 만들 수 있는 하트 모양은 '
                                   '몇 개인지 풀이 과정을 쓰고 답을 구해보시오.'},
    'domain': {   'objects': [   {   'id': 'o1',
                                     'type': 'question',
                                     'text': '철사 15/16 m로 만들 수 있는 하트 모양은 몇 개인지'},
                                 {'id': 'o2', 'type': 'fraction', 'value': '3/16', 'text': '3/16'},
                                 {'id': 'o3', 'type': 'unit', 'value': 'm', 'text': 'm'},
                                 {   'id': 'o4',
                                     'type': 'fraction',
                                     'value': '15/16',
                                     'text': '15/16'},
                                 {'id': 'o5', 'type': 'unknown', 'text': '하트 모양'},
                                 {'id': 'o6', 'type': 'unknown', 'text': '철사'},
                                 {'id': 'o7', 'type': 'instruction', 'text': '풀이 과정을 쓰고 답을 구해보시오'}],
                  'relations': [   {   'id': 'r1',
                                       'type': 'applies_to',
                                       'from_id': 'o2',
                                       'to_id': 'o5'},
                                   {   'id': 'r2',
                                       'type': 'references',
                                       'from_id': 'o4',
                                       'to_id': 'o6'},
                                   {'id': 'r3', 'type': 'asks_for', 'from_id': 'o1', 'to_id': 'o5'},
                                   {   'id': 'r4',
                                       'type': 'contains',
                                       'from_id': 'o7',
                                       'to_id': 'o1'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 5, 'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_015',
    'problem_type': 'word_problem',
    'inputs': {   'total_ticks': 5,
                  'target_label': '정답',
                  'target_ticks': 5,
                  'target_count': 5,
                  'unit': ''},
    'plan': ['15/16 ÷ 3/16 = 5 이므로 하트 모양은 5개입니다.'],
    'steps': [{'id': 'step.1', 'expr': '15/16 ÷ 3/16 = 5 이므로 하트 모양은 5개입니다.', 'value': 5}],
    'checks': [],
    'answer': {'value': 5, 'unit': ''}}
