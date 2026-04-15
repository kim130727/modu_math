from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from .validate import canonicalize_and_validate
from modu_semantic.semantic_json_builder import build_from_semantic_file


def export_bundle(problem_id: str, semantic: dict[str, Any]) -> dict[str, bytes]:
    canonical = canonicalize_and_validate(semantic)

    with tempfile.TemporaryDirectory(prefix=f"modu_export_{problem_id}_") as tmp_dir:
        tmp_root = Path(tmp_dir)
        semantic_path = tmp_root / "semantic.json"
        semantic_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")

        out_prefix = tmp_root / problem_id
        py_path = tmp_root / f"{problem_id}.generated.py"
        outputs = build_from_semantic_file(
            input_semantic_path=semantic_path,
            out_prefix=out_prefix,
            emit_py_path=py_path,
            validate_input=False,
            validate_output=True,
        )

        copied: dict[str, bytes] = {}
        for key, path in outputs.items():
            copied[path.name] = path.read_bytes()
        return copied
