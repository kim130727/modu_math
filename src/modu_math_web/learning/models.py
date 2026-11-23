from __future__ import annotations

import re
import unicodedata
from typing import Any

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction


def _normalized(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(unicodedata.normalize("NFKC", value).split()).casefold()
    if isinstance(value, dict):
        for key in ("value", "answer", "choice_id", "id"):
            if key in value and len(value) == 1:
                return _normalized(value[key])
        return tuple(
            sorted((str(key), _normalized(item)) for key, item in value.items())
        )
    if isinstance(value, list):
        return tuple(_normalized(item) for item in value)
    if isinstance(value, bool) or value is None:
        return value
    return str(value)


def _submitted_choice_value(value):
    if isinstance(value, dict):
        return value.get("choice_id", value.get("id", value.get("value")))
    return value


def _choice_id(value, choices):
    value = _submitted_choice_value(value)
    if isinstance(value, str) and value in choices:
        return value
    # Older clients submitted a one-based position or the displayed text.
    if type(value) is int and 0 < value <= len(choices):
        return list(choices)[value - 1]
    normalized = _normalized(value)
    matches = [
        choice_id for choice_id, choice in choices.items()
        if any(key in choice and _normalized(choice[key]) == normalized
               for key in ("text", "value", "label"))
    ]
    if matches:
        return matches[0] if len(matches) == 1 else None
    if isinstance(value, str):
        match = re.fullmatch(r"(?:choice\.|slot\.(?:choice|opt|option)\.)?(\d+)", value.strip())
        if match and 0 < (position := int(match.group(1))) <= len(choices):
            return list(choices)[position - 1]
    return None


def _keyed_choice_matches(choices, submitted, expected_ids):
    if len(expected_ids) > 1 and isinstance(submitted, str) and "," in submitted:
        submitted = submitted.split(",")
    values = submitted if isinstance(submitted, list) else [submitted]
    if len(values) != len(expected_ids):
        return False
    return {_choice_id(value, choices) for value in values} == expected_ids


def _answer_choice_id(key, choices):
    if not isinstance(key, dict):
        return None
    identity = key.get("id")
    slot = key.get("slot_id")
    for ref in (identity, slot):
        if isinstance(ref, str) and ref in choices:
            return ref
    if isinstance(slot, str):
        matches = [choice_id for choice_id, choice in choices.items()
                   if choice.get("slot_id") == slot]
        if len(matches) == 1:
            return matches[0]
    return None


def answer_matches(answer: dict[str, Any], submitted: Any) -> bool:
    """Compare a client answer with the existing answer contract without rewriting it."""
    candidates: list[Any] = []
    if "value" in answer:
        candidates.append(answer["value"])
    answer_key = answer.get("answer_key", [])
    if not isinstance(answer_key, list):
        answer_key = []
    review = (answer.get("presentation") or {}).get("review") or {}
    raw_choices = answer.get("choices") or []
    choices_by_id = {
        choice["id"]: choice for choice in raw_choices
        if isinstance(choice, dict) and isinstance(choice.get("id"), str)
    }
    choice_set = answer.get("target", {}).get("type") == "multiple_choice_set"
    # The input schema sends the actual choice ID. Grade that identity before
    # interpreting any legacy answer text or one-based choice number.
    if answer_key and (len(answer_key) == 1 or choice_set or review.get("mode") == "canvas_select"):
        expected_ids = [_answer_choice_id(key, choices_by_id) for key in answer_key]
        if all(expected_ids):
            return _keyed_choice_matches(choices_by_id, submitted, set(expected_ids))
    if review.get("mode") == "canvas_select" and not answer_key:
        return False
    if len(answer_key) > 1 or (
        answer_key and answer.get("target", {}).get("type") == "multiple_choice_set"
    ):
        expected = [
            item.get("value", item.get("id")) if isinstance(item, dict) else item
            for item in answer_key
        ]
        if isinstance(submitted, dict):
            slot_ids = [
                item.get("slot_id", item.get("id")) if isinstance(item, dict) else None
                for item in answer_key
            ]
            if all(slot_ids) and set(submitted) == set(slot_ids):
                submitted = [submitted[key] for key in slot_ids]
        if isinstance(submitted, str) and "," in submitted:
            submitted = submitted.split(",")

        def choice_value(value, expected_value=False):
            choices = answer.get("choices") or []
            for index, choice in enumerate(choices):
                if (isinstance(choice, dict) and value == choice.get("id")) or (
                    not isinstance(value, bool)
                    and (not expected_value or isinstance(value, int))
                    and str(value) == str(index + 1)
                ):
                    return (
                        choice.get("value", choice.get("text", choice.get("label")))
                        if isinstance(choice, dict)
                        else choice
                    )
            return value

        expected = [choice_value(value, expected_value=True) for value in expected]
        if not isinstance(submitted, list):
            return False
        submitted = [choice_value(value) for value in submitted]
        if answer.get("target", {}).get("type") == "multiple_choice_set":
            return len(submitted) == len(set(map(str, submitted))) and sorted(
                map(str, _normalized(submitted))
            ) == sorted(map(str, _normalized(expected)))
        return _normalized(submitted) == _normalized(expected)
    for item in answer_key:
        if isinstance(item, dict):
            candidates.append(item.get("value", item.get("id")))
        else:
            candidates.append(item)

    normalized_submitted = _normalized(submitted)
    if any(normalized_submitted == _normalized(candidate) for candidate in candidates):
        return True
    if isinstance(submitted, list) and isinstance(answer.get("value"), str):
        comma_separated = answer["value"].split(",")
        if len(comma_separated) > 1 and normalized_submitted == _normalized(
            comma_separated
        ):
            return True

    # Mobile clients commonly submit a one-based choice number or choice id.
    submitted_choice = _submitted_choice_value(submitted)
    choice_number: int | None = None
    if isinstance(submitted_choice, str) and submitted_choice in choices_by_id:
        choice_number = next(
            i for i, choice in enumerate(raw_choices, 1)
            if isinstance(choice, dict) and choice.get("id") == submitted_choice
        )
    elif isinstance(submitted_choice, int) and not isinstance(submitted_choice, bool):
        choice_number = submitted_choice
    elif isinstance(submitted_choice, str):
        match = re.fullmatch(
            r"(?:choice\.|slot\.(?:choice|opt|option)\.)?(\d+)",
            submitted_choice.strip(),
        )
        if match:
            choice_number = int(match.group(1))

    expected_value = answer.get("value")
    if choice_number is not None and isinstance(expected_value, int):
        return choice_number == expected_value
    if choice_number is not None:
        choices = answer.get("choices", [])
        if 0 < choice_number <= len(choices):
            choice = choices[choice_number - 1]
            if isinstance(choice, dict):
                return any(
                    _normalized(choice.get(key)) == _normalized(candidate)
                    for key in ("id", "value", "text")
                    if key in choice
                    for candidate in candidates
                )
            return any(
                _normalized(choice) == _normalized(candidate)
                for candidate in candidates
            )
    return False


class Problem(models.Model):
    problem_id = models.CharField(max_length=128)
    language = models.CharField(max_length=16, default="ko")
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    problem_type = models.CharField(max_length=128, blank=True)
    concepts = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    catalog_data = models.JSONField(default=dict, blank=True)
    answer = models.JSONField(default=dict)
    semantic_data = models.JSONField(default=dict)
    solvable_data = models.JSONField(default=dict)
    layout_data = models.JSONField(default=dict)
    renderer_data = models.JSONField(default=dict)
    source_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("problem_id", "language"),
                name="learning_problem_id_language_uniq",
            )
        ]
        indexes = [
            models.Index(
                fields=("language", "grade", "problem_type"), name="problem_catalog_idx"
            ),
            models.Index(fields=("problem_id",), name="problem_external_id_idx"),
        ]
        ordering = ("problem_id", "language")

    def __str__(self) -> str:
        return f"{self.problem_id} ({self.language})"

    def check_answer(self, submitted: Any) -> bool:
        return answer_matches(self.answer, submitted)

    @property
    def effective_concepts(self) -> list[str]:
        if hasattr(self, "tagging") and self.tagging:
            return self.tagging.effective_concepts or self.concepts
        return self.concepts

    @property
    def effective_skills(self) -> list[str]:
        if hasattr(self, "tagging") and self.tagging:
            return self.tagging.effective_skills or self.skills
        return self.skills


