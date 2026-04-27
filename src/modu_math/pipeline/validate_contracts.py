from __future__ import annotations

from typing import Any

"""
Cross-layer contract validation rules (strict mode).

Conventions enforced here:
- canonical layout (`regions/slots`) is the default contract shape.
- layout `source_ref` (optional, when present on contract objects): must
  reference a known semantic id.
- semantic required-layout markers (optional):
  - `domain.objects[].layout_required == true`
  - `metadata.required_layout_ids[]`
  Any id marked required must be represented by either:
  - a layout object with matching `id`, or
  - a layout object whose `source_ref` matches that semantic id.
- renderer element linkage:
  - canonical layout: renderer `refs.layout_*_id` must map to layout ids.
  - legacy layout (`nodes`): renderer `id` must map to a layout node id.
  - optional `source_ref` (element-level or attributes-level) must map to
    a layout id or semantic id.
"""


class CrossLayerValidationError(Exception):
    pass


def _collect_semantic_ids(semantic: dict[str, Any]) -> set[str]:
    domain = semantic.get("domain", {})
    answer = semantic.get("answer", {})
    semantic_ids: set[str] = set()

    objects = domain.get("objects", []) if isinstance(domain, dict) else []
    if isinstance(objects, list):
        for index, obj in enumerate(objects):
            if not isinstance(obj, dict):
                continue
            object_id = obj.get("id")
            if isinstance(object_id, str) and object_id.strip():
                semantic_ids.add(object_id)
            elif "id" in obj:
                raise CrossLayerValidationError(
                    f"$.domain.objects[{index}].id must be a non-empty string when present"
                )

    blanks = answer.get("blanks", []) if isinstance(answer, dict) else []
    if isinstance(blanks, list):
        for index, blank in enumerate(blanks):
            if isinstance(blank, dict):
                blank_id = blank.get("id") or blank.get("blank_id")
                if isinstance(blank_id, str) and blank_id.strip():
                    semantic_ids.add(blank_id)
                elif "id" in blank or "blank_id" in blank:
                    raise CrossLayerValidationError(
                        f"$.answer.blanks[{index}] id/blank_id must be a non-empty string when present"
                    )
    return semantic_ids


def _collect_required_layout_ids(semantic: dict[str, Any]) -> set[str]:
    domain = semantic.get("domain", {})
    metadata = semantic.get("metadata", {})
    required_ids: set[str] = set()

    objects = domain.get("objects", []) if isinstance(domain, dict) else []
    if isinstance(objects, list):
        for index, obj in enumerate(objects):
            if not isinstance(obj, dict):
                continue
            if obj.get("layout_required") is True:
                object_id = obj.get("id")
                if not isinstance(object_id, str) or not object_id.strip():
                    raise CrossLayerValidationError(
                        f"$.domain.objects[{index}] has layout_required=true but missing valid id"
                    )
                required_ids.add(object_id)

    metadata_required = metadata.get("required_layout_ids", []) if isinstance(metadata, dict) else []
    if isinstance(metadata_required, list):
        for index, required_id in enumerate(metadata_required):
            if not isinstance(required_id, str) or not required_id.strip():
                raise CrossLayerValidationError(
                    f"$.metadata.required_layout_ids[{index}] must be a non-empty string"
                )
            required_ids.add(required_id)

    return required_ids


