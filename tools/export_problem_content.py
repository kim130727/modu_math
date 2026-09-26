"""Build disposable offline/mobile content without writing into authored problems."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil

from modu_math.dsl.problem_store import atomic_write
from modu_math_web.editor.services.content_store import list_content, read_content


def export(root: Path, output: Path, *, emit_svg: bool = False) -> int:
    root, output = root.resolve(), output.resolve()
    if output == root or root in output.parents or output in root.parents:
        raise ValueError("Export must be outside the authored problem tree (including junctions)")
    output.mkdir(parents=True, exist_ok=True)
    manifest = root / "manifest.json"
    if manifest.exists():
        atomic_write(output / "manifest.json", manifest.read_bytes())
    count = 0
    for paths in list_content(root):
        content = read_content(paths)
        directory = output / paths.base_dir.relative_to(root)
        directory.mkdir(parents=True, exist_ok=True)
        if not emit_svg:
            (directory / f"{paths.artifact_base}.svg").unlink(missing_ok=True)
        exported_keys = {"semantic", "layout", "renderer", "solvable"}
        if emit_svg:
            exported_keys.add("svg")
        for key, value in content.items():
            if value in (None, "") or key not in exported_keys:
                continue
            suffix = ".svg" if key == "svg" else f".{key}.json"
            text = value if key == "svg" else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            atomic_write(directory / (paths.artifact_base + suffix), text.encode("utf-8"))
        count += 1
    # Renderer image hrefs may still refer to authored image assets.
    for path in root.rglob("*"):
        if ".modu-cache" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".ttf"}:
            destination = output / path.relative_to(root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
    return count


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
    import django
    django.setup()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("examples/problems"))
    parser.add_argument("--out", type=Path, default=Path("apps/mobile/generated/examples/problems"))
    parser.add_argument(
        "--emit-svg",
        action="store_true",
        help="Also export optional derived SVG previews.",
    )
    args = parser.parse_args()
    print(
        f"Exported {export(args.root, args.out, emit_svg=args.emit_svg)} "
        f"language bundles to {args.out}"
    )
