"""Utilities for preparing and verifying student-safe builds across Web, Android, and iOS.

Ensures no authored problem DSLs, solutions, or offline answer artifacts leak into production apps.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

REPO = Path(__file__).resolve().parents[3]
APP_DIR = REPO / "apps/mobile"

FORBIDDEN_EXTENSIONS = (
    ".dsl.py",
    ".semantic.json",
    ".solvable.json",
    ".renderer.json",
    ".layout.json",
)

FORBIDDEN_PATHS = (
    "generated/examples",
    "examples/problems",
)


def verify_student_bundle(directory: Path | str) -> list[str]:
    """Scan directory recursively and assert no raw answers or authoring files exist.

    Returns list of violations, or empty list if valid.
    """
    target = Path(directory)
    if not target.is_dir():
        raise ValueError(f"Target directory does not exist: {target}")

    violations: list[str] = []
    for file in target.rglob("*"):
        if not file.is_file():
            continue
        rel = file.relative_to(target).as_posix()
        name_lower = file.name.lower()
        rel_lower = rel.lower()

        if any(pat in rel_lower for pat in FORBIDDEN_PATHS):
            violations.append(f"Forbidden directory path detected: {rel}")
        elif any(name_lower.endswith(ext) for ext in FORBIDDEN_EXTENSIONS):
            violations.append(f"Forbidden artifact extension detected: {rel}")
        elif ".solvable." in name_lower:
            violations.append(f"Solvable artifact detected: {rel}")

    return violations


def prepare_student_manifest(source_pubspec: Path, dest_pubspec: Path) -> None:
    """Produce a sanitized pubspec.yaml stripped of generated offline problem assets."""
    lines = source_pubspec.read_text(encoding="utf-8").splitlines()
    filtered = [
        line
        for line in lines
        if not line.strip().startswith("- generated/")
    ]
    dest_pubspec.write_text("\n".join(filtered) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-dir", type=Path, help="Directory to verify for student safety")
    parser.add_argument("--stage-dir", type=Path, help="Prepare a clean staged directory for building")
    args = parser.parse_args()

    if args.verify_dir:
        violations = verify_student_bundle(args.verify_dir)
        if violations:
            print("ERROR: Student bundle verification failed with private assets:", file=sys.stderr)
            for v in violations:
                print(f"  - {v}", file=sys.stderr)
            sys.exit(1)
        print(f"PASS: Verified student bundle has no authored answers: {args.verify_dir}")

    if args.stage_dir:
        args.stage_dir.mkdir(parents=True, exist_ok=True)
        for folder in ("lib", "web", "assets/i18n", "assets/characters"):
            src = APP_DIR / folder
            if src.exists():
                shutil.copytree(src, args.stage_dir / folder, dirs_exist_ok=True)
        prepare_student_manifest(APP_DIR / "pubspec.yaml", args.stage_dir / "pubspec.yaml")
        for lock in ("pubspec.lock", "analysis_options.yaml"):
            if (APP_DIR / lock).exists():
                shutil.copy2(APP_DIR / lock, args.stage_dir / lock)
        print(f"PASS: Prepared student build workspace in: {args.stage_dir}")


if __name__ == "__main__":
    main()
