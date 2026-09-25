"""Migrate translated Python to verified JSON differences; delete only after verification."""

from __future__ import annotations

import argparse
from pathlib import Path

from modu_math.dsl.variants import (
    delta_path,
    materialized_snapshot,
    read_source,
    save_variant,
    snapshot,
)


def migrate(root: Path, *, delete: bool = False) -> dict:
    root = root.resolve()
    candidates = sorted(
        path
        for language in ("uk",)
        for path in (root / language).rglob("*.dsl.py")
    )
    verified = []
    before_bytes = after_bytes = 0
    for path in candidates:
        if root not in path.resolve().parents:
            raise ValueError(f"Outside migration root: {path}")
        canonical = (
            root / "ko" / path.relative_to(root / path.relative_to(root).parts[0])
        )
        if not canonical.is_file():
            raise ValueError(f"Missing Korean source: {canonical}")
        target = snapshot(path.read_text(encoding="utf-8-sig"), path)
        save_variant(path, canonical, target)
        if (
            materialized_snapshot(path) != target
            or snapshot(read_source(path), path) != target
        ):
            raise ValueError(f"Migration round-trip failed: {path}")
        verified.append(path)
        before_bytes += path.stat().st_size
        after_bytes += delta_path(path).stat().st_size
    # Verify all candidates before deleting any authored file.
    if delete:
        for path in verified:
            path.unlink()
    return {
        "verified": len(verified),
        "deleted": len(verified) if delete else 0,
        "dsl_bytes": before_bytes,
        "delta_bytes": after_bytes,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()
    print(migrate(args.root, delete=args.delete))
