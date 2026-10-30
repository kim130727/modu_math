"""Full end-to-end integration test:

Teacher assigns -> Two students solve -> Server grades -> Teacher checks results -> Wrong items reassigned -> Student re-solves.
"""

from __future__ import annotations

import uuid
import pytest
from rest_framework.test import APIClient

from modu_math_web.learning.models import (
    Assignment,
    AssignmentItem,
    AssignmentRecipient,
    Attempt,
)
from .test_learning_platform import env, make_assignment

pytestmark = pytest.mark.django_db


def test_full_assignment_lifecycle_two_students_and_reassign_wrong(env):
    teacher = env["teacher"]
    student_a_profile = env["students"][0]
    student_b_profile = env["students"][1]
    student_a_user = student_a_profile.user
    student_b_user = student_b_profile.user

    teacher_client = APIClient()
    teacher_client.force_authenticate(teacher)

    student_a_client = APIClient()
    student_a_client.force_authenticate(student_a_user)

    student_b_client = APIClient()
    student_b_client.force_authenticate(student_b_user)

    # 1. Teacher assigns a 10-item assignment to both students
    assignment = make_assignment(
        env,
        max_attempts=2,
        release_policy="after_submission",
    )
    assignment_id = assignment.pk
    items = list(assignment.items.order_by("position"))
    assert len(items) == 10

    # 2. Student A solves all 10 items correctly
    for idx, item in enumerate(items):
        correct_ans = item.answer["value"]
        res = student_a_client.post(
            f"/api/v1/student/assignments/{assignment_id}/answers/",
            {
                "item_id": item.pk,
                "answer": correct_ans,
                "submission_key": f"student-a-q{idx}-{uuid.uuid4()}",
                "elapsed_ms": 1000 + idx * 100,
            },
            format="json",
        )
        assert res.status_code == 201

    # Student A submits the assignment
    submit_res_a = student_a_client.post(
        f"/api/v1/student/assignments/{assignment_id}/submit/",
        {},
        format="json",
    )
    assert submit_res_a.status_code == 200

    # Student A inspects results (after_submission policy releases immediately upon submission)
    detail_a = student_a_client.get(f"/api/v1/student/assignments/{assignment_id}/").data
    assert detail_a["results_released"] is True
    assert detail_a["completed"] == 10
    assert detail_a["correct"] == 10
    assert detail_a["accuracy"] == 1.0
    assert detail_a["wrong_item_ids"] == []

    # 3. Student B solves: items 0..7 correct, items 8..9 wrong (exceeding 2 attempts)
    for idx in range(8):
        item = items[idx]
        res = student_b_client.post(
            f"/api/v1/student/assignments/{assignment_id}/answers/",
            {
                "item_id": item.pk,
                "answer": item.answer["value"],
                "submission_key": f"student-b-q{idx}-{uuid.uuid4()}",
                "elapsed_ms": 900,
            },
            format="json",
        )
        assert res.status_code == 201

    wrong_item_ids = []
    for idx in (8, 9):
        item = items[idx]
        wrong_item_ids.append(item.pk)
        wrong_ans = 99999 + idx

        # Attempt 1 (wrong)
        res1 = student_b_client.post(
            f"/api/v1/student/assignments/{assignment_id}/answers/",
            {
                "item_id": item.pk,
                "answer": wrong_ans,
                "submission_key": f"student-b-q{idx}-att1-{uuid.uuid4()}",
                "elapsed_ms": 1200,
            },
            format="json",
        )
        assert res1.status_code == 201

        # Attempt 2 (wrong again, reaching max_attempts = 2)
        res2 = student_b_client.post(
            f"/api/v1/student/assignments/{assignment_id}/answers/",
            {
                "item_id": item.pk,
                "answer": wrong_ans + 1,
                "submission_key": f"student-b-q{idx}-att2-{uuid.uuid4()}",
                "elapsed_ms": 1100,
            },
            format="json",
        )
        assert res2.status_code == 201

        # Attempt 3 (must be rejected)
        res3 = student_b_client.post(
            f"/api/v1/student/assignments/{assignment_id}/answers/",
            {
                "item_id": item.pk,
                "answer": wrong_ans + 2,
                "submission_key": f"student-b-q{idx}-att3-{uuid.uuid4()}",
            },
            format="json",
        )
        assert res3.status_code == 400
        assert "시도 횟수" in str(res3.data)

    # Student B submits
    submit_res_b = student_b_client.post(
        f"/api/v1/student/assignments/{assignment_id}/submit/",
        {},
        format="json",
    )
    assert submit_res_b.status_code == 200

    detail_b = student_b_client.get(f"/api/v1/student/assignments/{assignment_id}/").data
    assert detail_b["results_released"] is True
    assert detail_b["completed"] == 10
    assert detail_b["correct"] == 8
    assert detail_b["accuracy"] == 0.8
    assert set(detail_b["wrong_item_ids"]) == set(wrong_item_ids)

    # 4. Teacher reviews results for the assignment
    teacher_results = teacher_client.get(
        f"/api/v1/assignments/{assignment_id}/results/"
    ).data

    summary = teacher_results["assignment"]
    assert summary["recipient_count"] == 2
    assert summary["submitted_count"] == 2
    assert summary["accuracy"] == 0.9  # (10 + 8) / (10 * 2) = 0.9

    recipients_data = {r["student_id"]: r for r in teacher_results["recipients"]}

    rec_a = recipients_data[student_a_profile.pk]
    assert rec_a["accuracy"] == 1.0
    assert rec_a["correct"] == 10
    assert rec_a["wrong_item_ids"] == []

    rec_b = recipients_data[student_b_profile.pk]
    assert rec_b["accuracy"] == 0.8
    assert rec_b["correct"] == 8
    assert set(rec_b["wrong_item_ids"]) == set(wrong_item_ids)

    # 5. Teacher reassigns wrong items specifically for Student B
    reassign_res = teacher_client.post(
        f"/api/v1/assignments/{assignment_id}/reassign-wrong/",
        {
            "recipient_id": rec_b["recipient_id"],
            "title": "Student B 오답 클리닉 과제",
        },
        format="json",
    )
    assert reassign_res.status_code == 201
    reassigned_assignment_id = reassign_res.data["id"]

    # Verify newly created remediation assignment
    reassigned = Assignment.objects.get(pk=reassigned_assignment_id)
    assert reassigned.title == "Student B 오답 클리닉 과제"
    assert reassigned.items.count() == 2  # exactly the 2 wrong items
    assert reassigned.recipients.count() == 1
    assert reassigned.recipients.first().student == student_b_profile

    # Student A has no access to this remediation assignment
    detail_a_rem = student_a_client.get(f"/api/v1/student/assignments/{reassigned_assignment_id}/")
    assert detail_a_rem.status_code == 404

    # 6. Student B solves the reassigned wrong items and achieves 100%
    rem_detail_b = student_b_client.get(
        f"/api/v1/student/assignments/{reassigned_assignment_id}/"
    ).data
    assert rem_detail_b["total"] == 2
    assert rem_detail_b["can_work"] is True

    rem_items = rem_detail_b["items"]
    assert len(rem_items) == 2

    for r_item in rem_items:
        # Fetch the underlying item answer
        item_obj = AssignmentItem.objects.get(pk=r_item["id"])
        ans_res = student_b_client.post(
            f"/api/v1/student/assignments/{reassigned_assignment_id}/answers/",
            {
                "item_id": r_item["id"],
                "answer": item_obj.answer["value"],
                "submission_key": f"rem-ans-{r_item['id']}-{uuid.uuid4()}",
                "elapsed_ms": 1500,
            },
            format="json",
        )
        assert ans_res.status_code == 201

    # Student B submits remediation
    sub_rem = student_b_client.post(
        f"/api/v1/student/assignments/{reassigned_assignment_id}/submit/",
        {},
        format="json",
    )
    assert sub_rem.status_code == 200

    final_rem_detail = student_b_client.get(
        f"/api/v1/student/assignments/{reassigned_assignment_id}/"
    ).data
    assert final_rem_detail["completed"] == 2
    assert final_rem_detail["correct"] == 2
    assert final_rem_detail["accuracy"] == 1.0
    assert final_rem_detail["wrong_item_ids"] == []

    # Final check: Teacher sees Student B remediation 100%
    teacher_rem_res = teacher_client.get(
        f"/api/v1/assignments/{reassigned_assignment_id}/results/"
    ).data
    assert teacher_rem_res["assignment"]["submitted_count"] == 1
    assert teacher_rem_res["recipients"][0]["accuracy"] == 1.0
