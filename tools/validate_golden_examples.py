from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_EXACT = [
    "input.png",
    "vision_draft.md",
    "refined_draft.md",
    "problem.dsl.py",
    "problem.semantic.json",
    "problem.layout.json",
    "problem.renderer.json",
    "problem.svg",
    "build_report.json",
]
SOLVABLE_ALIASES = [
    "problem.solvable.json",
    "problem.solvable.v1.json",
    "problem.solvable.v1.1.json",
    "problem.solvable.v1.2.json",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate golden example bundles")
    parser.add_argument("--root", default="examples/problems", help="problem root directory")
    parser.add_argument("--limit", type=int, default=10, help="number of golden examples to validate")
    parser.add_argument(
        "--problems",
        nargs="*",
        default=None,
        help="explicit relative problem directories under --root",
    )
    parser.add_argument(
        "--manifest-out",
        default=None,
        help="write selected problem directories as JSON manifest",
    )
    return parser.parse_args(argv)


def _is_golden_candidate(problem_dir: Path) -> bool:
    for name in REQUIRED_EXACT:
        if not (problem_dir / name).exists():
            return False
    if not any((problem_dir / alias).exists() for alias in SOLVABLE_ALIASES):
        return False
    return True


def _all_problem_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_dir())


def _select_problem_dirs(root: Path, explicit: list[str] | None, limit: int) -> list[Path]:
    if explicit:
        return [root / rel for rel in explicit]

    selected: list[Path] = []
    for problem_dir in _all_problem_dirs(root):
        if _is_golden_candidate(problem_dir):
            selected.append(problem_dir)
        if len(selected) >= limit:
            break
    return selected


def _missing_items(problem_dir: Path) -> list[str]:
    missing = [name for name in REQUIRED_EXACT if not (problem_dir / name).exists()]
    if not any((problem_dir / alias).exists() for alias in SOLVABLE_ALIASES):
        missing.append("problem.solvable.json|problem.solvable.v1.json|problem.solvable.v1.1.json|problem.solvable.v1.2.json")
    return missing


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    if not root.exists():
        raise FileNotFoundError(f"Root not found: {root}")

    selected = _select_problem_dirs(root, args.problems, max(1, int(args.limit)))
    if not selected:
        print("No golden candidates found.")
        return 1

    failures = 0
    problem_labels: list[str] = []
    for problem_dir in selected:
        rel = problem_dir.relative_to(root).as_posix()
        problem_labels.append(rel)
        missing = _missing_items(problem_dir)
        if missing:
            failures += 1
            print(f"[fail] {rel}: missing {', '.join(missing)}")
        else:
            print(f"[ok] {rel}")

    if args.manifest_out:
        manifest_path = Path(args.manifest_out)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_payload = {"root": str(root), "problems": problem_labels}
        manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Manifest written: {manifest_path}")

    print(f"Validated {len(selected)} candidate(s), failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
