"""One policy for discovery, solving, authoring and reuse.

Existing catalog entries without a publication are legacy public content.
New authored content always has an explicit private publication.
"""

from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from ..models import Problem
from ..platform_permissions import is_manager


def is_admin(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_active
        and (user.is_staff or user.is_superuser)
    )


def public_condition():
    return Q(publication__isnull=True) | Q(
        publication__status="published", publication__visibility="public"
    )


def public_problems():
    return Problem.objects.filter(public_condition())


def accessible_problems(user):
    qs = Problem.objects.select_related("publication", "publication__owner")
    if is_admin(user):
        return qs
    condition = public_condition()
    if user and user.is_authenticated and user.is_active:
        if is_manager(user):
            condition |= Q(publication__owner=user)
        condition |= Q(
            publication__status="published",
            publication__visibility="class",
            publication__classrooms__archived=False,
            publication__classrooms__enrollments__student__user=user,
            publication__classrooms__enrollments__status="approved",
        )
    return qs.filter(condition).distinct()


def can_edit(user, problem):
    publication = getattr(problem, "publication", None)
    return is_admin(user) or bool(
        is_manager(user) and publication and publication.owner_id == user.pk
    )


def reusable_problems(user):
    if is_admin(user):
        return Problem.objects.all()
    if not is_manager(user):
        return Problem.objects.none()
    return (
        Problem.objects.filter(
            Q(publication__owner=user)
            | Q(publication__isnull=True)
            | Q(
                publication__status="published",
                publication__visibility="public",
                publication__allow_classroom_use=True,
            )
        )
        .exclude(publication__status="archived")
        .distinct()
    )


def require_reusable(user, problems):
    ids = {p.pk for p in problems}
    if reusable_problems(user).filter(pk__in=ids).count() != len(ids):
        raise PermissionDenied(
            "사용할 수 없는 문제가 있습니다. 공개 범위와 수업 사용 허용을 확인해 주세요."
        )
