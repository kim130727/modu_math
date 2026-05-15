from __future__ import annotations

import math

from modu_math.dsl import Canvas, LineSlot, PolygonSlot, ProblemTemplate, Region, TextSlot


TICK_COUNT = 20
CHART_CX = 400.0
CHART_CY = 392.0
CHART_RADIUS = 140.0
TICK_OUTER_RADIUS = CHART_RADIUS - 1.0
TICK_INNER_RADIUS = CHART_RADIUS - 14.0
START_DEGREE = -90.0
SAMPLES_PER_TICK = 6


def _point_on_tick(tick: float, radius: float) -> tuple[float, float]:
    degree = START_DEGREE + (360.0 * tick / TICK_COUNT)
    radian = math.radians(degree)
    x = CHART_CX + radius * math.cos(radian)
    y = CHART_CY + radius * math.sin(radian)
    return (x, y)


def _build_sector_points(start_tick: int, span_ticks: int) -> tuple[tuple[float, float], ...]:
    points: list[tuple[float, float]] = [(CHART_CX, CHART_CY)]
    total_samples = max(1, span_ticks * SAMPLES_PER_TICK)

    for i in range(total_samples + 1):
        t = start_tick + (span_ticks * i / total_samples)
        points.append(_point_on_tick(t, CHART_RADIUS))

    return tuple(points)


def _build_tick_slots() -> tuple[LineSlot, ...]:
    tick_slots: list[LineSlot] = []
    for tick in range(TICK_COUNT):
        x1, y1 = _point_on_tick(tick, TICK_OUTER_RADIUS)
        x2, y2 = _point_on_tick(tick, TICK_INNER_RADIUS)
        tick_slots.append(
            LineSlot(
                id=f"slot.tick_{tick:02d}",
                prompt="",
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                stroke="#222222",
                stroke_width=1.4,
                semantic_role="scale_tick",
            )
        )
    return tuple(tick_slots)


def _build_problem_text_slots() -> tuple[TextSlot, ...]:
    return (
        TextSlot(
            id="slot.q1",
            prompt="",
            text="준호네 학교 학생들이 좋아하는 과일을 조사한 원그래프입니다.",
            style_role="body",
            x=14.0,
            y=44.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        ),
        TextSlot(
            id="slot.q2",
            prompt="",
            text="바나나를 좋아하는 학생이 60명이면 전체 학생 수는",
            style_role="body",
            x=14.0,
            y=94.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        ),
        TextSlot(
            id="slot.q3",
            prompt="",
            text="몇 명인가요?",
            style_role="body",
            x=14.0,
            y=142.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        ),
        TextSlot(
            id="slot.title",
            prompt="",
            text="좋아하는 과일별 학생 수",
            style_role="body",
            x=206.0,
            y=204.0,
            font_size=32,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="label",
        ),
        TextSlot(
            id="slot.scale_0",
            prompt="",
            text="0",
            style_role="body",
            x=400.0,
            y=241.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="scale_label",
        ),
        TextSlot(
            id="slot.scale_25",
            prompt="",
            text="25",
            style_role="body",
            x=565.0,
            y=400.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="scale_label",
        ),
        TextSlot(
            id="slot.scale_50",
            prompt="",
            text="50",
            style_role="body",
            x=400.0,
            y=565.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="scale_label",
        ),
        TextSlot(
            id="slot.scale_75",
            prompt="",
            text="75",
            style_role="body",
            x=235.0,
            y=400.0,
            font_size=30,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="scale_label",
        ),
        TextSlot(
            id="slot.fruit_1",
            prompt="",
            text="사과",
            style_role="body",
            x=461.37686860699233,
            y=330.62313139300767,
            font_size=26,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="chart_label",
        ),
        TextSlot(
            id="slot.fruit_2",
            prompt="",
            text="포도",
            style_role="body",
            x=470.22267511174545,
            y=443.01975989898665,
            font_size=26,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="chart_label",
        ),
        TextSlot(
            id="slot.fruit_3",
            prompt="",
            text="바나나",
            style_role="body",
            x=386.421488434508,
            y=477.731347963658,
            font_size=26,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="chart_label",
        ),
        TextSlot(
            id="slot.fruit_4",
            prompt="",
            text="복숭아",
            style_role="body",
            x=317.44829438558065,
            y=418.82267511174547,
            font_size=26,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="chart_label",
        ),
        TextSlot(
            id="slot.fruit_5",
            prompt="",
            text="기타",
            style_role="body",
            x=348.98024010101335,
            y=321.77732488825455,
            font_size=26,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="chart_label",
        ),
    )


def _build_chart_shape_slots() -> tuple[PolygonSlot | LineSlot, ...]:
    # Each tuple is (sector_id, radial_id, start_tick, span_ticks, fill).
    # "start_tick + span_ticks" defines the next radial boundary.
    sector_specs = (
        ("slot.sector_1", "slot.radial_1", 0, 5, "#EFEFEF"),
        ("slot.sector_2", "slot.radial_2", 5, 4, "#E8E8E8"),
        ("slot.sector_3", "slot.radial_3", 9, 3, "#DDDDDD"),
        ("slot.sector_4", "slot.radial_4", 12, 4, "#C9C9C9"),
        ("slot.sector_5", "slot.radial_5", 16, 4, "#B3B3B3"),
    )

    shape_slots: list[PolygonSlot | LineSlot] = []
    for sector_id, radial_id, start_tick, span_ticks, fill in sector_specs:
        shape_slots.append(
            PolygonSlot(
                id=sector_id,
                prompt="",
                points=_build_sector_points(start_tick, span_ticks),
                stroke="#222222",
                stroke_width=1.6,
                fill=fill,
                semantic_role="chart_sector",
            )
        )

        rx, ry = _point_on_tick(start_tick, CHART_RADIUS)
        shape_slots.append(
            LineSlot(
                id=radial_id,
                prompt="",
                x1=CHART_CX,
                y1=CHART_CY,
                x2=rx,
                y2=ry,
                stroke="#222222",
                stroke_width=1.6,
                semantic_role="chart_radial",
            )
        )

    shape_slots.extend(_build_tick_slots())
    return tuple(shape_slots)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=805,
        height=591,
        coordinate_mode="logical",
    )

    # Render chart shapes first, then text so labels are not hidden by sectors.
    slots = _build_chart_shape_slots() + _build_problem_text_slots()
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="vertical",
            # Keep renderer order aligned with slot tuple order.
            slot_ids=tuple(slot.id for slot in slots),
        ),
    )

    return ProblemTemplate(
        id="0013",
        title="",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
