from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from django.conf import settings

from .dsl_format import format_dsl_source

ARTIFACT_FILES = {
    "semantic": ".semantic.json",
    "solvable": ".solvable.json",
    "layout": ".layout.json",
    "renderer": ".renderer.json",
    "svg": ".svg",
}


@dataclass(frozen=True)
class ProblemPaths:
    problem_id: str
    root_alias: str
    root_dir: Path
    base_dir: Path
    dsl_path: Path
    artifact_base: str

    def artifact_path(self, key: str) -> Path:
        return self.base_dir / f"{self.artifact_base}{ARTIFACT_FILES[key]}"


def problems_root() -> Path:
    return Path(settings.PROBLEMS_ROOT).resolve()


def problem_roots() -> list[tuple[str, Path]]:
    roots = [("", problems_root())]
    golden_root = Path(
        getattr(settings, "GOLDEN_PROBLEMS_ROOT", Path(settings.BASE_DIR) / "examples" / "golden")
    ).resolve()
    if golden_root != roots[0][1]:
        roots.append(("golden", golden_root))
    return roots


def validate_problem_id(problem_id: str) -> str:
    if not problem_id:
        raise ValueError("problem_id is required")
    normalized = problem_id.replace("\\", "/")
    if normalized.startswith("/"):
        raise ValueError("invalid problem_id")
    parts = PurePosixPath(normalized).parts
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("invalid problem_id")
    return "/".join(parts)


def _split_problem_root(problem_id: str) -> tuple[str, str, Path]:
    parts = problem_id.split("/")
    for alias, root in problem_roots():
        if alias and parts[0] == alias:
            relative_id = "/".join(parts[1:])
            if not relative_id:
                raise ValueError("problem_id is required")
            return alias, relative_id, root
    return "", problem_id, problems_root()


def _display_problem_id(alias: str, relative_id: str) -> str:
    return f"{alias}/{relative_id}" if alias else relative_id


def resolve_problem_paths(problem_id: str) -> ProblemPaths:
    safe_problem_id = validate_problem_id(problem_id)
    alias, relative_id, root = _split_problem_root(safe_problem_id)
    target = (root / relative_id).resolve()
    if target != root and root not in target.parents:
        raise ValueError("invalid problem path")

    if target.exists() and target.is_dir():
        dsl_path = target / "problem.dsl.py"
        if not dsl_path.exists():
            raise FileNotFoundError(f"dsl file not found in folder: {safe_problem_id}")
        return ProblemPaths(
            problem_id=_display_problem_id(alias, relative_id),
            root_alias=alias,
            root_dir=root,
            base_dir=target,
            dsl_path=dsl_path,
            artifact_base="problem",
        )

    if target.exists() and target.is_file() and target.name.endswith(".dsl.py"):
        artifact_base = target.name[: -len(".dsl.py")]
        rel = target.relative_to(root).as_posix()
        return ProblemPaths(
            problem_id=_display_problem_id(alias, rel),
            root_alias=alias,
            root_dir=root,
            base_dir=target.parent,
            dsl_path=target,
            artifact_base=artifact_base,
        )

    raise FileNotFoundError(f"problem not found: {safe_problem_id}")


