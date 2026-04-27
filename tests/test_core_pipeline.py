import subprocess
import sys

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, compile_problem_template_to_layout, compile_problem_template_to_semantic
from modu_math.layout.validate import validate_layout_json
from modu_math.pipeline.validate_contracts import validate_contract_bundle
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