class ProblemTagging(models.Model):
    problem = models.OneToOneField(
        Problem, on_delete=models.CASCADE, related_name="tagging"
    )
    auto_concepts = models.JSONField(default=list, blank=True)
    auto_skills = models.JSONField(default=list, blank=True)
    rule_version = models.CharField(max_length=32, default="1.0.0")
    source = models.CharField(max_length=64, default="rule_based")
    confidence = models.FloatField(
        default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    review_status = models.CharField(
        max_length=32,
        default="pending",
        choices=[
            ("pending", "대기"),
            ("reviewed", "검토완료"),
            ("confirmed", "확정"),
        ],
    )
    reviewed_concepts = models.JSONField(null=True, blank=True)
    reviewed_skills = models.JSONField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_tags",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=("review_status",), name="tagging_status_idx"),
            models.Index(fields=("confidence",), name="tagging_confidence_idx"),
        ]

    def __str__(self) -> str:
        return f"Tagging for {self.problem} ({self.review_status}, conf={self.confidence:.2f})"

    @property
    def effective_concepts(self) -> list[str]:
        if self.reviewed_concepts is not None:
            return self.reviewed_concepts
        return self.auto_concepts

    @property
    def effective_skills(self) -> list[str]:
        if self.reviewed_skills is not None:
            return self.reviewed_skills
        return self.auto_skills


