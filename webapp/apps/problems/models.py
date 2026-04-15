from __future__ import annotations

from django.db import models


class ProblemRecord(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_REVIEW = "in_review", "In Review"
        DONE = "done", "Done"

    problem_id = models.CharField(max_length=120, unique=True)
    title = models.CharField(max_length=255, blank=True, default="")
    semantic_path = models.CharField(max_length=500, blank=True, default="")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.problem_id

