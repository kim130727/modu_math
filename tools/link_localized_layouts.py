"""Link existing translations to shared authored geometry without rewriting prose."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from modu_math.layout.shared_layout import override_path, read_overrides

LOCALES = ("ko", "en", "ja", "zh", "km", "uk")


def link_localized_layouts(root: Path, problem: str | None = None) -> list[Path]:
    """Keep target edits; every subsequent build resolves the latest source DSL."""
    changed = []
    for source in sorted((root / "ko").rglob("*.dsl.py")):
        if problem and source.name != f"{problem}.dsl.py":
            continue
        relative = source.relative_to(root / "ko")
        targets = [root / locale / relative for locale in LOCALES if locale != "ko"
                   and (root / locale / relative).exists()]
        if not targets:
            continue
        for dsl in [source, *targets]:
            overrides = read_overrides(dsl)
            overrides.setdefault("version", 1)
            if dsl == source:
                overrides["text_layout"] = "fit"
            else:
                overrides["layout_source"] = Path(os.path.relpath(source.resolve(), dsl.resolve().parent)).as_posix()
            path = override_path(dsl)
            text = json.dumps(overrides, ensure_ascii=False, indent=2) + "\n"
            if not path.exists() or path.read_text(encoding="utf-8-sig") != text:
                path.write_text(text, encoding="utf-8")
                changed.append(path)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT / "examples" / "problems")
    parser.add_argument("--problem", help="Optional problem ID; otherwise link all matching translations")
    args = parser.parse_args()
    changed = link_localized_layouts(args.root, args.problem)
    print(f"Linked {len(changed)} layout configurations; existing translations and local edits preserved.")


if __name__ == "__main__":
    main()
