from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

def _ensure_repo_root_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise RuntimeError("Could not locate repository root from stage_cli.py")


_ensure_repo_root_on_path()

from problem.common.layout_tools import write_layout, write_layout_diff
from problem.common.semantic_edit_tools import build_semantic_edit_from_svg
from problem.common.stage_paths import (
    all_required_dirs,
    layout_edit_json,
    layout_final_json,
    layout_stage1_json,
    manim_edit_source,
    manim_source,
    problem_dir,
    problem_input_json,
    semantic_edit_json,
    semantic_final_json,
    semantic_stage1_json,
    svg_final,
    svg_stage1,
    svg_stage_edit,
)
from problem.common.validator import validate_logic, validate_structure


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run_python(args: list[str], repo_root: Path) -> None:
    cmd = [sys.executable, *args]
    result = subprocess.run(cmd, cwd=repo_root, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}")


def _validate_semantic_file(path: Path) -> None:
    import json

    semantic = json.loads(path.read_text(encoding="utf-8"))
    structure = validate_structure(semantic)
    logic = validate_logic(semantic)
    if structure or logic:
        lines = [f"semantic validation failed: {path}"]
        if structure:
            lines.append("[structure]")
            lines.extend(f"- {x}" for x in structure)
        if logic:
            lines.append("[logic]")
            lines.extend(f"- {x}" for x in logic)
        raise ValueError("\n".join(lines))


def _write_edit_manim_if_missing(repo_root: Path, problem_id: str) -> Path:
    out = manim_edit_source(repo_root, problem_id)
    if out.exists():
        return out

    template = f'''from __future__ import annotations

import json
import sys
from pathlib import Path

from manim import Scene

sys.dont_write_bytecode = True


def _ensure_repo_root_on_path() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return parent
    raise RuntimeError("Repository root could not be resolved.")


REPO_ROOT = _ensure_repo_root_on_path()

from problem.common.manim_renderer import render_manim_from_semantic
from problem.common.validator import validate_logic, validate_structure


PROBLEM_ID = "{problem_id}"
SEMANTIC_EDIT_PATH = REPO_ROOT / "problem" / PROBLEM_ID / "json" / "semantic_edit" / "semantic_edit.json"


def _load_semantic() -> dict:
    if not SEMANTIC_EDIT_PATH.exists():
        raise FileNotFoundError(f"Missing semantic_edit.json: {{SEMANTIC_EDIT_PATH}}")
    return json.loads(SEMANTIC_EDIT_PATH.read_text(encoding="utf-8"))


def _validate_or_raise(semantic: dict) -> None:
    structure_errors = validate_structure(semantic)
    logic_errors = validate_logic(semantic)
    if structure_errors or logic_errors:
        lines = ["semantic validation failed:"]
        if structure_errors:
            lines.append("[structure]")
            lines.extend(f"- {{x}}" for x in structure_errors)
        if logic_errors:
            lines.append("[logic]")
            lines.extend(f"- {{x}}" for x in logic_errors)
        raise ValueError("\\n".join(lines))


class ProblemEditScene(Scene):
    def construct(self) -> None:
        semantic = _load_semantic()
        _validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)
'''
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template, encoding="utf-8")
    return out


def init_problem_structure(repo_root: Path, problem_id: str) -> None:
    for d in all_required_dirs(repo_root, problem_id):
        d.mkdir(parents=True, exist_ok=True)
    _write_edit_manim_if_missing(repo_root, problem_id)
    print(f"[OK] initialized structure: {problem_dir(repo_root, problem_id)}")


def run_stage1(repo_root: Path, problem_id: str) -> None:
    source = manim_source(repo_root, problem_id)
    if not source.exists():
        raise FileNotFoundError(f"missing manim source: {source}")
    if not problem_input_json(repo_root, problem_id).exists():
        raise FileNotFoundError(f"missing input/problem.json: {problem_input_json(repo_root, problem_id)}")

    semantic_out = semantic_stage1_json(repo_root, problem_id)
    svg_out = svg_stage1(repo_root, problem_id)

    _run_python(
        [
            str(source),
            "--export-semantic",
            "--semantic-out",
            str(semantic_out),
            "--problem-in",
            str(problem_input_json(repo_root, problem_id)),
        ],
        repo_root,
    )
    _run_python(
        [
            str(source),
            "--render-svg",
            "--semantic-in",
            str(semantic_out),
            "--svg-out",
            str(svg_out),
        ],
        repo_root,
    )
    write_layout(svg_out, layout_stage1_json(repo_root, problem_id))
    print(f"[OK] stage1 complete: semantic/layout/svg generated for {problem_id}")


def run_stage2(repo_root: Path, problem_id: str) -> None:
    stage1_sem = semantic_stage1_json(repo_root, problem_id)
    stage1_svg = svg_stage1(repo_root, problem_id)
    edit_svg = svg_stage_edit(repo_root, problem_id)
    sem_edit = semantic_edit_json(repo_root, problem_id)
    lay_edit = layout_edit_json(repo_root, problem_id)

    if not stage1_sem.exists() or not stage1_svg.exists():
        raise FileNotFoundError("stage1 outputs are missing. run stage1 first.")
    if not edit_svg.exists():
        edit_svg.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(stage1_svg, edit_svg)
        print(f"[INFO] no edited svg found, seeded: {edit_svg}")

    write_layout(edit_svg, lay_edit)
    write_layout_diff(stage1_svg, edit_svg, lay_edit.with_name("layout_diff_stage1_to_edit.json"))
    build_semantic_edit_from_svg(stage1_sem, edit_svg, sem_edit)
    _validate_semantic_file(sem_edit)
    print(f"[OK] stage2 complete: semantic_edit/layout_edit generated for {problem_id}")


def run_final(repo_root: Path, problem_id: str) -> None:
    sem_edit = semantic_edit_json(repo_root, problem_id)
    if not sem_edit.exists():
        raise FileNotFoundError("semantic_edit.json is missing. run stage2 first.")

    sem_final = semantic_final_json(repo_root, problem_id)
    lay_final = layout_final_json(repo_root, problem_id)
    svg_out = svg_final(repo_root, problem_id)

    sem_final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(sem_edit, sem_final)

    from problem.common.svg_renderer import render_svg_from_semantic
    import json

    semantic = json.loads(sem_final.read_text(encoding="utf-8"))
    _validate_semantic_file(sem_final)
    render_svg_from_semantic(semantic, svg_out)
    write_layout(svg_out, lay_final)
    print(f"[OK] final complete: semantic/layout/svg final generated for {problem_id}")


def run_all(repo_root: Path, problem_id: str) -> None:
    init_problem_structure(repo_root, problem_id)
    run_stage1(repo_root, problem_id)
    run_stage2(repo_root, problem_id)
    run_final(repo_root, problem_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Staged pipeline for problem/{id} structure: stage1 -> edit -> final")
    parser.add_argument("--problem-id", required=True, help="Problem id in 4 digits, e.g. 0003")
    parser.add_argument(
        "--step",
        default="all",
        choices=["init", "stage1", "stage2", "final", "all"],
        help="Pipeline step to run",
    )
    args = parser.parse_args()

    root = _repo_root()
    pid = args.problem_id
    step = args.step

    if step == "init":
        init_problem_structure(root, pid)
        return
    if step == "stage1":
        run_stage1(root, pid)
        return
    if step == "stage2":
        run_stage2(root, pid)
        return
    if step == "final":
        run_final(root, pid)
        return
    run_all(root, pid)


if __name__ == "__main__":
    main()
