from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from django.conf import settings


_SAFE_ID_RE = re.compile(r"[^a-zA-Z0-9_-]+")


def _store_root() -> Path:
    return Path(settings.PROBLEM_STORE_ROOT)


def normalize_problem_id(problem_id: str) -> str:
    normalized = _SAFE_ID_RE.sub("_", (problem_id or "").strip())
    return normalized.strip("_") or "untitled_problem"


def semantic_path(problem_id: str) -> Path:
    safe_id = normalize_problem_id(problem_id)
    return _store_root() / safe_id / "semantic.json"


def list_problems() -> list[dict[str, Any]]:
    root = _store_root()
    root.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/semantic.json")):
        problem_id = path.parent.name
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
    if not path.exists():
        return {
            "schema_version": "modu_math.semantic.v3",
            "render_contract_version": "modu_math.render.v1",
            "problem_id": normalize_problem_id(problem_id),
            "problem_type": "generic",
            "metadata": {},
            "domain": {},
            "render": {
                "canvas": {"width": 1200, "height": 700, "background": "#F6F6F6"},
                "elements": [],
            },
            "answer": {"blanks": [], "choices": [], "answer_key": []},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_semantic(problem_id: str, semantic: dict[str, Any]) -> Path:
    path = semantic_path(problem_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

