from datetime import datetime, timedelta, timezone

from django.test import TestCase
from rest_framework.test import APIClient

from .store import store


class ApiContractTests(TestCase):
    def setUp(self):
        store.clear()
        self.client = APIClient()

    def _session(self):
        response = self.client.post(
            "/api/v1/auth/anonymous-session",
            {"deviceId": "device-1", "grade": 3, "displayName": "Student"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return response

    def test_anonymous_session_returns_student_and_token(self):
        response = self._session()

        self.assertEqual(response.data["student"]["grade"], 3)
        self.assertEqual(response.data["student"]["targetDailyCount"], 10)
        self.assertTrue(response.data["token"])
        self.assertTrue(response.data["expiresAt"].endswith("Z"))

    def test_learning_attempts_feed_summary_mastery_and_review_queue(self):
        self._session()
        answered_at = datetime.now(timezone.utc) - timedelta(days=2)

        response = self.client.post(
            "/api/v1/learning/attempts",
            {
                "problemId": "P001",
                "unit": "multiplication",
                "answer": "18",
                "isCorrect": False,
                "hintLevelUsed": 2,
                "timeSpentSeconds": 91,
                "errorCategory": "execution_calculation",
                "answeredAt": answered_at.isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["attempt"]["problemId"], "P001")
        self.assertEqual(response.data["reviewSchedule"]["interval"], "P1D")

        summary = self.client.get(
            f"/api/v1/learning/daily-summary?date={answered_at.date().isoformat()}"
        )
        self.assertEqual(summary.status_code, 200)
        self.assertEqual(summary.data["totalAttempted"], 1)
        self.assertEqual(summary.data["totalCorrect"], 0)

        masteries = self.client.get("/api/v1/learning/masteries")
        self.assertEqual(masteries.status_code, 200)
        self.assertEqual(masteries.data["masteries"][0]["unit"], "multiplication")

        review_queue = self.client.get("/api/v1/learning/review-queue")
        self.assertEqual(review_queue.status_code, 200)
        self.assertEqual(review_queue.data["items"][0]["problemId"], "P001")

    def test_tutor_proxy_requires_auth_and_returns_scaffold_message(self):
        unauthenticated = self.client.post(
            "/api/v1/tutor/messages",
            {"action": "hint"},
            format="json",
        )
        self.assertEqual(unauthenticated.status_code, 401)

        self._session()
        response = self.client.post(
            "/api/v1/tutor/messages",
            {
                "action": "hint",
                "hintLevel": 1,
                "problem": {
                    "id": "P001",
                    "grade": 3,
                    "subject": "math",
                    "unit": "multiplication",
                    "type": "word_problem",
                    "title": "Problem 1",
                    "prompt": "What is 6 times 4?",
                    "choices": ["18", "24", "30"],
                    "correctAnswer": "24",
                    "answerMap": {},
                    "semantic": {},
                    "solvable": {},
                },
                "messages": [],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"]["role"], "tutor")
        self.assertEqual(response.data["message"]["replyType"], "hint")
        self.assertNotIn("24", response.data["message"]["text"])
