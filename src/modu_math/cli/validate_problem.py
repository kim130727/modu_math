from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        src_dir = parent / "src"
        if src_dir.is_dir():
            src_path = str(src_dir)
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            return
    raise RuntimeError("Could not locate src directory.")


_ensure_src_on_path()

from modu_math.validators.validate import run_all_validations


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Validate semantic.json with schema/logic/layout validators.")
    parser.add_argument("--semantic", type=Path, required=True)
    args = parser.parse_args()

    semantic = json.loads(args.semantic.read_text(encoding="utf-8-sig"))
    report = run_all_validations(semantic)
    if not report.ok:
        print(report.to_text())
        raise SystemExit(1)
    print("[OK] semantic payload is valid")


if __name__ == "__main__":
    run_cli()
