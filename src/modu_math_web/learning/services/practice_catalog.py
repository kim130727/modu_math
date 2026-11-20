"""Permission-filtered level cards and a student's daily practice goal."""

from collections import defaultdict
from zoneinfo import ZoneInfo

from django.utils import timezone

from ..models import Attempt


def category_key(catalog):
    return str(
        catalog.get("unit_topic")
        or catalog.get("unitTopic")
        or catalog.get("unit")
        or catalog.get("topic")
        or ""
    ).strip()


def practice_catalog(queryset, user):
    levels = defaultdict(lambda: defaultdict(int))
    for grade, catalog in queryset.values_list("grade", "catalog_data"):
        levels[grade][category_key(catalog)] += 1
    grades = [
        {
            "grade": grade,
            "count": sum(categories.values()),
            "categories": [
                {"key": key, "count": count}
                for key, count in sorted(categories.items())
            ],
        }
        for grade, categories in sorted(
            levels.items(), key=lambda pair: (pair[0] is None, pair[0] or 0)
        )
    ]
    now = timezone.now().astimezone(ZoneInfo("Asia/Seoul"))
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    completed = []
    if user.is_authenticated and user.is_active:
        completed = list(
            Attempt.objects.filter(
                user=user,
                problem__in=queryset,
                is_correct=True,
                assignment_item__isnull=True,
                created_at__gte=start,
                created_at__lte=now,
            )
            .order_by("problem_id")
            .values_list("problem_id", flat=True)
            .distinct()
        )
    return {
        "revision": next(
            (
                value.isoformat()
                for value in queryset.order_by("-updated_at").values_list(
                    "updated_at", flat=True
                )[:1]
            ),
            None,
        ),
        "grades": grades,
        "goal": {
            "date": now.date().isoformat(),
            "target": min(5, sum(level["count"] for level in grades)),
            "completed_ids": completed,
        },
    }