def _collect_layout_ids(layout: dict[str, Any]) -> tuple[set[str], list[tuple[str, str]], str]:
    layout_ids: set[str] = set()
    source_refs: list[tuple[str, str]] = []

    has_contract_shape = (
        isinstance(layout.get("regions"), list)
        or isinstance(layout.get("slots"), list)
        or isinstance(layout.get("diagrams"), list)
    )
    if has_contract_shape:
        def consume_id(path: str, value: Any) -> str:
            if not isinstance(value, str) or not value.strip():
                raise CrossLayerValidationError(f"{path} must be a non-empty string")
            if value in layout_ids:
                raise CrossLayerValidationError(f"{path} duplicates existing layout id '{value}'")
            layout_ids.add(value)
            return value

        def consume_optional_source_ref(path: str, raw: Any) -> None:
            if raw is None:
                return
            if not isinstance(raw, str) or not raw.strip():
                raise CrossLayerValidationError(f"{path} must be a non-empty string when present")
            source_refs.append((path, raw))

        regions = layout.get("regions", [])
        if not isinstance(regions, list):
            raise CrossLayerValidationError("$.regions must be an array in layout payload")
        for index, region in enumerate(regions):
            if not isinstance(region, dict):
                raise CrossLayerValidationError(f"$.regions[{index}] must be an object")
            consume_id(f"$.regions[{index}].id", region.get("id"))
            consume_optional_source_ref(f"$.regions[{index}].source_ref", region.get("source_ref"))

        slots = layout.get("slots", [])
        if not isinstance(slots, list):
            raise CrossLayerValidationError("$.slots must be an array in layout payload")
        for index, slot in enumerate(slots):
            if not isinstance(slot, dict):
                raise CrossLayerValidationError(f"$.slots[{index}] must be an object")
            consume_id(f"$.slots[{index}].id", slot.get("id"))
            consume_optional_source_ref(f"$.slots[{index}].source_ref", slot.get("source_ref"))

        groups = layout.get("groups", [])
        if isinstance(groups, list):
            for index, group in enumerate(groups):
                if isinstance(group, dict) and "id" in group:
                    consume_id(f"$.groups[{index}].id", group.get("id"))
                    consume_optional_source_ref(f"$.groups[{index}].source_ref", group.get("source_ref"))

        constraints = layout.get("constraints", [])
        if isinstance(constraints, list):
            for index, constraint in enumerate(constraints):
                if isinstance(constraint, dict) and "id" in constraint:
                    consume_id(f"$.constraints[{index}].id", constraint.get("id"))
                    consume_optional_source_ref(
                        f"$.constraints[{index}].source_ref",
                        constraint.get("source_ref"),
                    )

        diagrams = layout.get("diagrams", [])
        if not isinstance(diagrams, list):
            raise CrossLayerValidationError("$.diagrams must be an array in layout payload")
        for index, diagram in enumerate(diagrams):
            if not isinstance(diagram, dict):
                raise CrossLayerValidationError(f"$.diagrams[{index}] must be an object")
            consume_id(f"$.diagrams[{index}].id", diagram.get("id"))
            consume_optional_source_ref(f"$.diagrams[{index}].source_ref", diagram.get("source_ref"))

            objects = diagram.get("objects", [])
            if isinstance(objects, list):
                for obj_index, obj in enumerate(objects):
                    if not isinstance(obj, dict):
                        raise CrossLayerValidationError(
                            f"$.diagrams[{index}].objects[{obj_index}] must be an object"
                        )
                    consume_id(
                        f"$.diagrams[{index}].objects[{obj_index}].id",
                        obj.get("id"),
                    )
                    consume_optional_source_ref(
                        f"$.diagrams[{index}].objects[{obj_index}].source_ref",
                        obj.get("source_ref"),
                    )

            label_slots = diagram.get("label_slots", [])
            if isinstance(label_slots, list):
                for slot_index, label_slot in enumerate(label_slots):
                    if not isinstance(label_slot, dict):
                        raise CrossLayerValidationError(
                            f"$.diagrams[{index}].label_slots[{slot_index}] must be an object"
                        )
                    consume_id(
                        f"$.diagrams[{index}].label_slots[{slot_index}].id",
                        label_slot.get("id"),
                    )
                    consume_optional_source_ref(
                        f"$.diagrams[{index}].label_slots[{slot_index}].source_ref",
                        label_slot.get("source_ref"),
                    )

            diagram_constraints = diagram.get("constraints", [])
            if isinstance(diagram_constraints, list):
                for cons_index, constraint in enumerate(diagram_constraints):
                    if isinstance(constraint, dict) and "id" in constraint:
                        consume_id(
                            f"$.diagrams[{index}].constraints[{cons_index}].id",
                            constraint.get("id"),
                        )
                        consume_optional_source_ref(
                            f"$.diagrams[{index}].constraints[{cons_index}].source_ref",
                            constraint.get("source_ref"),
                        )
        return layout_ids, source_refs, "contract"

    nodes = layout.get("nodes", [])
    if not isinstance(nodes, list):
        raise CrossLayerValidationError(
            "$.layout must contain canonical regions/slots or legacy nodes array"
        )
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise CrossLayerValidationError(f"$.nodes[{index}] must be an object")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            raise CrossLayerValidationError(f"$.nodes[{index}].id must be a non-empty string")
        if node_id in layout_ids:
            raise CrossLayerValidationError(f"$.nodes[{index}].id duplicates existing node id '{node_id}'")
        layout_ids.add(node_id)
        source_ref = node.get("source_ref")
        if source_ref is not None:
            if not isinstance(source_ref, str) or not source_ref.strip():
                raise CrossLayerValidationError(
                    f"$.nodes[{index}].source_ref must be a non-empty string when present"
                )
            source_refs.append((f"$.nodes[{index}].source_ref", source_ref))
    return layout_ids, source_refs, "legacy_nodes"


