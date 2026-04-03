from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ValidationIssue:
    level: str
    code: str
    message: str


class SchemaValidator:
    REQUIRED_ROOT = ("schema_version", "problem_id", "problem_type", "metadata", "domain", "render", "answer")
    REQUIRED_RENDER = ("canvas", "elements")
    REQUIRED_CANVAS = ("width", "height", "background")
    ELEMENT_TYPES = {"text", "rect", "line", "circle", "polygon", "path", "arc", "image"}

    def validate(self, semantic: dict[str, Any]) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not isinstance(semantic, dict):
            return [ValidationIssue("error", "schema.root_type", "semantic must be object")]

        for key in self.REQUIRED_ROOT:
            if key not in semantic:
                issues.append(ValidationIssue("error", "schema.missing_root", f"missing root key: {key}"))

        render = semantic.get("render", {})
        if not isinstance(render, dict):
            issues.append(ValidationIssue("error", "schema.render_type", "render must be object"))
            return issues

        for key in self.REQUIRED_RENDER:
            if key not in render:
                issues.append(ValidationIssue("error", "schema.missing_render", f"missing render key: {key}"))

        canvas = render.get("canvas", {})
        if isinstance(canvas, dict):
            for key in self.REQUIRED_CANVAS:
                if key not in canvas:
                    issues.append(ValidationIssue("error", "schema.missing_canvas", f"missing canvas key: {key}"))

        elements = render.get("elements", [])
        if not isinstance(elements, list) or not elements:
            issues.append(ValidationIssue("error", "schema.elements_empty", "render.elements must be non-empty list"))
            return issues

        seen_ids: set[str] = set()
        for idx, elem in enumerate(elements):
            if not isinstance(elem, dict):
                issues.append(ValidationIssue("error", "schema.element_type", f"elements[{idx}] must be object"))
                continue

            elem_id = elem.get("id")
            if not isinstance(elem_id, str) or not elem_id:
                issues.append(ValidationIssue("error", "schema.element_id", f"elements[{idx}] invalid id"))
            elif elem_id in seen_ids:
                issues.append(ValidationIssue("error", "schema.element_id_dup", f"duplicate element id: {elem_id}"))
            else:
                seen_ids.add(elem_id)

            elem_type = elem.get("type")
            if elem_type not in self.ELEMENT_TYPES:
                issues.append(ValidationIssue("error", "schema.element_type_value", f"unsupported type: {elem_type}"))

            role = elem.get("semantic_role")
            if not isinstance(role, str) or not role:
                issues.append(ValidationIssue("error", "schema.semantic_role", f"elements[{idx}] missing semantic_role"))

        return issues