class Attempt(models.Model):
    assignment_item = models.ForeignKey(
        "learning.AssignmentItem",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="attempts",
    )
    recipient = models.ForeignKey(
        "learning.AssignmentRecipient",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="attempts",
    )
    submission_key = models.CharField(max_length=64, null=True, blank=True)
    assignment_try = models.PositiveSmallIntegerField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attempts"
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="attempts"
    )
    submitted_answer = models.JSONField()
    is_correct = models.BooleanField(editable=False)
    elapsed_ms = models.PositiveIntegerField(default=0)
    hint_count = models.PositiveSmallIntegerField(default=0)
    retry_count = models.PositiveSmallIntegerField(default=0)
    events = models.JSONField(default=list, blank=True)
    session_id = models.CharField(max_length=128, blank=True, default="")
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("recipient", "submission_key"),
                name="attempt_recipient_key_uniq",
            ),
            models.UniqueConstraint(
                fields=("recipient", "assignment_item", "assignment_try"),
                name="attempt_assignment_try_uniq",
            ),
            models.CheckConstraint(
                check=(
                    models.Q(
                        recipient__isnull=True,
                        assignment_item__isnull=True,
                        assignment_try__isnull=True,
                        submission_key__isnull=True,
                    )
                    | models.Q(
                        recipient__isnull=False,
                        assignment_item__isnull=False,
                        assignment_try__isnull=False,
                        assignment_try__gte=1,
                        submission_key__isnull=False,
                    )
                ),
                name="attempt_assignment_links",
            ),
        ]
        indexes = [
            models.Index(
                fields=("user", "-created_at"), name="attempt_user_recent_idx"
            ),
            models.Index(
                fields=("user", "problem", "-created_at"),
                name="attempt_user_problem_idx",
            ),
        ]
        ordering = ("-created_at",)

    def save(self, *args: Any, **kwargs: Any) -> None:
        is_new = self._state.adding
        if is_new:
            self.is_correct = answer_matches(
                (
                    self.assignment_item.answer
                    if self.assignment_item_id
                    else self.problem.answer
                ),
                self.submitted_answer,
            )
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                all_concepts = (
                    self.assignment_item.concepts
                    if self.assignment_item_id
                    else list(
                        dict.fromkeys(
                            list(self.problem.effective_concepts)
                            + list(self.problem.concepts)
                        )
                    )
                )
                for concept in all_concepts:
                    Mastery.record(
                        self.user,
                        str(concept),
                        self.is_correct,
                        self.created_at,
                        tag_type="concept",
                    )


class Mastery(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="masteries"
    )
    concept = models.CharField(max_length=255)
    tag_type = models.CharField(
        max_length=16,
        default="concept",
        choices=[("concept", "Concept"), ("skill", "Skill")],
    )
    score = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    attempt_count = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    last_practiced_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "concept"), name="mastery_user_concept_uniq"
            )
        ]
        indexes = [
            models.Index(fields=("user", "-updated_at"), name="mastery_user_recent_idx")
        ]
        ordering = ("concept",)

    @classmethod
    @transaction.atomic
    def record(
        cls,
        user: Any,
        concept: str,
        correct: bool,
        practiced_at: Any,
        tag_type: str = "concept",
    ) -> "Mastery":
        mastery, _ = cls.objects.select_for_update().get_or_create(
            user=user, concept=concept, defaults={"tag_type": tag_type}
        )
        mastery.tag_type = tag_type
        mastery.attempt_count += 1
        mastery.correct_count += int(correct)
        mastery.score = mastery.correct_count / mastery.attempt_count
        mastery.last_practiced_at = practiced_at
        mastery.save(
            update_fields=(
                "tag_type",
                "attempt_count",
                "correct_count",
                "score",
                "last_practiced_at",
                "updated_at",
            )
        )
        return mastery


# Register the additive management models with this existing Django app.
from .platform_models import (  # noqa: E402,F401
    Assignment,
    AssignmentItem,
    AssignmentProgress,
    AssignmentRecipient,
    Classroom,
    Enrollment,
    ProblemPublication,
    ProblemSet,
    ProblemSetItem,
    StudentProfile,
)
