from __future__ import annotations

from dataclasses import asdict
from typing import Any

from ..semantic.models.answer import SemanticAnswer
from ..semantic.models.domain import DomainObject, DomainRelation, SemanticDomain
from ..semantic.models.metadata import SemanticMetadata
from ..semantic.models.problem import SemanticProblem
from ..semantic.normalize import normalize_semantic
from .models.base import BlankSlot, ChoiceSlot, CircleSlot, LabelSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, Region, TextSlot
from .models.objects import ShapeObject
from .models.templates import AuthoringSlot, DiagramTemplate, ProblemTemplate


def compile_problem_template_to_semantic(
    problem: ProblemTemplate,
    *,
    problem_type: str | None = None,
    default_confidence: float = 1.0,
) -> dict[str, Any]:
    _assert_unique_ids(problem)

    slot_to_region = _slot_to_region(problem.regions)
    domain_objects: list[DomainObject] = []
    domain_relations: list[DomainRelation] = []
    answer = SemanticAnswer()
    required_layout_ids: list[str] = []

    question_text: str | None = None
    instruction_text: str | None = None
    question_consumed = False

    for slot in problem.slots:
        region = slot_to_region.get(slot.id)

        if isinstance(slot, TextSlot):
            semantic_role = _infer_text_role(slot, region, question_consumed)
            question_consumed = question_consumed or semantic_role == "question"
            if semantic_role == "question" and question_text is None:
                question_text = slot.text
            elif semantic_role == "instruction" and instruction_text is None:
                instruction_text = slot.text
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type=semantic_role,
                    refs=_refs_for_slot(slot.id, region),
                    properties={"text": slot.text},
                )
            )
            continue

        if isinstance(slot, ChoiceSlot):
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="choice_set",
                    refs=_refs_for_slot(slot.id, region),
                    properties={
                        "prompt": slot.prompt or "",
                        "choice_count": len(slot.choices),
                        "multiple_select": slot.multiple_select,
                    },
                )
            )
            if question_text is None and slot.prompt:
                question_text = slot.prompt

            for index, choice_text in enumerate(slot.choices):
                choice_id = f"{slot.id}.choice.{index + 1}"
                answer.choices.append(
                    {
                        "id": choice_id,
                        "slot_id": slot.id,
                        "value": choice_text,
                        "index": index,
                    }
                )
            answer.answer_key.append(
                {
                    "slot_id": slot.id,
                    "values": list(slot.answer_key),
                }
            )
            continue

        if isinstance(slot, BlankSlot):
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="blank",
                    refs=_refs_for_slot(slot.id, region),
                    properties={"prompt": slot.prompt or "", "placeholder": slot.placeholder},
                )
            )
            answer.blanks.append(
                {
                    "id": slot.id,
                    "slot_id": slot.id,
                    "expected": slot.answer_key,
                }
            )
            if question_text is None and slot.prompt:
                question_text = slot.prompt
            continue

        if isinstance(slot, LabelSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="label",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "text": slot.text,
                        "target_object_id": slot.target_object_id,
                        "target_anchor": slot.target_anchor,
                    },
                )
            )
            if slot.target_object_id:
                domain_relations.append(
                    DomainRelation(
                        id=f"rel.{slot.id}.targets",
                        type="targets",
                        from_id=slot.id,
                        to_id=slot.target_object_id,
                    )
                )

        if isinstance(slot, RectSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="rect_slot",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "x": slot.x,
                        "y": slot.y,
                        "width": slot.width,
                        "height": slot.height,
                        "stroke": slot.stroke,
                        "stroke_width": slot.stroke_width,
                        "rx": slot.rx,
                        "ry": slot.ry,
                        "fill": slot.fill,
                        "semantic_role": slot.semantic_role,
                    },
                )
            )
            continue

        if isinstance(slot, LineSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="line_slot",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "x1": slot.x1,
                        "y1": slot.y1,
                        "x2": slot.x2,
                        "y2": slot.y2,
                        "stroke": slot.stroke,
                        "stroke_width": slot.stroke_width,
                        "stroke_dasharray": slot.stroke_dasharray,
                        "semantic_role": slot.semantic_role,
                    },
                )
            )
            continue

        if isinstance(slot, CircleSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="circle_slot",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "cx": slot.cx,
                        "cy": slot.cy,
                        "r": slot.r,
                        "stroke": slot.stroke,
                        "stroke_width": slot.stroke_width,
                        "fill": slot.fill,
                        "semantic_role": slot.semantic_role,
                    },
                )
            )
            continue

        if isinstance(slot, PolygonSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="polygon_slot",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "points": [[x, y] for x, y in slot.points],
                        "stroke": slot.stroke,
                        "stroke_width": slot.stroke_width,
                        "fill": slot.fill,
                        "semantic_role": slot.semantic_role,
                    },
                )
            )
            continue

        if isinstance(slot, PathSlot):
            required_layout_ids.append(slot.id)
            domain_objects.append(
                DomainObject(
                    id=slot.id,
                    type="path_slot",
                    refs=_refs_for_slot(slot.id, region),
                    layout_required=True,
                    properties={
                        "d": slot.d,
                        "stroke": slot.stroke,
                        "stroke_width": slot.stroke_width,
                        "stroke_dasharray": slot.stroke_dasharray,
                        "fill": slot.fill,
                        "semantic_role": slot.semantic_role,
                    },
                )
            )
            continue

    for diagram in problem.diagrams:
        required_layout_ids.append(diagram.id)
        domain_objects.append(
            DomainObject(
                id=diagram.id,
                type="diagram_template",
                refs=[{"kind": "diagram", "id": diagram.id}],
                layout_required=True,
                properties={"object_ids": [obj.id for obj in diagram.objects]},
            )
        )
        _append_diagram_semantics(
            diagram=diagram,
            objects=domain_objects,
            relations=domain_relations,
            required_layout_ids=required_layout_ids,
        )

    semantic = SemanticProblem(
        problem_id=problem.id,
        problem_type=problem_type or _infer_problem_type(problem),
        metadata=SemanticMetadata(
            title=problem.title,
            tags=list(problem.tags),
            instruction=instruction_text,
            question=question_text,
            required_layout_ids=_stable_unique(required_layout_ids),
        ),
        domain=SemanticDomain(objects=domain_objects, relations=domain_relations),
        answer=answer,
    )
    normalized = normalize_semantic(semantic.to_dict())
    return _attach_confidence_defaults(normalized, default_confidence=default_confidence)


