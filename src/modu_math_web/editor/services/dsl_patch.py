from __future__ import annotations

import math
import re
import json
from dataclasses import dataclass
from typing import Any

import libcst as cst

from .problems import resolve_problem_paths

SUPPORTED_SLOTS = {
    "TextSlot": {"text", "x", "y", "font_size", "max_width", "font_family", "anchor", "fill", "style_role", "transform"},
    "TextBoxSlot": {"text", "x", "y", "width", "height", "font_size", "font_family", "align", "valign", "line_height", "fill", "style_role", "transform"},
    "CircleSlot": {"cx", "cy", "r", "stroke", "stroke_width", "stroke_dasharray", "fill", "transform"},
    "LineSlot": {"x1", "y1", "x2", "y2", "stroke", "stroke_width", "stroke_dasharray", "transform"},
    "RectSlot": {"x", "y", "width", "height", "stroke", "stroke_width", "stroke_dasharray", "rx", "ry", "fill", "transform"},
    "PolygonSlot": {"points", "stroke", "stroke_width", "stroke_dasharray", "fill", "transform"},
    "ImageSlot": {"href", "x", "y", "width", "height", "preserve_aspect_ratio", "transform"},
    "PathSlot": {"d", "stroke", "stroke_width", "stroke_dasharray", "fill", "transform"},
}
SLOT_KIND_TO_CTOR = {
    "text": "TextSlot",
    "text_box": "TextBoxSlot",
    "circle": "CircleSlot",
    "line": "LineSlot",
    "rect": "RectSlot",
    "polygon": "PolygonSlot",
    "image": "ImageSlot",
    "path": "PathSlot",
}
FRACTION_SLOT_PARTS = {"num", "bar", "den"}
FRACTION_MOVE_FIELDS = {"move_dx", "move_dy"}
PERSON_SLOT_PARTS = {"body", "head", "eye1", "eye2", "mouth"}
CHARACTER_MOVE_FIELDS = {"move_dx", "move_dy"}
FIGURE_MOVE_FIELDS = {"move_dx", "move_dy"}
BASE_TEN_HELPERS = {"_base_ten_model", "_partition_box"}
PAPER_FOLD_SEQUENCE_HELPERS = {"circle_fold_sequence_slots"}
PAPER_FOLD_SINGLE_HELPERS = {"folded_half_circle_slots", "opened_circle_with_fold_slots"}
GRID_HELPERS = {"_grid_slots"}
CANDIDATE_POINT_HELPERS = {"_candidate_slots"}
MEASUREMENT_TOOL_HELPERS = {"compass_on_ruler_slots"}
CANVAS_TARGETS = {"__canvas__", "canvas"}
CANVAS_FIELDS = {"width", "height"}
EDITOR_OVERRIDE_FIELDS = set().union(*SUPPORTED_SLOTS.values()) - {"move_dx", "move_dy"}


@dataclass
class AppliedPatch:
    target: str
    op: str
    fields: list[str]


class DslPatchError(ValueError):
    pass


