from __future__ import annotations

import json
from pathlib import Path

from modu_semantic.semantic_json_builder import build_from_semantic_file, build_problem_from_semantic_dict


def _sample_semantic() -> dict[str, object]:
    return {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": "semantic_build_0001",
        "problem_type": "addition_subtraction_symbol_equations",
        "title": "기호 수식",
        "metadata": {"source": {"input_type": "python_dsl", "generator": "modu_semantic"}, "warnings": []},
        "domain": {"instruction": "괄호 안에 알맞은 수의 값을 구하시오."},
        "render": {
            "canvas": {"width": 417.0, "height": 220.0, "background": "#F6F6F6"},
            "elements": [
                {
                    "id": "bg",
                    "type": "rect",
                    "x": 0,
                    "y": 0,
                    "width": 417,
                    "height": 220,
                    "fill": "#FFFFFF",
                    "stroke": "none",
                    "stroke_width": 0,
                },
                {
                    "id": "instruction_1",
                    "type": "text",
                    "x": 6.0,
                    "y": 30.0,
                    "text": "괄호 안에 알맞은 수의 값을 구하시오.",
                    "font_size": 17,
                    "font_family": "Malgun Gothic",
                },
                {
                    "id": "circle_symbol",
                    "type": "circle",
                    "x": 202.0,
                    "y": 133.0,
                    "r": 7,
                    "fill": "#000000",
                    "stroke": "#000000",
                    "stroke_width": 1,
                },
            ],
        },
        "answer": {
            "blanks": [{"id": "blank_1", "type": "numeric_or_text"}],
            "choices": [],
            "answer_key": [{"blank_id": "blank_1", "value": 621.0}],
        },
    }


def test_build_problem_from_semantic_dict_roundtrip() -> None:
    problem = build_problem_from_semantic_dict(_sample_semantic())
    semantic = problem.to_semantic_json(validate=True)

    assert semantic["problem_id"] == "semantic_build_0001"
    assert semantic["problem_type"] == "addition_subtraction_symbol_equations"
    assert semantic["render"]["canvas"]["width"] == 417.0
    assert len(semantic["render"]["elements"]) == 3
    assert semantic["answer"]["answer_key"][0]["value"] == 621.0


def test_build_from_semantic_file_writes_outputs_and_scaffold(tmp_path: Path) -> None:
    input_semantic = tmp_path / "input" / "semantic.json"
    input_semantic.parent.mkdir(parents=True, exist_ok=True)
    input_semantic.write_text(json.dumps(_sample_semantic(), ensure_ascii=False, indent=2), encoding="utf-8")

    out_prefix = tmp_path / "output" / "sample_build"
    emit_py = tmp_path / "generated" / "sample_build.generated.py"

    outputs = build_from_semantic_file(
        input_semantic_path=input_semantic,
        out_prefix=out_prefix,
        emit_py_path=emit_py,
    )

    assert outputs["semantic"].exists()
    assert outputs["svg"].exists()
    assert outputs["answer_svg"].exists()
    assert outputs["py"].exists()

    generated_code = emit_py.read_text(encoding="utf-8")
    assert "def build() -> Problem" in generated_code
    assert "p.set_domain(" in generated_code
    assert "p.add(" in generated_code
