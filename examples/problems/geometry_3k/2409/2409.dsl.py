from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)

# Choice text template (easy to reuse/tune)
# - Keep radicals tight with digits: √2, √3
# - Use a math-friendly font to improve radical glyph rendering.
CHOICE_FONT_FAMILY = "Cambria Math"
CHOICE_FONT_SIZE = 48
CHOICE_X = 860.0
CHOICE_Y_1 = 320.0
CHOICE_Y_2 = 384.8

RAD2 = "√2"
RAD3 = "√3"
CHOICE_LINE_1 = f"1. 21 / 2. 21 {RAD2} /"
CHOICE_LINE_2 = f"3. 21 {RAD3} / 4."


def _append_line_slots(
    slots: list,
    lines: list[tuple[str, float, float, float, float]],
    *,
    stroke: str,
    stroke_width: float,
) -> None:
    for sid, x1, y1, x2, y2 in lines:
        slots.append(
            LineSlot(
                id=sid,
                prompt="",
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                stroke=stroke,
                stroke_width=stroke_width,
            )
        )


def _build_arc_polyline(
    *,
    slot_prefix: str,
    cx: float,
    cy: float,
    r: float,
    start_deg: float,
    end_deg: float,
    segments: int,
) -> list[tuple[str, float, float, float, float]]:
    points = []
    for i in range(segments + 1):
        t = i / segments
        deg = start_deg + (end_deg - start_deg) * t
        rad = math.radians(deg)
        points.append((round(cx + r * math.cos(rad), 1), round(cy + r * math.sin(rad), 1)))

    lines = []
    for i in range(segments):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        lines.append((f"{slot_prefix}.{i+1:02d}", x1, y1, x2, y2))
    return lines


