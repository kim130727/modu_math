from __future__ import annotations

import pytest

from modu_math.layout.validate import LayoutValidationError, validate_layout_json


def _base_layout() -> dict:
    return {
        "problem_id": "p_layout_001",
        "schema": "modu.layout.v1",
        "canvas": {
            "width": 640,
            "height": 360,
            "coordinate_mode": "logical",
        },
        "regions": [
            {
                "id": "region.stem",
                "role": "stem",
                "flow": "vertical",
                "slot_ids": ["slot.stem"],
            }
        ],
        "slots": [
            {
                "id": "slot.stem",
                "kind": "text",
                "prompt": "",
                "content": {"text": "2 + 3 = ?"},
            }
        ],
    }


def test_validate_layout_rejects_unknown_region_slot_id() -> None:
    layout = _base_layout()
    layout["regions"][0]["slot_ids"] = ["slot.unknown"]

    with pytest.raises(LayoutValidationError, match="contains unknown slot id"):
        validate_layout_json(layout)


def test_validate_layout_rejects_duplicate_slot_ids() -> None:
    layout = _base_layout()
    layout["slots"].append(
        {
            "id": "slot.stem",
            "kind": "text",
            "prompt": "",
            "content": {"text": "duplicate"},
        }
    )

    with pytest.raises(LayoutValidationError, match="duplicates existing slot id"):
        validate_layout_json(layout)


def test_validate_layout_rejects_invalid_region_slot_id_entry() -> None:
    layout = _base_layout()
    layout["regions"][0]["slot_ids"] = ["slot.stem", ""]

    with pytest.raises(LayoutValidationError, match="slot_ids\\[1\\] must be a non-empty string"):
        validate_layout_json(layout)
