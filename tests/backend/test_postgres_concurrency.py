"""PostgreSQL concurrency tests for assignment submissions, retry limits, and submission keys."""

from __future__ import annotations

import threading
import uuid
import pytest
from django.db import connection, connections
from rest_framework.exceptions import ValidationError

from modu_math_web.learning.models import (
    Assignment,
    AssignmentItem,
    AssignmentRecipient,
    Attempt,
)
from modu_math_web.learning.services.assignments import (
    record_answer,
    submit_assignment,
)
from .test_learning_platform import env, make_assignment

pytestmark = [
    pytest.mark.django_db(transaction=True),
]


@pytest.fixture(autouse=True)
def require_postgresql():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL is required to verify row-level locking concurrency.")


def test_concurrent_identical_submission_key(env):
    """Multiple threads sending the exact same submission_key simultaneously.

    Must produce exactly 1 Attempt record, exactly 1 thread seeing created=True,
    and all threads safely returning the same Attempt instance without duplicates.
    """
    assignment = make_assignment(env, max_attempts=5)
    recipient = assignment.recipients.filter(student=env["students"][0]).first()
    student_user = env["students"][0].user
    item = assignment.items.first()

    shared_key = f"idempotent-key-{uuid.uuid4()}"
    num_threads = 8
    barrier = threading.Barrier(num_threads)
    results: list[tuple[bool, int]] = []
    errors: list[Exception] = []
    lock = threading.Lock()

    def worker():
        try:
            barrier.wait()
            _, attempt, created = record_answer(
                recipient.pk,
                student_user,
                {
                    "item_id": item.pk,
                    "answer": 10,
                    "submission_key": shared_key,
                    "elapsed_ms": 500,
                },
            )
            with lock:
                results.append((created, attempt.pk))
        except Exception as exc:
            with lock:
                errors.append(exc)
        finally:
            connections.close_all()

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Unexpected errors: {errors}"
    assert len(results) == num_threads

    created_counts = [r[0] for r in results]
    assert created_counts.count(True) == 1, "Exactly one thread must create the attempt"
    assert created_counts.count(False) == num_threads - 1

    attempt_ids = {r[1] for r in results}
    assert len(attempt_ids) == 1, "All threads must reference the identical attempt PK"

    db_attempts = Attempt.objects.filter(
        recipient=recipient, assignment_item=item, submission_key=shared_key
    )
    assert db_attempts.count() == 1


def test_concurrent_retry_limit(env):
    """Concurrent attempts exceeding max_attempts must be strictly bounded.

    When max_attempts is 2, 8 threads racing with unique submission keys must
    yield exactly 2 created attempts, and exactly 6 ValidationError rejections.
    """
    max_allowed = 2
    assignment = make_assignment(env, max_attempts=max_allowed)
    recipient = assignment.recipients.filter(student=env["students"][0]).first()
    student_user = env["students"][0].user
    item = assignment.items.first()

    num_threads = 8
    barrier = threading.Barrier(num_threads)
    successes: list[int] = []
    rejections: list[str] = []
    lock = threading.Lock()

    def worker(idx: int):
        unique_key = f"retry-key-{idx}-{uuid.uuid4()}"
        try:
            barrier.wait()
            _, attempt, created = record_answer(
                recipient.pk,
                student_user,
                {
                    "item_id": item.pk,
                    "answer": 10 + idx,
                    "submission_key": unique_key,
                    "elapsed_ms": 300,
                },
            )
            if created:
                with lock:
                    successes.append(attempt.pk)
        except ValidationError as exc:
            with lock:
                rejections.append(str(exc))
        finally:
            connections.close_all()

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(successes) == max_allowed, (
        f"Expected exactly {max_allowed} successes, got {len(successes)}"
    )
    assert len(rejections) == num_threads - max_allowed, (
        f"Expected {num_threads - max_allowed} rejections, got {len(rejections)}"
    )
    for err in rejections:
        assert "허용된 시도 횟수를 초과했습니다" in err

    db_attempts = Attempt.objects.filter(recipient=recipient, assignment_item=item)
    assert db_attempts.count() == max_allowed


