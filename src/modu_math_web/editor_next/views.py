from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

from django.conf import settings

from django.http import HttpRequest, FileResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

_ASSET_ROOT = (
    Path(__file__).resolve().parent / "static" / "editor_next" / "konva_assets"
)
_FLUTTER_ASSET_ROOT = (
    Path(__file__).resolve().parent / "static" / "editor_next" / "flutter_editor"
)
_STUDENT_ASSET_ROOT = _FLUTTER_ASSET_ROOT.with_name("student_app")


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
        fingerprints.append(
            _fingerprint_asset(str(asset), stat.st_mtime_ns, stat.st_size)
        )
    return hashlib.sha256(":".join(fingerprints).encode()).hexdigest()[:12]


def flutter_editor_asset_version() -> str:
    bundle = _FLUTTER_ASSET_ROOT / "main.dart.js"
    if not bundle.exists():
        return "missing"
    stat = bundle.stat()
    return _fingerprint_asset(str(bundle), stat.st_mtime_ns, stat.st_size)


@require_GET
def student_workspace(request: HttpRequest):
    index = _STUDENT_ASSET_ROOT / "index.html"
    if not index.is_file():
        return HttpResponse("학생 학습 화면을 준비하고 있습니다.", status=503)
    response = FileResponse(index.open("rb"), content_type="text/html; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    return response


@require_GET
def teacher_workspace(request: HttpRequest):
    fingerprints = []
    for name in ("teacher.js", "teacher.css"):
        asset = _ASSET_ROOT / name
        stat = asset.stat()
        fingerprints.append(
            _fingerprint_asset(str(asset), stat.st_mtime_ns, stat.st_size)
        )
    return render(
        request,
        "editor_next/teacher.html",
        {
            "teacher_asset_version": hashlib.sha256(
                ":".join(fingerprints).encode()
            ).hexdigest()[:12],
        },
    )


@require_GET
def editor_konva(request: HttpRequest):
    return render(
        request,
        "editor_next/konva.html",
        {
            "editor_asset_version": editor_asset_version(),
            "flutter_editor_asset_version": flutter_editor_asset_version(),
            "local_editor": settings.DEBUG,
        },
    )
