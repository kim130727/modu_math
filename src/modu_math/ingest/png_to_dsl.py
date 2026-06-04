from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from modu_math.dsl import (
    Arrow,
    Canvas,
    ChoiceSlot,
    Circle,
    Constraint,
    Cube,
    DiagramTemplate,
    FractionAreaModel,
    Grid,
    LabelSlot,
    ProblemTemplate,
    Region,
    ShapeObject,
    TextSlot,
    Triangle,
    compile_problem_template_to_layout,
    export_layout_to_dsl_source,
)

from .png_classifier import ProblemClassification, classify_png_problem


@dataclass(frozen=True)
class PngToDslResult:
    problem: ProblemTemplate
    source: str
    classification: ProblemClassification
    output_path: Path


def generate_dsl_from_png(
    *,
    image_path: Path,
    output_path: Path,
    problem_id: str,
    ocr_lines: tuple[str, ...] = (),
    llm_adapter: object | None = None,
) -> PngToDslResult:
    classification = classify_png_problem(
        image_path=image_path,
        problem_id=problem_id,
        ocr_lines=ocr_lines,
        llm_adapter=llm_adapter,
    )
    template = _build_problem_template(classification)
    layout = compile_problem_template_to_layout(template)
    source = export_layout_to_dsl_source(layout)
    output_path.write_text(source, encoding="utf-8")
    return PngToDslResult(problem=template, source=source, classification=classification, output_path=output_path)


def _build_problem_template(classification: ProblemClassification) -> ProblemTemplate:
    builder = _TEMPLATE_BUILDERS.get(classification.template_id, _build_generic_text_blank)
    return builder(classification)


def _build_generic_text_blank(classification: ProblemClassification) -> ProblemTemplate:
    question = classification.text_lines[0] if classification.text_lines else "문제를 읽고 답을 써 보세요."
    extra = classification.text_lines[1:4]
    slots: list[TextSlot] = [
        TextSlot(id="slot.stem", text=question, style_role="question"),
    ]
    for index, line in enumerate(extra, start=1):
        slots.append(TextSlot(id=f"slot.line.{index}", text=line, style_role="body"))

    return ProblemTemplate(
        id=classification.problem_id,
        title=_title_from_question(question),
        canvas=Canvas(width=classification.canvas_width, height=classification.canvas_height),
        regions=(
            Region(id="region.stem", role="stem", slot_ids=tuple(slot.id for slot in slots)),
            Region(id="region.diagram", role="diagram", flow="absolute"),
            Region(id="region.answer", role="answer", slot_ids=("slot.answer",)),
        ),
        slots=tuple([*slots, TextSlot(id="slot.answer", text="답: □", style_role="answer")]),
        diagrams=(),
        constraints=(),
        groups=(),
        tags=tuple(classification.template_hints),
    )


