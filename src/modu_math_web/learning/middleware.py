from __future__ import annotations

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .platform_permissions import is_manager


class EditorAccessMiddleware:
    """Local authoring stays available; production authoring APIs and assets require teacher role.

    DEBUG=True is a trusted local development mode, never a student deployment.
    In production (DEBUG=False):
    - Editor APIs (/api/editor/), web views (/editor/, /editor-konva/),
      and legacy Flutter editor static assets (/static/editor_next/flutter_editor/)
      require an authenticated manager (teacher or admin).
    - Session cookie (modu_editor_session) is strictly scoped to GET/HEAD requests
      for assets (/api/editor/assets/ and /static/editor_next/flutter_editor/).
      Authoring API JSON queries and mutations must provide a direct Token header.
    - Students and unauthenticated users are strictly forbidden from accessing
      raw problem DSLs, authoring assets, and answer bundles.
    """

    PROTECTED_PREFIXES = (
        "/api/editor/",
        "/editor/",
        "/editor-konva/",
        "/static/editor_next/flutter_editor/",
    )

    COOKIE_ALLOWED_PREFIXES = (
        "/editor/",
        "/editor-konva/",
        "/api/editor/assets/",
        "/static/editor_next/flutter_editor/",
    )

    FORBIDDEN_FILE_PATTERNS = (
        ".dsl.py",
        ".semantic.json",
        ".solvable.json",
        "generated/examples/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def _is_protected_path(self, path: str) -> bool:
        if path.startswith(self.PROTECTED_PREFIXES):
            return True
        path_lower = path.lower()
        if any(pat in path_lower for pat in self.FORBIDDEN_FILE_PATTERNS):
            return True
        return False

    def __call__(self, request):
        if (
            settings.DEBUG
            and request.path.startswith("/api/editor/")
            and request.headers.get("Authorization")
        ):
            try:
                credentials = TokenAuthentication().authenticate(request)
                if credentials:
                    request.user = credentials[0]
                    if not is_manager(request.user):
                        return JsonResponse(
                            {"detail": "Teacher permission required"}, status=403
                        )
            except AuthenticationFailed:
                return JsonResponse({"detail": "Authentication required"}, status=401)
        if not settings.DEBUG and self._is_protected_path(request.path):
            user = None
            if getattr(request, "user", None) and request.user.is_authenticated:
                user = request.user
            else:
                try:
                    credentials = TokenAuthentication().authenticate(request)
                    if credentials:
                        user = credentials[0]
                except AuthenticationFailed:
                    pass

                # Allow signed cookie only for static/asset GET/HEAD requests
                if (
                    user is None
                    and not request.headers.get("Authorization")
                    and request.method in {"GET", "HEAD"}
                    and request.path.startswith(self.COOKIE_ALLOWED_PREFIXES)
                ):
                    key = request.get_signed_cookie(
                        "modu_editor_session",
                        default="",
                        salt="modu.editor.session.v1",
                        max_age=3600,
                    )
                    if key:
                        token = (
                            Token.objects.select_related("user")
                            .filter(key=key, user__is_active=True)
                            .first()
                        )
                        if token:
                            user = token.user

            if user is None:
                if request.path in {"/editor/", "/editor-konva/"}:
                    return HttpResponseRedirect("/teacher/")
                if request.path.startswith("/api/"):
                    return JsonResponse(
                        {"detail": "Authentication required"}, status=401
                    )
                return HttpResponse("Authentication required", status=401)

            request.user = user
            if not is_manager(user):
                if request.path.startswith("/api/"):
                    return JsonResponse(
                        {"detail": "Teacher permission required"}, status=403
                    )
                return HttpResponse("Teacher permission required", status=403)

        return self.process_response(request, self.get_response(request))

    def process_view(self, request, view_func, view_args, view_kwargs):
        problem_id = view_kwargs.get("problem_id")
        if not problem_id or not request.path.startswith("/api/editor/"):
            return None
        user = getattr(request, "user", None)
        if settings.DEBUG and not (user and user.is_authenticated):
            return None
        from modu_math_web.editor.services.problems import resolve_problem_paths
        from .services.authoring_access import may_author

        try:
            paths = resolve_problem_paths(problem_id)
        except (ValueError, FileNotFoundError):
            return JsonResponse({"detail": "문제를 찾을 수 없습니다."}, status=404)
        if not user or not user.is_authenticated or not may_author(user, paths):
            return JsonResponse({"detail": "문제를 찾을 수 없습니다."}, status=404)
        return None

    def process_response(self, request, response):
        # Successful editor builds update the same owned DB record; publishing is explicit.
        if (
            request.method == "POST"
            and request.path.startswith("/api/editor/problems/")
            and response.status_code == 200
            and getattr(request, "user", None)
            and request.user.is_authenticated
        ):
            import json
            from modu_math_web.editor.services.problems import resolve_problem_paths
            from .services.authoring_access import sync_authored_artifacts

            try:
                payload = json.loads(response.content)
            except (ValueError, AttributeError):
                return response
            if (
                payload.get("ok")
                and payload.get("artifacts")
                and payload.get("problem_id")
            ):
                sync_authored_artifacts(
                    resolve_problem_paths(payload["problem_id"]), payload["artifacts"]
                )
        if request.path.startswith(
            ("/api/editor/", "/api/v1/problems/", "/api/v1/student/")
        ):
            response["Cache-Control"] = "private, no-store"
        return response