def _find_solvable_path(base_dir: Path, artifact_base: str) -> Path | None:
    canonical = base_dir / f"{artifact_base}{ARTIFACT_FILES['solvable']}"
    if canonical.exists():
        return canonical
    versioned = sorted(base_dir.glob(f"{artifact_base}.solvable.v*.json"))
    if not versioned:
        return None
    return versioned[-1]


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def list_problem_directories() -> list[dict[str, Any]]:
    problems: list[dict[str, Any]] = []
    for alias, root in problem_roots():
        if not root.exists():
            continue
        for dsl_path in sorted(root.rglob("problem.dsl.py")):
            child = dsl_path.parent
            artifact_base = "problem"
            solvable_path = _find_solvable_path(child, artifact_base)
            relative_id = child.relative_to(root).as_posix()
            problems.append(
                {
                    "problem_id": _display_problem_id(alias, relative_id),
                    "root": alias or "problems",
                    "path": str(child.relative_to(root.parent)).replace("\\", "/"),
                    "has_input_png": (child / "input.png").exists(),
                    "has_dsl": True,
                    "has_semantic": (child / f"{artifact_base}{ARTIFACT_FILES['semantic']}").exists(),
                    "has_solvable": solvable_path is not None,
                    "has_layout": (child / f"{artifact_base}{ARTIFACT_FILES['layout']}").exists(),
                    "has_renderer": (child / f"{artifact_base}{ARTIFACT_FILES['renderer']}").exists(),
                    "has_svg": (child / f"{artifact_base}{ARTIFACT_FILES['svg']}").exists(),
                }
            )

        for dsl_path in sorted(root.rglob("*.dsl.py")):
            if dsl_path.name == "problem.dsl.py":
                continue
            child = dsl_path.parent
            artifact_base = dsl_path.name[: -len(".dsl.py")]
            solvable_path = _find_solvable_path(child, artifact_base)
            relative_id = dsl_path.relative_to(root).as_posix()
            problems.append(
                {
                    "problem_id": _display_problem_id(alias, relative_id),
                    "root": alias or "problems",
                    "path": str(child.relative_to(root.parent)).replace("\\", "/"),
                    "has_input_png": (child / "input.png").exists(),
                    "has_dsl": True,
                    "has_semantic": (child / f"{artifact_base}{ARTIFACT_FILES['semantic']}").exists(),
                    "has_solvable": solvable_path is not None,
                    "has_layout": (child / f"{artifact_base}{ARTIFACT_FILES['layout']}").exists(),
                    "has_renderer": (child / f"{artifact_base}{ARTIFACT_FILES['renderer']}").exists(),
                    "has_svg": (child / f"{artifact_base}{ARTIFACT_FILES['svg']}").exists(),
                }
            )
    return sorted(problems, key=lambda p: p["problem_id"])


def read_problem_detail(problem_id: str) -> dict[str, Any]:
    paths = resolve_problem_paths(problem_id)
    dsl = paths.dsl_path.read_text(encoding="utf-8")
    solvable_path = _find_solvable_path(paths.base_dir, paths.artifact_base)
    return {
        "problem_id": paths.problem_id,
        "base_dir": str(paths.base_dir),
        "dsl": dsl,
        "semantic": _read_json(paths.artifact_path("semantic")),
        "solvable": _read_json(solvable_path) if solvable_path else None,
        "layout": _read_json(paths.artifact_path("layout")),
        "renderer": _read_json(paths.artifact_path("renderer")),
        "svg": _read_text(paths.artifact_path("svg")),
    }


def save_problem_dsl(problem_id: str, dsl: str) -> tuple[ProblemPaths, str]:
    paths = resolve_problem_paths(problem_id)
    formatted = format_dsl_source(dsl)
    paths.dsl_path.write_text(formatted, encoding="utf-8")
    return paths, formatted


def format_problem_dsl(problem_id: str) -> tuple[ProblemPaths, str]:
    paths = resolve_problem_paths(problem_id)
    dsl = paths.dsl_path.read_text(encoding="utf-8")
    formatted = format_dsl_source(dsl)
    paths.dsl_path.write_text(formatted, encoding="utf-8")
    return paths, formatted


def read_artifacts(problem_id: str) -> dict[str, Any]:
    paths = resolve_problem_paths(problem_id)
    solvable_path = _find_solvable_path(paths.base_dir, paths.artifact_base)
    return {
        "semantic": _read_json(paths.artifact_path("semantic")),
        "solvable": _read_json(solvable_path) if solvable_path else None,
        "layout": _read_json(paths.artifact_path("layout")),
        "renderer": _read_json(paths.artifact_path("renderer")),
        "svg": _read_text(paths.artifact_path("svg")),
    }
