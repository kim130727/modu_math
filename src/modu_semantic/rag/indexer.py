from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..schema import validate_layout_json, validate_semantic_json
from ..validator import validate_problem_bundle
from .index_schema import RagIndexEntry


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_python_file(problem_dir: Path) -> Path | None:
    candidates = sorted([p for p in problem_dir.glob("*.py") if p.name != "_problem_runner.py"])
    if not candidates:
        return None
    direct = problem_dir / f"{problem_dir.name}.py"
    if direct.exists():
        return direct
    return candidates[0]


def _find_semantic_file(problem_dir: Path) -> Path | None:
    output_json_dir = problem_dir / "output" / "json"
    if output_json_dir.exists():
        semantic_candidates = sorted(output_json_dir.glob("*.semantic.json"))
        if semantic_candidates:
            return semantic_candidates[0]

    input_semantic = problem_dir / "input" / "json" / "semantic_final.json"
    if input_semantic.exists():
        return input_semantic

    return None


def _find_layout_file(problem_dir: Path) -> Path | None:
    output_json_dir = problem_dir / "output" / "json"
    if output_json_dir.exists():
        layout_candidates = sorted(output_json_dir.glob("*.layout.json"))
        if layout_candidates:
            return layout_candidates[0]

    input_layout = problem_dir / "input" / "json" / "layout_final.json"
    if input_layout.exists():
        return input_layout

    return None


def _infer_tags(problem_id: str, problem_type: str, topic: str) -> list[str]:
    tokens = [token for token in problem_id.replace("-", "_").split("_") if token]
    tags = set(tokens)
    if problem_type and problem_type != "unknown":
        tags.add(problem_type)
        tags.update([token for token in problem_type.replace("-", "_").split("_") if token])
    if topic and topic != "unknown":
        tags.add(topic)
    return sorted(tags)


def _validate_discovered_files(
    *,
    problem_dir: Path,
    semantic_path: Path | None,
    layout_path: Path | None,
    semantic: dict[str, Any],
    layout: dict[str, Any],
) -> tuple[bool, list[str]]:
    errors = validate_problem_bundle(problem_dir)
    if not errors:
        return True, []

    fallback_errors: list[str] = []
    if semantic_path is None or not semantic:
        fallback_errors.append("Missing discovered semantic file.")
    else:
        try:
            validate_semantic_json(semantic)
        except Exception as exc:  # noqa: BLE001
            fallback_errors.append(f"Discovered semantic validation failed ({semantic_path}): {exc}")

    if layout_path is None or not layout:
        fallback_errors.append("Missing discovered layout file.")
    else:
        try:
            validate_layout_json(layout)
        except Exception as exc:  # noqa: BLE001
            fallback_errors.append(f"Discovered layout validation failed ({layout_path}): {exc}")

    if not fallback_errors:
        return True, []
    return False, fallback_errors


def _infer_layout_pattern(layout: dict[str, Any]) -> str:
    summary = layout.get("summary") if isinstance(layout, dict) else None
    if isinstance(summary, dict):
        total = summary.get("total_elements")
        if isinstance(total, int):
            if total <= 10:
                return "simple"
            if total <= 30:
                return "medium"
            return "dense"
    return "unknown"


def _infer_answer_style(semantic: dict[str, Any]) -> str:
    answer = semantic.get("answer") if isinstance(semantic, dict) else None
    if not isinstance(answer, dict):
        return "unknown"

    if answer.get("choices"):
        return "multiple_choice"
    if answer.get("blanks"):
        return "blank"
    if answer.get("answer_key"):
        return "answer_key_only"
    return "unknown"


def _relative(path: Path | None, root: Path) -> str:
    if path is None:
        return ""
    return path.relative_to(root).as_posix()


def build_index_entries(examples_root: str | Path = "examples/problem") -> list[RagIndexEntry]:
    root = Path(examples_root)
    if not root.exists():
        return []

    entries: list[RagIndexEntry] = []
    for problem_dir in sorted([d for d in root.iterdir() if d.is_dir()], key=lambda p: p.name):
        if problem_dir.name.startswith("_"):
            continue

        py_path = _find_python_file(problem_dir)
        semantic_path = _find_semantic_file(problem_dir)
        layout_path = _find_layout_file(problem_dir)

        semantic = _load_json(semantic_path) if semantic_path and semantic_path.exists() else {}
        layout = _load_json(layout_path) if layout_path and layout_path.exists() else {}

        validation_passed, validation_errors = _validate_discovered_files(
            problem_dir=problem_dir,
            semantic_path=semantic_path,
            layout_path=layout_path,
            semantic=semantic,
            layout=layout,
        )

        problem_id = str(semantic.get("problem_id") or problem_dir.name)
        problem_type = str(semantic.get("problem_type") or "unknown")
        topic = "unknown"
        grade = "unknown"
        visual_primitives: list[str] = []

        render = semantic.get("render") if isinstance(semantic, dict) else None
        if isinstance(render, dict):
            elements = render.get("elements")
            if isinstance(elements, list):
                visual_primitives = sorted(
                    {str(el.get("type")) for el in elements if isinstance(el, dict) and el.get("type")}
                )

        tags = _infer_tags(problem_id=problem_id, problem_type=problem_type, topic=topic)

        entry: RagIndexEntry = {
            "problem_id": problem_id,
            "py_path": _relative(py_path, root),
            "semantic_path": _relative(semantic_path, root),
            "layout_path": _relative(layout_path, root),
            "tags": tags,
            "validation_passed": validation_passed,
            "updated_at": _now_iso(),
            "problem_type": problem_type,
            "grade": grade,
            "topic": topic,
            "visual_primitives": visual_primitives,
            "layout_pattern": _infer_layout_pattern(layout),
            "answer_style": _infer_answer_style(semantic),
            "failure_notes": "; ".join(validation_errors),
            "source_image_hash": "",
        }
        entries.append(entry)

    return entries


def write_index_jsonl(entries: list[RagIndexEntry], index_path: str | Path) -> Path:
    path = Path(index_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [json.dumps(entry, ensure_ascii=False) for entry in entries]
    text = "\n".join(lines)
    if text:
        text += "\n"
    path.write_text(text, encoding="utf-8")
    return path


def build_and_write_index(
    *,
    examples_root: str | Path = "examples/problem",
    index_path: str | Path = "examples/problem/_rag/index.jsonl",
) -> Path:
    entries = build_index_entries(examples_root=examples_root)
    return write_index_jsonl(entries, index_path)


def load_index_jsonl(index_path: str | Path) -> list[RagIndexEntry]:
    path = Path(index_path)
    if not path.exists():
        return []

    entries: list[RagIndexEntry] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        entries.append(json.loads(line))
    return entries
