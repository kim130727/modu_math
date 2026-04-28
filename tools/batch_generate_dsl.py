from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from tools.generate_dsl_from_png import (
        DEFAULT_SYSTEM_PROMPT,
        DEFAULT_USER_TEMPLATE,
        generate_dsl_from_png,
        resolve_model_name,
    )
    from tools.validate_generated_dsl import main as validate_generated_dsl_main
except ImportError:
    from generate_dsl_from_png import (
        DEFAULT_SYSTEM_PROMPT,
        DEFAULT_USER_TEMPLATE,
        generate_dsl_from_png,
        resolve_model_name,
    )
    from validate_generated_dsl import main as validate_generated_dsl_main


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-generate problem.dsl.py files from examples/problems/<problem_id>/input.png."
    )
    parser.add_argument("--root", default="examples/problems", help="Root folder containing problem_id subfolders")
    parser.add_argument("--model", default=None, help="Optional model override")
    parser.add_argument("--force", action="store_true", help="Overwrite existing problem.dsl.py")
    parser.add_argument("--validate", action="store_true", help="Run validate_generated_dsl.py per generated DSL")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of problem folders to process")
    parser.add_argument("--dry-run", action="store_true", help="Do not call API; print and trace planned work only")
    return parser.parse_args(argv)


def _problem_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    out: list[Path] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "input.png").exists():
            out.append(child)
    return out


def _write_trace(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    system_prompt_path = DEFAULT_SYSTEM_PROMPT
    user_template_path = DEFAULT_USER_TEMPLATE
    resolved_model = resolve_model_name(args.model)

    dirs = _problem_dirs(root)
    if args.limit is not None:
        dirs = dirs[: max(0, args.limit)]

    if not dirs:
        print(f"No problem folders found under: {root}")
        return 0

    failures = 0
    processed = 0
    for problem_dir in dirs:
        processed += 1
        problem_id = problem_dir.name
        image_path = problem_dir / "input.png"
        out_path = problem_dir / "problem.dsl.py"
        trace_path = problem_dir / "agent_trace.json"

        trace: dict[str, Any] = {
            "problem_id": problem_id,
            "image_path": str(image_path),
            "output_path": str(out_path),
            "model": resolved_model,
            "prompt_files": {
                "system_prompt": str(system_prompt_path),
                "user_template": str(user_template_path),
            },
            "success": False,
        }

        try:
            if out_path.exists() and not args.force:
                trace["success"] = True
                trace["skipped"] = True
                trace["message"] = "Skipped existing problem.dsl.py (use --force to overwrite)."
                _write_trace(trace_path, trace)
                print(f"[skip] {problem_id} existing DSL")
                continue

            result = generate_dsl_from_png(
                image_path=image_path,
                problem_id=problem_id,
                out_path=out_path,
                model=args.model,
                system_prompt_path=system_prompt_path,
                user_template_path=user_template_path,
                force=bool(args.force),
                dry_run=bool(args.dry_run),
            )
            trace["generator"] = result

            if args.validate and not args.dry_run:
                validate_code = validate_generated_dsl_main(["--dsl", str(out_path)])
                trace["validation"] = {"requested": True, "exit_code": validate_code}
                if validate_code != 0:
                    raise RuntimeError("Validation failed for generated DSL.")
            else:
                trace["validation"] = {"requested": bool(args.validate), "skipped": bool(args.dry_run)}

            trace["success"] = True
            _write_trace(trace_path, trace)
            if args.dry_run:
                print(f"[dry-run] {problem_id} planned")
            else:
                print(f"[ok] {problem_id} generated")
        except Exception as exc:
            failures += 1
            trace["error"] = {"message": str(exc)}
            trace["success"] = False
            _write_trace(trace_path, trace)
            print(f"[fail] {problem_id}: {exc}")

    print(f"Processed {processed} folders; failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
