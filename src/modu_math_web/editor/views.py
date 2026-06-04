from __future__ import annotations

import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .services.build import build_with_artifacts
from .services.dsl_patch import DslPatchError, apply_layout_patches
from .services.problems import list_problem_directories, read_problem_detail, save_problem_dsl


def _json_body(request: HttpRequest) -> dict[str, Any]:
    try:
        raw = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(raw)
    except Exception as exc:
        raise ValueError(f"invalid JSON body: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object")
    return data


def _error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"ok": False, "error": message}, status=status)


@require_GET
def editor_index(request: HttpRequest):
    return render(request, "editor/index.html")


@require_GET
def problems_list(_: HttpRequest) -> JsonResponse:
    return JsonResponse({"problems": list_problem_directories()})


@require_GET
def problem_detail(_: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        detail = read_problem_detail(problem_id)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse(detail)


@require_POST
def save_dsl(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        data = _json_body(request)
        dsl = data.get("dsl")
        if not isinstance(dsl, str):
            return _error("'dsl' must be a string", status=400)
        save_problem_dsl(problem_id, dsl)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse({"ok": True, "problem_id": problem_id})


@require_POST
def build_problem(_: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        result, artifacts = build_with_artifacts(problem_id)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)

    payload: dict[str, Any] = {
        "ok": result.ok,
        "problem_id": problem_id,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "artifacts": artifacts,
    }
    if not result.ok:
        payload["error"] = result.error or "build failed"
        return JsonResponse(payload, status=500)
    return JsonResponse(payload)


@require_POST
def layout_patch(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        data = _json_body(request)
        patches = data.get("patches")
        if not isinstance(patches, list):
            return _error("'patches' must be a list", status=400)
        dsl_text, applied = apply_layout_patches(problem_id, patches)
    except DslPatchError as exc:
        return _error(str(exc), status=400)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)

    return JsonResponse(
        {
            "ok": True,
            "problem_id": problem_id,
            "applied": [a.__dict__ for a in applied],
            "dsl": dsl_text,
        }
    )


@require_POST
def layout_patch_and_build(request: HttpRequest, problem_id: str) -> JsonResponse:
    patch_response = layout_patch(request, problem_id)
    if patch_response.status_code != 200:
        return patch_response

    try:
        result, artifacts = build_with_artifacts(problem_id)
    except Exception as exc:
        return _error(str(exc), status=500)

    payload: dict[str, Any] = json.loads(patch_response.content.decode("utf-8"))
    payload.update(
        {
            "build": {
                "ok": result.ok,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
            "artifacts": artifacts,
        }
    )
    if not result.ok:
        payload["ok"] = False
        payload["build"]["error"] = result.error or "build failed"
        return JsonResponse(payload, status=500)
    return JsonResponse(payload)
