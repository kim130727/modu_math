from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from modu_math.core.base_problem import BaseProblemBuilder, BuildContext
from modu_math.renderers.svg_renderer import SvgRenderer
from modu_math.validators.validate import run_all_validations


@dataclass(slots=True)
class RunnerOptions:
    export_semantic: bool = False
    validate: bool = False
    render_svg: bool = False
    all: bool = False


class ProblemRunner:
    def __init__(self, builder: BaseProblemBuilder, svg_renderer: SvgRenderer | None = None) -> None:
        self.builder = builder
        self.svg_renderer = svg_renderer or SvgRenderer()

    @staticmethod
    def load_problem_json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8-sig"))

    @staticmethod
    def write_json(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def run(
        self,
        ctx: BuildContext,
        problem_json_path: Path,
        semantic_out: Path,
        svg_out: Path,
        options: RunnerOptions,
    ) -> dict[str, Any]:
        do_export = options.export_semantic or options.all
        do_validate = options.validate or options.all
        do_svg = options.render_svg or options.all

        raw = self.load_problem_json(problem_json_path)
        semantic = self.builder.build_semantic(ctx, raw).data

        if do_validate:
            report = run_all_validations(semantic)
            if not report.ok:
                raise ValueError(report.to_text())

        if do_export:
            self.write_json(semantic_out, semantic)

        if do_svg:
            self.svg_renderer.render_to_file(semantic, svg_out)

        return semantic
