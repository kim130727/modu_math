"""Ownership, public practice, classroom groups and revocation boundaries."""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from modu_math_web.learning.models import (
    Classroom,
    Enrollment,
    Problem,
    ProblemPublication,
    StudentProfile,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def community():
    group, _ = Group.objects.get_or_create(name="modu_teachers")
    teacher = get_user_model().objects.create_user("author")
    other = get_user_model().objects.create_user("other")
    teacher.groups.add(group)
    other.groups.add(group)
    student = get_user_model().objects.create_user("learner")
    profile = StudentProfile.objects.create(user=student, created_by=teacher)
    classroom = Classroom.objects.create(teacher=teacher, name="수학 탐험대")
    enrollment = Enrollment.objects.create(classroom=classroom, student=profile)
    problem = Problem.objects.create(
        problem_id="owned",
        answer={"value": 7},
        semantic_data={"metadata": {"question": "3 + 4 = ?"}},
        renderer_data={"elements": []},
    )
    publication = ProblemPublication.objects.create(
        problem=problem, owner=teacher, status="published"
    )
    return teacher, other, student, classroom, enrollment, problem, publication


def client(user=None):
    api = APIClient()
    if user:
        api.force_authenticate(user)
    return api


def test_private_problem_is_owned_even_for_other_teachers(community):
    teacher, other, student, _, _, problem, pub = community
    url = f"/api/v1/problems/{problem.pk}/"
    assert client(teacher).get(url).status_code == 200
    for user in (None, other, student):
        api = client(user)
        assert api.get(url).status_code == 404
        assert api.get("/api/v1/problems/").data["count"] == 0
        if user:
            assert (
                api.post(
                    "/api/v1/attempts/",
                    {"problem": problem.pk, "submitted_answer": 7},
                    format="json",
                ).status_code
                == 400
            )
    assert (
        client(other)
        .post(
            "/api/v1/problem-sets/",
            {"title": "copy", "problem_ids": [problem.pk]},
            format="json",
        )
        .status_code
        == 403
    )


def test_all_students_can_solve_public_without_class_and_cannot_edit(community):
    teacher, other, student, _, _, problem, pub = community
    pub.visibility = "public"
    pub.save()
    api = client(student)
    detail = api.get(f"/api/v1/problems/{problem.pk}/").data
    assert "answer" not in detail and "solvable_data" not in detail
    assert detail["owner_name"] == "author" and detail["visibility"] == "public"
    assert client().get("/api/v1/problems/").data["count"] == 1
    response = api.post(
        "/api/v1/attempts/",
        {"problem": problem.pk, "submitted_answer": 7},
        format="json",
    )
    assert response.status_code == 201 and response.data["is_correct"]
    assert (
        client(other)
        .patch(
            f"/api/v1/problems/{problem.pk}/publication/",
            {"visibility": "private"},
            format="json",
        )
        .status_code
        == 403
    )
    assert "answer" not in client(other).get(f"/api/v1/problems/{problem.pk}/").data


def test_class_shelf_requires_approval_and_active_class(community):
    _, other, student, classroom, enrollment, problem, pub = community
    pub.visibility = "class"
    pub.save()
    pub.classrooms.add(classroom)
    api = client(student)
    url = f"/api/v1/problems/{problem.pk}/"
    assert api.get(url).status_code == 404
    assert api.get("/api/v1/student/classes/").data[0]["status"] == "pending"
    enrollment.status = "approved"
    enrollment.save()
    assert api.get(url).status_code == 200
    assert api.get("/api/v1/problems/", {"scope": "public"}).data["count"] == 0
    assert (
        api.get(
            "/api/v1/problems/", {"scope": "class", "classroom": classroom.pk}
        ).data["count"]
        == 1
    )
    assert client(other).get(url).status_code == 404
    enrollment.status = "inactive"
    enrollment.save()
    assert api.get(url).status_code == 404
    joined = api.post("/api/v1/student/join-class/", {"invite_code": classroom.invite_code}, format="json")
    assert joined.status_code == 201 and joined.data["status"] == "pending"
    enrollment.refresh_from_db()
    enrollment.status = "approved"
    enrollment.save()
    classroom.archived = True
    classroom.save()
    assert api.get(url).status_code == 404
    assert api.get("/api/v1/student/classes/").data == []


def test_owner_can_only_share_to_owned_classes_and_must_confirm_rights(community):
    teacher, other, _, classroom, _, problem, pub = community
    api = client(teacher)
    url = f"/api/v1/problems/{problem.pk}/publication/"
    assert api.patch(url, {"visibility": "public"}, format="json").status_code == 400
    foreign = Classroom.objects.create(teacher=other, name="다른 클래스")
    assert (
        api.patch(
            url,
            {
                "visibility": "class",
                "rights_confirmed": True,
                "classroom_ids": [foreign.pk],
            },
            format="json",
        ).status_code
        == 400
    )
    assert (
        api.patch(
            url,
            {"visibility": "class", "rights_confirmed": True, "classroom_ids": []},
            format="json",
        ).status_code
        == 400
    )
    assert (
        api.patch(
            url,
            {
                "visibility": "class",
                "rights_confirmed": True,
                "classroom_ids": [classroom.pk],
                "owner": other.pk,
            },
            format="json",
        ).status_code
        == 200
    )
    pub.refresh_from_db()
    assert pub.owner_id == teacher.pk


def test_reuse_revocation_stops_new_assignment_preserves_old_snapshot(community):
    teacher, other, student, classroom, enrollment, problem, pub = community
    pub.visibility = "public"
    pub.allow_classroom_use = True
    pub.save()
    api = client(other)
    set_response = api.post(
        "/api/v1/problem-sets/",
        {"title": "수업", "problem_ids": [problem.pk]},
        format="json",
    )
    assert set_response.status_code == 201
    from modu_math_web.learning.models import (
        Assignment,
        AssignmentItem,
        AssignmentRecipient,
    )

    assignment = Assignment.objects.create(
        owner=other,
        problem_set_id=set_response.data["id"],
        source_version=1,
        title="기존 과제",
    )
    from modu_math_web.learning.services.assignments import snapshot_item

    snapshot_item(assignment, problem, 0)
    AssignmentRecipient.objects.create(
        assignment=assignment, student=enrollment.student
    )
    pub.visibility = "private"
    pub.save()
    assert (
        api.post(
            f"/api/v1/problem-sets/{set_response.data['id']}/duplicate/"
        ).status_code
        == 403
    )
    assert client(student).get(f"/api/v1/problems/{problem.pk}/").status_code == 404
    result = client(student).get(f"/api/v1/student/assignments/{assignment.pk}/")
    assert result.status_code == 200 and len(result.data["items"]) == 1
    assert AssignmentItem.objects.filter(assignment=assignment).count() == 1


def test_editor_creation_owns_source_and_blocks_other_teacher(
    community, settings, tmp_path, monkeypatch
):
    teacher, other, _, _, _, _, _ = community
    settings.DEBUG = False
    settings.PROBLEMS_ROOT = tmp_path
    api = APIClient()
    api.credentials(
        HTTP_AUTHORIZATION="Token " + Token.objects.create(user=teacher).key
    )
    created = api.post(
        "/api/editor/problems/create/",
        {"problem_id": "ko/new.dsl.py", "title": "새 문제"},
        format="json",
    )
    assert created.status_code == 200
    source = created.json()["problem_id"]
    pub = ProblemPublication.objects.get(source_path=source)
    assert (
        pub.owner == teacher and pub.visibility == "private" and pub.status == "draft"
    )
    assert api.get(f"/api/editor/problems/{source}/").status_code == 200
    from modu_math_web.editor.services.build import BuildResult

    artifacts = {
        "semantic": {
            "metadata": {"title": "새 문제", "grade": 3},
            "answer": {"value": 7},
        },
        "renderer": {"elements": []},
        "layout": {},
        "solvable": {},
    }
    monkeypatch.setattr(
        "modu_math_web.editor.views.build_with_artifacts",
        lambda _: (BuildResult(True, "", ""), artifacts),
    )
    assert api.post(f"/api/editor/problems/{source}/build/").status_code == 200
    pub.problem.refresh_from_db()
    pub.refresh_from_db()
    assert pub.problem.answer == {"value": 7} and pub.problem.grade == 3
    assert pub.visibility == "private" and pub.status == "draft"
    assert (
        api.patch(
            f"/api/editor/problems/{source}/publication/",
            {"visibility": "public", "status": "published", "rights_confirmed": True},
            format="json",
        ).status_code
        == 200
    )
    assert client().get(f"/api/v1/problems/{pub.problem_id}/").status_code == 200
    api.credentials(HTTP_AUTHORIZATION="Token " + Token.objects.create(user=other).key)
    assert api.get(f"/api/editor/problems/{source}/").status_code == 404
    assert (
        api.post(
            f"/api/editor/problems/{source}/dsl/", {"dsl": "secret"}, format="json"
        ).status_code
        == 404
    )
    assert api.get(f"/api/editor/assets/{source}/new.dsl.py").status_code == 404
    assert api.get("/api/editor/problems/").json()["problems"] == []


def test_private_problem_never_appears_in_recommendations(community):
    _, _, student, _, _, _, _ = community
    response = client(student).get("/api/v1/recommendations/")
    assert response.status_code == 200
    assert "owned" not in str(response.data)
