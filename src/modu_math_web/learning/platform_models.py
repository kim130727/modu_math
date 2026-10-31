"""Management records live separately from authored DSL/problem contracts."""

import secrets

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def invite_code():
    return secrets.token_urlsafe(18)


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="registered_students",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Classroom(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="classrooms"
    )
    name = models.CharField(max_length=120)
    invite_code = models.CharField(
        max_length=64, unique=True, default=invite_code, editable=False
    )
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.PROTECT, related_name="enrollments"
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.PROTECT, related_name="enrollments"
    )
    status = models.CharField(
        max_length=16,
        choices=[
            ("pending", "승인 대기"),
            ("approved", "승인"),
            ("inactive", "비활성"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("classroom", "student"), name="enrollment_class_student_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("student", "status"), name="enrollment_student_status_idx"
            )
        ]


class ProblemPublication(models.Model):
    problem = models.OneToOneField(
        "learning.Problem", on_delete=models.CASCADE, related_name="publication"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="authored_problems",
    )
    source_path = models.CharField(max_length=512, null=True, blank=True, unique=True)
    visibility = models.CharField(
        max_length=16,
        default="private",
        choices=[
            ("private", "나만 보기"),
            ("class", "선택한 클래스"),
            ("public", "모두에게 공개"),
        ],
    )
    classrooms = models.ManyToManyField(
        Classroom, blank=True, related_name="shared_problems"
    )
    allow_classroom_use = models.BooleanField(default=False)
    source_credit = models.CharField(max_length=500, blank=True)
    rights_note = models.CharField(max_length=1000, blank=True)
    rights_confirmed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=16,
        choices=[
            ("draft", "초안"),
            ("review", "검수 중"),
            ("published", "사용 가능"),
            ("archived", "보관"),
        ],
        default="draft",
    )
    difficulty = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)


class ProblemSet(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="problem_sets"
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProblemSetItem(models.Model):
    problem_set = models.ForeignKey(
        ProblemSet, on_delete=models.CASCADE, related_name="items"
    )
    problem = models.ForeignKey("learning.Problem", on_delete=models.PROTECT)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ("position",)
        constraints = [
            models.UniqueConstraint(
                fields=("problem_set", "position"), name="set_item_position_uniq"
            )
        ]


class Assignment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assignments"
    )
    problem_set = models.ForeignKey(
        ProblemSet, on_delete=models.PROTECT, related_name="assignments"
    )
    source_version = models.PositiveIntegerField()
    title = models.CharField(max_length=160)
    starts_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    max_attempts = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    release_policy = models.CharField(
        max_length=24,
        default="after_submission",
        choices=[
            ("immediate", "풀이 후"),
            ("after_submission", "과제 제출 후"),
            ("after_due", "마감 후"),
            ("never", "비공개"),
        ],
    )
    status = models.CharField(
        max_length=16,
        default="active",
        choices=[("active", "진행"), ("closed", "종료"), ("cancelled", "취소")],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(max_attempts__gte=1, max_attempts__lte=20),
                name="assignment_attempt_range",
            ),
            models.CheckConstraint(
                check=models.Q(starts_at__isnull=True)
                | models.Q(due_at__isnull=True)
                | models.Q(due_at__gt=models.F("starts_at")),
                name="assignment_date_order",
            ),
        ]
        indexes = [
            models.Index(
                fields=("owner", "status", "due_at"), name="assignment_owner_status_idx"
            )
        ]


class AssignmentItem(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.PROTECT, related_name="items"
    )
    problem = models.ForeignKey("learning.Problem", on_delete=models.PROTECT)
    position = models.PositiveIntegerField()
    # Immutable after creation; never exposed through a writable serializer.
    public_content = models.JSONField(default=dict)
    answer = models.JSONField(default=dict)
    solution = models.JSONField(default=dict)
    hints = models.JSONField(default=list)
    concepts = models.JSONField(default=list)

    class Meta:
        ordering = ("position",)
        constraints = [
            models.UniqueConstraint(
                fields=("assignment", "position"), name="assignment_item_position_uniq"
            )
        ]


class AssignmentRecipient(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.PROTECT, related_name="recipients"
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.PROTECT, related_name="assignment_recipients"
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("assignment", "student"), name="assignment_recipient_uniq"
            )
        ]
        indexes = [
            models.Index(
                fields=("student", "submitted_at"), name="recipient_student_submit_idx"
            )
        ]


class AssignmentProgress(models.Model):
    hint_count = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(10)]
    )
    recipient = models.ForeignKey(
        AssignmentRecipient, on_delete=models.PROTECT, related_name="progress"
    )
    item = models.ForeignKey(AssignmentItem, on_delete=models.PROTECT)
    answer = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(hint_count__lte=10), name="assignment_hint_count_range"
            ),
            models.UniqueConstraint(
                fields=("recipient", "item"), name="assignment_progress_item_uniq"
            ),
        ]
