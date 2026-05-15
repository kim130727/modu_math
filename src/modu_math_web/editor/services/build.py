from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .problems import read_artifacts, resolve_problem_paths, validate_problem_id


@dataclass
class BuildResult:
    ok: bool
    stdout: str
    stderr: str
    error: str | None = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def run_problem_build(problem_id: str) -> BuildResult:
    safe_problem_id = validate_problem_id(problem_id)
    problem_paths = resolve_problem_paths(safe_problem_id)
    repo_root = _repo_root()
    script_path = repo_root / "scripts" / "watch_build.ps1"
    cmd = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-DslPath",
        str(problem_paths.dsl_path),
        "-Once",
    ]

    try:
        completed = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except Exception as exc:  # pragma: no cover
        return BuildResult(ok=False, stdout="", stderr="", error=str(exc))

    ok = completed.returncode == 0
    return BuildResult(
        ok=ok,
        stdout=completed.stdout,
        stderr=completed.stderr,
        error=None if ok else f"build exited with code {completed.returncode}",
    )


def build_with_artifacts(problem_id: str) -> tuple[BuildResult, dict[str, Any]]:
    result = run_problem_build(problem_id)
    artifacts = read_artifacts(problem_id)
    return result, artifacts
