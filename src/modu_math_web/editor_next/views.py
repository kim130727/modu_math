from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

_ASSET_ROOT = Path(__file__).resolve().parent / "static" / "editor_next" / "konva_assets"


@lru_cache(maxsize=8)
def _fingerprint_asset(path: str, modified_ns: int, size: int) -> str:
    del modified_ns, size
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]


def editor_asset_version() -> str:
    """Return a stable content version for the compiled editor bundle."""
    bundle = _ASSET_ROOT / "editor-konva.js"
    stat = bundle.stat()
    return _fingerprint_asset(str(bundle), stat.st_mtime_ns, stat.st_size)


@require_GET
def editor_konva(request: HttpRequest):
    return render(
        request,
        "editor_next/konva.html",
        {"editor_asset_version": editor_asset_version()},
    )
