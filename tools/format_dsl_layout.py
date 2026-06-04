from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def format_layout_sections(text: str) -> str:
    # Normalize newlines first.
    s = text.replace("\r\n", "\n").replace("\r", "\n")

    # Keep top-level sections visually separated.
    s = s.replace(
        "PROBLEM_TEMPLATE = build_problem_template()\nSEMANTIC_OVERRIDE =",
        "PROBLEM_TEMPLATE = build_problem_template()\n\nSEMANTIC_OVERRIDE =",
    )
    s = s.replace("}\nSOLVABLE =", "}\n\nSOLVABLE =")

    # Avoid overly large blank areas.
    while "\n\n\n" in s:
        s = s.replace("\n\n\n", "\n\n")

    return s.rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format DSL python file layout without touching string content."
    )
    parser.add_argument("--dsl", required=True, help="Path to *.dsl.py")
    args = parser.parse_args()

    path = Path(args.dsl)
    src = path.read_text(encoding="utf-8")
    out = format_layout_sections(src)
    if out != src:
        path.write_text(out, encoding="utf-8", newline="\n")

    # Apply full Python formatter for readability while preserving code semantics.
    proc = subprocess.run(
        [sys.executable, "-m", "black", "--quiet", str(path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"black failed for {path}: {proc.stderr.strip()}")

    print(f"Formatted DSL layout: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
