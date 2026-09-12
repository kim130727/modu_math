from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from modu_math_web.learning.models import Attempt, Mastery, Problem, answer_matches


class AnswerMatchingTests(TestCase):
    def test_accepts_answer_value_and_choice_id(self):
        answer = {
            "value": "60 × 4",
            "choices": [
                {"id": "choice.1", "text": "6 × 4"},
                {"id": "choice.2", "text": "60 × 4"},
            ],
            "answer_key": [{"id": "choice.2", "value": "60 × 4"}],
        }
        self.assertTrue(answer_matches(answer, " 60 × 4 "))
        self.assertTrue(answer_matches(answer, {"choice_id": "choice.2"}))
        self.assertFalse(answer_matches(answer, "choice.1"))

    def test_accepts_ordered_multi_part_answers(self):
        self.assertTrue(
            answer_matches(
                {"value": "나 물병, 나 물병", "answer_key": ["나 물병", "나 물병"]},
                ["나 물병", "나 물병"],
            )
        )


class LearningApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.problem = Problem.objects.create(
            problem_id="sample-1",
            language="ko",
            grade=3,
            problem_type="choice",
            concepts=["곱셈", "수와 연산"],
            skills=["place_value"],
            answer={"value": 2, "answer_key": []},
            semantic_data={"problem_id": "sample-1", "answer": {"value": 2}},
        )

    def _authenticate(self):
        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "username": "student",
                "email": "student@example.com",
                "password": "strong-pass-123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")

    def test_public_problem_list_and_detail(self):
        response = self.client.get("/api/v1/problems/?language=ko&grade=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        detail = self.client.get(f"/api/v1/problems/{self.problem.pk}/")
        self.assertEqual(detail.data["semantic_data"]["problem_id"], "sample-1")

    def test_attempt_is_graded_by_server_and_updates_mastery(self):
        self._authenticate()
        response = self.client.post(
            "/api/v1/attempts/",
            {
                "problem": self.problem.pk,
                "submitted_answer": 2,
                "is_correct": False,
                "elapsed_ms": 1250,
                "hint_count": 1,
                "retry_count": 0,
                "events": [{"type": "answer_submitted", "at_ms": 1250}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["is_correct"])
        self.assertEqual(Attempt.objects.count(), 1)
        self.assertEqual(Mastery.objects.count(), 2)
        self.assertTrue(all(item.score == 1.0 for item in Mastery.objects.all()))

        response = self.client.post(
            "/api/v1/attempts/",
            {"problem": self.problem.pk, "submitted_answer": 1},
            format="json",
        )
        self.assertFalse(response.data["is_correct"])
        mastery = Mastery.objects.get(concept="곱셈")
        self.assertEqual(
            (mastery.attempt_count, mastery.correct_count, mastery.score), (2, 1, 0.5)
        )

    def test_login_returns_a_token(self):
        get_user_model().objects.create_user("existing", password="strong-pass-123")
        response = self.client.post(
            "/api/v1/auth/login/",
            {"username": "existing", "password": "strong-pass-123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])

    def test_attempts_require_authentication(self):
        response = self.client.get("/api/v1/attempts/")
        self.assertEqual(response.status_code, 401)

    def test_users_cannot_read_each_others_attempts_or_mastery(self):
        owner = get_user_model().objects.create_user(
            "owner", password="strong-pass-123"
        )
        Attempt.objects.create(user=owner, problem=self.problem, submitted_answer=2)
        self._authenticate()
        self.assertEqual(self.client.get("/api/v1/attempts/").data["count"], 0)
        self.assertEqual(self.client.get("/api/v1/masteries/").data["count"], 0)


class SyncProblemsTests(TestCase):
    @override_settings(PROBLEMS_ROOT=None)
    def test_sync_imports_existing_contracts_without_modifying_them(self):
        from django.conf import settings

        root = settings.BASE_DIR / "examples" / "problems"
        semantic_path = next((root / "ko").glob("*.semantic.json"))
        before = semantic_path.read_bytes()
        call_command("sync_problems", root=root, verbosity=0)
        self.assertEqual(Problem.objects.count(), 60)
        self.assertEqual(semantic_path.read_bytes(), before)
        imported = Problem.objects.get(
            problem_id=semantic_path.name.removesuffix(".semantic.json"), language="ko"
        )
        self.assertEqual(imported.semantic_data["problem_id"], imported.problem_id)
        self.assertTrue(imported.answer)
