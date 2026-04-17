from __future__ import annotations

from typing import Any

from .compiler_json import compile_layout_json, compile_semantic_json
from .ir import ProblemIR


def serialize_semantic(problem_ir: ProblemIR, **kwargs: Any) -> dict[str, Any]:
    return compile_semantic_json(problem_ir, **kwargs)


def serialize_layout(problem_ir: ProblemIR) -> dict[str, Any]:
    return compile_layout_json(problem_ir)


def serialize_layout_diff(
    problem_id: str,
    *,
    diff: dict[str, Any],
    metrics: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "modu_math.layout_diff.v1",
        "problem_id": problem_id,
        "metadata": metadata or {"generator": "modu_semantic.output.save_bundle"},
        "diff": diff,
        "metrics": metrics,
    }
