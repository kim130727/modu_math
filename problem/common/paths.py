from __future__ import annotations

from pathlib import Path


def find_problem_dir(from_file: Path) -> Path:
    """
    Resolve `problem/{id}` directory from any file path under that subtree.

    We avoid fragile fixed parent indexes and instead detect the folder shape.
    """
    resolved = from_file.resolve()
    for parent in resolved.parents:
        if parent.parent.name == "problem" and parent.name.isdigit() and len(parent.name) == 4:
            return parent
    raise ValueError(f"Could not locate problem directory from: {from_file}")


def semantic_json_path(problem_dir: Path) -> Path:
    return problem_dir / "json" / "semantic.json"


def semantic_svg_path(problem_dir: Path) -> Path:
    return problem_dir / "svg" / "semantic.svg"


def problem_input_json_path(problem_dir: Path) -> Path:
    return problem_dir / "input" / "problem.json"


def baseline_dir_path(problem_dir: Path) -> Path:
    return problem_dir / "baseline"
