"""Disposable, compressed render bundles keyed by authored input content."""
from __future__ import annotations

from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

from modu_math.dsl.problem_store import (
    atomic_write, file_lock, locale_path, location, override_path, review_path,
)

CACHE_VERSION = "problem-bundle-v1"


@lru_cache(maxsize=1)
def compiler_fingerprint() -> str:
    root = Path(__file__).resolve().parents[4]
    digest = hashlib.sha256()
    for folder, pattern in ((root / "src" / "modu_math", "*.py"),
                            (root / "src" / "modu_math_web" / "editor" / "services", "*.py"),
                            (root / "schema", "*.json"),
                            (root / "src" / "modu_math" / "renderer" / "assets", "*.ttf")):
        for path in sorted(folder.rglob(pattern)):
            digest.update(str(path.relative_to(root)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def fingerprint(paths) -> str:
    canonical, language, root = location(paths.dsl_path)
    digest = hashlib.sha256((CACHE_VERSION + compiler_fingerprint()).encode())
    digest.update(canonical.read_bytes())
    dependencies = [override_path(canonical, "ko")]
    if language != "ko":
        dependencies.extend([
            locale_path(paths.dsl_path, language),
            override_path(paths.dsl_path, language),
            review_path(paths.dsl_path, language),
        ])
    for dependency in dependencies:
        if dependency.is_file():
            digest.update(str(dependency).encode())
            digest.update(dependency.read_bytes())
    # Local image assets affect embedded SVG, even if no DSL text changed.
    # Generated problem SVGs are outputs, not dependencies.
    for directory in sorted({canonical.parent, paths.base_dir}):
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
                continue
            if path.suffix == ".svg" and (path.with_suffix(".dsl.py").exists()
                    or path.with_suffix(".locale-delta.json").exists()
                    or (root / "ko" / path.relative_to(directory)).with_suffix(".dsl.py").exists()):
                continue
            digest.update(str(path.relative_to(root)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def cache_path(paths) -> Path:
    identity = hashlib.sha256(paths.dsl_path.relative_to(paths.root_dir).as_posix().encode()).hexdigest()
    return paths.root_dir / ".modu-cache" / (identity + ".json.gz")


def get_artifacts(paths, *, force=False) -> dict:
    output = cache_path(paths)
    with file_lock(output.parent / "locks" / (output.stem + ".lock")):
        expected = fingerprint(paths)
        if not force and output.exists():
            try:
                cached = json.loads(gzip.decompress(output.read_bytes()))
                if cached["fingerprint"] == expected:
                    return cached["artifacts"]
            except (ValueError, OSError, EOFError, KeyError):
                pass  # A deleted, old, or corrupt cache is safe to rebuild.
        from .build import compile_problem_artifacts
        for _ in range(3):
            artifacts = compile_problem_artifacts(paths)
            after = fingerprint(paths)
            if expected == after:
                break
            expected = after
        else:
            raise ValueError("Problem changed during rendering; retry the build")
        payload = json.dumps({"fingerprint": expected, "artifacts": artifacts},
                             ensure_ascii=False, separators=(",", ":")).encode()
        atomic_write(output, gzip.compress(payload, compresslevel=6, mtime=0))
        return artifacts


def artifact_key(filename: str, prefix: str) -> str | None:
    for key in ("semantic", "layout", "renderer"):
        if filename == f"{prefix}.{key}.json":
            return key
    if filename == f"{prefix}.svg":
        return "svg"
    if filename == f"{prefix}.solvable.json" or filename in {
        f"{prefix}.solvable.v1.json", f"{prefix}.solvable.v1.1.json",
        f"{prefix}.solvable.v1.2.json", f"{prefix}.solvable.v1.3.json",
    }:
        return "solvable"
    return None
