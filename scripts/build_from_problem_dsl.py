import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType

from modu_math.dsl import (
    ProblemTemplate,
    compile_problem_template_to_layout,
    compile_problem_template_to_semantic,
)
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build semantic/layout/renderer/svg artifacts from problem.dsl.py"
    )
    parser.add_argument("--dsl", required=True, help="Path to problem.dsl.py")
    parser.add_argument(
        "--out-prefix",
        default=None,
        help=(
            "Output prefix path without extension. "
            "Defaults to <dsl_dir>/problem"
        ),
    )
    return parser.parse_args()


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("problem_dsl_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_problem_template(path: Path) -> ProblemTemplate:
    module = _load_module(path)

    if hasattr(module, "PROBLEM_TEMPLATE"):
        candidate = module.PROBLEM_TEMPLATE
        if isinstance(candidate, ProblemTemplate):
            return candidate

    if hasattr(module, "build_problem_template"):
        candidate = module.build_problem_template()
        if isinstance(candidate, ProblemTemplate):
            return candidate

    raise RuntimeError(
        "problem.dsl.py must define PROBLEM_TEMPLATE or build_problem_template() "
        "returning ProblemTemplate."
    )


def main() -> None:
    args = parse_args()

    dsl_path = Path(args.dsl).resolve()
    if not dsl_path.exists():
        raise FileNotFoundError(f"DSL file not found: {dsl_path}")

    out_prefix = (
        Path(args.out_prefix).resolve()
        if args.out_prefix
        else dsl_path.parent / "problem"
    )
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    problem = _load_problem_template(dsl_path)
    semantic = compile_problem_template_to_semantic(problem)
    layout = compile_problem_template_to_layout(problem)
    renderer = compile_renderer_json(layout)
    svg = render_svg(renderer)

    semantic_path = out_prefix.with_suffix(".semantic.json")
    layout_path = out_prefix.with_suffix(".layout.json")
    renderer_path = out_prefix.with_suffix(".renderer.json")
    svg_path = out_prefix.with_suffix(".svg")

    semantic_path.write_text(
        json.dumps(semantic, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    layout_path.write_text(
        json.dumps(layout, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    renderer_path.write_text(
        json.dumps(renderer, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    svg_path.write_text(svg, encoding="utf-8")

    print(f"Generated semantic JSON: {semantic_path}")
    print(f"Generated layout JSON: {layout_path}")
    print(f"Generated renderer JSON: {renderer_path}")
    print(f"Generated SVG: {svg_path}")


if __name__ == "__main__":
    main()
