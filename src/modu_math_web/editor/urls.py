from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("problems/", views.problems_list),
    path("problems/<path:problem_id>/dsl/", views.save_dsl),
    path("problems/<path:problem_id>/build/", views.build_problem),
    path("problems/<path:problem_id>/layout-patch/", views.layout_patch),
    path("problems/<path:problem_id>/layout-patch-and-build/", views.layout_patch_and_build),
    path("problems/<path:problem_id>/", views.problem_detail),
]
