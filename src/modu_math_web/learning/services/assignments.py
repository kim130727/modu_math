"""Snapshot, visibility and transaction rules shared by teacher/student APIs."""

from copy import deepcopy
from types import SimpleNamespace

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from ..models import (
    Assignment,
    AssignmentItem,
    AssignmentProgress,
    AssignmentRecipient,
    Attempt,
    StudentProfile,
)
from .assignment_content import freeze_images, input_schema


def student_problem(problem):
    """Do not return domain quantities, solvable, tutor flow or arbitrary metadata."""
    semantic = problem.semantic_data
    metadata = semantic.get("metadata", {})
    prompt = (
        metadata.get("presentation_prompt")
        or metadata.get("question")
        or metadata.get("instruction")
        or ""
    )
    renderer = deepcopy(problem.renderer_data)
    public_renderer = {
        key: renderer[key]
        for key in ("view_box", "contract_version", "problem_id")
        if key in renderer
    }
    elements = []
    forbidden = {"answer", "solution", "explanation", "feedback", "correct_answer"}
    # Authored renderer attributes are visual-only; interaction/input defaults
    # and arbitrary extension data must not carry server answer contracts.
    attr_keys = set(
        "x y width height max_width x1 x2 y1 y2 cx cy r rx ry d points fill stroke stroke-width stroke-dasharray opacity transform font-size font-family font-weight text-anchor href data-slot-kind data-box-x data-box-y data-box-width data-box-height data-text-align data-vertical-align data-line-height data-semantic-role".split()
    )
    for raw in renderer.get("elements", []):
        attrs = raw.get("attributes", {})
        if attrs.get("data-semantic-role") in forbidden:
            continue
        element = {k: raw[k] for k in ("id", "type", "text", "source_ref") if k in raw}
        if isinstance(raw.get("refs"), dict) and "layout_slot_id" in raw["refs"]:
            element["refs"] = {"layout_slot_id": raw["refs"]["layout_slot_id"]}
        element["attributes"] = {k: v for k, v in attrs.items() if k in attr_keys}
        if isinstance(raw.get("interaction"), dict):
            element["interaction"] = {
                k: v
                for k, v in raw["interaction"].items()
                if k
                in {
                    "type",
                    "role",
                    "value_type",
                    "max_length",
                    "include_in_submission",
                    "order",
                    "group_id",
                    "auto_advance",
                    "keyboard",
                }
            }
        if isinstance(raw.get("input_style"), dict):
            element["input_style"] = {
                k: v
                for k, v in raw["input_style"].items()
                if k
                in {
                    "font_size_mode",
                    "font_size_adjust",
                    "min_font_size",
                    "max_font_size",
                    "font_weight",
                    "horizontal_align",
                    "vertical_align",
                    "padding",
                    "text_color",
                    "width",
                    "height",
                }
            }
        # Only render images; never allow an asset URL to request source JSON/DSL.
        href = element["attributes"].get("href", "")
        if href and not (
            href.startswith("data:image/")
            or href.lower()
            .split("?")[0]
            .endswith((".png", ".jpg", ".jpeg", ".webp", ".svg"))
        ):
            element["attributes"].pop("href", None)
        elements.append(element)
    public_renderer["elements"] = elements
    choices = []
    source_choices = metadata.get("choices", semantic.get("choices", []))
    if isinstance(source_choices, list):
        for choice in source_choices:
            if isinstance(choice, dict):
                choices.append(
                    {k: choice[k] for k in ("id", "text", "label") if k in choice}
                )
            elif isinstance(choice, str):
                choices.append(choice)
    return {
        "id": problem.pk,
        "problem_id": problem.problem_id,
        "language": problem.language,
        "grade": problem.grade,
        "problem_type": problem.problem_type,
        "prompt": prompt,
        "choices": choices,
        "renderer_data": public_renderer,
        "semantic_data": {
            "problem_id": problem.problem_id,
            "metadata": {"question": prompt, "choices": choices},
        },
        "layout_data": {},
        "input_schema": input_schema(problem),
    }


