from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image
from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_version_key(tag: str) -> tuple[int, ...]:
    return tuple(int(p) for p in tag[1:].split("."))


def find_latest_solvable_schema_path(repo: Path) -> Path:
    schema_dir = repo / "schema" / "solvable"
    candidates: list[tuple[tuple[int, ...], Path]] = []
    for path in schema_dir.glob("solvable.v*.json"):
        tag = path.stem.replace("solvable.", "", 1)
        if not tag.startswith("v"):
            continue
        try:
            key = _schema_version_key(tag)
        except ValueError:
            continue
        candidates.append((key, path))
    if not candidates:
        raise FileNotFoundError(f"No solvable schema files found in: {schema_dir}")
    candidates.sort(key=lambda x: x[0])
    return candidates[-1][1]


def find_latest_solvable_artifact(base: Path) -> Path | None:
    candidates: list[tuple[tuple[int, ...], Path]] = []
    for path in base.parent.glob(f"{base.name}.solvable.v*.json"):
        tag = path.stem.split(".solvable.", 1)[-1]
        if not tag.startswith("v"):
            continue
        try:
            key = _schema_version_key(tag)
        except ValueError:
            continue
        candidates.append((key, path))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[-1][1]


def run_build(dsl_path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            "scripts/watch_build.ps1",
            "-DslPath",
            str(dsl_path),
            "-Once",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    ok = proc.returncode == 0 and "build_ok" in output
    return ok, output


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    raw_dir = repo / "examples/problems/260427/raw"
    if not raw_dir.exists():
        print(f"raw dir not found: {raw_dir}")
        return 1

    semantic_schema = load_json(repo / "schema/semantic/semantic.v1.json")
    solvable_schema = load_json(find_latest_solvable_schema_path(repo))

    sem_validator = Draft202012Validator(semantic_schema)
    sol_validator = Draft202012Validator(solvable_schema)

    rows: list[dict] = []

    for dsl_path in sorted(raw_dir.glob("*.dsl.py")):
        stem = dsl_path.name.replace(".dsl.py", "")
        base = raw_dir / stem
        row = {
            "id": stem,
            "build_ok": False,
            "semantic_ok": False,
            "solvable_ok": False,
            "size_match": False,
            "question_marks": {},
            "errors": [],
        }

        build_ok, out = run_build(dsl_path)
        row["build_ok"] = build_ok
        if not build_ok:
            row["errors"].append("build_failed")
            row["errors"].append(out.splitlines()[-1] if out.splitlines() else "unknown")
            rows.append(row)
            continue

        sem_path = base.with_suffix(".semantic.json")
        sol_path = find_latest_solvable_artifact(base)
        lay_path = base.with_suffix(".layout.json")
        png_path = base.with_suffix(".png")
        svg_path = base.with_suffix(".svg")

        try:
            sem = load_json(sem_path)
            sem_validator.validate(sem)
            row["semantic_ok"] = True
        except Exception as exc:  # noqa: BLE001
            row["errors"].append(f"semantic_schema_error: {exc}")

        try:
            if sol_path is None:
                raise FileNotFoundError("no solvable.v*.json artifact found")
            sol = load_json(sol_path)
            sol_validator.validate(sol)
            row["solvable_ok"] = True
        except Exception as exc:  # noqa: BLE001
            row["errors"].append(f"solvable_schema_error: {exc}")

        try:
            layout = load_json(lay_path)
            with Image.open(png_path) as img:
                w, h = img.size
            lw = int(layout["canvas"]["width"])
            lh = int(layout["canvas"]["height"])
            row["size_match"] = (w == lw and h == lh)
            if not row["size_match"]:
                row["errors"].append(f"size_mismatch png=({w},{h}) layout=({lw},{lh})")
        except Exception as exc:  # noqa: BLE001
            row["errors"].append(f"size_check_error: {exc}")

        for p in [sem_path, sol_path, svg_path]:
            try:
                txt = p.read_text(encoding="utf-8")
                row["question_marks"][p.name] = txt.count("?")
            except Exception as exc:  # noqa: BLE001
                row["question_marks"][p.name] = f"read_error: {exc}"

        rows.append(row)

    report = {
        "total": len(rows),
        "build_fail": sum(1 for r in rows if not r["build_ok"]),
        "semantic_fail": sum(1 for r in rows if not r["semantic_ok"]),
        "solvable_fail": sum(1 for r in rows if not r["solvable_ok"]),
        "size_mismatch": sum(1 for r in rows if not r["size_match"]),
        "rows": rows,
    }

    out_path = raw_dir / "audit_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote: {out_path}")
    print(
        "summary:",
        {
            "total": report["total"],
            "build_fail": report["build_fail"],
            "semantic_fail": report["semantic_fail"],
            "solvable_fail": report["solvable_fail"],
            "size_mismatch": report["size_mismatch"],
        },
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
