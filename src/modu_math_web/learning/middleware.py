from django.conf import settings
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .platform_permissions import is_manager


class EditorAccessMiddleware:
    """Local authoring stays available; production source APIs require a role.

    DEBUG=True is a trusted local development mode, never a student deployment.
    Static offline/editor artifacts still need separate deployment isolation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG and request.path.startswith("/api/editor/"):
            try:
                credentials = TokenAuthentication().authenticate(request)
            except AuthenticationFailed:
                credentials = None
            if credentials is None:
                return JsonResponse({"detail": "Authentication required"}, status=401)
            request.user = credentials[0]
            if not is_manager(request.user):
                return JsonResponse(
                    {"detail": "Teacher permission required"}, status=403
                )
        return self.get_response(request)
