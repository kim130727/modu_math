from __future__ import annotations

from django.urls import path

from . import views


app_name = "editor"

urlpatterns = [
    path("", views.problem_list, name="problem_list"),
    path("<str:problem_id>/", views.problem_edit, name="problem_edit"),
    path("<str:problem_id>/save/", views.save_problem, name="save_problem"),
    path("<str:problem_id>/export/", views.export_problem, name="export_problem"),
]

