import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from modu_math_web.learning.models import Problem, ProblemPublication

pytestmark = pytest.mark.django_db


@pytest.fixture
def teacher():
    user = get_user_model().objects.create_user("workspace-teacher")
    group, _ = Group.objects.get_or_create(name="modu_teachers")
    user.groups.add(group)
    return user


def test_workspace_serves_the_separate_teacher_bundle(client):
    response = client.get("/teacher/")
    assert response.status_code == 200
    assert b"teacher.js?v=" in response.content
    assert b"teacher.css?v=" in response.content
    assert b"editor-konva.js" not in response.content


def test_problem_catalog_has_lifecycle_fields_and_bounded_id_filter(teacher):
    first = Problem.objects.create(problem_id="workspace-first", answer={"value": 1})
    second = Problem.objects.create(problem_id="workspace-second", answer={"value": 2})
    ProblemPublication.objects.create(problem=second, status="review", difficulty=4)
    client = APIClient()
    client.force_authenticate(teacher)
    rows = client.get("/api/v1/problems/", {"ids": str(second.pk)}).data["results"]
    assert len(rows) == 1
    assert rows[0]["publication_status"] == "review" and rows[0]["difficulty"] == 4
    for ids in ("x", "-1", ",", ",".join(["1"] * 201)):
        assert client.get("/api/v1/problems/", {"ids": ids}).status_code == 400
    public = (
        APIClient()
        .get("/api/v1/problems/", {"ids": f"{first.pk},{second.pk}"})
        .data["results"]
    )
    assert len(public) == 1
    assert (
        public[0]["publication_status"] == "published" and public[0]["difficulty"] == 1
    )


def test_signed_image_session_is_scoped_and_revocable(teacher, tmp_path, settings):
    settings.DEBUG = False
    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko"
    directory.mkdir()
    (directory / "sample.dsl.py").write_text("# image fixture", encoding="utf-8")
    (directory / "image.png").write_bytes(b"test-image")
    client = APIClient()
    token = Token.objects.create(user=teacher)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    response = client.post("/api/v1/auth/editor-session/")
    assert response.status_code == 204
    cookie = response.cookies["modu_editor_session"]
    assert cookie["httponly"] and cookie["secure"]
    assert cookie["samesite"] == "Strict" and cookie["path"] == "/"
    assert cookie["max-age"] == 3600
    client.credentials()
    asset = "/api/editor/assets/ko/sample.dsl.py/image.png"
    assert client.get(asset).status_code == 200
    # A cookie can load images, but cannot read source API responses or write.
    assert client.get("/api/editor/problems/").status_code == 401
    assert (
        client.post("/api/editor/problems/create/", {}, format="json").status_code
        == 401
    )
    teacher.groups.clear()
    assert client.get(asset).status_code == 403
    teacher.groups.add(Group.objects.get(name="modu_teachers"))
    token.delete()
    assert client.get(asset).status_code == 401


def test_students_cannot_obtain_editor_image_credentials():
    user = get_user_model().objects.create_user("workspace-student")
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION="Token " + Token.objects.create(user=user).key
    )
    assert client.post("/api/v1/auth/editor-session/").status_code == 403


def test_logout_removes_image_cookie(teacher):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION="Token " + Token.objects.create(user=teacher).key
    )
    assert client.post("/api/v1/auth/editor-session/").status_code == 204
    response = client.post("/api/v1/auth/logout/")
    assert response.status_code == 204
    assert response.cookies["modu_editor_session"]["max-age"] == 0
