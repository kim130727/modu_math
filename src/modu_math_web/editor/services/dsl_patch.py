from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import libcst as cst

from .problems import resolve_problem_paths

SUPPORTED_SLOTS = {
    "TextSlot": {"text", "x", "y", "font_size"},
    "CircleSlot": {"cx", "cy", "r"},
    "LineSlot": {"x1", "y1", "x2", "y2"},
    "RectSlot": {"x", "y", "width", "height"},
    "PolygonSlot": {"points"},
}


@dataclass
class AppliedPatch:
    target: str
    op: str
    fields: list[str]


class DslPatchError(ValueError):
    pass


def _arg_value_to_cst(value: Any) -> cst.BaseExpression:
    if isinstance(value, str):
        return cst.SimpleString(repr(value))
    if isinstance(value, bool):
        return cst.Name("True" if value else "False")
    if isinstance(value, int):
        return cst.Integer(str(value))
    if isinstance(value, float):
        return cst.Float(repr(value))
    if value is None:
        return cst.Name("None")
    if isinstance(value, list):
        return cst.List([cst.Element(_arg_value_to_cst(v)) for v in value])
    if isinstance(value, tuple):
        return cst.Tuple([cst.Element(_arg_value_to_cst(v)) for v in value])
    raise DslPatchError(f"unsupported value type: {type(value).__name__}")


def _call_name(node: cst.Call) -> str | None:
    if isinstance(node.func, cst.Name):
        return node.func.value
    return None


def _keyword_arg(call: cst.Call, name: str) -> cst.Arg | None:
    for arg in call.args:
        if arg.keyword and arg.keyword.value == name:
            return arg
    return None


class SlotUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        slot_type = _call_name(original_node)
        if slot_type not in SUPPORTED_SLOTS:
            return updated_node

        id_arg = _keyword_arg(original_node, "id")
        if id_arg is None or not isinstance(id_arg.value, cst.SimpleString):
            return updated_node

        try:
            slot_id = cst.parse_expression(id_arg.value.value).evaluated_value
        except Exception:
            return updated_node

        if slot_id != self.target:
            return updated_node

        allowed = SUPPORTED_SLOTS[slot_type]
        invalid = sorted(set(self.fields) - allowed)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for {slot_type}: {', '.join(invalid)}")

        args = list(updated_node.args)
        for field_name, field_value in self.fields.items():
            replacement = cst.Arg(keyword=cst.Name(field_name), value=_arg_value_to_cst(field_value))
            replaced = False
            for idx, arg in enumerate(args):
                if arg.keyword and arg.keyword.value == field_name:
                    args[idx] = replacement
                    replaced = True
                    break
            if not replaced:
                args.append(replacement)

        self.updated = True
        return updated_node.with_changes(args=tuple(args))


def apply_layout_patches(problem_id: str, patches: list[dict[str, Any]]) -> tuple[str, list[AppliedPatch]]:
    paths = resolve_problem_paths(problem_id)
    source = paths.dsl_path.read_text(encoding="utf-8")
    module = cst.parse_module(source)

    applied: list[AppliedPatch] = []
    transformed = module

    for patch in patches:
        target = patch.get("target")
        op = patch.get("op")
        value = patch.get("value")
        if op != "update":
            raise DslPatchError("only 'update' op is supported")
        if not isinstance(target, str) or not target:
            raise DslPatchError("patch target must be a non-empty string")
        if not isinstance(value, dict):
            raise DslPatchError("patch value must be an object")

        updater = SlotUpdater(target=target, fields=value)
        transformed = transformed.visit(updater)
        if not updater.updated:
            raise DslPatchError(f"target slot not found: {target}")

        applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))

    updated_code = transformed.code
    paths.dsl_path.write_text(updated_code, encoding="utf-8")
    return updated_code, applied
