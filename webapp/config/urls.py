from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="editor:problem_list", permanent=False)),
    path("admin/", admin.site.urls),
    path("problems/", include("apps.problems.urls")),
    path("editor/", include("apps.editor.urls")),
]