def snapshot_item(assignment, problem, position):
    return AssignmentItem.objects.create(
        assignment=assignment,
        problem=problem,
        position=position,
        public_content=freeze_images(student_problem(problem), problem),
        answer=deepcopy(problem.answer),
        solution={
            "steps": deepcopy(problem.solvable_data.get("steps", [])),
            "checks": deepcopy(problem.solvable_data.get("checks", [])),
        },
        concepts=list(
            dict.fromkeys(list(problem.effective_concepts) + list(problem.concepts))
        ),
        hints=[
            {"title": str(h.get("title") or ""), "text": str(h["text"])}
            for h in problem.solvable_data.get("student_hints", [])
            if isinstance(h, dict) and isinstance(h.get("text"), str)
        ][:10],
    )


def released(recipient):
    assignment = recipient.assignment
    return (
        assignment.release_policy == "immediate"
        or (
            assignment.release_policy == "after_submission"
            and recipient.submitted_at is not None
        )
        or (
            assignment.release_policy == "after_due"
            and assignment.due_at is not None
            and timezone.now() >= assignment.due_at
        )
    )


def visible_attempts(queryset):
    """Enforce release rules on legacy history and diagnostic APIs too."""
    return queryset.filter(
        Q(recipient__isnull=True)
        | Q(recipient__assignment__release_policy="immediate")
        | Q(
            recipient__assignment__release_policy="after_submission",
            recipient__submitted_at__isnull=False,
        )
        | Q(
            recipient__assignment__release_policy="after_due",
            recipient__assignment__due_at__lte=timezone.now(),
        )
    )


def latest_attempts(recipient):
    latest = {}
    for attempt in recipient.attempts.order_by("created_at", "id"):
        latest[attempt.assignment_item_id] = attempt
    return latest


def recipient_result(recipient, *, teacher=False, detail=False):
    assignment = recipient.assignment
    latest = latest_attempts(recipient)
    total = assignment.items.count()
    visible = teacher or released(recipient)
    now = timezone.now()
    result = {
        "id": assignment.pk,
        "recipient_id": recipient.pk,
        "title": assignment.title,
        "status": assignment.status,
        "starts_at": assignment.starts_at,
        "due_at": assignment.due_at,
        "max_attempts": assignment.max_attempts,
        "release_policy": assignment.release_policy,
        "submitted_at": recipient.submitted_at,
        "total": total,
        "completed": len(latest),
        "progress": len(latest) / total if total else 0,
        "results_released": visible,
        "server_time": now,
        "can_work": recipient.submitted_at is None
        and assignment.status == "active"
        and (assignment.starts_at is None or now >= assignment.starts_at)
        and (assignment.due_at is None or now < assignment.due_at),
    }
    if teacher:
        result.update(
            student_id=recipient.student_id,
            username=recipient.student.user.get_username(),
        )
    if visible:
        hints_by_item = {}
        for attempt in recipient.attempts.all():
            hints_by_item[attempt.assignment_item_id] = max(
                hints_by_item.get(attempt.assignment_item_id, 0), attempt.hint_count
            )
        for progress in recipient.progress.all():
            hints_by_item[progress.item_id] = max(
                hints_by_item.get(progress.item_id, 0), progress.hint_count
            )
        correct = sum(a.is_correct for a in latest.values())
        result.update(
            correct=correct,
            accuracy=correct / total if total else 0,
            elapsed_ms=sum(a.elapsed_ms for a in recipient.attempts.all()),
            hint_count=sum(hints_by_item.values()),
            wrong_item_ids=[key for key, a in latest.items() if not a.is_correct],
        )
    if detail:
        progress = {p.item_id: p for p in recipient.progress.all()}
        result["items"] = []
        for item in assignment.items.all():
            data = {
                "id": item.pk,
                "position": item.position,
                "content": {
                    **item.public_content,
                    "input_schema": item.public_content.get("input_schema")
                    or input_schema(
                        SimpleNamespace(
                            answer=item.answer,
                            semantic_data={
                                "metadata": {
                                    "choices": item.public_content.get("choices", [])
                                }
                            },
                        )
                    ),
                },
                "draft_answer": (
                    progress[item.pk].answer if item.pk in progress else None
                ),
                "draft_updated_at": (
                    progress[item.pk].updated_at if item.pk in progress else None
                ),
                "hint_total": len(item.hints),
                "revealed_hints": (
                    item.hints[: progress[item.pk].hint_count]
                    if item.pk in progress
                    else []
                ),
                "attempt_count": recipient.attempts.filter(
                    assignment_item=item
                ).count(),
            }
            attempt = latest.get(item.pk)
            if attempt:
                data["submitted_answer"] = attempt.submitted_answer
                data["last_submitted_at"] = attempt.submitted_at
            # Immediate release still requires answering this particular item.
            if visible and (teacher or attempt):
                data.update(answer=item.answer, solution=item.solution)
                if attempt:
                    data["is_correct"] = attempt.is_correct
            result["items"].append(data)
    return result