def _build_arithmetic_two_panel(classification: ProblemClassification) -> ProblemTemplate:
    lines = classification.text_lines or ("문제를 풀어 보세요.",)
    stem = lines[0]
    panel_lines = tuple(lines[1:5])
    objects = (
        ShapeObject(id="obj.panel.left", object_type="number_panel", style_role="default"),
        ShapeObject(id="obj.panel.right", object_type="number_panel", style_role="default"),
    )
    return ProblemTemplate(
        id=classification.problem_id,
        title=_title_from_question(stem),
        canvas=Canvas(width=classification.canvas_width, height=classification.canvas_height),
        regions=(
            Region(id="region.stem", role="stem", slot_ids=("slot.stem", "slot.step.1", "slot.step.2")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.answer", role="answer", slot_ids=("slot.answer",)),
        ),
        slots=(
            TextSlot(id="slot.stem", text=stem, style_role="question"),
            TextSlot(id="slot.step.1", text=panel_lines[0] if len(panel_lines) > 0 else "(1)", style_role="body"),
            TextSlot(id="slot.step.2", text=panel_lines[1] if len(panel_lines) > 1 else "(2)", style_role="body"),
            TextSlot(id="slot.answer", text="답: □", style_role="answer"),
        ),
        diagrams=(
            DiagramTemplate(
                id="diagram.main",
                objects=objects,
                constraints=(
                    Constraint(
                        id="c.distribute.panels",
                        type="distribute",
                        target_ids=("obj.panel.left", "obj.panel.right"),
                        params={"axis": "x"},
                    ),
                ),
            ),
        ),
        tags=tuple(_append_hint(classification.template_hints, "two_panel")),
    )


def _build_multiple_choice(classification: ProblemClassification) -> ProblemTemplate:
    lines = classification.text_lines or ("알맞은 답을 고르세요.",)
    question = lines[0]
    choices = _extract_choices(lines[1:]) or ("①", "②", "③", "④")
    return ProblemTemplate(
        id=classification.problem_id,
        title=_title_from_question(question),
        canvas=Canvas(width=classification.canvas_width, height=classification.canvas_height),
        regions=(
            Region(id="region.stem", role="stem", slot_ids=("slot.question",)),
            Region(id="region.choices", role="choices", slot_ids=("slot.choices",)),
            Region(id="region.diagram", role="diagram", flow="absolute"),
        ),
        slots=(
            TextSlot(id="slot.question", text=question, style_role="question"),
            ChoiceSlot(id="slot.choices", prompt="정답을 고르세요.", choices=tuple(choices), multiple_select=False),
        ),
        diagrams=(),
        tags=tuple(_append_hint(classification.template_hints, "multiple_choice")),
    )


def _build_cube_diagram(classification: ProblemClassification) -> ProblemTemplate:
    return _build_object_label_template(
        classification=classification,
        object_id="obj.cube.main",
        object_value=Cube(id="obj.cube.main", edge_label_mode="auto", perspective="isometric"),
        extra_hints=("cube",),
    )


def _build_triangle_diagram(classification: ProblemClassification) -> ProblemTemplate:
    variant = "right" if _contains_any(classification.text_lines, ("직각", "right")) else "scalene"
    return _build_object_label_template(
        classification=classification,
        object_id="obj.triangle.main",
        object_value=Triangle(id="obj.triangle.main", variant=variant),
        extra_hints=("triangle",),
    )


def _build_circle_diagram(classification: ProblemClassification) -> ProblemTemplate:
    mark_center = _contains_any(classification.text_lines, ("중심", "center"))
    return _build_object_label_template(
        classification=classification,
        object_id="obj.circle.main",
        object_value=Circle(id="obj.circle.main", mark_center=mark_center),
        extra_hints=("circle",),
    )


def _build_grid_diagram(classification: ProblemClassification) -> ProblemTemplate:
    rows, cols = _extract_grid_shape(classification.text_lines)
    return _build_object_label_template(
        classification=classification,
        object_id="obj.grid.main",
        object_value=Grid(id="obj.grid.main", rows=rows, cols=cols),
        extra_hints=("grid",),
    )


def _build_fraction_area_model(classification: ProblemClassification) -> ProblemTemplate:
    numerator, denominator = _extract_fraction(classification.text_lines)
    return _build_object_label_template(
        classification=classification,
        object_id="obj.fraction.main",
        object_value=FractionAreaModel(
            id="obj.fraction.main",
            partitions=denominator,
            shaded=numerator,
            orientation="horizontal",
        ),
        extra_hints=("fraction_area_model",),
    )


def _build_arrow_flow(classification: ProblemClassification) -> ProblemTemplate:
    direction = "left" if _contains_any(classification.text_lines, ("왼쪽", "left", "←")) else "right"
    return _build_object_label_template(
        classification=classification,
        object_id="obj.arrow.main",
        object_value=Arrow(id="obj.arrow.main", direction=direction),
        extra_hints=("arrow",),
    )


def _build_object_label_template(
    *,
    classification: ProblemClassification,
    object_id: str,
    object_value: ShapeObject,
    extra_hints: tuple[str, ...],
) -> ProblemTemplate:
    question = classification.text_lines[0] if classification.text_lines else "도형을 보고 물음에 답하세요."
    labels = _extract_label_candidates(classification.text_lines)
    label_text = labels[0] if labels else "A"
    return ProblemTemplate(
        id=classification.problem_id,
        title=_title_from_question(question),
        canvas=Canvas(width=classification.canvas_width, height=classification.canvas_height),
        regions=(
            Region(id="region.stem", role="stem", slot_ids=("slot.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute"),
            Region(id="region.answer", role="answer", slot_ids=("slot.answer",)),
        ),
        slots=(
            TextSlot(id="slot.question", text=question, style_role="question"),
            TextSlot(id="slot.answer", text="답: □", style_role="answer"),
        ),
        diagrams=(
            DiagramTemplate(
                id="diagram.main",
                objects=(object_value,),
                label_slots=(LabelSlot(id="slot.label.main", text=label_text, target_object_id=object_id),),
            ),
        ),
        tags=tuple(_append_hint(classification.template_hints, *extra_hints)),
    )


def _extract_grid_shape(lines: tuple[str, ...]) -> tuple[int, int]:
    pattern = re.compile(r"(\d+)\s*[xX×]\s*(\d+)")
    for line in lines:
        match = pattern.search(line)
        if not match:
            continue
        rows = max(1, min(12, int(match.group(1))))
        cols = max(1, min(12, int(match.group(2))))
        return (rows, cols)
    return (4, 4)


def _extract_fraction(lines: tuple[str, ...]) -> tuple[int, int]:
    pattern = re.compile(r"(\d+)\s*/\s*(\d+)")
    for line in lines:
        match = pattern.search(line)
        if not match:
            continue
        numerator = int(match.group(1))
        denominator = max(1, int(match.group(2)))
        numerator = max(0, min(numerator, denominator))
        return (numerator, denominator)
    return (1, 2)


def _extract_choices(lines: tuple[str, ...]) -> tuple[str, ...]:
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^[①②③④⑤]", stripped):
            out.append(stripped)
            continue
        if re.match(r"^\d+\.", stripped):
            out.append(stripped)
    return tuple(out[:5])


def _extract_label_candidates(lines: tuple[str, ...]) -> tuple[str, ...]:
    found: list[str] = []
    for line in lines:
        for token in re.findall(r"\b[A-Z]\b", line):
            found.append(token)
    return tuple(_append_hint((), *found))


def _contains_any(lines: tuple[str, ...], words: tuple[str, ...]) -> bool:
    joined = " ".join(lines).lower()
    return any(word.lower() in joined for word in words)


def _append_hint(base: tuple[str, ...], *items: str) -> list[str]:
    out = list(base)
    for item in items:
        cleaned = item.strip()
        if cleaned and cleaned not in out:
            out.append(cleaned)
    return out


def _title_from_question(question: str) -> str:
    candidate = question.strip().replace("\n", " ")
    if not candidate:
        return "문제"
    return candidate[:48]


_TEMPLATE_BUILDERS = {
    "generic_text_blank": _build_generic_text_blank,
    "arithmetic_two_panel": _build_arithmetic_two_panel,
    "multiple_choice": _build_multiple_choice,
    "cube_diagram_label": _build_cube_diagram,
    "triangle_diagram_label": _build_triangle_diagram,
    "circle_diagram_label": _build_circle_diagram,
    "grid_diagram": _build_grid_diagram,
    "fraction_area_model": _build_fraction_area_model,
    "arrow_flow": _build_arrow_flow,
}

