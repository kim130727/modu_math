from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, fraction_slots


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=694,
        height=305,
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
            text="영재네 반 학생들에게 찰흙",
            style_role="body",
            x=10.0,
            y=54.0,
            font_size=35,
            fill="#2a2728",
        ),
        *fraction_slots(
            id_prefix="slot.l1.frac",
            numerator="7",
            denominator="2",
            x=434.0,
            numerator_y=34.0,
            bar_y=49.0,
            denominator_y=86.0,
            bar_width=38.0,
            font_size=35,
            fill="#2a2728",
            stroke="#2a2728",
            stroke_width=2.1,
        ),
        TextSlot(
            id="slot.l1.post",
            prompt="",
            text="kg을 똑같이",
            style_role="body",
            x=475.0,
            y=54.0,
            font_size=35,
            fill="#2a2728",
        ),
        TextSlot(
            id="slot.l2.pre",
            prompt="",
            text="나누어 주었더니 한 사람이",
            style_role="body",
            x=10.0,
            y=134.0,
            font_size=35,
            fill="#2a2728",
        ),
        *fraction_slots(
            id_prefix="slot.l2.frac",
            numerator="1",
            denominator="4",
            x=444.0,
            numerator_y=112.0,
            bar_y=127.0,
            denominator_y=164.0,
            bar_width=38.0,
            font_size=35,
            fill="#2a2728",
            stroke="#2a2728",
            stroke_width=2.1,
        ),
        TextSlot(
            id="slot.l2.post",
            prompt="",
            text="kg씩 가지게",
            style_role="body",
            x=485.0,
            y=134.0,
            font_size=35,
            fill="#2a2728",
        ),
        TextSlot(
            id="slot.l3",
            prompt="",
            text="되었습니다. 찰흙을 몇 명에게 나누어 주었습",
            style_role="body",
            x=10.0,
            y=214.0,
            font_size=35,
            fill="#2a2728",
        ),
        TextSlot(
            id="slot.l4",
            prompt="",
            text="니까?",
            style_role="body",
            x=10.0,
            y=284.0,
            font_size=35,
            fill="#2a2728",
        ),
    )

    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="msedge_mvG3o5s2c5",
        title="",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_011',
    'problem_type': 'word_problem',
    'metadata': {   'language': 'ko',
                    'question': '찰흙을 몇 명에게 나누어 주었습니까?',
                    'instruction': '영재네 반 학생들에게 찰흙 7/2 kg을 똑같이 나누어 주었더니 한 사람이 1/4 kg씩 가지게 되었습니다. '
                                   '찰흙을 몇 명에게 나누어 주었습니까?'},
    'domain': {   'objects': [   {   'id': 'o1',
                                     'type': 'instruction',
                                     'text': '영재네 반 학생들에게 찰흙 7/2 kg을 똑같이 나누어 주었더니 한 사람이 1/4 kg씩 '
                                             '가지게 되었습니다.'},
                                 {'id': 'o2', 'type': 'question', 'text': '찰흙을 몇 명에게 나누어 주었습니까?'},
                                 {'id': 'o3', 'type': 'fraction', 'value': '7/2', 'text': '7/2'},
                                 {'id': 'o4', 'type': 'fraction', 'value': '1/4', 'text': '1/4'},
                                 {'id': 'o5', 'type': 'unit', 'value': 'kg', 'text': 'kg'},
                                 {'id': 'o6', 'type': 'unknown', 'text': '학생'}],
                  'relations': [   {'id': 'r1', 'type': 'asks_for', 'from_id': 'o2', 'to_id': 'o6'},
                                   {   'id': 'r2',
                                       'type': 'applies_to',
                                       'from_id': 'o3',
                                       'to_id': 'o5'},
                                   {   'id': 'r3',
                                       'type': 'applies_to',
                                       'from_id': 'o4',
                                       'to_id': 'o5'},
                                   {   'id': 'r4',
                                       'type': 'depends_on',
                                       'from_id': 'o2',
                                       'to_id': 'o3'},
                                   {   'id': 'r5',
                                       'type': 'depends_on',
                                       'from_id': 'o2',
                                       'to_id': 'o4'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 14, 'unit': '명'}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_011',
    'problem_type': 'word_problem',
    'inputs': {   'total_ticks': 14,
                  'target_label': '정답',
                  'target_ticks': 14,
                  'target_count': 14,
                  'unit': '명'},
    'plan': ['전체 7/2 kg을 한 사람당 1/4 kg씩 나누면 7/2 ÷ 1/4 = 14이므로 14명입니다.'],
    'steps': [   {   'id': 'step.1',
                     'expr': '전체 7/2 kg을 한 사람당 1/4 kg씩 나누면 7/2 ÷ 1/4 = 14이므로 14명입니다.',
                     'value': 14}],
    'checks': [],
    'answer': {'value': 14, 'unit': '명'}}
