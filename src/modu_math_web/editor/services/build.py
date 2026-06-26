from __future__ import annotations

import importlib.util
import json
import time
import uuid
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from modu_math.dsl import (
    ProblemTemplate,
    compile_problem_template_to_layout,
    compile_problem_template_to_semantic,
)
from modu_math.layout.editor_overrides import apply_editor_overrides
from modu_math.pipeline.validate_contracts import validate_semantic_solvable_answer_match
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import inline_local_image_hrefs, render_svg

from .problems import read_artifacts, resolve_problem_paths, validate_problem_id


@dataclass
class BuildResult:
    ok: bool
    stdout: str
    stderr: str
    error: str | None = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@lru_cache(maxsize=8)
def _schema_validator(relative_path: str) -> Draft202012Validator:
    schema_path = _repo_root() / relative_path
    schema = json.loads(schema_path.read_text(encoding="utf-8-sig"))
    return Draft202012Validator(schema)


def _load_dsl_module(dsl_path: Path) -> Any:
    module_name = f"modu_editor_build_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, dsl_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"unable to load DSL file: {dsl_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _problem_template_from_module(module: Any, dsl_path: Path) -> ProblemTemplate:
    if hasattr(module, "PROBLEM_TEMPLATE") and isinstance(module.PROBLEM_TEMPLATE, ProblemTemplate):
        return module.PROBLEM_TEMPLATE
    if hasattr(module, "build_problem_template"):
        problem = module.build_problem_template()
        if isinstance(problem, ProblemTemplate):
            return problem
    raise ValueError(f"DSL file {dsl_path} does not define PROBLEM_TEMPLATE or build_problem_template()")


def _deep_merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = _deep_merge_dict(out[key], value)
        else:
            out[key] = value
    return out


def _parse_solvable_schema_tag(solvable: dict[str, Any]) -> str:
    schema_value = solvable.get("schema")
    if not isinstance(schema_value, str):
        raise ValueError("SOLVABLE['schema'] must be a string like 'modu.solvable.v1' or 'modu.solvable.v1.1'.")
    prefix = "modu.solvable."
    if not schema_value.startswith(prefix):
        raise ValueError(f"Unsupported solvable schema format: {schema_value}")
    tag = schema_value[len(prefix) :]
    if not tag:
        raise ValueError(f"Invalid solvable schema tag: {schema_value}")
    return tag


def _build_problem_artifacts(problem_id: str) -> str:
    safe_problem_id = validate_problem_id(problem_id)
    problem_paths = resolve_problem_paths(safe_problem_id)
    module = _load_dsl_module(problem_paths.dsl_path)
    problem = _problem_template_from_module(module, problem_paths.dsl_path)

    semantic = compile_problem_template_to_semantic(problem, problem_type="diagram_problem")
    layout = compile_problem_template_to_layout(problem)

    editor_overrides_path = problem_paths.base_dir / f"{problem_paths.artifact_base}.editor_overrides.json"
    if editor_overrides_path.exists():
        editor_overrides = json.loads(editor_overrides_path.read_text(encoding="utf-8-sig"))
        layout = apply_editor_overrides(layout, editor_overrides)

    renderer = compile_renderer_json(layout)
    svg = inline_local_image_hrefs(render_svg(renderer), problem_paths.base_dir)

    if hasattr(module, "SEMANTIC_OVERRIDE"):
        semantic_override = module.SEMANTIC_OVERRIDE
        if not isinstance(semantic_override, dict):
            raise ValueError("SEMANTIC_OVERRIDE must be a dict when provided.")
        semantic = _deep_merge_dict(semantic, semantic_override)

    if hasattr(module, "SEMANTIC_ANSWER"):
        semantic["answer"] = module.SEMANTIC_ANSWER

    solvable = None
    if hasattr(module, "SOLVABLE"):
        solvable = module.SOLVABLE
    elif hasattr(module, "build_solvable"):
        solvable = module.build_solvable()

    _schema_validator("schema/semantic/semantic.v1.json").validate(semantic)
    _schema_validator("schema/layout/layout.v1.json").validate(layout)
    _schema_validator("schema/renderer/renderer.v1.json").validate(renderer)

    problem_paths.artifact_path("semantic").write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("layout").write_text(
        json.dumps(layout, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("renderer").write_text(
        json.dumps(renderer, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    problem_paths.artifact_path("svg").write_text(svg, encoding="utf-8")

    if solvable:
        solvable_tag = _parse_solvable_schema_tag(solvable)
        schema_relative = f"schema/solvable/solvable.{solvable_tag}.json"
        schema_path = _repo_root() / schema_relative
        if not schema_path.exists():
            raise FileNotFoundError(
                f"Solvable schema file not found for '{solvable.get('schema')}': {schema_path}"
            )
        _schema_validator(schema_relative).validate(solvable)
        validate_semantic_solvable_answer_match(semantic, solvable)
        (problem_paths.base_dir / f"{problem_paths.artifact_base}.solvable.{solvable_tag}.json").write_text(
            json.dumps(solvable, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return "build_ok"


def run_problem_build(problem_id: str) -> BuildResult:
    started = time.perf_counter()
    try:
        output = _build_problem_artifacts(problem_id)
    except Exception as exc:  # pragma: no cover
        return BuildResult(ok=False, stdout="", stderr="", error=str(exc))

    elapsed_ms = (time.perf_counter() - started) * 1000
    return BuildResult(
        ok=True,
        stdout=f"{output}\n[editor_build] {elapsed_ms:.0f} ms\n",
        stderr="",
        error=None,
    )


def build_with_artifacts(problem_id: str) -> tuple[BuildResult, dict[str, Any]]:
    result = run_problem_build(problem_id)
    artifacts = read_artifacts(problem_id)
    return result, artifacts
