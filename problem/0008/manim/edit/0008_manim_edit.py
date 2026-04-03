from __future__ import annotations

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


PROBLEM_ID = "0008"
SEMANTIC_EDIT_PATH = REPO_ROOT / "problem" / PROBLEM_ID / "json" / "semantic_edit" / "semantic_edit.json"


def _load_semantic() -> dict:
    if not SEMANTIC_EDIT_PATH.exists():
        raise FileNotFoundError(f"Missing semantic_edit.json: {SEMANTIC_EDIT_PATH}")
    return json.loads(SEMANTIC_EDIT_PATH.read_text(encoding="utf-8"))


def _validate_or_raise(semantic: dict) -> None:
    structure_errors = validate_structure(semantic)
    logic_errors = validate_logic(semantic)
    if structure_errors or logic_errors:
        lines = ["semantic validation failed:"]
        if structure_errors:
            lines.append("[structure]")
            lines.extend(f"- {x}" for x in structure_errors)
        if logic_errors:
            lines.append("[logic]")
            lines.extend(f"- {x}" for x in logic_errors)
        raise ValueError("\n".join(lines))


class ProblemEditScene(Scene):
    def construct(self) -> None:
        semantic = _load_semantic()
        _validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)
