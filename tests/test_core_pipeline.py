import subprocess
import sys

import pytest

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, compile_problem_template_to_layout, compile_problem_template_to_semantic
from modu_math.layout.validate import validate_layout_json
from modu_math.pipeline.validate_contracts import (
    CrossLayerValidationError,
    validate_contract_bundle,
    validate_semantic_solvable_answer_match,
)
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg
from modu_math.renderer.validate import validate_renderer_json
from modu_math.semantic.validate import validate_semantic_json


def _build_problem() -> ProblemTemplate:
    return ProblemTemplate(
        id="core_0001",
        title="core pipeline sample",
        canvas=Canvas(width=640, height=360),
        regions=(Region(id="region.stem", role="stem", slot_ids=("slot.stem",)),),
        slots=(TextSlot(id="slot.stem", text="2 + 3 = ?"),),
    )


def test_package_import_smoke() -> None:
    import modu_math  # noqa: F401


def test_cli_help_smoke() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "modu_math", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert "usage:" in completed.stdout.lower() or "usage:" in completed.stderr.lower()


def test_core_contract_pipeline_and_svg() -> None:
    problem = _build_problem()

    semantic = compile_problem_template_to_semantic(problem)
    validate_semantic_json(semantic)

    layout = compile_problem_template_to_layout(problem)
    validate_layout_json(layout)

    renderer = compile_renderer_json(layout)
    validate_renderer_json(renderer)

    validate_contract_bundle(semantic, layout, renderer)

    svg = render_svg(renderer)
    assert svg.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert "<svg" in svg
    assert "</svg>" in svg


def test_contract_validation_fails_on_layout_source_ref_mismatch() -> None:
    problem = _build_problem()
    semantic = compile_problem_template_to_semantic(problem)
    layout = compile_problem_template_to_layout(problem)
    renderer = compile_renderer_json(layout)

    layout["slots"][0]["source_ref"] = "semantic.unknown"

    with pytest.raises(CrossLayerValidationError, match="does not match any semantic id"):
        validate_contract_bundle(semantic, layout, renderer)


def test_contract_validation_fails_on_renderer_refs_mismatch() -> None:
    problem = _build_problem()
    semantic = compile_problem_template_to_semantic(problem)
    layout = compile_problem_template_to_layout(problem)
    renderer = compile_renderer_json(layout)

    renderer["elements"][0]["refs"] = {"layout_slot_id": "slot.unknown"}

    with pytest.raises(CrossLayerValidationError, match="unknown layout id"):
        validate_contract_bundle(semantic, layout, renderer)


def test_validate_semantic_solvable_answer_match_accepts_identical_payloads() -> None:
    answer = {
        "blanks": [{"id": "slot.blank", "slot_id": "slot.blank", "expected": "5"}],
        "choices": [],
        "answer_key": [{"slot_id": "slot.blank", "values": ["5"]}],
    }
    semantic = {"answer": answer}
    solvable = {"answer": answer.copy()}

    validate_semantic_solvable_answer_match(semantic, solvable)


def test_validate_semantic_solvable_answer_match_rejects_mismatch() -> None:
    semantic = {
        "answer": {
            "blanks": [{"id": "slot.blank", "slot_id": "slot.blank", "expected": "5"}],
            "choices": [],
            "answer_key": [{"slot_id": "slot.blank", "values": ["5"]}],
        }
    }
    solvable = {
        "answer": {
            "blanks": [{"id": "slot.blank", "slot_id": "slot.blank", "expected": "7"}],
            "choices": [],
            "answer_key": [{"slot_id": "slot.blank", "values": ["7"]}],
        }
    }

    with pytest.raises(CrossLayerValidationError, match="must exactly match"):
        validate_semantic_solvable_answer_match(semantic, solvable)
