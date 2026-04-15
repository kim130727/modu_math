from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from django.conf import settings


_SAFE_SEGMENT_RE = re.compile(r"[^a-zA-Z0-9_-]+")


def _store_root() -> Path:
    return Path(settings.PROBLEM_STORE_ROOT)


def _sanitize_segment(seg: str) -> str:
    cleaned = _SAFE_SEGMENT_RE.sub("_", seg.strip())
    return cleaned.strip("_") or "untitled"


def normalize_problem_id(problem_id: str) -> str:
    text = (problem_id or "").replace("\\", "/").strip("/")
    if not text:
        return "untitled_problem"
    parts = [p for p in text.split("/") if p and p != "."]
    safe_parts = [_sanitize_segment(p) for p in parts if p != ".."]
    return "/".join(safe_parts) or "untitled_problem"


def _safe_rel_problem_id(problem_id: str) -> str:
    normalized = normalize_problem_id(problem_id)
    p = PurePosixPath(normalized)
    if p.is_absolute() or ".." in p.parts:
        return "untitled_problem"
    return p.as_posix()


def _id_from_candidate(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    if path.name == "semantic.json":
        return "/".join(parts[:-1]) or None
    if len(parts) >= 4 and parts[-3:] == ["output", "json", parts[-1]] and path.name.endswith(".semantic.json"):
        return "/".join(parts[:-3]) or None
    if path.name.endswith(".semantic.json"):
        # ex) geometry_3k/2401/2401.semantic.json
        return "/".join(parts[:-1]) or None
    if len(parts) >= 4 and parts[-3:] == ["input", "json", "semantic_final.json"]:
        return "/".join(parts[:-3]) or None
    return None


def _discover_candidates() -> dict[str, Path]:
    root = _store_root()
    root.mkdir(parents=True, exist_ok=True)

    # 우선순위: semantic.json > output/json/*.semantic.json > input/json/semantic_final.json
    collected: dict[str, tuple[int, Path]] = {}

    def put(path: Path, priority: int) -> None:
        problem_id = _id_from_candidate(path, root)
        if not problem_id:
            return
        prev = collected.get(problem_id)
        if prev is None or priority < prev[0]:
            collected[problem_id] = (priority, path)

    for path in root.rglob("semantic.json"):
        put(path, 1)
    for path in root.rglob("*.semantic.json"):
        # Avoid re-picking plain semantic.json if name happens to match pattern.
        if path.name == "semantic.json":
            continue
        put(path, 2)
    for path in root.rglob("semantic_final.json"):
        put(path, 3)

    return {k: v[1] for k, v in collected.items()}


def semantic_path(problem_id: str) -> Path:
    root = _store_root()
    safe_id = _safe_rel_problem_id(problem_id)
    known = _discover_candidates().get(safe_id)
    if known is not None:
        return known
    return root / safe_id / "semantic.json"


def list_problems() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for problem_id, path in sorted(_discover_candidates().items(), key=lambda item: item[0]):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        rows.append(
            {
                "problem_id": problem_id,
                "title": data.get("title") or problem_id,
                "problem_type": data.get("problem_type") or "",
                "path": path,
            }
        )
    return rows


def load_semantic(problem_id: str) -> dict[str, Any]:
    path = semantic_path(problem_id)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    safe_id = _safe_rel_problem_id(problem_id)
    return {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": safe_id.replace("/", "_"),
        "problem_type": "generic",
        "metadata": {},
        "domain": {},
        "render": {
            "canvas": {"width": 1200, "height": 700, "background": "#F6F6F6"},
            "elements": [],
        },
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }


def save_semantic(problem_id: str, semantic: dict[str, Any]) -> Path:
    path = semantic_path(problem_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