def _collect_renderer_elements(renderer: dict[str, Any]) -> list[dict[str, Any]]:
    elements = renderer.get("elements")
    if not isinstance(elements, list):
        raise CrossLayerValidationError("$.elements must be an array in renderer payload")

    flat: list[dict[str, Any]] = []

    def walk(items: list[Any], path: str) -> None:
        for index, element in enumerate(items):
            current_path = f"{path}[{index}]"
            if not isinstance(element, dict):
                raise CrossLayerValidationError(f"{current_path} must be an object")
            flat.append(element)
            children = element.get("elements")
            if children is not None:
                if not isinstance(children, list):
                    raise CrossLayerValidationError(f"{current_path}.elements must be an array when present")
                walk(children, f"{current_path}.elements")

    walk(elements, "$.elements")
    return flat


def validate_contract_bundle(
    semantic: dict[str, Any],
    layout: dict[str, Any],
    renderer: dict[str, Any],
) -> None:
    semantic_ids = _collect_semantic_ids(semantic)
    required_layout_ids = _collect_required_layout_ids(semantic)
    layout_ids, layout_source_refs, layout_mode = _collect_layout_ids(layout)

    mapped_semantic_ids: set[str] = set()
    for path, source_ref in layout_source_refs:
        if source_ref not in semantic_ids:
            if semantic_ids:
                raise CrossLayerValidationError(
                    f"{path} '{source_ref}' does not match any semantic id"
                )
            raise CrossLayerValidationError(
                f"{path} '{source_ref}' cannot be validated: semantic ids are missing"
            )
        mapped_semantic_ids.add(source_ref)

    for required_id in required_layout_ids:
        if required_id not in mapped_semantic_ids and required_id not in layout_ids:
            raise CrossLayerValidationError(
                f"Required semantic id '{required_id}' has no corresponding layout representation"
            )

    renderer_elements = _collect_renderer_elements(renderer)
    for index, element in enumerate(renderer_elements):
        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id.strip():
            raise CrossLayerValidationError(f"renderer element at index {index} has invalid id")
        if layout_mode == "legacy_nodes":
            if element_id not in layout_ids:
                raise CrossLayerValidationError(
                    f"renderer element id '{element_id}' does not map to any layout node id"
                )
        else:
            refs = element.get("refs")
            ref_ids: list[str] = []
            if isinstance(refs, dict):
                for key in ("layout_slot_id", "layout_object_id", "layout_diagram_id", "layout_node_id"):
                    raw = refs.get(key)
                    if raw is None:
                        continue
                    if not isinstance(raw, str) or not raw.strip():
                        raise CrossLayerValidationError(
                            f"renderer element '{element_id}' refs.{key} must be a non-empty string when present"
                        )
                    ref_ids.append(raw)
            if not ref_ids:
                # Compatibility escape hatch: allow direct id mapping if present.
                if element_id not in layout_ids:
                    raise CrossLayerValidationError(
                        f"renderer element '{element_id}' must reference layout via refs.layout_*_id in canonical layout"
                    )
            else:
                for ref_id in ref_ids:
                    if ref_id not in layout_ids:
                        raise CrossLayerValidationError(
                            f"renderer element '{element_id}' refs references unknown layout id '{ref_id}'"
                        )

        source_ref = element.get("source_ref")
        if source_ref is not None:
            if not isinstance(source_ref, str) or not source_ref.strip():
                raise CrossLayerValidationError(
                    f"renderer element '{element_id}' has invalid source_ref (expected non-empty string)"
                )
            if source_ref not in layout_ids and source_ref not in semantic_ids:
                raise CrossLayerValidationError(
                    f"renderer element '{element_id}' source_ref '{source_ref}' "
                    "must reference a layout id or semantic id"
                )

        attributes = element.get("attributes")
        if isinstance(attributes, dict) and "source_ref" in attributes:
            attr_source_ref = attributes.get("source_ref")
            if not isinstance(attr_source_ref, str) or not attr_source_ref.strip():
                raise CrossLayerValidationError(
                    f"renderer element '{element_id}' attributes.source_ref must be a non-empty string"
                )
            if attr_source_ref not in layout_ids and attr_source_ref not in semantic_ids:
                raise CrossLayerValidationError(
                    f"renderer element '{element_id}' attributes.source_ref '{attr_source_ref}' "
                    "must reference a layout id or semantic id"
                )
