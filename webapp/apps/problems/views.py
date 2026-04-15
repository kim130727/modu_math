from __future__ import annotations

from django.shortcuts import redirect


def problem_index(request):
    return redirect("editor:problem_list")

