from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from modu_math_web.learning.models import (
    Assignment,
    AssignmentRecipient,
    Attempt,
    Classroom,
    Enrollment,
    Problem,
    ProblemPublication,
    ProblemSet,
    StudentProfile,
)
from modu_math_web.learning.services.assignments import snapshot_item

pytestmark = pytest.mark.django_db


@pytest.fixture
def catalog_env():
    teacher = get_user_model().objects.create_user("catalog-teacher")
    student = get_user_model().objects.create_user("catalog-student")
    profile = StudentProfile.objects.create(user=student, created_by=teacher)
    problems = []
    for index, (grade, category, visibility) in enumerate(
        [
            (3, "덧셈", "public"),
            (3, "도형", "public"),
            (4, "덧셈과 뺄셈", "public"),
            (3, "비공개", "private"),
            (3, "우리 반", "class"),
            (None, "", "public"),
        ]
    ):
        problem = Problem.objects.create(
            problem_id=f"catalog-{index}",
            grade=grade,
            catalog_data={"unit": category},
            answer={"value": 7},
        )
        ProblemPublication.objects.create(
            problem=problem, owner=teacher, visibility=visibility, status="published"
        )
        problems.append(problem)
    classroom = Classroom.objects.create(teacher=teacher, name="반")
    Enrollment.objects.create(classroom=classroom, student=profile, status="approved")
    problems[4].publication.classrooms.add(classroom)
    api = APIClient()
    api.force_authenticate(student)
    return api, student, teacher, profile, classroom, problems


def test_catalog_and_exact_category_filter_preserve_access(catalog_env):
    api, _, _, _, classroom, problems = catalog_env
    response = api.get("/api/v1/problems/catalog/", {"scope": "public"})
    assert response.status_code == 200
    levels = response.data["grades"]
    assert sum(row["count"] for row in levels) == 4
    assert levels[0] == {
        "grade": 3,
        "count": 2,
        "categories": [
            {"key": "덧셈", "count": 1},
            {"key": "도형", "count": 1},
        ],
    }
    assert response.data["goal"]["target"] == 4
    assert response.data["goal"]["completed_ids"] == []
    exact = api.get("/api/v1/problems/", {"scope": "public", "category": "덧셈"})
    assert [row["id"] for row in exact.data["results"]] == [problems[0].pk]
    ungraded = api.get("/api/v1/problems/", {"scope": "public", "grade": "null"})
    assert [row["id"] for row in ungraded.data["results"]] == [problems[5].pk]
    own_class = api.get(
        "/api/v1/problems/catalog/", {"scope": "class", "classroom": classroom.pk}
    )
    assert own_class.data["grades"][0]["count"] == 1
    Enrollment.objects.update(status="pending")
    assert (
        api.get(
            "/api/v1/problems/catalog/",
            {
                "scope": "class",
                "classroom": classroom.pk,
            },
        ).data["grades"]
        == []
    )


def test_daily_goal_counts_unique_correct_free_practice_in_kst(catalog_env):
    api, student, teacher, profile, _, problems = catalog_env
    now = datetime(2026, 11, 19, 1, tzinfo=timezone.utc)
    start = datetime(2026, 11, 18, 15, tzinfo=timezone.utc)

    def attempt(problem, answer=7, user=student, at=None):
        record = Attempt.objects.create(
            user=user, problem=problem, submitted_answer=answer
        )
        Attempt.objects.filter(pk=record.pk).update(
            created_at=at or now - timedelta(minutes=1)
        )

    attempt(problems[0])
    attempt(problems[0])  # Repeated correct answers count once.
    attempt(problems[1], answer=0)
    attempt(problems[1], user=teacher)
    attempt(problems[2], at=start - timedelta(seconds=1))
    attempt(problems[3])  # Private content never appears in public progress.
    problem_set = ProblemSet.objects.create(owner=teacher, title="set")
    assignment = Assignment.objects.create(
        owner=teacher, problem_set=problem_set, source_version=1, title="homework"
    )
    recipient = AssignmentRecipient.objects.create(
        assignment=assignment, student=profile
    )
    item = snapshot_item(assignment, problems[1], 0)
    record = Attempt.objects.create(
        user=student,
        problem=problems[1],
        submitted_answer=7,
        recipient=recipient,
        assignment_item=item,
        assignment_try=1,
        submission_key="homework",
    )
    Attempt.objects.filter(pk=record.pk).update(created_at=now - timedelta(minutes=1))
    with patch(
        "modu_math_web.learning.services.practice_catalog.timezone.now",
        return_value=now,
    ):
        goal = api.get("/api/v1/problems/catalog/", {"scope": "public"}).data["goal"]
        assert goal["date"] == "2026-11-19"
        assert goal["completed_ids"] == [problems[0].pk]
        attempt(problems[2], at=start)  # Korean midnight is included.
        ids = api.get("/api/v1/problems/catalog/", {"scope": "public"}).data["goal"][
            "completed_ids"
        ]
        assert set(ids) == {problems[0].pk, problems[2].pk}
    with patch(
        "modu_math_web.learning.services.practice_catalog.timezone.now",
        return_value=now + timedelta(days=1),
    ):
        assert (
            api.get("/api/v1/problems/catalog/", {"scope": "public"}).data["goal"][
                "completed_ids"
            ]
            == []
        )
    anonymous = APIClient().get("/api/v1/problems/catalog/", {"scope": "public"})
    assert anonymous.data["goal"]["completed_ids"] == []
