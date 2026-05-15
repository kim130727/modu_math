from __future__ import annotations

from django.urls import include, path

from modu_math_web.editor import views as editor_views

urlpatterns = [
    path("editor/", editor_views.editor_index),
    path("api/editor/", include("modu_math_web.editor.urls")),
]
