from __future__ import annotations

import pytest

from modu_math.pipeline.tutor_renderer_flow import (
    TutorRendererFlowError,
    normalize_tutor_renderer_flow,
    validate_tutor_renderer_flow,
)


def test_normalize_tutor_renderer_flow_accepts_phase_sections() -> None:
    flow = [
        {
            "phase": "understand",
            "title": "Understand",
            "source_refs": ["inputs"],
            "frames": [{"id": "understand.given", "overlays": [{"type": "label", "text": "Given"}]}],
        },
        {
            "phase": "execute",
            "step_id": "step.1",
            "frames": [{"id": "step.1.work", "overlays": [{"type": "highlight", "target_ref": "slot.a"}]}],
        },
    ]

    normalized = normalize_tutor_renderer_flow(flow)

    assert normalized[0]["step_id"] == "understand"
    assert normalized[0]["phase"] == "understand"
    assert normalized[0]["title"] == "Understand"
    assert normalized[0]["source_refs"] == ["inputs"]
    assert normalized[1]["step_id"] == "step.1"


def test_validate_tutor_renderer_flow_allows_non_execute_phase_ids() -> None:
    renderer = {
        "elements": [{"id": "element.a", "source_ref": "slot.a"}],
        "tutor_flow": [
            {"phase": "understand", "frames": [{"id": "understand.given", "overlays": [{"type": "label"}]}]},
            {
                "phase": "execute",
                "step_id": "step.1",
                "frames": [{"id": "step.1.work", "overlays": [{"type": "highlight", "target_ref": "slot.a"}]}],
            },
        ],
    }
    solvable = {"steps": [{"id": "step.1"}]}

    validate_tutor_renderer_flow(renderer, solvable)


def test_validate_tutor_renderer_flow_rejects_unknown_execute_step() -> None:
    renderer = {
        "elements": [],
        "tutor_flow": [{"phase": "execute", "step_id": "step.2", "frames": [{"id": "step.2.work", "overlays": []}]}],
    }
    solvable = {"steps": [{"id": "step.1"}]}

    with pytest.raises(TutorRendererFlowError, match="does not match solvable.steps"):
        validate_tutor_renderer_flow(renderer, solvable)
