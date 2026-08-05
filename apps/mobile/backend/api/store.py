from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import secrets
from typing import Any


@dataclass
class Student:
    id: str
    device_id: str
    grade: int
    display_name: str
    target_daily_count: int = 10
    token: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    expires_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )


@dataclass
class Attempt:
    id: str
    student_id: str
    problem_id: str
    unit: str
    answer: str
    is_correct: bool
    hint_level_used: int
    time_spent_seconds: int
    error_category: str
    answered_at: datetime


class LearningStore:
    def __init__(self):
        self.students_by_device: dict[str, Student] = {}
        self.students_by_token: dict[str, Student] = {}
        self.attempts: list[Attempt] = []

    def get_or_create_student(
        self,
        *,
        device_id: str,
        grade: int,
        display_name: str,
    ) -> Student:
        existing = self.students_by_device.get(device_id)
        if existing is not None:
            existing.grade = grade
            existing.display_name = display_name
            return existing

        student = Student(
            id=f"stu_{secrets.token_hex(8)}",
            device_id=device_id,
            grade=grade,
            display_name=display_name,
        )
        self.students_by_device[device_id] = student
        self.students_by_token[student.token] = student
        return student

    def student_for_token(self, token: str | None) -> Student | None:
        if not token:
            return None
        student = self.students_by_token.get(token)
        if student is None or student.expires_at <= datetime.now(timezone.utc):
            return None
        return student

    def record_attempt(self, student: Student, payload: dict[str, Any]) -> Attempt:
        attempt = Attempt(
            id=f"att_{secrets.token_hex(8)}",
            student_id=student.id,
            problem_id=payload["problem_id"],
            unit=payload["unit"],
            answer=payload["answer"],
            is_correct=payload["is_correct"],
            hint_level_used=payload["hint_level_used"],
            time_spent_seconds=payload["time_spent_seconds"],
            error_category=payload["error_category"],
            answered_at=payload["answered_at"],
        )
        self.attempts.append(attempt)
        return attempt

    def attempts_for(self, student: Student) -> list[Attempt]:
        return [attempt for attempt in self.attempts if attempt.student_id == student.id]

    def clear(self):
        self.students_by_device.clear()
        self.students_by_token.clear()
        self.attempts.clear()


store = LearningStore()
