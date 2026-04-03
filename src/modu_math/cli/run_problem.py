from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_src_on_path() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.is_dir():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return src_dir
    raise RuntimeError("Could not locate src directory.")


_ensure_src_on_path()

# registry side effects
import modu_math.problem_types  # noqa: F401
from modu_math.core.base_problem import BuildContext
from modu_math.core.problem_runner import ProblemRunner, RunnerOptions
from modu_math.registry.problem_registry import get_builder


def _infer_problem_paths(problem_id: str) -> tuple[Path, Path, Path]:
    root = Path.cwd()
    problem_dir = root / "problem" / problem_id
    return (
        problem_dir / "input" / "problem.json",
        problem_dir / "json" / "semantic.json",
        problem_dir / "svg" / "semantic.svg",
    )


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Run semantic pipeline using registry-based builders.")
    parser.add_argument("--problem-id", required=True, help="Problem id like 0001")
    parser.add_argument("--problem-in", type=Path, help="Input problem.json path override")
    parser.add_argument("--semantic-out", type=Path, help="semantic output path override")
    parser.add_argument("--svg-out", type=Path, help="svg output path override")
    parser.add_argument("--grade-band", default="unknown")
    parser.add_argument("--export-semantic", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--render-svg", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    default_problem_in, default_semantic_out, default_svg_out = _infer_problem_paths(args.problem_id)
    problem_in = args.problem_in or default_problem_in
    semantic_out = args.semantic_out or default_semantic_out
    svg_out = args.svg_out or default_svg_out

    raw = json.loads(problem_in.read_text(encoding="utf-8-sig"))
    problem_type = raw.get("type")
    if not isinstance(problem_type, str):
        raise ValueError("problem.json must include string field 'type'")

    builder = get_builder(problem_type)
    runner = ProblemRunner(builder)

    options = RunnerOptions(
        export_semantic=args.export_semantic,
        validate=args.validate,
        render_svg=args.render_svg,
        all=args.all,
    )

    if not (options.export_semantic or options.validate or options.render_svg or options.all):
        parser.print_help()
        return

    ctx = BuildContext(
        problem_id=args.problem_id,
        problem_type=problem_type,
        source_file=str(problem_in),
        grade_band=args.grade_band,
    )

    runner.run(
        ctx=ctx,
        problem_json_path=problem_in,
        semantic_out=semantic_out,
        svg_out=svg_out,
        options=options,
    )

    if options.export_semantic or options.all:
        print(f"[OK] semantic json created: {semantic_out}")
    if options.validate or options.all:
        print("[OK] semantic payload is valid")
    if options.render_svg or options.all:
        print(f"[OK] svg rendered: {svg_out}")


if __name__ == "__main__":
    run_cli()
