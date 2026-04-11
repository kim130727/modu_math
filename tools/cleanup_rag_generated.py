from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_runs(runs_path: Path) -> list[dict]:
    if not runs_path.exists():
        return []
    rows: list[dict] = []
    for raw in runs_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _collect_failed_generated_files(runs: list[dict]) -> set[Path]:
    files: set[Path] = set()
    for row in runs:
        if bool(row.get("build_success")) and bool(row.get("validation_success")):
            continue
        generated = str(row.get("generated_py_path") or "").strip()
        if generated:
            files.add(Path(generated))
    return files


def _collect_old_runid_artifacts(generated_dir: Path, keep_prefixes: set[str]) -> set[Path]:
    delete_set: set[Path] = set()
    for path in generated_dir.glob("rag_*.*"):
        stem = path.name.split(".", 1)[0]
        if stem in keep_prefixes:
            continue
        delete_set.add(path)
    return delete_set


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cleanup RAG generated artifacts")
    parser.add_argument("--runs-path", default="examples/problem/_rag/runs.jsonl")
    parser.add_argument("--generated-dir", default="examples/problem/_rag/generated")
    parser.add_argument("--delete-failed", action="store_true", help="Delete generated_py_path files from failed runs")
    parser.add_argument(
        "--delete-old-runid",
        action="store_true",
        help="Delete legacy rag_<runid>.* artifacts (keeps the latest run id only)",
    )
    parser.add_argument("--apply", action="store_true", help="Actually delete files (default is dry-run)")
    args = parser.parse_args(argv)

    runs_path = Path(args.runs_path)
    generated_dir = Path(args.generated_dir)
    runs = _load_runs(runs_path)

    to_delete: set[Path] = set()
    if args.delete_failed:
        to_delete.update(_collect_failed_generated_files(runs))

    if args.delete_old_runid and runs:
        latest_run_id = str(runs[-1].get("run_id") or "")
        keep = {latest_run_id} if latest_run_id else set()
        to_delete.update(_collect_old_runid_artifacts(generated_dir, keep))

    existing = sorted([p for p in to_delete if p.exists()], key=lambda p: str(p))

    if not existing:
        print("No cleanup targets found.")
        return 0

    print("Cleanup targets:")
    for path in existing:
        print(f"  - {path}")

    if not args.apply:
        print("Dry-run only. Add --apply to delete.")
        return 0

    for path in existing:
        path.unlink(missing_ok=True)

    print(f"Deleted {len(existing)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
