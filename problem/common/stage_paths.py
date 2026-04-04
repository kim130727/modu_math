from __future__ import annotations

from pathlib import Path


def ensure_problem_id(problem_id: str) -> str:
    pid = str(problem_id).strip()
    if not (pid.isdigit() and len(pid) == 4):
        raise ValueError(f"problem_id must be 4 digits, got: {problem_id}")
    return pid


def problem_dir(repo_root: Path, problem_id: str) -> Path:
    return repo_root / "problem" / ensure_problem_id(problem_id)


def input_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "input"


def manim_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "manim"


def manim_edit_dir(repo_root: Path, problem_id: str) -> Path:
    return manim_dir(repo_root, problem_id) / "edit"


def manim_final_dir(repo_root: Path, problem_id: str) -> Path:
    return manim_dir(repo_root, problem_id) / "final"


def json_semantic_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "semantic"


def json_layout_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "layout"


def json_semantic_edit_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "semantic_edit"


def json_layout_edit_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "layout_edit"


def json_semantic_final_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "semantic_final"


def json_layout_final_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "json" / "layout_final"


def svg_dir(repo_root: Path, problem_id: str) -> Path:
    return problem_dir(repo_root, problem_id) / "svg"


def svg_edit_dir(repo_root: Path, problem_id: str) -> Path:
    return svg_dir(repo_root, problem_id) / "edit"


def svg_final_dir(repo_root: Path, problem_id: str) -> Path:
    return svg_dir(repo_root, problem_id) / "final"


def problem_input_json(repo_root: Path, problem_id: str) -> Path:
    return input_dir(repo_root, problem_id) / "problem.json"


def manim_source(repo_root: Path, problem_id: str) -> Path:
    return manim_dir(repo_root, problem_id) / f"{ensure_problem_id(problem_id)}_manim.py"


def manim_edit_source(repo_root: Path, problem_id: str) -> Path:
    return manim_edit_dir(repo_root, problem_id) / f"{ensure_problem_id(problem_id)}_manim_edit.py"


def manim_final_source(repo_root: Path, problem_id: str) -> Path:
    return manim_final_dir(repo_root, problem_id) / f"{ensure_problem_id(problem_id)}_manim_final.py"


def semantic_stage1_json(repo_root: Path, problem_id: str) -> Path:
    return json_semantic_dir(repo_root, problem_id) / "semantic.json"


def layout_stage1_json(repo_root: Path, problem_id: str) -> Path:
    return json_layout_dir(repo_root, problem_id) / "layout.json"


def svg_stage1(repo_root: Path, problem_id: str) -> Path:
    return svg_dir(repo_root, problem_id) / "semantic.svg"


def svg_stage_edit(repo_root: Path, problem_id: str) -> Path:
    return svg_edit_dir(repo_root, problem_id) / "semantic_edit.svg"


def semantic_edit_json(repo_root: Path, problem_id: str) -> Path:
    return json_semantic_edit_dir(repo_root, problem_id) / "semantic_edit.json"


def layout_edit_json(repo_root: Path, problem_id: str) -> Path:
    return json_layout_edit_dir(repo_root, problem_id) / "layout_edit.json"


def semantic_final_json(repo_root: Path, problem_id: str) -> Path:
    return json_semantic_final_dir(repo_root, problem_id) / "semantic_final.json"


def layout_final_json(repo_root: Path, problem_id: str) -> Path:
    return json_layout_final_dir(repo_root, problem_id) / "layout_final.json"


def svg_final(repo_root: Path, problem_id: str) -> Path:
    return svg_final_dir(repo_root, problem_id) / "semantic_final.svg"


def all_required_dirs(repo_root: Path, problem_id: str) -> list[Path]:
    return [
        input_dir(repo_root, problem_id),
        manim_dir(repo_root, problem_id),
        manim_edit_dir(repo_root, problem_id),
        manim_final_dir(repo_root, problem_id),
        json_semantic_dir(repo_root, problem_id),
        json_layout_dir(repo_root, problem_id),
        json_semantic_edit_dir(repo_root, problem_id),
        json_layout_edit_dir(repo_root, problem_id),
        json_semantic_final_dir(repo_root, problem_id),
        json_layout_final_dir(repo_root, problem_id),
        svg_dir(repo_root, problem_id),
        svg_edit_dir(repo_root, problem_id),
        svg_final_dir(repo_root, problem_id),
    ]