def _attach_confidence_defaults(
    semantic: dict[str, Any],
    *,
    default_confidence: float,
) -> dict[str, Any]:
    metadata = semantic.get("metadata")
    if isinstance(metadata, dict) and "extraction_confidence" not in metadata:
        metadata["extraction_confidence"] = float(default_confidence)

    domain = semantic.get("domain")
    if isinstance(domain, dict):
        objects = domain.get("objects")
        if isinstance(objects, list):
            for obj in objects:
                if isinstance(obj, dict) and "confidence" not in obj:
                    obj["confidence"] = float(default_confidence)

        relations = domain.get("relations")
        if isinstance(relations, list):
            for rel in relations:
                if isinstance(rel, dict) and "confidence" not in rel:
                    rel["confidence"] = float(default_confidence)

        if "confidence" not in domain:
            domain["confidence"] = float(default_confidence)

    answer = semantic.get("answer")
    if isinstance(answer, dict) and "confidence" not in answer:
        answer["confidence"] = float(default_confidence)

    return semantic


def _assert_unique_ids(problem: ProblemTemplate) -> None:
    seen_ids: set[str] = set()

    def consume(node_id: str, scope: str) -> None:
        if node_id in seen_ids:
            raise ValueError(f"Duplicate id '{node_id}' in {scope}")
        seen_ids.add(node_id)

    consume(problem.id, "problem")
    for region in problem.regions:
        consume(region.id, "regions")
    for slot in problem.slots:
        consume(slot.id, "slots")
    for diagram in problem.diagrams:
        consume(diagram.id, "diagrams")
        for obj in diagram.objects:
            consume(obj.id, f"diagram '{diagram.id}' objects")
        for label_slot in diagram.label_slots:
            consume(label_slot.id, f"diagram '{diagram.id}' label_slots")
        for constraint in diagram.constraints:
            consume(constraint.id, f"diagram '{diagram.id}' constraints")


def _slot_to_region(regions: tuple[Region, ...]) -> dict[str, Region]:
    mapping: dict[str, Region] = {}
    for region in regions:
        for slot_id in region.slot_ids:
            mapping[slot_id] = region
    return mapping


def _refs_for_slot(slot_id: str, region: Region | None) -> list[dict[str, str]]:
    refs = [{"kind": "slot", "id": slot_id}]
    if region is not None:
        refs.append({"kind": "region", "id": region.id})
    return refs


def _infer_text_role(slot: TextSlot, region: Region | None, question_consumed: bool) -> str:
    style = slot.style_role.lower()
    if style in {"instruction", "directive"}:
        return "instruction"
    if style in {"question", "stem"}:
        return "question"

    if region is not None:
        if region.role == "stem":
            return "instruction" if question_consumed else "question"
        if region.role == "note":
            return "note"
    return "text"


def _infer_problem_type(problem: ProblemTemplate) -> str:
    has_choice = any(isinstance(slot, ChoiceSlot) for slot in problem.slots)
    has_blank = any(isinstance(slot, BlankSlot) for slot in problem.slots)
    has_diagram = len(problem.diagrams) > 0
    if has_choice:
        return "multiple_choice"
    if has_blank:
        return "fill_in_blank"
    if has_diagram:
        return "diagram_problem"
    return "generic"


def _append_diagram_semantics(
    *,
    diagram: DiagramTemplate,
    objects: list[DomainObject],
    relations: list[DomainRelation],
    required_layout_ids: list[str],
) -> None:
    for obj in diagram.objects:
        required_layout_ids.append(obj.id)
        objects.append(
            DomainObject(
                id=obj.id,
                type=obj.object_type,
                refs=[{"kind": "diagram", "id": diagram.id}, {"kind": "object", "id": obj.id}],
                layout_required=True,
                properties=_semantic_properties_for_shape(obj),
            )
        )
        relations.append(
            DomainRelation(
                id=f"rel.{diagram.id}.contains.{obj.id}",
                type="diagram_contains",
                from_id=diagram.id,
                to_id=obj.id,
            )
        )

    for label_slot in diagram.label_slots:
        required_layout_ids.append(label_slot.id)
        objects.append(
            DomainObject(
                id=label_slot.id,
                type="label",
                refs=[
                    {"kind": "diagram", "id": diagram.id},
                    {"kind": "slot", "id": label_slot.id},
                ],
                layout_required=True,
                properties={
                    "text": label_slot.text,
                    "target_object_id": label_slot.target_object_id,
                    "target_anchor": label_slot.target_anchor,
                },
            )
        )
        if label_slot.target_object_id:
            relations.append(
                DomainRelation(
                    id=f"rel.{label_slot.id}.targets",
                    type="targets",
                    from_id=label_slot.id,
                    to_id=label_slot.target_object_id,
                )
            )


def _semantic_properties_for_shape(obj: ShapeObject) -> dict[str, Any]:
    raw = asdict(obj)
    ignored = {"id", "object_type", "style_role"}
    return {key: value for key, value in raw.items() if key not in ignored}


def _stable_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique
