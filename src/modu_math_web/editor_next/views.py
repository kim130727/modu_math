from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

_ASSET_ROOT = Path(__file__).resolve().parent / "static" / "editor_next" / "konva_assets"
_FLUTTER_ASSET_ROOT = Path(__file__).resolve().parent / "static" / "editor_next" / "flutter_editor"


@lru_cache(maxsize=8)
def _fingerprint_asset(path: str, modified_ns: int, size: int) -> str:
    del modified_ns, size
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


def editor_asset_version() -> str:
    """Return a stable content version for the compiled editor assets."""
    fingerprints: list[str] = []
    for asset_name in ("editor-konva.js", "editor-konva.css"):
        asset = _ASSET_ROOT / asset_name
        stat = asset.stat()
        fingerprints.append(_fingerprint_asset(str(asset), stat.st_mtime_ns, stat.st_size))
    return hashlib.sha256(":".join(fingerprints).encode()).hexdigest()[:12]


def flutter_editor_asset_version() -> str:
    bundle = _FLUTTER_ASSET_ROOT / "main.dart.js"
    if not bundle.exists():
        return "missing"
    stat = bundle.stat()
    return _fingerprint_asset(str(bundle), stat.st_mtime_ns, stat.st_size)


@require_GET
def editor_konva(request: HttpRequest):
    return render(
        request,
        "editor_next/konva.html",
        {
            "editor_asset_version": editor_asset_version(),
            "flutter_editor_asset_version": flutter_editor_asset_version(),
        },
    )
