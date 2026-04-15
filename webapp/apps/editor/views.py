from __future__ import annotations

import io
import json
import time
import zipfile
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .services import io as io_service
from .services.export_py import export_bundle
from .services.validate import canonicalize_and_validate


@require_GET
def problem_list(request: HttpRequest) -> HttpResponse:
    problems = io_service.list_problems()
    return render(request, "editor/problem_list.html", {"problems": problems})


@require_GET
@ensure_csrf_cookie
def problem_edit(request: HttpRequest, problem_id: str) -> HttpResponse:
    semantic = io_service.load_semantic(problem_id)
    canonical = canonicalize_and_validate(semantic)
    io_service.save_semantic(problem_id, canonical)

    context = {
        "problem_id": io_service.normalize_problem_id(problem_id),
        "semantic_text": json.dumps(canonical, ensure_ascii=False, indent=2),
        "semantic_payload": canonical,
        "asset_version": str(int(time.time())),
    }
    return render(request, "editor/problem_edit.html", context)


@require_http_methods(["POST"])
@csrf_exempt
def save_problem(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8"))
        raw_semantic: dict[str, Any] = payload["semantic"]
        dry_run = bool(payload.get("dry_run"))
    except Exception:
        return JsonResponse({"ok": False, "errors": ["요청 본문 JSON 형식이 올바르지 않습니다."]}, status=400)

    try:
        canonical = canonicalize_and_validate(raw_semantic)
        if not canonical.get("problem_id"):
            canonical["problem_id"] = io_service.normalize_problem_id(problem_id).replace("/", "_")
        if not dry_run:
            io_service.save_semantic(problem_id, canonical)
    except Exception as exc:
        return JsonResponse({"ok": False, "errors": [str(exc)]}, status=400)

    return JsonResponse(
        {
            "ok": True,
            "dry_run": dry_run,
            "semantic": canonical,
            "semantic_text": json.dumps(canonical, ensure_ascii=False, indent=2),
        }
    )


@require_GET
def export_problem(request: HttpRequest, problem_id: str) -> HttpResponse:
    semantic = io_service.load_semantic(problem_id)
    outputs = export_bundle(problem_id=io_service.normalize_problem_id(problem_id), semantic=semantic)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, file_bytes in outputs.items():
            zf.writestr(filename, file_bytes)

    file_name = f"{io_service.normalize_problem_id(problem_id)}_export.zip"
    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response
