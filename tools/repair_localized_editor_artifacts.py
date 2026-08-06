from __future__ import annotations

import argparse
import json
import os
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from modu_math.dsl import compile_problem_template_to_layout
from modu_math.layout.editor_overrides import apply_editor_overrides
from modu_math.renderer.svg.render import _wrap_text
from modu_math_web.editor.services.build import run_problem_build
from tools.extract_dsl_localization import load_dsl_module


LOCALE_SUFFIX_RE = re.compile(
    r"^(?P<base>.+)(?:[._])(?P<locale>[a-z]{2}(?:-[A-Z]{2})?)\.dsl\.py$"
)
TEXT_FIELDS = {"text", "prompt", "placeholder"}
TEXT_BOX_KINDS = {"text_box"}
MIN_FONT_SIZE = 14


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return loaded


def write_json(path: Path, payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8-sig") == text:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def infer_source_dsl(localized_dsl: Path, explicit_source: Path | None = None) -> Path:
    if explicit_source is not None:
        return explicit_source
    match = LOCALE_SUFFIX_RE.match(localized_dsl.name)
    if not match:
        raise ValueError(
            "Cannot infer source DSL. Use --source-dsl for files not named '<base>.<locale>.dsl.py'."
        )
    source = localized_dsl.with_name(f"{match.group('base')}.dsl.py")
    if not source.exists():
        raise FileNotFoundError(f"Source DSL not found: {source}")
    return source


def artifact_base(dsl_path: Path) -> str:
    if not dsl_path.name.endswith(".dsl.py"):
        raise ValueError(f"Expected *.dsl.py path: {dsl_path}")
    return dsl_path.name[: -len(".dsl.py")]


def override_path_for(dsl_path: Path) -> Path:
    return dsl_path.with_name(f"{artifact_base(dsl_path)}.editor_overrides.json")


def layout_from_dsl(dsl_path: Path) -> dict[str, Any]:
    module = load_dsl_module(dsl_path)
    template = getattr(module, "PROBLEM_TEMPLATE", None)
    if template is None:
        raise ValueError(f"DSL must define PROBLEM_TEMPLATE: {dsl_path}")
    return compile_problem_template_to_layout(template)


def slot_map(layout: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        slot["id"]: slot
        for slot in layout.get("slots", [])
        if isinstance(slot, dict) and isinstance(slot.get("id"), str)
    }


def merge_non_text_slot_patch(source_patch: dict[str, Any], localized_content: dict[str, Any]) -> dict[str, Any]:
    patch: dict[str, Any] = {}
    for key, value in source_patch.items():
        if key in TEXT_FIELDS:
            continue
        patch[key] = deepcopy(value)
    for key in TEXT_FIELDS:
        if key in localized_content:
            patch[key] = localized_content[key]
    return patch


def merged_overrides(
    *,
    source_overrides: dict[str, Any] | None,
    existing_localized_overrides: dict[str, Any] | None,
    localized_layout: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {"version": 1}
    localized_slots = slot_map(localized_layout)

    if source_overrides:
        if isinstance(source_overrides.get("canvas"), dict):
            out["canvas"] = deepcopy(source_overrides["canvas"])
        if isinstance(source_overrides.get("deleted_slots"), list):
            out["deleted_slots"] = [
                slot_id for slot_id in source_overrides["deleted_slots"] if isinstance(slot_id, str)
            ]
        if isinstance(source_overrides.get("region_slot_orders"), dict):
            out["region_slot_orders"] = deepcopy(source_overrides["region_slot_orders"])

        source_slots = source_overrides.get("slots")
        if isinstance(source_slots, dict):
            out_slots: dict[str, Any] = {}
            for slot_id, source_patch in source_slots.items():
                if not isinstance(slot_id, str) or not isinstance(source_patch, dict):
                    continue
                localized_slot = localized_slots.get(slot_id)
                localized_content = localized_slot.get("content", {}) if isinstance(localized_slot, dict) else {}
                out_slots[slot_id] = merge_non_text_slot_patch(
                    source_patch,
                    localized_content if isinstance(localized_content, dict) else {},
                )
            if out_slots:
                out["slots"] = out_slots

    # Preserve answer behavior if it was already authored into the localized DSL.
    out_slots = out.setdefault("slots", {})
    for slot_id, slot in localized_slots.items():
        content = slot.get("content")
        if not isinstance(content, dict):
            continue
        if isinstance(content.get("interaction"), dict) or isinstance(content.get("input_style"), dict):
            patch = out_slots.setdefault(slot_id, {})
            if isinstance(content.get("interaction"), dict):
                patch["interaction"] = deepcopy(content["interaction"])
            if isinstance(content.get("input_style"), dict):
                patch["input_style"] = deepcopy(content["input_style"])

    if existing_localized_overrides:
        if isinstance(existing_localized_overrides.get("canvas"), dict):
            out["canvas"] = deepcopy(existing_localized_overrides["canvas"])
        if isinstance(existing_localized_overrides.get("deleted_slots"), list):
            out["deleted_slots"] = [
                slot_id
                for slot_id in existing_localized_overrides["deleted_slots"]
                if isinstance(slot_id, str)
            ]
        if isinstance(existing_localized_overrides.get("region_slot_orders"), dict):
            out["region_slot_orders"] = deepcopy(existing_localized_overrides["region_slot_orders"])

        existing_slots = existing_localized_overrides.get("slots")
        if isinstance(existing_slots, dict):
            out_slots = out.setdefault("slots", {})
            for slot_id, patch in existing_slots.items():
                if isinstance(slot_id, str) and isinstance(patch, dict):
                    merged_patch = out_slots.setdefault(slot_id, {})
                    merged_patch.update(deepcopy(patch))

    return out


def text_height(text: str, width: float, font_size: float, line_height: float) -> float:
    return max(1, len(_wrap_text(text, width, font_size))) * font_size * line_height


def fit_text_box_patch(slot: dict[str, Any], patch: dict[str, Any], canvas: dict[str, Any]) -> bool:
    if slot.get("kind") not in TEXT_BOX_KINDS:
        return False
    content = slot.get("content")
    if not isinstance(content, dict):
        return False
    merged = {**content, **patch}
    text = merged.get("text")
    if not isinstance(text, str) or not text.strip():
        return False

    width = float(merged.get("width") or 0)
    height = float(merged.get("height") or 0)
    font_size = float(merged.get("font_size") or 24)
    line_height = float(merged.get("line_height") or 1.25)
    if width <= 0 or height <= 0:
        return False

    changed = False
    while font_size > MIN_FONT_SIZE and text_height(text, width, font_size, line_height) > height:
        font_size -= 1
        changed = True

    required = text_height(text, width, font_size, line_height)
    if required > height:
        y = float(merged.get("y") or 0)
        canvas_height = float(canvas.get("height") or 0)
        max_height = max(height, canvas_height - y - 8) if canvas_height > 0 else height
        next_height = min(max_height, required + 8)
        if next_height > height:
            height = next_height
            changed = True

    if changed:
        patch["font_size"] = int(font_size) if font_size.is_integer() else font_size
        patch["height"] = round(height, 3)
    return changed


def fit_text_boxes(overrides: dict[str, Any], localized_layout: dict[str, Any]) -> int:
    out_slots = overrides.setdefault("slots", {})
    slots = slot_map(localized_layout)
    preview_layout = apply_editor_overrides(deepcopy(localized_layout), deepcopy(overrides))
    preview_slots = slot_map(preview_layout)
    canvas = preview_layout.get("canvas") if isinstance(preview_layout.get("canvas"), dict) else {}

    changed = 0
    for slot_id, preview_slot in preview_slots.items():
        source_slot = slots.get(slot_id, preview_slot)
        patch = out_slots.setdefault(slot_id, {})
        if fit_text_box_patch(source_slot, patch, canvas):
            changed += 1
    return changed


def problem_id_for_build(dsl_path: Path) -> str:
    return artifact_base(dsl_path)


def repair_localized_artifacts(
    *,
    localized_dsl: Path,
    source_dsl: Path | None,
    build: bool,
) -> dict[str, Any]:
    localized_dsl = localized_dsl.resolve()
    source_dsl = infer_source_dsl(localized_dsl, source_dsl.resolve() if source_dsl else None)

    localized_layout = layout_from_dsl(localized_dsl)
    source_overrides = read_json(override_path_for(source_dsl))
    localized_override_path = override_path_for(localized_dsl)
    existing_localized_overrides = read_json(localized_override_path)
    overrides = merged_overrides(
        source_overrides=source_overrides,
        existing_localized_overrides=existing_localized_overrides,
        localized_layout=localized_layout,
    )
    fitted_text_boxes = fit_text_boxes(overrides, localized_layout)

    out_path = localized_override_path
    wrote_overrides = write_json(out_path, overrides)

    build_ok: bool | None = None
    build_error: str | None = None
    if build:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
        result = run_problem_build(problem_id_for_build(localized_dsl))
        build_ok = result.ok
        build_error = result.error

    answer_slots = [
        slot_id
        for slot_id, patch in overrides.get("slots", {}).items()
        if isinstance(patch, dict) and isinstance(patch.get("interaction"), dict) and patch["interaction"].get("role") == "answer"
    ]
    return {
        "localized_dsl": str(localized_dsl),
        "source_dsl": str(source_dsl),
        "override_path": str(out_path),
        "wrote_overrides": wrote_overrides,
        "fitted_text_boxes": fitted_text_boxes,
        "answer_slot_count": len(answer_slots),
        "build_ok": build_ok,
        "build_error": build_error,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Repair editor overrides and generated artifacts for a localized DSL file."
    )
    parser.add_argument("--localized-dsl", required=True, help="Localized *.dsl.py path.")
    parser.add_argument("--source-dsl", help="Optional source *.dsl.py path. Inferred from filename when omitted.")
    parser.add_argument("--no-build", action="store_true", help="Only write editor_overrides; do not rebuild artifacts.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = repair_localized_artifacts(
        localized_dsl=Path(args.localized_dsl),
        source_dsl=Path(args.source_dsl) if args.source_dsl else None,
        build=not args.no_build,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("build_ok") is False:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
