from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from modu_math.adapters.dsl.export_py import build_generated_py_template
from modu_math.renderer.svg.render import render_svg

from . import io as io_service
from .validate import canonicalize_and_validate


def export_bundle(problem_id: str, semantic: dict[str, Any]) -> dict[str, bytes]:
    canonical = canonicalize_and_validate(semantic)
    normalized_id = io_service.normalize_problem_id(problem_id)
    file_stem = normalized_id.replace("/", "_")

    with tempfile.TemporaryDirectory(prefix=f"modu_export_{file_stem}_") as tmp_dir:
        tmp_root = Path(tmp_dir)
        layout_path = io_service.layout_path(normalized_id)
        renderer_path = io_service.renderer_path(normalized_id)

        if layout_path.exists():
            layout_payload = json.loads(layout_path.read_text(encoding="utf-8"))
        else:
            layout_payload = io_service._layout_from_semantic_render(normalized_id, canonical)

        if renderer_path.exists():
            renderer_payload = json.loads(renderer_path.read_text(encoding="utf-8"))
        else:
            renderer_payload = io_service._renderer_from_layout(layout_payload)

        semantic_export_path = tmp_root / f"{file_stem}.semantic.json"
        layout_export_path = tmp_root / f"{file_stem}.layout.json"
        renderer_export_path = tmp_root / f"{file_stem}.renderer.json"
        generated_py_path = tmp_root / f"{file_stem}.generated.py"
        svg_path = tmp_root / f"{file_stem}.svg"

        semantic_export_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")
        layout_export_path.write_text(json.dumps(layout_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        renderer_export_path.write_text(json.dumps(renderer_payload, ensure_ascii=False, indent=2), encoding="utf-8")

        generated_source = build_generated_py_template(
            semantic=canonical,
            layout=layout_payload,
            renderer=renderer_payload,
            source_semantic_name=semantic_export_path.name,
            source_layout_name=layout_export_path.name,
            source_renderer_name=renderer_export_path.name,
        )
        generated_py_path.write_text(generated_source, encoding="utf-8")
        svg_path.write_text(render_svg(renderer_payload), encoding="utf-8")

        outputs = [
            semantic_export_path,
            layout_export_path,
            renderer_export_path,
            generated_py_path,
            svg_path,
        ]
        return {path.name: path.read_bytes() for path in outputs}
