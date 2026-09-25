"""Shared content access for the editor, learning import, and mobile dev server."""
from __future__ import annotations

import json
from pathlib import Path

from modu_math.dsl.problem_store import (
    LANGUAGES, consolidated, locale_path, location, override_path, review_path,
    virtual_paths,
)
from .problems import ProblemPaths


def paths_for(root: Path, relative_id: str) -> ProblemPaths:
    root = root.resolve()
    path = (root / relative_id).resolve()
    if root not in path.parents or not path.name.endswith(".dsl.py"):
        raise ValueError("Invalid content path")
    return ProblemPaths(path.relative_to(root).as_posix(), "", root, path.parent,
                        path, path.name.removesuffix(".dsl.py"))


def list_content(root: Path, language: str | None = None):
    root = root.resolve()
    if language is not None and language not in LANGUAGES:
        raise ValueError("Unsupported language")
    candidates = set(virtual_paths(root))
    candidates.update(path for path in (root / "ko").rglob("*.dsl.py") if consolidated(path))
    candidates.update(path.with_name(path.name.removesuffix(".renderer.json") + ".dsl.py")
                      for path in root.glob("*/*.renderer.json"))
    for path in sorted(candidates):
        relative = path.relative_to(root)
        if relative.parts[0] not in LANGUAGES or (language and relative.parts[0] != language):
            continue
        yield paths_for(root, relative.as_posix())


def read_content(paths) -> dict:
    if consolidated(paths.dsl_path):
        from .artifact_cache import get_artifacts
        return get_artifacts(paths)
    result = {}
    for key in ("semantic", "layout", "renderer", "solvable", "svg"):
        path = paths.artifact_path(key)
        if key == "solvable" and not path.exists():
            candidates = sorted(paths.base_dir.glob(paths.artifact_base + ".solvable.v*.json"))
            path = candidates[-1] if candidates else path
        result[key] = (path.read_text(encoding="utf-8-sig") if key == "svg" else
                       json.loads(path.read_text(encoding="utf-8-sig"))) if path.exists() else ("" if key == "svg" else {})
    return result


def source_files(paths):
    if consolidated(paths.dsl_path):
        canonical, language, _ = location(paths.dsl_path)
        files = [canonical, override_path(canonical, "ko")]
        if language != "ko":
            files.extend([
                locale_path(paths.dsl_path, language),
                override_path(paths.dsl_path, language),
                review_path(paths.dsl_path, language),
            ])
        return [path for path in files if path.exists()]
    return [path for path in paths.base_dir.glob(paths.artifact_base + ".*.json") if path.is_file()]


def content_title(paths, default: str) -> str:
    if consolidated(paths.dsl_path):
        from modu_math.dsl.variants import load_module
        return load_module(paths.dsl_path).PROBLEM_TEMPLATE.title
    data = read_content(paths).get("semantic", {})
    return data.get("metadata", {}).get("title") or default
