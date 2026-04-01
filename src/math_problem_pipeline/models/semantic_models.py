"""Semantic models optimized for renderable math problem representation."""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from .raw_models import BBox
from .render_models import LayoutHint


class CoordinateSystemRef(BaseModel):
    """Explicit coordinate layering reference.

    - source_coordinates: PDF page coordinate info.
    - semantic_coordinates: normalized shape relation data.
    - render_coordinates: final placement in scene space.
    """

    source_coordinates: dict = Field(default_factory=dict)
    semantic_coordinates: dict = Field(default_factory=dict)
    render_coordinates: dict = Field(default_factory=dict)


class SemanticProblemBase(BaseModel):
    """Base semantic problem fields shared by all types."""

    schema_version: str = "0.1.0"
    problem_id: str
    source_pdf: str
    page_number: int
    type: str
    question_text: str
    answer: str | None = None
    explanation: str | None = None
    bbox: BBox | None = None
    confidence: float = 0.0
    warnings: list[str] = Field(default_factory=list)
    render_hint: LayoutHint = Field(default_factory=LayoutHint)
    coordinates: CoordinateSystemRef = Field(default_factory=CoordinateSystemRef)


class MultipleChoiceTextProblem(SemanticProblemBase):
    type: Literal["multiple_choice_text"]
    choices: list[str] = Field(default_factory=list)


class ArithmeticExpressionProblem(SemanticProblemBase):
    type: Literal["arithmetic_expression"]
    expression: str
    variables: dict[str, float | int | str] = Field(default_factory=dict)


class FractionPartition(BaseModel):
    shape: Literal["rectangle", "circle"]
    total_parts: int
    shaded_parts: int
    rows: int | None = None
    cols: int | None = None
    partition: Literal["grid", "radial"] = "grid"
    shaded_indices: list[int] = Field(default_factory=list)


class FractionShadedAreaProblem(SemanticProblemBase):
    type: Literal["fraction_shaded_area"]
    fraction: FractionPartition


class ClockHandSpec(BaseModel):
    hour: int | None = None
    minute: int | None = None
    hour_angle: float | None = None
    minute_angle: float | None = None


class ClockReadingProblem(SemanticProblemBase):
    type: Literal["clock_reading"]
    clock: ClockHandSpec


class GeometryPoint(BaseModel):
    label: str
    x: float
    y: float


class GeometrySegment(BaseModel):
    start: str
    end: str
    length_label: str | None = None


class GeometryAngle(BaseModel):
    vertex: str
    ray1: str
    ray2: str
    degree_label: str | None = None


class GeometryBasicProblem(SemanticProblemBase):
    type: Literal["geometry_basic"]
    points: list[GeometryPoint] = Field(default_factory=list)
    segments: list[GeometrySegment] = Field(default_factory=list)
    angles: list[GeometryAngle] = Field(default_factory=list)
    polygons: list[list[str]] = Field(default_factory=list)


class TableSpec(BaseModel):
    headers: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)


class BarValue(BaseModel):
    label: str
    value: float


class ChartSpec(BaseModel):
    chart_type: Literal["bar"] = "bar"
    bars: list[BarValue] = Field(default_factory=list)


class TableOrChartBasicProblem(SemanticProblemBase):
    type: Literal["table_or_chart_basic"]
    table: TableSpec | None = None
    chart: ChartSpec | None = None


SemanticProblem = Annotated[
    Union[
        MultipleChoiceTextProblem,
        ArithmeticExpressionProblem,
        FractionShadedAreaProblem,
        ClockReadingProblem,
        GeometryBasicProblem,
        TableOrChartBasicProblem,
    ],
    Field(discriminator="type"),
]
