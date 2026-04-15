from __future__ import annotations

from django.contrib import admin

from .models import ProblemRecord


@admin.register(ProblemRecord)
class ProblemRecordAdmin(admin.ModelAdmin):
    list_display = ("problem_id", "title", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("problem_id", "title")