def _normalize_slot_id(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _measurement_tool_base_from_slot_id(slot_id: str) -> str | None:
    match = re.match(r"^(slot\..+)\.(?:ruler|compass)(?:\.|$)", slot_id)
    return match.group(1) if match else None


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


def _qualified_name(node: cst.BaseExpression | None) -> str:
    if isinstance(node, cst.Name):
        return node.value
    if isinstance(node, cst.Attribute):
        prefix = _qualified_name(node.value)
        return f"{prefix}.{node.attr.value}" if prefix else node.attr.value
    return ""


class DslImportEnsurer(cst.CSTTransformer):
    def __init__(self, name: str):
        self.name = name
        self.saw_dsl_import = False
        self.changed = False

    def leave_ImportFrom(self, original_node: cst.ImportFrom, updated_node: cst.ImportFrom) -> cst.ImportFrom:
        if _qualified_name(original_node.module) != "modu_math.dsl":
            return updated_node
        self.saw_dsl_import = True
        if isinstance(updated_node.names, cst.ImportStar):
            return updated_node

        names = list(updated_node.names)
        for alias in names:
            if isinstance(alias.name, cst.Name) and alias.name.value == self.name:
                return updated_node

        names.append(cst.ImportAlias(name=cst.Name(self.name)))
        self.changed = True
        return updated_node.with_changes(names=tuple(names))

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        if self.saw_dsl_import:
            return updated_node

        import_stmt = cst.parse_statement(f"from modu_math.dsl import {self.name}\n")
        body = list(updated_node.body)
        insert_at = 0
        while insert_at < len(body):
            stmt = body[insert_at]
            if (
                isinstance(stmt, cst.SimpleStatementLine)
                and stmt.body
                and isinstance(stmt.body[0], cst.ImportFrom)
                and _qualified_name(stmt.body[0].module) == "__future__"
            ):
                insert_at += 1
                continue
            break
        body.insert(insert_at, import_stmt)
        self.changed = True
        return updated_node.with_changes(body=tuple(body))


def _ensure_dsl_import(module: cst.Module, name: str) -> cst.Module:
    ensurer = DslImportEnsurer(name)
    return module.visit(ensurer)


def _keyword_arg(call: cst.Call, name: str) -> cst.Arg | None:
    for arg in call.args:
        if arg.keyword and arg.keyword.value == name:
            return arg
    return None


def _keyword_index(args: list[cst.Arg], name: str) -> int | None:
    for idx, arg in enumerate(args):
        if arg.keyword and arg.keyword.value == name:
            return idx
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


class CanvasUpdater(cst.CSTTransformer):
    def __init__(self, fields: dict[str, Any]):
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if self.updated or _call_name(original_node) != "Canvas":
            return updated_node

        invalid = sorted(set(self.fields) - CANVAS_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for Canvas: {', '.join(invalid)}")

        args = list(updated_node.args)
        for field_name, field_value in self.fields.items():
            _replace_or_append_arg(args, field_name, int(field_value))

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


def _replace_or_append_arg(args: list[cst.Arg], name: str, value: Any) -> None:
    replacement = cst.Arg(keyword=cst.Name(name), value=_arg_value_to_cst(value))
    for idx, arg in enumerate(args):
        if arg.keyword and arg.keyword.value == name:
            args[idx] = replacement
            return
    args.append(replacement)


def _shift_or_append_numeric_arg(args: list[cst.Arg], name: str, delta: float, default: float | None = None) -> bool:
    if delta == 0 and default is None:
        return False
    for idx, arg in enumerate(args):
        if arg.keyword and arg.keyword.value == name:
            args[idx] = cst.Arg(keyword=cst.Name(name), value=_shift_numeric_expr(arg.value, delta))
            return True
    if default is not None:
        args.append(cst.Arg(keyword=cst.Name(name), value=_arg_value_to_cst(default + delta)))
        return True
    return False


def _shift_slot_call_args(args: list[cst.Arg], slot_type: str, dx: float, dy: float) -> bool:
    changed = False
    if slot_type in {"TextSlot", "TextBoxSlot", "RectSlot"}:
        changed = _shift_or_append_numeric_arg(args, "x", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "y", dy) or changed
    elif slot_type == "CircleSlot":
        changed = _shift_or_append_numeric_arg(args, "cx", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "cy", dy) or changed
    elif slot_type == "LineSlot":
        for name, delta in (("x1", dx), ("x2", dx), ("y1", dy), ("y2", dy)):
            changed = _shift_or_append_numeric_arg(args, name, delta) or changed
    return changed


def _first_string_arg(call: cst.Call, keyword_name: str) -> str | None:
    arg: cst.Arg | None = None
    if call.args and call.args[0].keyword is None:
        arg = call.args[0]
    else:
        arg = _keyword_arg(call, keyword_name)
    if arg is None or not isinstance(arg.value, cst.SimpleString):
        return None
    try:
        value = cst.parse_expression(arg.value.value).evaluated_value
    except Exception:
        return None
    return value if isinstance(value, str) else None


def _path_number_bounds(d: str) -> tuple[float, float, float, float] | None:
    numbers = [float(m.group(0)) for m in re.finditer(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", d)]
    if len(numbers) < 4:
        return None
    xs = numbers[0::2]
    ys = numbers[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def _editor_overrides_path(paths: Any):
    return paths.base_dir / f"{paths.artifact_base}.editor_overrides.json"


def _save_editor_slot_override(paths: Any, target: str, fields: dict[str, Any]) -> None:
    invalid = sorted(set(fields) - EDITOR_OVERRIDE_FIELDS)
    if invalid:
        raise DslPatchError(f"unsupported override field(s): {', '.join(invalid)}")
    path = _editor_overrides_path(paths)
    data: dict[str, Any] = {}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(loaded, dict):
            data = loaded
    slots = data.setdefault("slots", {})
    if not isinstance(slots, dict):
        slots = {}
        data["slots"] = slots
    current = slots.setdefault(target, {})
    if not isinstance(current, dict):
        current = {}
        slots[target] = current
    current.update(fields)
    data["version"] = 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _save_editor_slot_delete(paths: Any, target: str) -> None:
    path = _editor_overrides_path(paths)
    data: dict[str, Any] = {}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(loaded, dict):
            data = loaded
    deleted = data.setdefault("deleted_slots", [])
    if not isinstance(deleted, list):
        deleted = []
        data["deleted_slots"] = deleted
    if target not in deleted:
        deleted.append(target)
    slots = data.get("slots")
    if isinstance(slots, dict):
        slots.pop(target, None)
    data["version"] = 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _save_editor_region_slot_order(paths: Any, region_id: str, slot_ids: list[Any]) -> None:
    clean_slot_ids = [slot_id for slot_id in slot_ids if isinstance(slot_id, str) and slot_id]
    if not region_id or not clean_slot_ids:
        raise DslPatchError("layer patch requires value.region_id and non-empty value.slot_ids")
    path = _editor_overrides_path(paths)
    data: dict[str, Any] = {}
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(loaded, dict):
            data = loaded
    orders = data.setdefault("region_slot_orders", {})
    if not isinstance(orders, dict):
        orders = {}
        data["region_slot_orders"] = orders
    orders[region_id] = clean_slot_ids
    data["version"] = 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _circle_helper_prefix(target: str, helper_name: str) -> str | None:
    suffixes = {
        "folded_half_circle_slots": (".paper", ".edge"),
        "opened_circle_with_fold_slots": (".paper", ".fold_line"),
    }[helper_name]
    for suffix in suffixes:
        if target.endswith(suffix):
            return target[: -len(suffix)]
    return target


def _function_contains_single_paper_helper(function_node: cst.FunctionDef, target: str) -> bool:
    class Finder(cst.CSTVisitor):
        def __init__(self) -> None:
            self.found = False

        def visit_Call(self, node: cst.Call) -> None:
            call_name = _call_name(node)
            if call_name not in PAPER_FOLD_SINGLE_HELPERS:
                return
            prefix = _first_string_arg(node, "prefix")
            if prefix is not None and _circle_helper_prefix(target, call_name) == prefix:
                self.found = True

    finder = Finder()
    function_node.visit(finder)
    return finder.found


def _generated_slot_override_statement(target: str, fields: dict[str, Any]) -> cst.BaseStatement:
    replacements = ", ".join(f"{name}={repr(value)}" for name, value in fields.items())
    code = f"slots = tuple(replace(slot, {replacements}) if slot.id == {target!r} else slot for slot in slots)"
    return cst.parse_statement(code)


class GeneratedHelperSlotOverrideUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def _is_target_slot_test(self, test: cst.BaseExpression) -> bool:
        code = cst.Module([]).code_for_node(test)
        return code in {f"slot.id == {self.target!r}", f"{self.target!r} == slot.id"}

    def leave_IfExp(self, original_node: cst.IfExp, updated_node: cst.IfExp) -> cst.BaseExpression:
        if not self._is_target_slot_test(original_node.test):
            return updated_node
        if not isinstance(updated_node.body, cst.Call) or _call_name(updated_node.body) != "replace":
            return updated_node
        args = list(updated_node.body.args)
        for name, value in self.fields.items():
            _replace_or_append_arg(args, name, value)
        self.updated = True
        return updated_node.with_changes(body=updated_node.body.with_changes(args=tuple(args)))

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        if self.updated or not _function_contains_single_paper_helper(original_node, self.target):
            return updated_node
        if "d" not in self.fields:
            return updated_node

        invalid = sorted(set(self.fields) - {"d", "transform", "stroke", "stroke_width", "fill"})
        if invalid:
            return updated_node

        body = list(updated_node.body.body)
        insert_at = next((idx for idx, stmt in enumerate(body) if isinstance(stmt, cst.SimpleStatementLine) and any(isinstance(item, cst.Return) for item in stmt.body)), None)
        if insert_at is None:
            return updated_node
        body.insert(insert_at, _generated_slot_override_statement(self.target, self.fields))
        self.updated = True
        return updated_node.with_changes(body=updated_node.body.with_changes(body=tuple(body)))


class SinglePaperFoldHelperUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        call_name = _call_name(original_node)
        if call_name not in PAPER_FOLD_SINGLE_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix is None or _circle_helper_prefix(self.target, call_name) != prefix:
            return updated_node

        invalid = sorted(set(self.fields) - {"cx", "cy", "r", "d", "x1", "y1", "x2", "y2", "transform"})
        if invalid:
            raise DslPatchError(f"unsupported field(s) for paper fold helper: {', '.join(invalid)}")

        updates: dict[str, float] = {}
        if {"cx", "cy", "r"} & set(self.fields):
            for name in ("cx", "cy", "r"):
                if name in self.fields:
                    updates[name] = float(self.fields[name])

        if "d" in self.fields and isinstance(self.fields["d"], str):
            bounds = _path_number_bounds(self.fields["d"])
            if bounds is not None:
                min_x, min_y, max_x, max_y = bounds
                updates["cx"] = (min_x + max_x) / 2.0
                updates["r"] = max(2.0, (max_x - min_x) / 2.0)
                if call_name == "folded_half_circle_slots":
                    updates["cy"] = min_y
                else:
                    updates["cy"] = (min_y + max_y) / 2.0

        if {"x1", "y1", "x2", "y2"}.issubset(self.fields):
            x1 = float(self.fields["x1"])
            y1 = float(self.fields["y1"])
            x2 = float(self.fields["x2"])
            y2 = float(self.fields["y2"])
            updates["cx"] = (x1 + x2) / 2.0
            updates["cy"] = (y1 + y2) / 2.0
            updates["r"] = max(2.0, math.hypot(x2 - x1, y2 - y1) / 2.0)
            if call_name == "opened_circle_with_fold_slots":
                updates["angle"] = math.degrees(math.atan2(y2 - y1, x2 - x1))

        if not updates:
            return updated_node

        args = list(updated_node.args)
        for name, value in updates.items():
            _replace_or_append_arg(args, name, value)
        self.updated = True
        return updated_node.with_changes(args=tuple(args))


def _person_anchor_from_patch(part: str, fields: dict[str, Any]) -> tuple[float | None, float | None]:
    cx: float | None = None
    head_cy: float | None = None

    if part == "body":
        if "x" in fields:
            cx = float(fields["x"]) + 15.0
        if "y" in fields:
            head_cy = float(fields["y"]) - 20.0
    elif part == "head":
        if "cx" in fields:
            cx = float(fields["cx"])
        if "cy" in fields:
            head_cy = float(fields["cy"])
    elif part == "eye1":
        if "cx" in fields:
            cx = float(fields["cx"]) + 8.0
        if "cy" in fields:
            head_cy = float(fields["cy"]) + 3.0
    elif part == "eye2":
        if "cx" in fields:
            cx = float(fields["cx"]) - 8.0
        if "cy" in fields:
            head_cy = float(fields["cy"]) + 3.0
    elif part == "mouth":
        if "x1" in fields and "x2" in fields:
            cx = (float(fields["x1"]) + float(fields["x2"])) / 2.0
        if "y1" in fields:
            head_cy = float(fields["y1"]) - 10.0

    return cx, head_cy


class PersonSlotsUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if _call_name(original_node) != "person_slots":
            return updated_node

        if "." not in self.target:
            return updated_node
        target_prefix, part = self.target.rsplit(".", 1)
        if part not in PERSON_SLOT_PARTS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix != target_prefix:
            return updated_node

        cx, head_cy = _person_anchor_from_patch(part, self.fields)
        if cx is None and head_cy is None:
            return updated_node

        args = list(updated_node.args)
        if cx is not None:
            _replace_or_append_arg(args, "cx", cx)
        if head_cy is not None:
            _replace_or_append_arg(args, "head_cy", head_cy)

        self.updated = True
        return updated_node.with_changes(args=tuple(args))


def _character_group_key(target: str) -> str | None:
    prefix = "slot.character."
    if not target.startswith(prefix):
        return None
    key = target[len(prefix) :]
    return key or None


def _speaker_name_y_default(call_name: str) -> float:
    return 242.0 if call_name == "comparison_speaker" else 383.0


class CharacterGroupMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.key = _character_group_key(target)
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if not self.key:
            return updated_node

        invalid = sorted(set(self.fields) - CHARACTER_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for character group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        call_name = _call_name(original_node)
        args = list(updated_node.args)

        if call_name in {"SpeakerSpec", "comparison_speaker"}:
            key_arg = _keyword_arg(original_node, "key")
            if key_arg is None or _string_literal_value(key_arg.value) != self.key:
                return updated_node
            changed = False
            changed = _shift_or_append_numeric_arg(args, "cx", dx) or changed
            changed = _shift_or_append_numeric_arg(args, "bubble_cy", dy) or changed
            changed = _shift_or_append_numeric_arg(args, "head_cy", dy) or changed
            changed = _shift_or_append_numeric_arg(args, "tail_y", dy) or changed
            changed = _shift_or_append_numeric_arg(args, "name_y", dy, _speaker_name_y_default(call_name)) or changed
            if changed:
                self.updated = True
                return updated_node.with_changes(args=tuple(args))
            return updated_node

        if call_name == "character_body_slots":
            prefix = _first_string_arg(original_node, "prefix")
            if prefix != f"slot.person_{self.key}":
                return updated_node
            changed = False
            changed = _shift_or_append_numeric_arg(args, "cx", dx) or changed
            changed = _shift_or_append_numeric_arg(args, "head_cy", dy) or changed
            if changed:
                self.updated = True
                return updated_node.with_changes(args=tuple(args))
            return updated_node

        if call_name == "character_hand_slots":
            prefix = _first_string_arg(original_node, "prefix")
            if prefix != f"slot.person_{self.key}":
                return updated_node
            changed = False
            changed = _shift_or_append_numeric_arg(args, "card_x", dx) or changed
            changed = _shift_or_append_numeric_arg(args, "card_y", dy) or changed
            if changed:
                self.updated = True
                return updated_node.with_changes(args=tuple(args))
            return updated_node

        if call_name in SUPPORTED_SLOTS:
            id_arg = _keyword_arg(original_node, "id")
            if id_arg is None or not isinstance(id_arg.value, cst.SimpleString):
                return updated_node
            try:
                slot_id = cst.parse_expression(id_arg.value.value).evaluated_value
            except Exception:
                return updated_node
            if not isinstance(slot_id, str):
                return updated_node
            if not (
                slot_id == f"slot.name_{self.key}"
                or slot_id.startswith(f"slot.name_{self.key}_")
                or slot_id == f"slot.card_{self.key}"
                or slot_id.startswith(f"slot.card_{self.key}_")
            ):
                return updated_node
            if _shift_slot_call_args(args, call_name, dx, dy):
                self.updated = True
                return updated_node.with_changes(args=tuple(args))

        return updated_node


class FigureGroupMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        call_name = _call_name(original_node)
        if call_name not in BASE_TEN_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "slot_id")
        if prefix != self.target:
            return updated_node

        invalid = sorted(set(self.fields) - FIGURE_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for figure group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        args = list(updated_node.args)
        changed = False

        if len(args) >= 3 and args[1].keyword is None and args[2].keyword is None:
            args[1] = cst.Arg(value=_shift_numeric_expr(args[1].value, dx))
            args[2] = cst.Arg(value=_shift_numeric_expr(args[2].value, dy))
            changed = True
        else:
            changed = _shift_or_append_numeric_arg(args, "x", dx) or changed
            changed = _shift_or_append_numeric_arg(args, "y", dy) or changed

        if changed:
            self.updated = True
            return updated_node.with_changes(args=tuple(args))
        return updated_node


class PaperFoldSequenceMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        call_name = _call_name(original_node)
        if call_name not in PAPER_FOLD_SEQUENCE_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix != self.target:
            return updated_node

        invalid = sorted(set(self.fields) - FIGURE_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for paper fold group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        args = list(updated_node.args)
        changed = False
        changed = _shift_or_append_numeric_arg(args, "x", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "y", dy) or changed

        if changed:
            self.updated = True
            return updated_node.with_changes(args=tuple(args))
        return updated_node


class MeasurementToolMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if _call_name(original_node) not in MEASUREMENT_TOOL_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix != self.target:
            return updated_node

        invalid = sorted(set(self.fields) - FIGURE_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for measurement tool group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        args = list(updated_node.args)
        changed = False
        changed = _shift_or_append_numeric_arg(args, "x", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "y", dy) or changed

        if changed:
            self.updated = True
            return updated_node.with_changes(args=tuple(args))
        return updated_node


class GridSlotsMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if _call_name(original_node) not in GRID_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix != self.target:
            return updated_node

        invalid = sorted(set(self.fields) - FIGURE_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for grid group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        args = list(updated_node.args)
        changed = False
        changed = _shift_or_append_numeric_arg(args, "x", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "y", dy) or changed

        if changed:
            self.updated = True
            return updated_node.with_changes(args=tuple(args))
        return updated_node


class CandidatePointMoveUpdater(cst.CSTTransformer):
    def __init__(self, target: str, fields: dict[str, Any]):
        self.target = target
        self.fields = fields
        self.updated = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        if _call_name(original_node) not in CANDIDATE_POINT_HELPERS:
            return updated_node

        prefix = _first_string_arg(original_node, "prefix")
        if prefix != self.target:
            return updated_node

        invalid = sorted(set(self.fields) - FIGURE_MOVE_FIELDS)
        if invalid:
            raise DslPatchError(f"unsupported field(s) for candidate point group: {', '.join(invalid)}")

        dx = float(self.fields.get("move_dx", 0.0))
        dy = float(self.fields.get("move_dy", 0.0))
        args = list(updated_node.args)
        changed = False
        changed = _shift_or_append_numeric_arg(args, "origin_x", dx) or changed
        changed = _shift_or_append_numeric_arg(args, "origin_y", dy) or changed

        if changed:
            self.updated = True
            return updated_node.with_changes(args=tuple(args))
        return updated_node


def _string_literal_value(expr: cst.BaseExpression) -> str | None:
    if not isinstance(expr, cst.SimpleString):
        return None
    try:
        value = cst.parse_expression(expr.value).evaluated_value
    except Exception:
        return None
    return value if isinstance(value, str) else None


def _slot_call_from_value(slot_id: str, value: dict[str, Any]) -> cst.Call:
    kind = value.get("kind")
    if not isinstance(kind, str):
        raise DslPatchError("add patch value.kind must be a string")
    ctor = SLOT_KIND_TO_CTOR.get(kind)
    if ctor is None:
        raise DslPatchError(f"unsupported slot kind for add: {kind}")

    content = value.get("content")
    if not isinstance(content, dict):
        raise DslPatchError("add patch value.content must be an object")

    allowed = SUPPORTED_SLOTS[ctor]
    invalid = sorted(set(content) - allowed)
    if invalid:
        raise DslPatchError(f"unsupported field(s) for {ctor}: {', '.join(invalid)}")

    args = [
        cst.Arg(keyword=cst.Name("id"), value=_arg_value_to_cst(slot_id)),
        cst.Arg(keyword=cst.Name("prompt"), value=_arg_value_to_cst(value.get("prompt", ""))),
    ]
    for field_name, field_value in content.items():
        if field_value is not None:
            args.append(cst.Arg(keyword=cst.Name(field_name), value=_arg_value_to_cst(field_value)))
    return cst.Call(func=cst.Name(ctor), args=tuple(args))


def _tuple_with_appended_value(expr: cst.BaseExpression, value: cst.BaseExpression) -> cst.Tuple:
    if isinstance(expr, cst.Tuple):
        elements = list(expr.elements)
    else:
        elements = [cst.Element(expr)]
    elements.append(cst.Element(value))
    return cst.Tuple(elements=tuple(elements))


def _region_matches(region_call: cst.Call, region_id: str | None) -> bool:
    if region_id:
        id_arg = _keyword_arg(region_call, "id")
        return id_arg is not None and _string_literal_value(id_arg.value) == region_id

    role_arg = _keyword_arg(region_call, "role")
    role = _string_literal_value(role_arg.value) if role_arg else None
    return role == "diagram"


class SlotAddTransformer(cst.CSTTransformer):
    def __init__(self, target: str, value: dict[str, Any]):
        self.target = target
        self.value = value
        self.added_slot = False
        self.added_region_ref = False

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.BaseExpression:
        slot_type = _call_name(original_node)
        if slot_type != "ProblemTemplate":
            return updated_node

        args = list(updated_node.args)
        slots_idx = _keyword_index(args, "slots")
        if slots_idx is None:
            raise DslPatchError("ProblemTemplate missing slots argument")

        slot_call = _slot_call_from_value(self.target, self.value)
        slots_arg = args[slots_idx]
        args[slots_idx] = slots_arg.with_changes(value=_tuple_with_appended_value(slots_arg.value, slot_call))
        self.added_slot = True

        region_id = self.value.get("region_id")
        if region_id is not None and not isinstance(region_id, str):
            raise DslPatchError("add patch value.region_id must be a string")

        regions_idx = _keyword_index(args, "regions")
        if regions_idx is not None and isinstance(args[regions_idx].value, cst.Tuple):
            regions_arg = args[regions_idx]
            new_region_elements: list[cst.Element] = []
            for el in regions_arg.value.elements:
                region_value = el.value
                if not isinstance(region_value, cst.Call) or _call_name(region_value) != "Region":
                    new_region_elements.append(el)
                    continue
                if not self.added_region_ref and _region_matches(region_value, region_id):
                    region_args = list(region_value.args)
                    slot_ids_idx = _keyword_index(region_args, "slot_ids")
                    if slot_ids_idx is None:
                        region_args.append(
                            cst.Arg(
                                keyword=cst.Name("slot_ids"),
                                value=cst.Tuple(elements=(cst.Element(_arg_value_to_cst(self.target)),)),
                            )
                        )
                    else:
                        slot_ids_arg = region_args[slot_ids_idx]
                        region_args[slot_ids_idx] = slot_ids_arg.with_changes(
                            value=_tuple_with_appended_value(slot_ids_arg.value, _arg_value_to_cst(self.target))
                        )
                    region_value = region_value.with_changes(args=tuple(region_args))
                    self.added_region_ref = True
                new_region_elements.append(el.with_changes(value=region_value))
            args[regions_idx] = regions_arg.with_changes(
                value=regions_arg.value.with_changes(elements=tuple(new_region_elements))
            )

        if regions_idx is not None and not self.added_region_ref:
            raise DslPatchError(f"target region not found: {region_id or 'diagram'}")

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
    if not source.strip():
        raise DslPatchError("DSL file is empty; restore or save a valid DSL before editing layout")
    module = cst.parse_module(source)

    applied: list[AppliedPatch] = []
    transformed = module

    for patch in patches:
        target = patch.get("target")
        op = patch.get("op")
        value = patch.get("value")
        if not isinstance(target, str) or not target:
            raise DslPatchError("patch target must be a non-empty string")

        if op == "delete":
            target = _resolve_target_slot_id(transformed, target)
            deleter = SlotDeleteTransformer(target=target)
            transformed = transformed.visit(deleter)
            if not deleter.deleted_slot:
                _save_editor_slot_delete(paths, target)
                applied.append(AppliedPatch(target=target, op=op, fields=[]))
                continue
            applied.append(AppliedPatch(target=target, op=op, fields=[]))
            continue

        if op == "add":
            if not isinstance(value, dict):
                raise DslPatchError("patch value must be an object")
            kind = value.get("kind")
            ctor = SLOT_KIND_TO_CTOR.get(kind) if isinstance(kind, str) else None
            if ctor is None:
                raise DslPatchError(f"unsupported slot kind for add: {kind}")
            collector = SlotIdCollector()
            transformed.visit(collector)
            if target in collector.slot_ids:
                raise DslPatchError(f"target slot already exists: {target}")
            adder = SlotAddTransformer(target=target, value=value)
            transformed = transformed.visit(adder)
            if not adder.added_slot:
                raise DslPatchError("ProblemTemplate not found")
            transformed = _ensure_dsl_import(transformed, ctor)
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        if not isinstance(value, dict):
            raise DslPatchError("patch value must be an object")

        if op == "layer":
            region_id = value.get("region_id")
            slot_ids = value.get("slot_ids")
            if not isinstance(region_id, str) or not isinstance(slot_ids, list):
                raise DslPatchError("layer patch requires value.region_id and value.slot_ids")
            _save_editor_region_slot_order(paths, region_id, slot_ids)
            applied.append(AppliedPatch(target=target, op=op, fields=["region_id", "slot_ids"]))
            continue

        if op != "update":
            raise DslPatchError("only 'add', 'update', 'delete', and 'layer' ops are supported")

        if target in CANVAS_TARGETS:
            updater = CanvasUpdater(fields=value)
            transformed = transformed.visit(updater)
            if not updater.updated:
                raise DslPatchError("Canvas not found")
            applied.append(AppliedPatch(target="__canvas__", op=op, fields=list(value.keys())))
            continue

        if _character_group_key(target):
            updater = CharacterGroupMoveUpdater(target=target, fields=value)
            transformed = transformed.visit(updater)
            if not updater.updated:
                raise DslPatchError(f"target character group not found: {target}")
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        if target.startswith("slot.figure."):
            updater = FigureGroupMoveUpdater(target=target, fields=value)
            transformed = transformed.visit(updater)
            if updater.updated:
                applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
                continue

        paper_fold_updater = PaperFoldSequenceMoveUpdater(target=target, fields=value)
        transformed = transformed.visit(paper_fold_updater)
        if paper_fold_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        measurement_tool_updater = MeasurementToolMoveUpdater(target=target, fields=value)
        transformed = transformed.visit(measurement_tool_updater)
        if measurement_tool_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        generated_slot_override_updater = GeneratedHelperSlotOverrideUpdater(target=target, fields=value)
        transformed = transformed.visit(generated_slot_override_updater)
        if generated_slot_override_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        single_paper_fold_updater = SinglePaperFoldHelperUpdater(target=target, fields=value)
        transformed = transformed.visit(single_paper_fold_updater)
        if single_paper_fold_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        if _measurement_tool_base_from_slot_id(target):
            raise DslPatchError("measurement tool parts must be moved as a group")

        grid_updater = GridSlotsMoveUpdater(target=target, fields=value)
        transformed = transformed.visit(grid_updater)
        if grid_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        candidate_point_updater = CandidatePointMoveUpdater(target=target, fields=value)
        transformed = transformed.visit(candidate_point_updater)
        if candidate_point_updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        target = _resolve_target_slot_id(transformed, target)

        updater = SlotUpdater(target=target, fields=value)
        transformed = transformed.visit(updater)
        if updater.updated:
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        person_updater = PersonSlotsUpdater(target=target, fields=value)
        transformed = transformed.visit(person_updater)
        if person_updater.updated:
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

        if set(value).issubset(EDITOR_OVERRIDE_FIELDS):
            _save_editor_slot_override(paths, target, value)
            applied.append(AppliedPatch(target=target, op=op, fields=list(value.keys())))
            continue

        raise DslPatchError(f"target slot not found: {target}")

    updated_code = transformed.code
    paths.dsl_path.write_text(updated_code, encoding="utf-8")
    return updated_code, applied
