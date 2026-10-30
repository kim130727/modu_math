import base64

import pytest
from django.contrib.auth import get_user_model

from modu_math_web.learning.models import AssignmentProgress, Attempt
from modu_math_web.learning.services.assignment_content import input_schema
from .test_learning_platform import env, make_assignment

pytestmark = pytest.mark.django_db


def test_input_schema_does_not_identify_the_correct_choice(env):
    problem = env["problems"][0]
    problem.answer = {
        "value": "second",
        "answer_key": [{"id": "choice.2", "value": "second"}],
        "choices": [
            {"id": "choice.1", "text": "first", "correct": False},
            {"id": "choice.2", "text": "second", "correct": True},
        ],
    }
    schema = input_schema(problem)
    assert schema["fields"][0]["id"] == "field-1"
    assert schema["fields"][0]["choices"] == [
        {"label": "first", "value": "choice.1"},
        {"label": "second", "value": "choice.2"},
    ]
    assert "correct" not in str(schema)
    problem.answer = {
        "answer_key": [{"slot_id": "a", "value": 507}, {"slot_id": "b", "value": 999}]
    }
    assert len(input_schema(problem)["fields"]) == 2
    assert "507" not in str(input_schema(problem)) and "999" not in str(
        input_schema(problem)
    )


def test_hints_are_sequential_idempotent_and_counted_on_server(env):
    problem = env["problems"][0]
    problem.solvable_data = {
        "student_hints": [
            {"title": "첫 단계", "text": "일의 자리부터 더해 보세요."},
            {"text": "받아올림을 확인하세요."},
        ]
    }
    problem.save()
    assignment = make_assignment(env, max_attempts=2)
    item = assignment.items.first()
    client = env["client"]
    client.force_authenticate(env["students"][0].user)
    prefix = f"/api/v1/student/assignments/{assignment.pk}/"
    detail = client.get(prefix).data
    assert detail["can_work"] is True
    assert detail["items"][0]["hint_total"] == 2
    assert detail["items"][0]["revealed_hints"] == []
    assert (
        client.post(
            prefix + "hints/", {"item_id": item.pk, "level": 2}, format="json"
        ).status_code
        == 400
    )
    body = {"item_id": item.pk, "level": 1}
    assert client.post(prefix + "hints/", body, format="json").status_code == 200
    assert client.post(prefix + "hints/", body, format="json").status_code == 200
    assert AssignmentProgress.objects.get(item=item).hint_count == 1
    assert len(client.get(prefix).data["items"][0]["revealed_hints"]) == 1
    for number in [1, 2]:
        response = client.post(
            prefix + "answers/",
            {
                "item_id": item.pk,
                "answer": 10,
                "submission_key": f"hint-{number}",
                "hint_count": 999,
            },
            format="json",
        )
        assert response.status_code == 201
    assert list(Attempt.objects.values_list("hint_count", flat=True)) == [1, 1]
    client.force_authenticate(env["teacher"])
    recipients = client.get(f"/api/v1/assignments/{assignment.pk}/recipients/").data
    assert recipients[0]["hint_count"] == 1
    outsider = get_user_model().objects.create_user("hint-outsider")
    client.force_authenticate(outsider)
    assert client.post(prefix + "hints/", body, format="json").status_code == 404


def test_images_are_copied_into_the_assignment_before_source_changes(
    env, settings, tmp_path
):
    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko"
    directory.mkdir()
    image = directory / "figure.png"
    original = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a5bQAAAAASUVORK5CYII="
    )
    image.write_bytes(original)
    problem = env["problems"][0]
    problem.renderer_data = {
        "view_box": {"width": 100, "height": 100},
        "elements": [
            {
                "id": "picture",
                "type": "image",
                "attributes": {
                    "x": 0,
                    "y": 0,
                    "width": 100,
                    "height": 100,
                    "href": "figure.png",
                },
            }
        ],
    }
    problem.save()
    assignment = make_assignment(env)
    snapshot = assignment.items.first().public_content
    image.write_bytes(b"changed source")
    href = snapshot["renderer_data"]["elements"][0]["attributes"]["href"]
    assert href.startswith("data:image/png;base64,")
    assert base64.b64decode(href.split(",")[1]) == original
    env["client"].force_authenticate(env["students"][0].user)
    payload = env["client"].get(f"/api/v1/student/assignments/{assignment.pk}/").data
    assert (
        payload["items"][0]["content"]["renderer_data"]["elements"][0]["attributes"][
            "href"
        ]
        == href
    )


@pytest.mark.parametrize(
    "href", ["../secret.png", "https://outside.invalid/figure.png"]
)
def test_assignment_cannot_snapshot_external_or_escaping_assets(
    env, settings, tmp_path, href
):
    from rest_framework.exceptions import ValidationError
    from modu_math_web.learning.services.assignments import snapshot_item

    settings.PROBLEMS_ROOT = tmp_path
    assignment = make_assignment(env)
    problem = env["problems"][0]
    problem.renderer_data = {
        "elements": [{"type": "image", "attributes": {"href": href}}]
    }
    with pytest.raises(ValidationError):
        snapshot_item(assignment, problem, 99)


def test_multiple_selection_does_not_reveal_the_correct_selection_count(env):
    from modu_math_web.learning.models import answer_matches

    problem = env["problems"][0]
    problem.answer = {
        "choices": ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ"],
        "answer_key": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
        "target": {"type": "multiple_choice_set"},
    }
    fields = input_schema(problem)["fields"]
    assert len(fields) == 1 and fields[0]["type"] == "multi_choice"
    assert len(fields[0]["choices"]) == 6
    assert answer_matches(problem.answer, [4, 1, 3, 2])
    assert not answer_matches(problem.answer, [1, 1, 2, 3, 4])
    assert not answer_matches(problem.answer, [1, 2, 3])


@pytest.mark.parametrize(
    "svg,valid",
    [
        (
            '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10" fill="url(\'#color\')"/></svg>',
            True,
        ),
        ("<svg><script>alert(1)</script></svg>", False),
        ('<svg><image href="https://outside.invalid/a.png"/></svg>', False),
    ],
)
def test_svg_snapshots_are_self_contained(env, settings, tmp_path, svg, valid):
    from rest_framework.exceptions import ValidationError
    from modu_math_web.learning.services.assignments import snapshot_item

    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko"
    directory.mkdir()
    (directory / "figure.svg").write_text(svg)
    assignment = make_assignment(env)
    problem = env["problems"][0]
    problem.renderer_data = {
        "elements": [{"type": "image", "attributes": {"href": "figure.svg"}}]
    }
    if valid:
        snapshot = snapshot_item(assignment, problem, 99)
        assert snapshot.public_content["renderer_data"]["elements"][0]["attributes"][
            "href"
        ].startswith("data:image/svg+xml;base64,")
    else:
        with pytest.raises(ValidationError):
            snapshot_item(assignment, problem, 99)
