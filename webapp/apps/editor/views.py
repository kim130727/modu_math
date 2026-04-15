from __future__ import annotations

import io
import json
import zipfile
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from .services import io as io_service
from .services.export_py import export_bundle
from .services.render_svg import render_preview_svg
from .services.validate import canonicalize_and_validate


@require_GET
def problem_list(request: HttpRequest) -> HttpResponse:
    problems = io_service.list_problems()
    return render(request, "editor/problem_list.html", {"problems": problems})


@require_GET
def problem_edit(request: HttpRequest, problem_id: str) -> HttpResponse:
    semantic = io_service.load_semantic(problem_id)
    canonical = canonicalize_and_validate(semantic)
    svg_preview = render_preview_svg(canonical)
    io_service.save_semantic(problem_id, canonical)

    context = {
        "problem_id": io_service.normalize_problem_id(problem_id),
        "semantic_json": json.dumps(canonical, ensure_ascii=False, indent=2),
        "svg_preview": svg_preview,
    }
    return render(request, "editor/problem_edit.html", context)


@require_http_methods(["POST"])
def save_problem(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8"))
        raw_semantic: dict[str, Any] = payload["semantic"]
    except Exception:
        return JsonResponse({"ok": False, "errors": ["요청 본문 JSON 형식이 올바르지 않습니다."]}, status=400)

    try:
        canonical = canonicalize_and_validate(raw_semantic)
        canonical["problem_id"] = io_service.normalize_problem_id(problem_id)
        svg_preview = render_preview_svg(canonical)
        io_service.save_semantic(problem_id, canonical)
    except Exception as exc:
        return JsonResponse({"ok": False, "errors": [str(exc)]}, status=400)

    return JsonResponse(
        {
            "ok": True,
            "semantic": canonical,
            "semantic_text": json.dumps(canonical, ensure_ascii=False, indent=2),
            "svg_preview": svg_preview,
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
