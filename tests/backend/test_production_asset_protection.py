"""Test production asset protection and route isolation for students, teachers, and anonymous users."""

from __future__ import annotations

from pathlib import Path
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.signing import TimestampSigner
from django.test import Client, override_settings
from rest_framework.authtoken.models import Token

from modu_math_web.learning.models import StudentProfile
from apps.mobile.scripts.prepare_student_build import verify_student_bundle

pytestmark = pytest.mark.django_db


@pytest.fixture
def protection_env():
    users = get_user_model()
    teacher = users.objects.create_user("sec-teacher", password="pw")
    group, _ = Group.objects.get_or_create(name="modu_teachers")
    teacher.groups.add(group)
    teacher_token = Token.objects.create(user=teacher)

    student_user = users.objects.create_user("sec-student", password="pw")
    student_profile = StudentProfile.objects.create(user=student_user, created_by=teacher)
    student_token = Token.objects.create(user=student_user)

    return {
        "teacher": teacher,
        "teacher_token": teacher_token.key,
        "student": student_user,
        "student_token": student_token.key,
    }


@override_settings(DEBUG=False)
def test_production_root_redirect_to_student():
    client = Client()
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/student/"


@override_settings(DEBUG=False)
def test_anonymous_user_blocked_from_editor_and_assets():
    client = Client()

    # Web pages redirect anonymous visitors to teacher login
    res_konva = client.get("/editor-konva/")
    assert res_konva.status_code == 302
    assert res_konva.headers["Location"] == "/teacher/"

    res_legacy = client.get("/editor/")
    assert res_legacy.status_code == 302
    assert res_legacy.headers["Location"] == "/teacher/"

    # API returns 401
    res_api = client.get("/api/editor/problems/")
    assert res_api.status_code == 401
    assert "Authentication required" in res_api.json().get("detail", "")

    # Static Flutter editor assets return 401
    res_static = client.get("/static/editor_next/flutter_editor/main.dart.js")
    assert res_static.status_code == 401


@override_settings(DEBUG=False)
def test_student_forbidden_from_editor_and_authoring_assets(protection_env):
    client = Client()
    headers = {"HTTP_AUTHORIZATION": f"Token {protection_env['student_token']}"}

    # Student cannot open editor web pages
    res_konva = client.get("/editor-konva/", **headers)
    assert res_konva.status_code == 403

    res_legacy = client.get("/editor/", **headers)
    assert res_legacy.status_code == 403

    # Student cannot query editor API
    res_api = client.get("/api/editor/problems/", **headers)
    assert res_api.status_code == 403
    assert "Teacher permission required" in res_api.json().get("detail", "")

    # Student cannot access Flutter editor assets containing bundled answers
    res_static = client.get("/static/editor_next/flutter_editor/main.dart.js", **headers)
    assert res_static.status_code == 403

    # Student cannot request raw semantic, solvable or dsl files
    res_dsl = client.get("/static/generated/examples/day_01/001.semantic.json", **headers)
    assert res_dsl.status_code == 403


@override_settings(DEBUG=False)
def test_teacher_allowed_with_token_and_cookie(protection_env):
    client = Client()
    headers = {"HTTP_AUTHORIZATION": f"Token {protection_env['teacher_token']}"}

    # Teacher token can access editor API
    res_api = client.get("/api/editor/problems/", **headers)
    assert res_api.status_code == 200

    # Signed session cookie allows editor assets
    from django.http import HttpResponse
    resp = HttpResponse()
    resp.set_signed_cookie("modu_editor_session", protection_env["teacher_token"], salt="modu.editor.session.v1")
    client.cookies["modu_editor_session"] = resp.cookies["modu_editor_session"].value

    res_static = client.get("/static/editor_next/flutter_editor/main.dart.js")
    # Middleware allows it (returns static 404 or file, but not 401/403)
    assert res_static.status_code in {200, 404}


def test_student_bundle_verifier_catches_leaked_answers(tmp_path: Path):
    clean_dir = tmp_path / "clean"
    clean_dir.mkdir()
    (clean_dir / "main.dart.js").write_text("// clean", encoding="utf-8")
    (clean_dir / "assets").mkdir()
    (clean_dir / "assets" / "strings.json").write_text("{}", encoding="utf-8")

    assert verify_student_bundle(clean_dir) == []

    # Injecting private artifacts must trigger verification failure
    (clean_dir / "assets" / "sample.semantic.json").write_text("{}", encoding="utf-8")
    (clean_dir / "assets" / "problem.dsl.py").write_text("# dsl", encoding="utf-8")

    violations = verify_student_bundle(clean_dir)
    assert len(violations) == 2
    assert any(".semantic.json" in v for v in violations)
    assert any(".dsl.py" in v for v in violations)
