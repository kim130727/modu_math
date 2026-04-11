from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .index_schema import RagRunLog


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_run_log(
    *,
    runs_path: str | Path,
    run_id: str,
    input_meta: dict[str, Any],
    retrieved_examples: list[str],
    generated_py_path: str,
    build_success: bool,
    validation_success: bool,
    error_message: str = "",
) -> RagRunLog:
    path = Path(runs_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    record: RagRunLog = {
        "run_id": run_id,
        "input_meta": input_meta,
        "retrieved_examples": retrieved_examples,
        "generated_py_path": generated_py_path,
        "build_success": build_success,
        "validation_success": validation_success,
        "error_message": error_message,
        "created_at": _now_iso(),
    }

    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def load_run_logs(runs_path: str | Path) -> list[RagRunLog]:
    path = Path(runs_path)
    if not path.exists():
        return []

    rows: list[RagRunLog] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows
