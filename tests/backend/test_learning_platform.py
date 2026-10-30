"""Exercise public APIs, including the requested two-student/ten-item flow."""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.test import override_settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from modu_math_web.learning.models import (
    Assignment,
    AssignmentItem,
    AssignmentRecipient,
    Attempt,
    Classroom,
    Enrollment,
    Mastery,
    Problem,
    ProblemPublication,
    ProblemSet,
    StudentProfile,
    answer_matches,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def env():
    users = get_user_model()
    teacher = users.objects.create_user("teacher", password="teacher-password")
    group, _ = Group.objects.get_or_create(name="modu_teachers")
    teacher.groups.add(group)
    other = users.objects.create_user("other-teacher", password="teacher-password")
    other.groups.add(group)
    students = [
        StudentProfile.objects.create(
            user=users.objects.create_user(f"student-{i}", password="student-password"),
            created_by=teacher,
        )
        for i in range(2)
    ]
    problems = [
        Problem.objects.create(
            problem_id=f"platform-{i}",
            grade=3,
            concepts=["addition"],
            answer={"value": i + 10},
            catalog_data={"unit": "덧셈"},
            semantic_data={
                "metadata": {"question": f"{i} + 10 = ?"},
                "domain": {"secret_total": i + 10},
                "answer": {"value": i + 10},
            },
            solvable_data={"steps": [{"value": i + 10}], "answer": {"value": i + 10}},
            renderer_data={
                "view_box": {"width": 900, "height": 200},
                "tutor_flow": [{"answer": i + 10}],
                "elements": [
                    {
                        "id": "input",
                        "type": "rect",
                        "attributes": {
                            "x": 10,
                            "y": 10,
                            "width": 100,
                            "height": 40,
                            "expected": i + 10,
                        },
                        "interaction": {
                            "type": "input",
                            "value": i + 10,
                            "expected": i + 10,
                        },
                    }
                ],
            },
        )
        for i in range(10)
    ]
    client = APIClient()
    client.force_authenticate(teacher)
    return {
        "teacher": teacher,
        "other": other,
        "students": students,
        "problems": problems,
        "client": client,
    }


def make_assignment(env, **options):
    client = env["client"]
    client.force_authenticate(env["teacher"])
    response = client.post(
        "/api/v1/problem-sets/",
        {"title": "열 문제", "problem_ids": [p.pk for p in env["problems"]]},
        format="json",
    )
    assert response.status_code == 201, response.data
    response = client.post(
        "/api/v1/assignments/",
        {
            "title": "첫 과제",
            "problem_set": response.data["id"],
            "student_ids": [s.pk for s in env["students"]],
            **options,
        },
        format="json",
    )
    assert response.status_code == 201, response.data
    return Assignment.objects.get(pk=response.data["id"])


def url(assignment, suffix=""):
    return f"/api/v1/student/assignments/{assignment.pk}/{suffix}"


def answer(client, assignment, item, value, key=None, **extra):
    return client.post(
        url(assignment, "answers/"),
        {
            "item_id": item.pk,
            "answer": value,
            "submission_key": key or f"item-{item.pk}",
            "elapsed_ms": 1200,
            "hint_count": 1,
            **extra,
        },
        format="json",
    )


def test_two_students_ten_questions_server_grading_and_review(env):
    client = env["client"]
    assignment = make_assignment(env)
    for index, student in enumerate(env["students"]):
        # Use real login/token authentication, as the mobile app will.
        client = APIClient()
        login = client.post(
            "/api/v1/auth/login/",
            {"username": student.user.username, "password": "student-password"},
            format="json",
        )
        assert login.status_code == 200
        client.credentials(HTTP_AUTHORIZATION="Token " + login.data["token"])
        assert len(client.get("/api/v1/student/assignments/").data) == 1
        assert client.get(url(assignment)).data["completed"] == 0
        for item in assignment.items.all():
            value = item.answer["value"] if index == 0 or item.position > 1 else -1
            response = answer(client, assignment, item, value, is_correct=True)
            assert response.status_code == 201, response.data
            assert "is_correct" not in response.data
        response = client.post(url(assignment, "submit/"), {}, format="json")
        assert response.status_code == 200
        assert response.data["completed"] == 10
        assert response.data["correct"] == (10 if index == 0 else 8)
        assert response.data["progress"] == 1
        assert (
            client.post(url(assignment, "submit/"), {}, format="json").status_code
            == 200
        )
    client.credentials()
    client.force_authenticate(env["teacher"])
    results = client.get(f"/api/v1/assignments/{assignment.pk}/results/")
    assert results.status_code == 200
    assert results.data["assignment"]["accuracy"] == 0.9
    assert results.data["assignment"]["submitted_count"] == 2
    assert results.data["unsubmitted_recipient_ids"] == []
    assert results.data["concepts"]["addition"] == {"correct": 18, "total": 20}
    recipient = assignment.recipients.get(student=env["students"][1])
    review = client.post(
        f"/api/v1/assignments/{assignment.pk}/reassign-wrong/",
        {"recipient_id": recipient.pk},
        format="json",
    )
    assert review.status_code == 201
    assert review.data["item_count"] == 2
    assert review.data["recipient_count"] == 1
    assert Attempt.objects.count() == 20
    assert (
        Mastery.objects.get(
            user=env["students"][1].user, concept="addition"
        ).correct_count
        == 8
    )


def test_teacher_and_student_object_isolation(env):
    assignment = make_assignment(env)
    client = env["client"]
    student = env["students"][0]
    client.force_authenticate(student.user)
    for path in (
        "students",
        "classes",
        "problem-sets",
        "assignments",
        "teacher/dashboard",
    ):
        assert client.get(f"/api/v1/{path}/").status_code == 403
    stranger = get_user_model().objects.create_user("stranger")
    client.force_authenticate(stranger)
    assert client.get(url(assignment)).status_code == 404
    assert client.post(url(assignment, "submit/"), {}).status_code == 404
    client.force_authenticate(env["other"])
    assert client.get(f"/api/v1/assignments/{assignment.pk}/").status_code == 404
    assert (
        client.get(f"/api/v1/assignments/{assignment.pk}/recipients/").status_code
        == 404
    )
    assert client.get(f"/api/v1/students/{student.pk}/").status_code == 404
    assert client.get("/api/v1/teacher/dashboard/").data["students"] == 0
    bad = client.post(
        "/api/v1/assignments/",
        {
            "problem_set": assignment.problem_set_id,
            "title": "도용",
            "student_ids": [student.pk],
        },
        format="json",
    )
    assert bad.status_code == 404


def test_registration_invitation_approval_and_privilege_escalation(env):
    client = env["client"]
    classroom = client.post(
        "/api/v1/classes/", {"name": "3학년", "teacher": env["other"].pk}, format="json"
    )
    assert classroom.status_code == 201
    assert classroom.data["teacher"] == env["teacher"].pk
    client = APIClient()
    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "new-student",
            "password": "safe-password",
            "invite_code": classroom.data["invite_code"],
            "is_staff": True,
            "is_superuser": True,
            "role": "teacher",
            "groups": [1],
        },
        format="json",
    )
    assert response.status_code == 201, response.data
    user = get_user_model().objects.get(username="new-student")
    assert not user.is_staff and not user.is_superuser and not user.groups.exists()
    assert response.data["user"]["role"] == "student"
    enrollment = Enrollment.objects.get(student__user=user)
    assert enrollment.status == "pending"
    client.force_authenticate(env["teacher"])
    assert enrollment.student_id not in [
        row["id"] for row in client.get("/api/v1/students/").data
    ]
    response = client.patch(
        f"/api/v1/classes/{enrollment.classroom_id}/enrollments/{enrollment.pk}/",
        {"status": "approved"},
        format="json",
    )
    assert response.status_code == 200
    assert enrollment.student_id in [
        row["id"] for row in client.get("/api/v1/students/").data
    ]


def test_student_creation_and_class_recipient_snapshot(env):
    client = env["client"]
    created = client.post(
        "/api/v1/students/",
        {"username": "created-student", "password": "safe-password", "is_staff": True},
        format="json",
    )
    assert created.status_code == 201
    assert not get_user_model().objects.get(pk=created.data["user_id"]).is_staff
    classroom = client.post("/api/v1/classes/", {"name": "반"}, format="json").data
    for student in env["students"]:
        assert (
            client.post(
                f"/api/v1/classes/{classroom['id']}/enrollments/",
                {"student_id": student.pk},
                format="json",
            ).status_code
            == 201
        )
    assignment = make_assignment(env, class_ids=[classroom["id"]], student_ids=[])
    assert assignment.recipients.count() == 2
    Enrollment.objects.filter(classroom_id=classroom["id"]).update(status="inactive")
    assert assignment.recipients.count() == 2
    client.force_authenticate(env["students"][0].user)
    assert client.get(url(assignment)).status_code == 200


def test_snapshots_survive_source_and_problem_set_edits(env):
    assignment = make_assignment(env)
    client = env["client"]
    first = assignment.items.first()
    original = first.answer.copy()
    Problem.objects.filter(pk=first.problem_id).update(
        answer={"value": 999}, concepts=["changed"], renderer_data={}
    )
    updated = client.patch(
        f"/api/v1/problem-sets/{assignment.problem_set_id}/",
        {"problem_ids": [env["problems"][-1].pk]},
        format="json",
    )
    assert updated.status_code == 200
    assert updated.data["version"] == 2
    assert assignment.items.count() == 10
    first.refresh_from_db()
    assert first.answer == original
    assert first.concepts == ["addition"]
    client.force_authenticate(env["students"][0].user)
    assert answer(client, assignment, first, original["value"]).status_code == 201
    assert Attempt.objects.get(recipient__student=env["students"][0]).is_correct
    assert not Mastery.objects.filter(concept="changed").exists()


def test_duplicate_problem_set_keeps_order_and_owner(env):
    assignment = make_assignment(env)
    client = env["client"]
    response = client.post(
        f"/api/v1/problem-sets/{assignment.problem_set_id}/duplicate/",
        {},
        format="json",
    )
    assert response.status_code == 201
    assert [i["problem"] for i in response.data["items"]] == [
        p.pk for p in env["problems"]
    ]
    assert response.data["version"] == 1


@pytest.mark.parametrize(
    "policy", ["immediate", "after_submission", "after_due", "never"]
)
def test_no_answer_contract_before_solving_and_release_rules(env, policy):
    options = {"release_policy": policy}
    if policy == "after_due":
        options["due_at"] = (timezone.now() + timedelta(days=1)).isoformat()
    assignment = make_assignment(env, **options)
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    before = client.get(url(assignment)).data
    first = before["items"][0]
    assert "answer" not in first and "solution" not in first
    content = first["content"]
    assert "solvable_data" not in content and "answer" not in content
    assert "domain" not in content["semantic_data"]
    assert "tutor_flow" not in content["renderer_data"]
    visual = content["renderer_data"]["elements"][0]
    assert (
        "value" not in visual["interaction"] and "expected" not in visual["attributes"]
    )
    item = assignment.items.first()
    response = answer(client, assignment, item, item.answer["value"])
    assert ("is_correct" in response.data) == (policy == "immediate")
    after = client.get(url(assignment)).data
    assert ("answer" in after["items"][0]) == (policy == "immediate")
    # Legacy history/mastery/diagnostic APIs cannot reveal hidden grades.
    assert client.get("/api/v1/attempts/").data["count"] == (
        1 if policy == "immediate" else 0
    )
    assert client.get("/api/v1/masteries/").data["count"] == (
        1 if policy == "immediate" else 0
    )
    assert client.get("/api/v1/diagnostics/summary/").data["total_attempts"] == (
        1 if policy == "immediate" else 0
    )
    if policy == "after_due":
        assignment.due_at = timezone.now() - timedelta(seconds=1)
        assignment.save(update_fields=("due_at",))
        assert "answer" in client.get(url(assignment)).data["items"][0]


def test_idempotency_attempt_limit_and_payload_conflicts(env):
    assignment = make_assignment(env, max_attempts=2)
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    item = assignment.items.first()
    first = answer(client, assignment, item, -1, "same")
    assert first.status_code == 201
    replay = answer(client, assignment, item, -1, "same")
    assert (
        replay.status_code == 200
        and replay.data["attempt_id"] == first.data["attempt_id"]
    )
    assert answer(client, assignment, item, 10, "same").status_code == 400
    assert answer(client, assignment, item, 10, "second").status_code == 201
    assert answer(client, assignment, item, 10, "third").status_code == 400
    assert Attempt.objects.count() == 2
    assert Mastery.objects.get(user=env["students"][0].user).attempt_count == 2
    # The legacy endpoint cannot bypass retries and release rules.
    assert (
        client.post(
            "/api/v1/attempts/",
            {"problem": item.problem_id, "submitted_answer": 10},
            format="json",
        ).status_code
        == 400
    )


def test_draft_resume_and_incomplete_submission(env):
    assignment = make_assignment(env)
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    item = assignment.items.first()
    response = client.put(
        url(assignment, "progress/"),
        {"item_id": item.pk, "answer": "12"},
        format="json",
    )
    assert response.status_code == 200
    detail = client.get(url(assignment)).data
    assert detail["items"][0]["draft_answer"] == "12"
    assert detail["completed"] == 0 and Attempt.objects.count() == 0
    assert client.post(url(assignment, "submit/"), {}, format="json").status_code == 400


@pytest.mark.parametrize("state", ["future", "past", "closed", "cancelled"])
def test_start_deadline_and_status_enforced(env, state):
    assignment = make_assignment(env)
    if state == "future":
        assignment.starts_at = timezone.now() + timedelta(days=1)
    elif state == "past":
        assignment.due_at = timezone.now() - timedelta(days=1)
    else:
        assignment.status = state
    assignment.save()
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    assert answer(client, assignment, assignment.items.first(), 10).status_code == 400
    if state == "future":
        assert "items" not in client.get(url(assignment)).data


def test_foreign_item_and_recipient_injection_rejected(env):
    first = make_assignment(env)
    second = make_assignment(env)
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    assert answer(client, first, second.items.first(), 10).status_code == 400
    response = answer(
        client,
        first,
        first.items.first(),
        10,
        recipient_id=first.recipients.get(student=env["students"][1]).pk,
        user=env["students"][1].user_id,
    )
    assert response.status_code == 201
    assert Attempt.objects.get().user_id == env["students"][0].user_id


def test_bank_search_publication_and_public_detail(env):
    client = env["client"]
    problem = env["problems"][0]
    response = client.patch(
        f"/api/v1/problems/{problem.pk}/publication/",
        {"status": "draft", "difficulty": 4},
        format="json",
    )
    assert response.status_code == 200
    assert (
        client.get(
            "/api/v1/problems/?grade=3&unit=덧셈&concept=addition&difficulty=4"
        ).data["count"]
        == 1
    )
    assert "answer" in client.get(f"/api/v1/problems/{problem.pk}/").data
    client.force_authenticate(env["students"][0].user)
    assert client.get(f"/api/v1/problems/{problem.pk}/").status_code == 404
    assert (
        client.post(
            "/api/v1/attempts/",
            {"problem": problem.pk, "submitted_answer": 10},
            format="json",
        ).status_code
        == 400
    )
    assert (
        client.patch(
            f"/api/v1/problems/{env['problems'][1].pk}/publication/",
            {"status": "published"},
            format="json",
        ).status_code
        == 403
    )
    client = APIClient()
    assert "answer" not in client.get(f"/api/v1/problems/{env['problems'][1].pk}/").data
    assert (
        client.get(
            f"/api/v1/problems/{env['problems'][1].pk}/asset/?filename=secret.renderer.json"
        ).status_code
        == 400
    )


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
def test_production_editor_api_requires_teacher_token(env):
    client = APIClient()
    assert client.get("/api/editor/problems/").status_code == 401
    token = Token.objects.create(user=env["students"][0].user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    assert client.get("/api/editor/problems/").status_code == 403
    token = Token.objects.create(user=env["teacher"])
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    # An authorized request reaches the view, rather than the middleware gate.
    assert client.get("/api/editor/tutor-preview/status/").status_code == 200


def test_database_duplicate_recipient_and_attempt_constraints(env):
    assignment = make_assignment(env)
    recipient = assignment.recipients.first()
    with pytest.raises(IntegrityError), transaction.atomic():
        AssignmentRecipient.objects.create(
            assignment=assignment, student=recipient.student
        )
    with pytest.raises(IntegrityError), transaction.atomic():
        Attempt.objects.create(
            user=recipient.student.user,
            problem=env["problems"][0],
            recipient=recipient,
            submitted_answer=10,
        )


def test_multi_blank_grading_requires_all_answers():
    contract = {
        "value": "1,2",
        "answer_key": [{"slot_id": "a", "value": 1}, {"slot_id": "b", "value": 2}],
    }
    assert not answer_matches(contract, 1)
    assert not answer_matches(contract, [1, 0])
    assert answer_matches(contract, [1, 2])
    assert answer_matches(contract, {"a": 1, "b": 2})
    assert not answer_matches(contract, {"a": 1})


def test_admin_roles_cannot_be_changed_by_teachers_or_staff_escalation(env):
    client = env["client"]
    student = env["students"][0].user
    assert (
        client.patch(
            f"/api/v1/admin/users/{student.pk}/", {"role": "admin"}, format="json"
        ).status_code
        == 403
    )
    staff = get_user_model().objects.create_user("staff", is_staff=True)
    client.force_authenticate(staff)
    assert (
        client.patch(
            f"/api/v1/admin/users/{student.pk}/", {"role": "admin"}, format="json"
        ).status_code
        == 403
    )
    response = client.patch(
        f"/api/v1/admin/users/{student.pk}/", {"role": "teacher"}, format="json"
    )
    assert response.status_code == 200
    student.refresh_from_db()
    assert not student.is_staff
    assert student.groups.filter(name="modu_teachers").exists()
    assert (
        client.patch(
            f"/api/v1/admin/users/{staff.pk}/", {"is_active": False}, format="json"
        ).status_code
        == 403
    )


def test_me_and_logout_revoke_token(env):
    client = APIClient()
    token = Token.objects.create(user=env["students"][0].user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    response = client.get("/api/v1/auth/me/")
    assert response.status_code == 200 and response.data["role"] == "student"
    assert "password" not in response.data
    assert client.post("/api/v1/auth/logout/").status_code == 204
    assert client.get("/api/v1/auth/me/").status_code == 401


def test_assignment_validation_and_foreign_class(env):
    assignment = make_assignment(env)
    client = env["client"]
    foreign = Classroom.objects.create(teacher=env["other"], name="다른 반")
    base = {
        "title": "검증",
        "problem_set": assignment.problem_set_id,
        "student_ids": [env["students"][0].pk],
    }
    for extra in (
        {"max_attempts": 0},
        {"max_attempts": 21},
        {"release_policy": "after_due"},
        {"class_ids": [foreign.pk]},
        {
            "starts_at": timezone.now().isoformat(),
            "due_at": (timezone.now() - timedelta(days=1)).isoformat(),
        },
    ):
        assert (
            client.post(
                "/api/v1/assignments/", {**base, **extra}, format="json"
            ).status_code
            == 400
        )
    stranger = StudentProfile.objects.create(
        user=get_user_model().objects.create_user("unrelated"), created_by=env["other"]
    )
    assert (
        client.post(
            "/api/v1/assignments/",
            {**base, "student_ids": [stranger.pk]},
            format="json",
        ).status_code
        == 400
    )


def test_completed_assignment_blocks_new_attempts_but_replays_original(env):
    assignment = make_assignment(env)
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    for item in assignment.items.all():
        assert answer(client, assignment, item, item.answer["value"]).status_code == 201
    assert client.post(url(assignment, "submit/")).status_code == 200
    item = assignment.items.first()
    assert answer(client, assignment, item, item.answer["value"]).status_code == 200
    assert (
        answer(client, assignment, item, item.answer["value"], "new-key").status_code
        == 400
    )
    assert (
        client.put(
            url(assignment, "progress/"),
            {"item_id": item.pk, "answer": "changed"},
            format="json",
        ).status_code
        == 400
    )
    assert Attempt.objects.count() == 10


def test_global_practice_statistics_do_not_inflate_assignment_results(env):
    assignment = make_assignment(env)
    student = env["students"][0]
    for _ in range(3):
        Attempt.objects.create(
            user=student.user, problem=env["problems"][0], submitted_answer=10
        )
    client = env["client"]
    client.force_authenticate(student.user)
    item = assignment.items.first()
    assert answer(client, assignment, item, -1).status_code == 201
    # Hidden assignment grade is removed from the public all-time aggregate.
    mastery = client.get("/api/v1/masteries/").data["results"][0]
    assert mastery["attempt_count"] == 3 and mastery["score"] == 1
    client.force_authenticate(env["teacher"])
    results = client.get(f"/api/v1/assignments/{assignment.pk}/results/").data
    assert results["recipients"][0]["completed"] == 1
    assert results["assignment"]["accuracy"] == 0


def test_sync_preserves_unlisted_learning_records_and_review_state(env, tmp_path):
    from django.core.management import call_command

    problem = env["problems"][0]
    attempt = Attempt.objects.create(
        user=env["students"][0].user, problem=problem, submitted_answer=10
    )
    source = tmp_path / "ko" / "imported.dsl.py"
    source.parent.mkdir()
    source.write_text(
        """from modu_math.dsl import Canvas, ProblemTemplate, TextSlot, Region
PROBLEM_TEMPLATE = ProblemTemplate(id="imported", title="문제", canvas=Canvas(width=400, height=200),
    regions=(Region(id="region.main", role="prompt", slot_ids=("slot.q",)),),
    slots=(TextSlot(id="slot.q", text="문제", x=10, y=20, width=300, height=50),))
""",
        encoding="utf-8",
    )
    source.with_name("imported.renderer.json").write_text(
        '{"elements": []}', encoding="utf-8"
    )
    source.with_name("imported.semantic.json").write_text(
        '{"problem_id": "imported", "answer": {"value": 1}}', encoding="utf-8"
    )
    call_command("sync_problems", root=tmp_path, verbosity=0)
    assert Attempt.objects.filter(pk=attempt.pk).exists()
    assert Problem.objects.filter(pk=problem.pk).exists()
    imported = Problem.objects.get(problem_id="imported")
    assert imported.publication.status == "draft"
    publication = imported.publication
    publication.status = "review"
    publication.save()
    call_command("sync_problems", root=tmp_path, new_status="published", verbosity=0)
    publication.refresh_from_db()
    assert publication.status == "review"


def test_korean_concept_search_uses_exact_tag_membership(env):
    problem = env["problems"][0]
    problem.concepts = ["받아올림 있는 덧셈"]
    problem.save(update_fields=("concepts",))
    client = env["client"]
    assert (
        client.get("/api/v1/problems/", {"concept": "받아올림 있는 덧셈"}).data["count"]
        == 1
    )
    assert client.get("/api/v1/problems/", {"concept": "받아올림"}).data["count"] == 0
