from __future__ import annotations

import json
import mimetypes
from typing import Any

from django.http import FileResponse, HttpResponse
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .services.build import build_with_artifacts
from .services.dsl_patch import DslPatchError, apply_layout_patches, save_tutor_renderer_flow
from .services.problems import (
    create_blank_problem,
    format_problem_dsl,
    list_problem_directories,
    read_problem_detail,
    resolve_problem_paths,
    save_problem_dsl,
)
from .services.tutor_preview import (
    mock_tutor_response,
    openai_tutor_response,
    openai_tutor_speech,
    rule_tutor_response,
    tutor_env_status,
    tutor_speech_locale,
    validate_tutor_payload,
)


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
def problems_list(request: HttpRequest) -> JsonResponse:
    include_artifacts = request.GET.get("artifacts") in {"1", "true", "yes"}
    return JsonResponse({"problems": list_problem_directories(include_artifacts=include_artifacts)})


@require_POST
def create_problem(request: HttpRequest) -> JsonResponse:
    try:
        data = _json_body(request)
        problem_id = data.get("problem_id")
        title = data.get("title")
        if not isinstance(problem_id, str):
            return _error("'problem_id' must be a string", status=400)
        if title is not None and not isinstance(title, str):
            return _error("'title' must be a string", status=400)
        detail = create_blank_problem(problem_id, title=title)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileExistsError as exc:
        return _error(str(exc), status=409)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse({"ok": True, **detail})


@require_GET
def tutor_preview_status(_: HttpRequest) -> JsonResponse:
    return JsonResponse({"ok": True, **tutor_env_status()})


@require_POST
def tutor_preview(request: HttpRequest) -> JsonResponse:
    try:
        data = _json_body(request)
        message = data.get("message")
        mode = data.get("mode", "mock")
        payload = data.get("payload")
        history = data.get("history", [])
        if not isinstance(message, str):
            return _error("'message' must be a string", status=400)
        if mode not in {"rule", "mock", "openai"}:
            return _error("'mode' must be 'rule', 'mock', or 'openai'", status=400)
        if not isinstance(payload, dict):
            return _error("'payload' must be an object", status=400)
        if not isinstance(history, list):
            return _error("'history' must be a list", status=400)
        clean_history = [
            {"role": str(item.get("role", "")), "content": str(item.get("content", ""))}
            for item in history
            if isinstance(item, dict)
        ]
        validations = validate_tutor_payload(payload)
        choices: list[str] = []
        current_step_id: str | None = None
        if mode == "openai":
            reply = openai_tutor_response(payload, message, clean_history)
        elif mode == "rule":
            rule_response = rule_tutor_response(payload, message, clean_history)
            if isinstance(rule_response, dict):
                reply = str(rule_response.get("reply", ""))
                raw_choices = rule_response.get("choices", [])
                choices = [str(choice) for choice in raw_choices] if isinstance(raw_choices, list) else []
                raw_step_id = rule_response.get("current_step_id")
                current_step_id = raw_step_id if isinstance(raw_step_id, str) else None
            else:
                reply = rule_response
        else:
            reply = mock_tutor_response(payload, message)
    except EnvironmentError as exc:
        return _error(str(exc), status=400)
    except ImportError as exc:
        return _error(str(exc), status=500)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse(
        {
            "ok": True,
            "reply": reply,
            "choices": choices,
            "current_step_id": current_step_id,
            "checks": [check.__dict__ for check in validations],
            **tutor_env_status(),
        }
    )


@require_POST
def tutor_preview_speech(request: HttpRequest) -> HttpResponse | JsonResponse:
    try:
        data = _json_body(request)
        text = data.get("text")
        locale = data.get("locale", "ko-KR")
        payload = data.get("payload")
        if not isinstance(text, str):
            return _error("'text' must be a string", status=400)
        if not isinstance(locale, str):
            return _error("'locale' must be a string", status=400)
        if payload is not None and not isinstance(payload, dict):
            return _error("'payload' must be an object", status=400)
        locale = tutor_speech_locale(payload, fallback=locale)
        audio, content_type = openai_tutor_speech(text, locale)
    except EnvironmentError as exc:
        return _error(str(exc), status=400)
    except ImportError as exc:
        return _error(str(exc), status=500)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except Exception as exc:
        return _error(str(exc), status=500)
    response = HttpResponse(audio, content_type=content_type)
    response["Cache-Control"] = "no-store"
    return response


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


@require_GET
def problem_asset(_: HttpRequest, problem_id: str, filename: str) -> FileResponse | JsonResponse:
    try:
        if not filename or "/" in filename or "\\" in filename or filename in {".", ".."}:
            return _error("invalid asset filename", status=400)
        paths = resolve_problem_paths(problem_id)
        asset_path = (paths.base_dir / filename).resolve()
        if asset_path.parent != paths.base_dir.resolve():
            return _error("invalid asset path", status=400)
        if not asset_path.exists() or not asset_path.is_file():
            return _error("asset not found", status=404)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)

    content_type = mimetypes.guess_type(asset_path.name)[0] or "application/octet-stream"
    return FileResponse(asset_path.open("rb"), content_type=content_type)


@require_POST
def save_dsl(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        data = _json_body(request)
        dsl = data.get("dsl")
        if not isinstance(dsl, str):
            return _error("'dsl' must be a string", status=400)
        if not dsl.strip():
            return _error("'dsl' must not be empty", status=400)
        save_problem_dsl(problem_id, dsl)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse({"ok": True, "problem_id": problem_id})


@require_POST
def format_dsl(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        _, dsl = format_problem_dsl(problem_id)
    except ValueError as exc:
        return _error(str(exc), status=400)
    except FileNotFoundError as exc:
        return _error(str(exc), status=404)
    except Exception as exc:
        return _error(str(exc), status=500)
    return JsonResponse({"ok": True, "problem_id": problem_id, "dsl": dsl})


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
        format_source = data.get("format", False)
        if not isinstance(format_source, bool):
            return _error("'format' must be a boolean", status=400)
        dsl_text, applied = apply_layout_patches(problem_id, patches, format_source=format_source)
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
def tutor_flow(request: HttpRequest, problem_id: str) -> JsonResponse:
    try:
        data = _json_body(request)
        flow = data.get("tutor_flow")
        format_source = data.get("format", False)
        if not isinstance(format_source, bool):
            return _error("'format' must be a boolean", status=400)
        dsl_text, normalized = save_tutor_renderer_flow(problem_id, flow, format_source=format_source)
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
            "tutor_flow": normalized,
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
