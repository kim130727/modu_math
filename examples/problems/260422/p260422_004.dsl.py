from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    fraction_slots,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=726,
        height=618,
        coordinate_mode="logical",
    )

    segments = 8
    bar_x = 60.0
    bar_y = 198.0
    bar_w = 600.0
    bar_h = 44.0
    step = bar_w / segments

    slot_ids = [
        "slot.title.text",
        "slot.title.blank",
        "slot.bar.outer",
        "slot.bar.filled",
        "slot.num.0",
        "slot.num.1",
        "slot.num.2",
        "slot.num.3",
        "slot.num.4",
        "slot.tick.1",
        "slot.tick.2",
        "slot.tick.3",
        "slot.tick.4",
        "slot.tick.5",
        "slot.tick.6",
        "slot.tick.7",
        "slot.arc.0",
        "slot.arc.1",
        "slot.arc.2",
        "slot.arc.3",
        "slot.arc.4",
        "slot.label.zero",
        "slot.label.one",
        "slot.exp.left.num",
        "slot.exp.left.bar",
        "slot.exp.left.den",
        "slot.exp.text.1",
        "slot.exp.mid.num",
        "slot.exp.mid.bar",
        "slot.exp.mid.den",
        "slot.exp.text.2",
        "slot.exp.blank",
        "slot.exp.text.3",
        "slot.eq.left.num",
        "slot.eq.left.bar",
        "slot.eq.left.den",
        "slot.eq.divide",
        "slot.eq.mid.num",
        "slot.eq.mid.bar",
        "slot.eq.mid.den",
        "slot.eq.equal",
        "slot.eq.blank",
    ]
    slot_ids.extend(
        [
            "slot.topfrac.0.num",
            "slot.topfrac.0.bar",
            "slot.topfrac.0.den",
            "slot.topfrac.1.num",
            "slot.topfrac.1.bar",
            "slot.topfrac.1.den",
            "slot.topfrac.2.num",
            "slot.topfrac.2.bar",
            "slot.topfrac.2.den",
            "slot.topfrac.3.num",
            "slot.topfrac.3.bar",
            "slot.topfrac.3.den",
            "slot.topfrac.4.num",
            "slot.topfrac.4.bar",
            "slot.topfrac.4.den",
        ]
    )

    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=tuple(slot_ids),
        ),
    )

    top_fractions = []
    for idx in range(5):
        center = bar_x + (idx + 0.5) * step
        top_fractions.extend(
            fraction_slots(
                id_prefix=f"slot.topfrac.{idx}",
                numerator="1",
                denominator="8",
                x=center,
                numerator_y=136.0,
                bar_y=144.0,
                denominator_y=176.0,
                bar_width=44.0,
                font_size=30,
                fill="#222222",
                stroke="#222222",
                stroke_width=2.2,
            )
        )

    ticks = []
    for idx in range(1, segments):
        x = bar_x + step * idx
        ticks.append(
            LineSlot(
                id=f"slot.tick.{idx}",
                prompt="",
                x1=x,
                y1=bar_y,
                x2=x,
                y2=bar_y + bar_h,
                stroke="#444444",
                stroke_width=1.2,
                stroke_dasharray="6 4",
            )
        )

    arcs = []
    for idx in range(5):
        x1 = bar_x + step * idx + 2.0
        x2 = bar_x + step * (idx + 1) - 2.0
        y = bar_y - 2.0
        # Dashed semicircle-like arc for each 1/8 partition marker.
        d = f"M {x1} {y} Q {(x1 + x2) / 2:.1f} {y - 34.0} {x2} {y}"
        arcs.append(
            PathSlot(
                id=f"slot.arc.{idx}",
                prompt="",
                d=d,
                stroke="#555555",
                stroke_width=1.1,
                stroke_dasharray="6 4",
                fill="none",
            )
        )

    slots = (
        TextSlot(
            id="slot.title.text",
            prompt="",
            text="그림을 보고 □ 안에 알맞은 수를 써넣으시오.",
            style_role="body",
            x=60.0,
            y=66.0,
            font_size=35,
            fill="#222222",
        ),
        *top_fractions,
        RectSlot(
            id="slot.bar.outer",
            prompt="",
            x=bar_x,
            y=bar_y,
            width=bar_w,
            height=bar_h,
            stroke="#444444",
            stroke_width=1.6,
            fill="none",
        ),
        RectSlot(
            id="slot.bar.filled",
            prompt="",
            x=bar_x,
            y=bar_y,
            width=step * 5,
            height=bar_h,
            fill="#d4d5d9",
            stroke="none",
        ),
        *ticks,
        *arcs,
        TextSlot(
            id="slot.label.zero",
            prompt="",
            text="0",
            style_role="body",
            x=bar_x - 10.0,
            y=274.0,
            font_size=26,
            fill="#222222",
        ),
        TextSlot(
            id="slot.label.one",
            prompt="",
            text="1",
            style_role="body",
            x=bar_x + bar_w - 8.0,
            y=274.0,
            font_size=26,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.exp.left",
            numerator="5",
            denominator="8",
            x=48.0,
            numerator_y=345.0,
            bar_y=355.0,
            denominator_y=397.0,
            bar_width=40.0,
            font_size=30,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.2,
        ),
        TextSlot(
            id="slot.exp.text.1",
            prompt="",
            text="에서",
            style_role="body",
            x=74.0,
            y=379.0,
            font_size=30,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.exp.mid",
            numerator="1",
            denominator="8",
            x=171.0,
            numerator_y=345.0,
            bar_y=355.0,
            denominator_y=397.0,
            bar_width=40.0,
            font_size=30,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.2,
        ),
        TextSlot(
            id="slot.exp.text.2",
            prompt="",
            text="를",
            style_role="body",
            x=200.0,
            y=379.0,
            font_size=30,
            fill="#222222",
        ),
        RectSlot(
            id="slot.exp.blank",
            prompt="",
            x=244.0,
            y=334.0,
            width=52.0,
            height=52.0,
            rx=6.0,
            ry=6.0,
            stroke="#666666",
            stroke_width=1.2,
            fill="none",
        ),
        TextSlot(
            id="slot.exp.text.3",
            prompt="",
            text="번 덜어 낼 수 있습니다.",
            style_role="body",
            x=306.0,
            y=379.0,
            font_size=30,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.eq.left",
            numerator="5",
            denominator="8",
            x=48.0,
            numerator_y=533.0,
            bar_y=540.0,
            denominator_y=580.0,
            bar_width=40.0,
            font_size=30,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.2,
        ),
        TextSlot(
            id="slot.eq.divide",
            prompt="",
            text="÷",
            style_role="body",
            x=75.0,
            y=555.0,
            font_size=30,
            fill="#222222",
        ),
        *fraction_slots(
            id_prefix="slot.eq.mid",
            numerator="1",
            denominator="8",
            x=131.0,
            numerator_y=533.0,
            bar_y=540.0,
            denominator_y=580.0,
            bar_width=40.0,
            font_size=30,
            fill="#222222",
            stroke="#222222",
            stroke_width=2.2,
        ),
        TextSlot(
            id="slot.eq.equal",
            prompt="",
            text="=",
            style_role="body",
            x=165.0,
            y=560.0,
            font_size=30,
            fill="#222222",
        ),
        RectSlot(
            id="slot.eq.blank",
            prompt="",
            x=202.0,
            y=516.0,
            width=52.0,
            height=52.0,
            rx=6.0,
            ry=6.0,
            stroke="#666666",
            stroke_width=1.2,
            fill="none",
        ),
    )

    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="p260422_004",
        title="",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_004',
    'problem_type': 'fill_in_blank',
    'metadata': {   'language': 'ko',
                    'question': '5/8에서 1/8을 □번 덜어 낼 수 있습니다. 5/8 ÷ 1/8 = □',
                    'instruction': '그림을 보고 □ 안에 알맞은 수를 써넣으시오.'},
    'domain': {   'objects': [   {   'id': 'obj_instruction',
                                     'type': 'instruction',
                                     'text': '그림을 보고 □ 안에 알맞은 수를 써넣으시오.'},
                                 {   'id': 'obj_question1',
                                     'type': 'question',
                                     'text': '5/8에서 1/8을 □번 덜어 낼 수 있습니다.'},
                                 {   'id': 'obj_question2',
                                     'type': 'question',
                                     'text': '5/8 ÷ 1/8 = □'},
                                 {   'id': 'obj_frac_5_8',
                                     'type': 'fraction',
                                     'value': '5/8',
                                     'text': '5/8'},
                                 {   'id': 'obj_frac_1_8',
                                     'type': 'fraction',
                                     'value': '1/8',
                                     'text': '1/8'},
                                 {'id': 'obj_blank1', 'type': 'blank', 'text': '□'},
                                 {'id': 'obj_blank2', 'type': 'blank', 'text': '□'},
                                 {   'id': 'obj_diagram',
                                     'type': 'shape',
                                     'value': 'bar_model',
                                     'text': '0 to 1 partitioned into eighths with 5 shaded parts'},
                                 {'id': 'obj_number0', 'type': 'number', 'value': 0, 'text': '0'},
                                 {'id': 'obj_number1', 'type': 'number', 'value': 1, 'text': '1'},
                                 {   'id': 'obj_unit_piece',
                                     'type': 'fraction',
                                     'value': '1/8',
                                     'text': '1/8'}],
                  'relations': [   {   'id': 'rel1',
                                       'type': 'references',
                                       'from_id': 'obj_question1',
                                       'to_id': 'obj_frac_5_8'},
                                   {   'id': 'rel2',
                                       'type': 'references',
                                       'from_id': 'obj_question1',
                                       'to_id': 'obj_frac_1_8'},
                                   {   'id': 'rel3',
                                       'type': 'applies_to',
                                       'from_id': 'obj_diagram',
                                       'to_id': 'obj_question1'},
                                   {   'id': 'rel4',
                                       'type': 'asks_for',
                                       'from_id': 'obj_question1',
                                       'to_id': 'obj_blank1'},
                                   {   'id': 'rel5',
                                       'type': 'asks_for',
                                       'from_id': 'obj_question2',
                                       'to_id': 'obj_blank2'},
                                   {   'id': 'rel6',
                                       'type': 'evaluates_to',
                                       'from_id': 'obj_question2',
                                       'to_id': 'obj_blank2'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 5, 'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_004',
    'problem_type': 'fill_in_blank',
    'inputs': {   'total_ticks': 5,
                  'target_label': '정답',
                  'target_ticks': 5,
                  'target_count': 5,
                  'unit': ''},
    'plan': ['5/8에는 1/8이 5개 들어 있으므로 빈칸은 5입니다.'],
    'steps': [{'id': 'step.1', 'expr': '5/8에는 1/8이 5개 들어 있으므로 빈칸은 5입니다.', 'value': 5}],
    'checks': [],
    'answer': {'value': 5, 'unit': ''}}