def test_concurrent_answer_and_final_submit(env):
    """Racing an answer submission with final submission must serialize safely.

    Either:
    1) Answer commits first -> Final submit sees all items answered -> Final submit succeeds.
    2) Final submit executes first -> Sees incomplete items -> Rejects with ValidationError.
       Then answer commits -> subsequent submit succeeds.
    Under no circumstance can an attempt be created AFTER final submit has committed.
    """
    assignment = make_assignment(env, max_attempts=3)
    recipient = assignment.recipients.filter(student=env["students"][0]).first()
    student_user = env["students"][0].user
    items = list(assignment.items.order_by("position"))
    # The assignment has 10 items. Answer 0..8 so only the last item (9) is pending.
    for i in range(len(items) - 1):
        record_answer(
            recipient.pk,
            student_user,
            {
                "item_id": items[i].pk,
                "answer": 10 + i,
                "submission_key": f"pre-{i}-{uuid.uuid4()}",
            },
        )

    last_item = items[-1]
    barrier = threading.Barrier(2)
    submit_result: list[tuple[str, str]] = []
    answer_result: list[tuple[str, str]] = []

    def answer_worker():
        try:
            barrier.wait()
            _, attempt, created = record_answer(
                recipient.pk,
                student_user,
                {
                    "item_id": last_item.pk,
                    "answer": 19,
                    "submission_key": f"race-ans-{uuid.uuid4()}",
                },
            )
            answer_result.append(("success", str(attempt.pk)))
        except Exception as exc:
            answer_result.append(("error", str(exc)))
        finally:
            connections.close_all()

    def submit_worker():
        try:
            barrier.wait()
            sub = submit_assignment(recipient.pk, student_user)
            submit_result.append(("success", str(sub.submitted_at)))
        except Exception as exc:
            submit_result.append(("error", str(exc)))
        finally:
            connections.close_all()

    t1 = threading.Thread(target=answer_worker)
    t2 = threading.Thread(target=submit_worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Answer worker must always succeed because it was either before submit or submit failed
    assert answer_result[0][0] == "success"

    recipient.refresh_from_db()
    if submit_result[0][0] == "success":
        # Case 1: Answer ran first, then submit succeeded
        assert recipient.submitted_at is not None
    else:
        # Case 2: Submit ran first and saw missing answers
        assert "모든 문항의 답을 제출해 주세요" in submit_result[0][1]
        # Now submit should cleanly succeed since last item was recorded
        final_recipient = submit_assignment(recipient.pk, student_user)
        assert final_recipient.submitted_at is not None

    # After submission, any further answers must be cleanly blocked
    with pytest.raises(ValidationError, match="이미 제출한 과제입니다"):
        record_answer(
            recipient.pk,
            student_user,
            {
                "item_id": items[0].pk,
                "answer": 999,
                "submission_key": f"post-submit-{uuid.uuid4()}",
            },
        )


def test_concurrent_independent_students(env):
    """Submissions from distinct students must not block or deadlock each other."""
    assignment = make_assignment(env, max_attempts=5)
    item = assignment.items.first()
    students = env["students"]
    recipients = [
        assignment.recipients.filter(student=student).first()
        for student in students
    ]

    num_threads = 6
    barrier = threading.Barrier(num_threads)
    results = []
    lock = threading.Lock()

    def worker(student_idx: int, thread_idx: int):
        rec = recipients[student_idx]
        user = students[student_idx].user
        try:
            barrier.wait()
            _, attempt, created = record_answer(
                rec.pk,
                user,
                {
                    "item_id": item.pk,
                    "answer": 10 + thread_idx,
                    "submission_key": f"stud-{student_idx}-th-{thread_idx}-{uuid.uuid4()}",
                },
            )
            with lock:
                results.append((student_idx, attempt.pk, created))
        finally:
            connections.close_all()

    threads = []
    for i in range(num_threads):
        s_idx = i % 2
        threads.append(threading.Thread(target=worker, args=(s_idx, i)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == num_threads
    student0_attempts = Attempt.objects.filter(recipient=recipients[0])
    student1_attempts = Attempt.objects.filter(recipient=recipients[1])
    assert student0_attempts.count() == num_threads // 2
    assert student1_attempts.count() == num_threads // 2
