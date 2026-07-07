from __future__ import annotations

from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def editor_next_index(request: HttpRequest):
    return render(request, "editor_next/index.html")


@require_GET
def editor_next_tldraw(request: HttpRequest):
    return render(request, "editor_next/tldraw.html")
