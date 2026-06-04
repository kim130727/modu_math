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
    "PathSlot": {"d"},
}
FRACTION_SLOT_PARTS = {"num", "bar", "den"}
FRACTION_MOVE_FIELDS = {"move_dx", "move_dy"}


@dataclass
class AppliedPatch:
    target: str
    op: str
    fields: list[str]


class DslPatchError(ValueError):
    pass


def _normalize_slot_id(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


class SlotIdCollector(cst.CSTVisitor):
    def __init__(self) -> None:
        self.slot_ids: set[str] = set()

    def visit_Call(self, node: cst.Call) -> None:
        slot_type = _call_name(node)
        if slot_type not in SUPPORTED_SLOTS:
            return
        id_arg = _keyword_arg(node, "id")
        if id_arg is None or not isinstance(id_arg.value, cst.SimpleString):
            return
        try:
            slot_id = cst.parse_expression(id_arg.value.value).evaluated_value
        except Exception:
            return
        if isinstance(slot_id, str) and slot_id:
            self.slot_ids.add(slot_id)


def _resolve_target_slot_id(module: cst.Module, target: str) -> str:
    collector = SlotIdCollector()
    module.visit(collector)
    if target in collector.slot_ids:
        return target
    norm_target = _normalize_slot_id(target)
    candidates = [sid for sid in collector.slot_ids if _normalize_slot_id(sid) == norm_target]
    if len(candidates) == 1:
        return candidates[0]
    # Allow unique prefix matching for shorthand ids like "slot.q".
    prefix_candidates = [sid for sid in collector.slot_ids if sid.startswith(target)]
    if len(prefix_candidates) == 1:
        return prefix_candidates[0]
    norm_prefix_candidates = [sid for sid in collector.slot_ids if _normalize_slot_id(sid).startswith(norm_target)]
    if len(norm_prefix_candidates) == 1:
        return norm_prefix_candidates[0]
    return target


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


def _shift_numeric_expr(expr: cst.BaseExpression, delta: float) -> cst.BaseExpression:
    if delta == 0:
        return expr
    code = cst.Module([]).code_for_node(expr)
    return cst.parse_expression(f"({code}) + ({repr(delta)})")


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


class FractionSlotsUpdater(cst.CSTTransformer):
    def __init__(self, target_prefix: str, fields: dict[str, Any]):
        self.target_prefix = target_prefix
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        slot_type = _call_name(original_node)
        if slot_type != "fraction_slots":
            return updated_node

        prefix_arg = _keyword_arg(original_node, "id_prefix")
        if prefix_arg is None or not isinstance(prefix_arg.value, cst.SimpleString):
            return updated_node

        try:
            id_prefix = cst.parse_expression(prefix_arg.value.value).evaluated_value
        except Exception:
            return updated_node
        if id_prefix != self.target_prefix:
            return updated_node

        invalid = sorted(set(self.fields) - FRACTION_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for fraction_slots: {', '.join(invalid)}")

        move_dx = float(self.fields.get("move_dx", 0.0))
        move_dy = float(self.fields.get("move_dy", 0.0))

        args = list(updated_node.args)
        kw_to_index: dict[str, int] = {}
        for idx, arg in enumerate(args):
            if arg.keyword:
                kw_to_index[arg.keyword.value] = idx

        required = ("x", "numerator_y", "bar_y", "denominator_y")
        missing = [name for name in required if name not in kw_to_index]
        if missing:
            raise DslPatchError(f"fraction_slots missing required arg(s): {', '.join(missing)}")

        def _replace_numeric_arg(name: str, delta: float) -> None:
            idx = kw_to_index[name]
            original = args[idx]
            args[idx] = cst.Arg(keyword=cst.Name(name), value=_shift_numeric_expr(original.value, delta))

        _replace_numeric_arg("x", move_dx)
        _replace_numeric_arg("numerator_y", move_dy)
        _replace_numeric_arg("bar_y", move_dy)
        _replace_numeric_arg("denominator_y", move_dy)

        self.updated = True
        return updated_node.with_changes(args=tuple(args))


class SlotDeleteTransformer(cst.CSTTransformer):
    def __init__(self, target: str):
        self.target = target
        self.deleted_slot = False
        self.cleaned_refs = False

    def leave_Element(
        self, original_node: cst.Element, updated_node: cst.Element
    ) -> cst.Element | cst.RemovalSentinel:
        val = original_node.value
        if isinstance(val, cst.Call):
            slot_type = _call_name(val)
            if slot_type in SUPPORTED_SLOTS:
                id_arg = _keyword_arg(val, "id")
                if id_arg is not None and isinstance(id_arg.value, cst.SimpleString):
                    try:
                        slot_id = cst.parse_expression(id_arg.value.value).evaluated_value
                    except Exception:
                        slot_id = None
                    if slot_id == self.target:
                        self.deleted_slot = True
                        return cst.RemoveFromParent()
        return updated_node

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        # Region(..., slot_ids=(...)) 참조 정리
        slot_type = _call_name(original_node)
        if slot_type == "Region":
            changed = False
            args = list(updated_node.args)
            for idx, arg in enumerate(args):
                if not arg.keyword or arg.keyword.value != "slot_ids":
                    continue
                val = arg.value
                if isinstance(val, cst.Tuple):
                    new_elems: list[cst.Element] = []
                    for el in val.elements:
                        if el is None:
                            continue
                        v = el.value
                        if isinstance(v, cst.SimpleString):
                            try:
                                sid = cst.parse_expression(v.value).evaluated_value
                            except Exception:
                                sid = None
                            if sid == self.target:
                                changed = True
                                self.cleaned_refs = True
                                continue
                        new_elems.append(el)
                    args[idx] = arg.with_changes(value=val.with_changes(elements=tuple(new_elems)))
                elif isinstance(val, cst.List):
                    new_elems = []
                    for el in val.elements:
                        if el is None:
                            continue
                        v = el.value
                        if isinstance(v, cst.SimpleString):
                            try:
                                sid = cst.parse_expression(v.value).evaluated_value
                            except Exception:
                                sid = None
                            if sid == self.target:
                                changed = True
                                self.cleaned_refs = True
                                continue
                        new_elems.append(el)
                    args[idx] = arg.with_changes(value=val.with_changes(elements=tuple(new_elems)))
            if changed:
                return updated_node.with_changes(args=tuple(args))
        return updated_node


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
        if not isinstance(target, str) or not target:
            raise DslPatchError("patch target must be a non-empty string")
        target = _resolve_target_slot_id(transformed, target)

        if op == "delete":
            deleter = SlotDeleteTransformer(target=target)
            transformed = transformed.visit(deleter)
            if not deleter.deleted_slot:
                raise DslPatchError(f"target slot not found: {target}")
            applied.append(AppliedPatch(target=target, op=op, fields=[]))
            continue

        if op != "update":
            raise DslPatchError("only 'update' and 'delete' ops are supported")
        if not isinstance(value, dict):
            raise DslPatchError("patch value must be an object")

        updater = SlotUpdater(target=target, fields=value)
        transformed = transformed.visit(updater)
        if updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        frac_prefix = target
        if "." in target:
            maybe_prefix, maybe_part = target.rsplit(".", 1)
            if maybe_part in FRACTION_SLOT_PARTS:
                frac_prefix = maybe_prefix

        frac_updater = FractionSlotsUpdater(target_prefix=frac_prefix, fields=value)
        transformed = transformed.visit(frac_updater)
        if frac_updater.updated:
            applied.append(AppliedPatch(target=frac_prefix, op=op, fields=list(value.keys())))
            continue

        raise DslPatchError(f"target slot not found: {target}")

    updated_code = transformed.code
    paths.dsl_path.write_text(updated_code, encoding="utf-8")
    return updated_code, applied
