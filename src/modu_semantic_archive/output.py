from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .normalizer import normalize_semantic
from .orderer import order_semantic
from .serializer import serialize_semantic
from .validator import validate_semantic


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_canonical_payloads(
    problem_ir,
    *,
    validate: bool = True,
    semantic_options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    semantic = serialize_semantic(problem_ir, **(semantic_options or {}))
    semantic = normalize_semantic(semantic)
    semantic = order_semantic(semantic)

    if validate:
        validate_semantic(semantic)

    return semantic


def save_bundle(
    problem_ir,
    out_dir: str | Path,
    *,
    include_layout_diff: bool = False,
    baseline_layout_path: str | Path | None = None,
    semantic_options: dict[str, Any] | None = None,
) -> dict[str, Path]:
    """Contract-first semantic output.

    Layout/layout_diff export has been removed.
    """
    if include_layout_diff is True or baseline_layout_path is not None:
        raise ValueError("layout/layout_diff export has been removed. Semantic JSON is the single canonical output.")

    out_root = Path(out_dir)
    outputs: dict[str, Path] = {}

    semantic = build_canonical_payloads(
        problem_ir,
        validate=True,
        semantic_options=semantic_options,
    )

    semantic_path = out_root / "json" / "semantic_final" / "semantic_final.json"
    _write_json(semantic_path, semantic)
    outputs["semantic"] = semantic_path

    return outputs
