from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from modu_math_web.learning.models import Attempt, Problem, ProblemTagging


class TaggingAndDiagnosticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "testpass123"
        self.user = get_user_model().objects.create_user(
            username="student_alice",
            email="alice@example.com",
            password=self.password,
        )
        self.other_user = get_user_model().objects.create_user(
            username="student_bob",
            email="bob@example.com",
            password=self.password,
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_user",
            email="admin@example.com",
            password=self.password,
        )

        # Create problems
        self.p_mult = Problem.objects.create(
            problem_id="p_mult_1",
            language="ko",
            grade=3,
            problem_type="multiple_choice_multiplication_place_value",
            concepts=["곱셈"],
            skills=["place_value_matching"],
            answer={"value": 1, "answer_key": []},
            semantic_data={
                "problem_id": "p_mult_1",
                "problem_type": "multiple_choice_multiplication_place_value",
                "metadata": {"unit": "곱셈", "title": "곱셈의 자릿값 알아보기"},
                "answer": {"value": 1},
            },
            solvable_data={"method": "place_value_matching"},
        )

        self.p_div = Problem.objects.create(
            problem_id="p_div_1",
            language="ko",
            grade=3,
            problem_type="multiple_choice_division",
            concepts=["나눗셈"],
            skills=["calculate"],
            answer={"value": 3, "answer_key": []},
            semantic_data={
                "problem_id": "p_div_1",
                "problem_type": "multiple_choice_division",
                "metadata": {"unit": "나눗셈", "title": "수 모형으로 나누기"},
                "answer": {"value": 3},
            },
            solvable_data={"method": "divide_models"},
        )

        self.p_circle = Problem.objects.create(
            problem_id="p_circle_1",
            language="ko",
            grade=3,
            problem_type="choice_selection",
            concepts=["원"],
            skills=["draw_figure"],
            answer={"value": "A", "answer_key": []},
            semantic_data={
                "problem_id": "p_circle_1",
                "problem_type": "choice_selection",
                "metadata": {"unit": "원", "title": "가장 큰 원 그리기"},
                "answer": {"value": "A"},
            },
            solvable_data={"method": "circle_radius"},
        )

    def _auth(self, user):
        login_res = self.client.post(
            "/api/v1/auth/login/",
            {"username": user.username, "password": self.password},
            format="json",
        )
        self.assertEqual(login_res.status_code, 200)
        token = login_res.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_auto_tagging_management_command(self):
        call_command("tag_problems")
        self.assertEqual(ProblemTagging.objects.count(), 3)

        tagging_mult = ProblemTagging.objects.get(problem=self.p_mult)
        self.assertIn("arithmetic.multiplication", tagging_mult.auto_concepts)
        self.assertIn("arithmetic.multiplication.place_value", tagging_mult.auto_concepts)
        self.assertIn("skill.place_value_matching", tagging_mult.auto_skills)
        self.assertEqual(tagging_mult.review_status, "pending")
        self.assertGreaterEqual(tagging_mult.confidence, 0.9)

        # Test confirmed tag preservation
        tagging_mult.review_status = "confirmed"
        tagging_mult.reviewed_concepts = ["arithmetic.multiplication.custom"]
        tagging_mult.save()

        call_command("tag_problems")
        tagging_mult.refresh_from_db()
        self.assertEqual(tagging_mult.reviewed_concepts, ["arithmetic.multiplication.custom"])
        self.assertEqual(tagging_mult.review_status, "confirmed")

    def test_admin_tagging_api_permissions_and_confirmation(self):
        call_command("tag_problems")
        tagging = ProblemTagging.objects.get(problem=self.p_mult)

        # Student cannot access admin tagging API
        self._auth(self.user)
        res = self.client.get(f"/api/v1/admin/problem-tags/{tagging.id}/")
        self.assertEqual(res.status_code, 403)

        # Admin can access and update
        self._auth(self.admin_user)
        res = self.client.get(f"/api/v1/admin/problem-tags/{tagging.id}/")
        self.assertEqual(res.status_code, 200)

        # Confirm tag action
        res = self.client.post(
            f"/api/v1/admin/problem-tags/{tagging.id}/confirm/",
            {
                "reviewed_concepts": ["arithmetic.multiplication", "arithmetic.multiplication.place_value"],
                "reviewed_skills": ["skill.place_value_matching"],
            },
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["review_status"], "confirmed")
        self.assertEqual(res.data["reviewed_by_username"], self.admin_user.username)

        self.p_mult.refresh_from_db()
        self.assertIn("arithmetic.multiplication.place_value", self.p_mult.concepts)

    def test_attempt_submission_with_session_and_server_grading(self):
        call_command("tag_problems")
        self._auth(self.user)

        # Submit attempt with problem_id string
        res = self.client.post(
            "/api/v1/attempts/",
            {
                "problem_id": "p_mult_1",
                "submitted_answer": 1,
                "elapsed_ms": 4500,
                "hint_count": 0,
                "retry_count": 0,
                "session_id": "sess_12345",
                "events": [{"type": "start", "time": 0}],
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.data["is_correct"])
        self.assertEqual(res.data["session_id"], "sess_12345")

        attempt = Attempt.objects.get(id=res.data["id"])
        self.assertEqual(attempt.user, self.user)
        self.assertEqual(attempt.problem, self.p_mult)

    def test_diagnostic_summary_concepts_and_skills_api(self):
        call_command("tag_problems")
        self._auth(self.user)

        # Submit 2 correct attempts on multiplication
        self.client.post(
            "/api/v1/attempts/",
            {"problem_id": "p_mult_1", "submitted_answer": 1, "hint_count": 0, "elapsed_ms": 3000},
            format="json",
        )
        self.client.post(
            "/api/v1/attempts/",
            {"problem_id": "p_mult_1", "submitted_answer": 1, "hint_count": 1, "elapsed_ms": 5000},
            format="json",
        )

        # Submit 1 incorrect attempt on division
        self.client.post(
            "/api/v1/attempts/",
            {"problem_id": "p_div_1", "submitted_answer": 99, "hint_count": 2, "elapsed_ms": 7000},
            format="json",
        )

        # Summary API
        res = self.client.get("/api/v1/diagnostics/summary/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["total_problems"], 2)
        self.assertEqual(res.data["total_attempts"], 3)
        self.assertAlmostEqual(res.data["accuracy"], 0.67, delta=0.01)
        self.assertGreater(res.data["avg_elapsed_ms"], 0)
        self.assertTrue(len(res.data["headline"]) > 0)

        # Concepts API
        res_concepts = self.client.get("/api/v1/diagnostics/concepts/")
        self.assertEqual(res_concepts.status_code, 200)
        mult_concept = next(
            (c for c in res_concepts.data if c["key"] == "arithmetic.multiplication"), None
        )
        self.assertIsNotNone(mult_concept)
        self.assertEqual(mult_concept["attempt_count"], 2)
        self.assertEqual(mult_concept["correct_count"], 2)
        self.assertGreater(mult_concept["score"], 0.6)

        # Skills API
        res_skills = self.client.get("/api/v1/diagnostics/skills/")
        self.assertEqual(res_skills.status_code, 200)
        calc_skill = next((s for s in res_skills.data if s["key"] == "skill.calculate"), None)
        self.assertIsNotNone(calc_skill)
        self.assertGreaterEqual(calc_skill["attempt_count"], 1)

        # History API
        res_history = self.client.get("/api/v1/diagnostics/history/")
        self.assertEqual(res_history.status_code, 200)
        self.assertEqual(len(res_history.data), 3)
        self.assertEqual(res_history.data[0]["problem_id"], "p_div_1")

    def test_recommendations_prioritize_weaknesses_and_unsolved(self):
        call_command("tag_problems")
        self._auth(self.user)

        # Fail division twice to create a weakness
        for _ in range(2):
            self.client.post(
                "/api/v1/attempts/",
                {"problem_id": "p_div_1", "submitted_answer": 999, "hint_count": 2},
                format="json",
            )

        # Recommendations API
        res = self.client.get("/api/v1/recommendations/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

        # Check structure
        rec1 = res.data[0]
        self.assertIn("problem", rec1)
        self.assertIn("reason", rec1)
        self.assertIn("concepts", rec1)
        self.assertIn("skills", rec1)
        self.assertIn("current_mastery", rec1)
        self.assertIn("priority", rec1)

    def test_user_data_isolation(self):
        call_command("tag_problems")

        # Alice solves p_mult_1
        self._auth(self.user)
        self.client.post(
            "/api/v1/attempts/",
            {"problem_id": "p_mult_1", "submitted_answer": 1},
            format="json",
        )

        # Bob logs in
        self._auth(self.other_user)

        # Bob should have 0 attempts and 0 problems in summary
        summary = self.client.get("/api/v1/diagnostics/summary/")
        self.assertEqual(summary.data["total_problems"], 0)
        self.assertEqual(summary.data["total_attempts"], 0)

        # Bob's history is empty
        history = self.client.get("/api/v1/diagnostics/history/")
        self.assertEqual(len(history.data), 0)

        # Unauthenticated request fails with 401
        self.client.credentials()  # clear auth
        self.assertEqual(self.client.get("/api/v1/diagnostics/summary/").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/diagnostics/concepts/").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/diagnostics/skills/").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/recommendations/").status_code, 401)