def require_open(recipient):
    assignment = recipient.assignment
    now = timezone.now()
    if recipient.submitted_at:
        raise ValidationError("이미 제출한 과제입니다.")
    if assignment.status != "active":
        raise ValidationError("진행 중인 과제가 아닙니다.")
    if assignment.starts_at and now < assignment.starts_at:
        raise ValidationError("과제 시작 전입니다.")
    if assignment.due_at and now >= assignment.due_at:
        raise ValidationError("과제 마감 시간이 지났습니다.")


@transaction.atomic
def record_answer(recipient_id, user, data):
    recipient = AssignmentRecipient.objects.select_for_update().get(
        pk=recipient_id, student__user=user
    )
    assignment = recipient.assignment
    item = assignment.items.filter(pk=data["item_id"]).first()
    if item is None:
        raise ValidationError({"item_id": "이 과제의 문항이 아닙니다."})
    existing = recipient.attempts.filter(submission_key=data["submission_key"]).first()
    if existing:
        if (
            existing.assignment_item_id != item.pk
            or existing.submitted_answer != data["answer"]
        ):
            raise ValidationError({"submission_key": "다른 요청에 사용한 키입니다."})
        return recipient, existing, False
    require_open(recipient)
    count = recipient.attempts.filter(assignment_item=item).count()
    if count >= assignment.max_attempts:
        raise ValidationError("허용된 시도 횟수를 초과했습니다.")
    progress = AssignmentProgress.objects.filter(recipient=recipient, item=item).first()
    attempt = Attempt.objects.create(
        user=user,
        problem=item.problem,
        assignment_item=item,
        recipient=recipient,
        submitted_answer=data["answer"],
        submission_key=data["submission_key"],
        assignment_try=count + 1,
        retry_count=count,
        elapsed_ms=data.get("elapsed_ms", 0),
        hint_count=progress.hint_count if progress else 0,
        submitted_at=timezone.now(),
    )
    AssignmentProgress.objects.update_or_create(
        recipient=recipient, item=item, defaults={"answer": data["answer"]}
    )
    return recipient, attempt, True


@transaction.atomic
def submit_assignment(recipient_id, user):
    recipient = AssignmentRecipient.objects.select_for_update().get(
        pk=recipient_id, student__user=user
    )
    if recipient.submitted_at:
        return recipient
    require_open(recipient)
    if len(latest_attempts(recipient)) != recipient.assignment.items.count():
        raise ValidationError("모든 문항의 답을 제출해 주세요.")
    recipient.submitted_at = timezone.now()
    recipient.save(update_fields=("submitted_at",))
    return recipient


@transaction.atomic
def reveal_hint(recipient_id, user, item_id, level):
    recipient = AssignmentRecipient.objects.select_for_update().get(
        pk=recipient_id, student__user=user
    )
    require_open(recipient)
    item = recipient.assignment.items.filter(pk=item_id).first()
    if item is None or level > len(item.hints):
        raise ValidationError("요청한 힌트를 찾을 수 없습니다.")
    progress, _ = AssignmentProgress.objects.get_or_create(
        recipient=recipient, item=item
    )
    if level > progress.hint_count + 1:
        raise ValidationError("힌트를 순서대로 열어 주세요.")
    if level > progress.hint_count:
        progress.hint_count = level
        progress.save(update_fields=("hint_count", "updated_at"))
    return {"level": level, "hint": item.hints[level - 1]}
