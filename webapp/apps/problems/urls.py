from __future__ import annotations

from django.urls import path

from . import views


app_name = "problems"

urlpatterns = [
    path("", views.problem_index, name="problem_index"),
]