def build_problem_template() -> ProblemTemplate:
    slots = [
        TextSlot(
            id="slot.q1",
            prompt="",
            text="Find y in triangle ABC.",
            style_role="question",
            x=40.0,
            y=80.0,
            font_size=48,
        ),
        RectSlot(
            id="slot.diagram.frame",
            prompt="",
            x=40.0,
            y=200.0,
            width=752.0,
            height=699.0,
            stroke="#D1D5DB",
            stroke_width=1.0,
            fill="none",
        ),
        LineSlot(
            id="slot.edge.1",
            prompt="",
            x1=110.2,
            y1=224.0,
            x2=333.8,
            y2=875.0,
            stroke="#374151",
            stroke_width=2.2,
        ),
        LineSlot(
            id="slot.edge.2",
            prompt="",
            x1=333.8,
            y1=875.0,
            x2=721.8,
            y2=750.0,
            stroke="#374151",
            stroke_width=2.2,
        ),
        LineSlot(
            id="slot.edge.3",
            prompt="",
            x1=110.2,
            y1=224.0,
            x2=721.8,
            y2=750.0,
            stroke="#374151",
            stroke_width=2.2,
        ),
        CircleSlot(
            id="slot.pt.A",
            prompt="",
            cx=333.8,
            cy=875.0,
            r=3.8,
            fill="#111111",
            stroke="#111111",
            stroke_width=1.0,
        ),
        CircleSlot(
            id="slot.pt.B",
            prompt="",
            cx=110.2,
            cy=224.0,
            r=3.8,
            fill="#111111",
            stroke="#111111",
            stroke_width=1.0,
        ),
        CircleSlot(
            id="slot.pt.C",
            prompt="",
            cx=721.8,
            cy=750.0,
            r=3.8,
            fill="#111111",
            stroke="#111111",
            stroke_width=1.0,
        ),
        TextSlot(
            id="slot.lb.A",
            prompt="",
            text="A",
            style_role="label",
            x=339.8,
            y=869.0,
            font_size=36,
        ),
        TextSlot(
            id="slot.lb.B",
            prompt="",
            text="B",
            style_role="label",
            x=116.2,
            y=218.0,
            font_size=36,
        ),
        TextSlot(
            id="slot.lb.C",
            prompt="",
            text="C",
            style_role="label",
            x=727.8,
            y=744.0,
            font_size=36,
        ),
        TextSlot(
            id="slot.len.AC",
            prompt="",
            text="21",
            style_role="label",
            x=531.8,
            y=808.5,
            font_size=36,
        ),
        TextSlot(
            id="slot.len.AB",
            prompt="",
            text="y",
            style_role="label",
            x=226.0,
            y=545.5,
            font_size=36,
        ),
        TextSlot(
            id="slot.len.BC",
            prompt="",
            text="x",
            style_role="label",
            x=420.0,
            y=483.0,
            font_size=36,
        ),
        TextSlot(
            id="slot.choice.1",
            prompt="",
            text=CHOICE_LINE_1,
            style_role="choice",
            x=CHOICE_X,
            y=CHOICE_Y_1,
            font_size=CHOICE_FONT_SIZE,
            font_family=CHOICE_FONT_FAMILY,
        ),
        TextSlot(
            id="slot.choice.2",
            prompt="",
            text=CHOICE_LINE_2,
            style_role="choice",
            x=CHOICE_X,
            y=CHOICE_Y_2,
            font_size=CHOICE_FONT_SIZE,
            font_family=CHOICE_FONT_FAMILY,
        ),
    ]

    arc_c = _build_arc_polyline(
        slot_prefix="slot.arc.C",
        cx=716.0,
        cy=747.0,
        r=12.0,
        start_deg=155.0,
        end_deg=205.0,
        segments=6,
    )
    arc_b = _build_arc_polyline(
        slot_prefix="slot.arc.B",
        cx=121.0,
        cy=224.0,
        r=11.0,
        start_deg=40.0,
        end_deg=105.0,
        segments=6,
    )
    _append_line_slots(slots, arc_c + arc_b, stroke="#7C3AED", stroke_width=2.0)

    slots.append(
        TextSlot(
            id="slot.arc.C.lb",
            prompt="",
            text="60",
            style_role="label",
            x=692.3,
            y=745.6,
            font_size=36,
        )
    )
    slots.append(
        TextSlot(
            id="slot.arc.B.lb",
            prompt="",
            text="30",
            style_role="label",
            x=127.1,
            y=242.2,
            font_size=36,
        )
    )

    return ProblemTemplate(
        id="2409",
        title="Find y in triangle ABC.",
        canvas=Canvas(width=1400, height=939, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=tuple(
                    slot.id for slot in slots if not slot.id.startswith("slot.choice")
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.1", "slot.choice.2"),
            ),
        ),
        slots=tuple(slots),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("triangle", "angle", "geometry"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {'problem_id': '2409',
 'problem_type': 'geometry_triangle',
 'metadata': {'title': 'Find y in triangle ABC.',
              'tags': ['triangle', 'angle', 'geometry'],
              'instruction': 'Find y.',
              'question': 'Find y in triangle ABC.',
              'required_layout_ids': ['slot.diagram.frame',
                                      'slot.edge.1',
                                      'slot.edge.2',
                                      'slot.edge.3',
                                      'slot.pt.A',
                                      'slot.pt.B',
                                      'slot.pt.C',
                                      'slot.arc.C.01',
                                      'slot.arc.C.02',
                                      'slot.arc.C.03',
                                      'slot.arc.C.04',
                                      'slot.arc.C.05',
                                      'slot.arc.C.06',
                                      'slot.arc.B.01',
                                      'slot.arc.B.02',
                                      'slot.arc.B.03',
                                      'slot.arc.B.04',
                                      'slot.arc.B.05',
                                      'slot.arc.B.06'],
              'extraction_confidence': 1.0,
              'language': 'en'},
 'domain': {'objects': [{'id': 'obj.triangle.ABC', 'type': 'triangle', 'name': 'ABC'},
                        {'id': 'obj.point.A', 'type': 'point', 'name': 'A'},
                        {'id': 'obj.point.B', 'type': 'point', 'name': 'B'},
                        {'id': 'obj.point.C', 'type': 'point', 'name': 'C'},
                        {'id': 'obj.segment.AC', 'type': 'segment', 'name': 'AC', 'value': 21},
                        {'id': 'obj.segment.AB', 'type': 'segment', 'name': 'AB'},
                        {'id': 'obj.angle.B', 'type': 'angle', 'name': 'angle B', 'value': 30},
                        {'id': 'obj.angle.C', 'type': 'angle', 'name': 'angle C', 'value': 60}],
            'relations': [{'id': 'rel.find_AB',
                           'type': 'find',
                           'from_id': 'obj.segment.AB',
                           'to_id': 'answer.target'}],
            'confidence': 1.0,
            'problem_solving': {'understand': {'given_refs': ['obj.segment.AC',
                                                              'obj.angle.B',
                                                              'obj.angle.C'],
                                               'target_ref': 'answer.target',
                                               'condition_refs': ['rel.find_AB']},
                                'plan': {'method': 'triangle_ratio_30_60_90',
                                         'description': 'Use 30-60-90 triangle side ratios to '
                                                        'compute AB.'},
                                'execute': {'expected_operations': ['infer_right_triangle',
                                                                    'apply_ratio',
                                                                    'compute_target_length']},
                                'review': {'check_methods': ['choice_match',
                                                             'value_consistency']}}},
 'answer': {'blanks': [],
            'choices': [{'index': 1, 'text': '1. 21', 'value': '21'},
                        {'index': 2, 'text': '2. 21*sqrt(2)', 'value': '21*sqrt(2)'},
                        {'index': 3, 'text': '3. 21*sqrt(3)', 'value': '21*sqrt(3)'},
                        {'index': 4, 'text': '4. (blank)', 'value': ''}],
            'answer_key': [3],
            'confidence': 1.0,
            'target': {'type': 'segment_length', 'description': 'AB (y)'},
            'value': 36.4,
            'unit': '',
            'exact_form': '21*sqrt(3)'}}

SOLVABLE = {'schema': 'modu.solvable.v1',
 'problem_id': '2409',
 'problem_type': 'geometry_triangle',
 'inputs': {'total_ticks': 0,
            'target_label': 'y',
            'target_ticks': 0,
            'target_count': 1,
            'unit': ''},
 'given': [{'ref': 'obj.segment.AC', 'value': 21},
           {'ref': 'obj.angle.B', 'value': 30},
           {'ref': 'obj.angle.C', 'value': 60}],
 'target': {'ref': 'answer.target', 'type': 'segment_length'},
 'method': 'triangle_ratio_30_60_90',
 'plan': ['Infer angle A = 90 from angle sum.', 'Apply ratio 1:sqrt(3):2.'],
 'steps': [{'id': 'step.1', 'operation': 'infer_angle_A', 'expr': 'A = 180 - 30 - 60', 'value': 90},
           {'id': 'step.2',
            'operation': 'apply_ratio',
            'expr': 'AB = AC*sqrt(3) = 21*sqrt(3)',
            'value': 36.4}],
 'checks': [{'id': 'check.1',
             'type': 'choice_match',
             'expr': 'match with choices',
             'expected': '21*sqrt(3)',
             'actual': '21*sqrt(3)',
             'pass': True}],
 'answer': {'value': 36.4, 'exact_form': '21*sqrt(3)', 'unit': '', 'derived_from': 'choice.3'}}
