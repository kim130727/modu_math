from __future__ import annotations

from django.conf import settings
from django.shortcuts import redirect
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from modu_math_web.editor import views as editor_views

urlpatterns = [
    path("", lambda request: redirect("/editor/")),
    path("editor/", editor_views.editor_index),
    path("api/editor/", include("modu_math_web.editor.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
