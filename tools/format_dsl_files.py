from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from modu_math_web.editor.services.dsl_format import format_dsl_source


def iter_dsl_paths(path: Path, *, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path] if path.name.endswith(".dsl.py") else []
    pattern = "**/*.dsl.py" if recursive else "*.dsl.py"
    return sorted(p for p in path.glob(pattern) if p.is_file())


def format_path(path: Path, *, write: bool) -> bool:
    source = path.read_text(encoding="utf-8")
    formatted = format_dsl_source(source)
    changed = formatted != source
    if changed and write:
        path.write_text(formatted, encoding="utf-8", newline="\n")
    return changed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check or format ModuMath *.dsl.py files.")
    parser.add_argument("path", help="A *.dsl.py file or directory containing DSL files.")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories recursively.")
    parser.add_argument("--write", action="store_true", help="Write formatted files. Without this, only report.")
    parser.add_argument("--quiet", action="store_true", help="Only print the final summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = Path(args.path)
    paths = iter_dsl_paths(target, recursive=args.recursive)
    if not paths:
        print(f"No *.dsl.py files found: {target}")
        return 0

    changed_paths: list[Path] = []
    failed_paths: list[tuple[Path, str]] = []
    for path in paths:
        try:
            changed = format_path(path, write=args.write)
        except Exception as exc:
            failed_paths.append((path, str(exc)))
            continue
        if changed:
            changed_paths.append(path)
            if not args.quiet:
                action = "formatted" if args.write else "would format"
                print(f"{action}: {path}")

    for path, message in failed_paths:
        print(f"failed: {path}: {message}", file=sys.stderr)

    action = "formatted" if args.write else "would format"
    print(f"{action} {len(changed_paths)} / {len(paths)} file(s)")
    if failed_paths:
        print(f"failed {len(failed_paths)} file(s)", file=sys.stderr)
        return 2
    return 1 if changed_paths and not args.write else 0


if __name__ == "__main__":
    raise SystemExit(main())
