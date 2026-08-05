from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AnonymousSessionSerializer,
    AttemptSerializer,
    TutorRequestSerializer,
)
from .store import Attempt, Student, store


def _token_from_request(request) -> str | None:
    header = request.headers.get("Authorization", "")
    prefix = "Bearer "
    if header.startswith(prefix):
        return header[len(prefix) :].strip()
    return None


def _require_student(request) -> Student | Response:
    student = store.student_for_token(_token_from_request(request))
    if student is None:
        return Response(
            {
                "error": {
                    "code": "unauthorized",
                    "message": "A valid bearer token is required.",
                    "fields": {},
                }
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return student


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class AnonymousSessionView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request):
        serializer = AnonymousSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        student = store.get_or_create_student(
            device_id=data["deviceId"],
            grade=data["grade"],
            display_name=data["displayName"] or "Student",
        )
        return Response(
            {
                "student": {
                    "id": student.id,
                    "grade": student.grade,
                    "displayName": student.display_name,
                    "targetDailyCount": student.target_daily_count,
                },
                "token": student.token,
                "expiresAt": _iso(student.expires_at),
            },
            status=status.HTTP_201_CREATED,
        )


class AttemptsView(APIView):
    def post(self, request):
        student = _require_student(request)
        if isinstance(student, Response):
            return student

        serializer = AttemptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attempt = store.record_attempt(student, serializer.validated_data)
        return Response(
            {
                "attempt": _attempt_response(attempt),
                "reviewSchedule": _review_schedule(attempt),
            },
            status=status.HTTP_201_CREATED,
        )


class DailySummaryView(APIView):
    def get(self, request):
        student = _require_student(request)
        if isinstance(student, Response):
            return student

        selected = _parse_date(request.query_params.get("date")) or date.today()
        start = datetime.combine(selected, time.min, tzinfo=timezone.utc)
        end = start + timedelta(days=1)
        attempts = [
            attempt
            for attempt in store.attempts_for(student)
            if start <= attempt.answered_at.astimezone(timezone.utc) < end
        ]
        attempted_problem_ids = {attempt.problem_id for attempt in attempts}
        correct_problem_ids = {
            attempt.problem_id for attempt in attempts if attempt.is_correct
        }
        total_attempted = len(attempted_problem_ids)
        total_correct = len(correct_problem_ids)
        return Response(
            {
                "date": selected.isoformat(),
                "totalAttempted": total_attempted,
                "totalCorrect": total_correct,
                "accuracy": 0 if total_attempted == 0 else total_correct / total_attempted,
                "streakDays": _streak_days(store.attempts_for(student), selected),
            }
        )


class MasteriesView(APIView):
    def get(self, request):
        student = _require_student(request)
        if isinstance(student, Response):
            return student

        grouped: dict[str, list[Attempt]] = {}
        for attempt in store.attempts_for(student):
            grouped.setdefault(attempt.unit, []).append(attempt)

        masteries = []
        for unit, attempts in sorted(grouped.items()):
            attempted = {attempt.problem_id for attempt in attempts}
            correct = {attempt.problem_id for attempt in attempts if attempt.is_correct}
            last_attempt = max(attempts, key=lambda item: item.answered_at)
            masteries.append(
                {
                    "unit": unit,
                    "totalAttempted": len(attempted),
                    "totalCorrect": len(correct),
                    "accuracy": 0 if not attempted else len(correct) / len(attempted),
                    "lastAttemptAt": _iso(last_attempt.answered_at),
                }
            )
        return Response({"masteries": masteries})


class ReviewQueueView(APIView):
    def get(self, request):
        student = _require_student(request)
        if isinstance(student, Response):
            return student

        now = datetime.now(timezone.utc)
        latest_by_problem: dict[str, Attempt] = {}
        for attempt in store.attempts_for(student):
            existing = latest_by_problem.get(attempt.problem_id)
            if existing is None or attempt.answered_at > existing.answered_at:
                latest_by_problem[attempt.problem_id] = attempt

        items = []
        for attempt in latest_by_problem.values():
            if attempt.is_correct:
                continue
            due_at = attempt.answered_at + timedelta(days=1)
            if due_at <= now:
                items.append(
                    {
                        "problemId": attempt.problem_id,
                        "unit": attempt.unit,
                        "lastAttemptId": attempt.id,
                        "lastAnsweredAt": _iso(attempt.answered_at),
                        "errorCategory": attempt.error_category,
                        "dueAt": _iso(due_at),
                    }
                )
        items.sort(key=lambda item: item["dueAt"])
        return Response({"items": items})


class TutorMessagesView(APIView):
    def post(self, request):
        student = _require_student(request)
        if isinstance(student, Response):
            return student

        serializer = TutorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        reply_type, text = _tutor_reply(data)
        return Response(
            {
                "message": {
                    "role": "tutor",
                    "text": text,
                    "replyType": reply_type,
                    "createdAt": _iso(datetime.now(timezone.utc)),
                },
                "moderation": {"filtered": False},
            }
        )


def _attempt_response(attempt: Attempt) -> dict[str, Any]:
    return {
        "id": attempt.id,
        "problemId": attempt.problem_id,
        "isCorrect": attempt.is_correct,
        "errorCategory": attempt.error_category,
        "answeredAt": _iso(attempt.answered_at),
    }


def _review_schedule(attempt: Attempt) -> dict[str, str] | None:
    if attempt.is_correct:
        return None
    due_at = attempt.answered_at + timedelta(days=1)
    return {"dueAt": _iso(due_at), "interval": "P1D"}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _streak_days(attempts: list[Attempt], selected: date) -> int:
    active_days = {
        attempt.answered_at.astimezone(timezone.utc).date() for attempt in attempts
    }
    streak = 0
    current = selected
    while current in active_days:
        streak += 1
        current -= timedelta(days=1)
    return streak


def _tutor_reply(data: dict[str, Any]) -> tuple[str, str]:
    action = data["action"]
    problem = data["problem"]
    unit = problem.get("unit") or "this concept"

    if action == "hint":
        level = data.get("hintLevel", 0)
        if level == 0:
            return "hint", "First, find exactly what the problem is asking for."
        if level == 1:
            return "hint", f"Connect the given numbers to {unit} before calculating."
        return "hint", "Choose one operation and check whether it matches the condition."

    if action == "next_question":
        return "question", "What condition should we check before doing the next step?"

    if action == "respond":
        return "question", "Good start. Which given value supports that idea?"

    return "retry", "Compare your answer with the condition once more before we finish."
