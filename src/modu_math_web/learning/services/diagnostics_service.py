from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q

from modu_math.taxonomy import get_taxonomy_registry
from modu_math_web.learning.models import Attempt, Problem

User = get_user_model()


class DiagnosticService:
    def __init__(self, user: Any) -> None:
        self.user = user
        self.registry = get_taxonomy_registry()

    def get_summary(self) -> dict[str, Any]:
        attempts_qs = Attempt.objects.filter(user=self.user).select_related("problem")
        total_attempts = attempts_qs.count()

        if total_attempts == 0:
            return {
                "total_problems": 0,
                "total_attempts": 0,
                "accuracy": 0.0,
                "avg_elapsed_ms": 0,
                "hint_rate": 0.0,
                "avg_retry_count": 0.0,
                "strengths": [],
                "weaknesses": [],
                "insufficient_data": [],
                "recent_trend": {
                    "direction": "insufficient",
                    "recent_accuracy": 0.0,
                    "message": "아직 풀이 기록이 없습니다. 첫 문제를 풀어보세요!",
                },
                "headline": "모두의 수학에 오신 것을 환영해요! 첫 문제를 풀어볼까요?",
            }

        total_problems = attempts_qs.values("problem__problem_id").distinct().count()
        correct_attempts = attempts_qs.filter(is_correct=True).count()
        accuracy = round(correct_attempts / total_attempts, 2)

        aggs = attempts_qs.aggregate(
            avg_elapsed=Avg("elapsed_ms"),
            avg_retry=Avg("retry_count"),
            hinted=Count("id", filter=Q(hint_count__gt=0)),
        )
        avg_elapsed_ms = int(aggs["avg_elapsed"] or 0)
        avg_retry_count = round(float(aggs["avg_retry"] or 0.0), 2)
        hint_rate = round((aggs["hinted"] or 0) / total_attempts, 2)

        # Concept masteries
        concept_diagnostics = self.get_tag_diagnostics(tag_type="concept")
        skill_diagnostics = self.get_tag_diagnostics(tag_type="skill")

        strengths = [
            item for item in concept_diagnostics
            if item["status"] == "stable" or (item["score"] >= 0.75 and item["attempt_count"] >= 2)
        ][:3]
        weaknesses = [
            item for item in concept_diagnostics
            if item["status"] == "needs_support" or (item["score"] < 0.60 and item["attempt_count"] >= 2)
        ][:3]
        insufficient = [
            item for item in concept_diagnostics
            if item["status"] == "insufficient" or item["attempt_count"] < 2
        ][:5]

        # Recent trend (last 5 vs previous 5)
        recent_5 = list(attempts_qs.order_by("-created_at")[:5])
        previous_5 = list(attempts_qs.order_by("-created_at")[5:10])

        recent_acc = (
            sum(1 for a in recent_5 if a.is_correct) / len(recent_5)
            if recent_5
            else 0.0
        )
        if len(previous_5) >= 3:
            prev_acc = sum(1 for a in previous_5 if a.is_correct) / len(previous_5)
            if recent_acc > prev_acc + 0.1:
                direction = "improving"
                trend_msg = "최근 정답률이 크게 오르고 있어요!"
            elif recent_acc < prev_acc - 0.1:
                direction = "declining"
                trend_msg = "최근 틀린 문제가 많았어요. 힌트를 꼼꼼히 확인해 보세요."
            else:
                direction = "stable"
                trend_msg = "안정적인 학습 실력을 유지하고 있어요."
        else:
            direction = "developing"
            trend_msg = f"최근 5문제 정답률 {int(recent_acc * 100)}%로 차근차근 실력을 쌓고 있어요."

        # Friendly headline
        if strengths:
            headline = f"'{strengths[0]['name_ko']}' 개념에 강점을 보이고 있어요!"
        elif weaknesses:
            headline = f"'{weaknesses[0]['name_ko']}' 개념을 조금 더 연습하면 실력이 쑥쑥 늘 거예요."
        else:
            headline = f"총 {total_problems}개 문제를 풀며 꾸준히 성장하고 있어요!"

        return {
            "total_problems": total_problems,
            "total_attempts": total_attempts,
            "accuracy": accuracy,
            "avg_elapsed_ms": avg_elapsed_ms,
            "hint_rate": hint_rate,
            "avg_retry_count": avg_retry_count,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "insufficient_data": insufficient,
            "recent_trend": {
                "direction": direction,
                "recent_accuracy": round(recent_acc, 2),
                "message": trend_msg,
            },
            "headline": headline,
        }

    def get_tag_diagnostics(self, tag_type: str = "concept") -> list[dict[str, Any]]:
        attempts_qs = (
            Attempt.objects.filter(user=self.user)
            .select_related("problem", "problem__tagging")
            .order_by("-created_at")
        )

        # Collect attempts by tag
        tag_attempts: dict[str, list[Attempt]] = {}
        for attempt in attempts_qs:
            problem = attempt.problem
            if tag_type == "concept":
                tags = problem.effective_concepts or problem.concepts
            else:
                tags = problem.effective_skills or problem.skills

            for tag in tags:
                tag_attempts.setdefault(str(tag), []).append(attempt)

        results: list[dict[str, Any]] = []

        # If user practiced specific tags, evaluate them
        for tag_key, attempts in tag_attempts.items():
            res = self._compute_tag_metric(tag_key, attempts, tag_type)
            results.append(res)

        # Also include registered tags that haven't been attempted yet as insufficient
        known_tags = self.registry.list_tags(tag_type)
        practiced_keys = set(tag_attempts.keys())
        for known in known_tags:
            if known.key not in practiced_keys and (known.parent_key is not None or known.type == "skill"):
                results.append({
                    "key": known.key,
                    "name_ko": known.name_ko,
                    "domain": known.domain,
                    "description": known.description,
                    "score": 0.0,
                    "raw_accuracy": 0.0,
                    "attempt_count": 0,
                    "correct_count": 0,
                    "confidence": 0.0,
                    "status": "insufficient",
                    "status_label": "기록 부족",
                    "status_message": "아직 풀이 기록이 없습니다.",
                    "avg_elapsed_ms": 0,
                    "avg_hint_count": 0.0,
                    "avg_retry_count": 0.0,
                })

        # Sort: first by attempt_count desc, then score desc
        results.sort(key=lambda item: (-item["attempt_count"], -item["score"]))
        return results

    def _compute_tag_metric(
        self, tag_key: str, attempts: list[Attempt], tag_type: str
    ) -> dict[str, Any]:
        n = len(attempts)
        correct_count = sum(1 for a in attempts if a.is_correct)
        raw_accuracy = correct_count / n if n > 0 else 0.0

        # Each attempt quality score q_i
        # Hint penalty: 0.15 per hint, max 0.45
        # Retry penalty: 0.10 per retry, max 0.30
        quality_sum = 0.0
        total_elapsed = 0
        total_hints = 0
        total_retries = 0

        for a in attempts:
            total_elapsed += a.elapsed_ms
            total_hints += a.hint_count
            total_retries += a.retry_count

            if a.is_correct:
                penalty = min(0.45, a.hint_count * 0.15) + min(0.30, a.retry_count * 0.10)
                quality = max(0.50, 1.0 - penalty)
                quality_sum += quality
            else:
                quality_sum += 0.0

        # Bayesian smoothing: prior M0=0.5, W=2.0
        w = 2.0
        m0 = 0.5
        score = (w * m0 + quality_sum) / (w + n)
        confidence = min(1.0, n / 5.0)

        # Status
        if n < 2:
            status = "insufficient"
            status_label = "기록 부족"
            status_msg = "충분한 진단을 위해 2문제 이상 풀어보세요."
        elif score >= 0.75 and confidence >= 0.6:
            status = "stable"
            status_label = "혼자서도 척척"
            status_msg = "개념을 깊이 이해하고 스스로 잘 해결해요."
        elif score < 0.55:
            status = "needs_support"
            status_label = "도움이 필요해요"
            status_msg = "힌트를 활용하여 기본 개념을 다시 점검해 보세요."
        else:
            status = "developing"
            status_label = "성장 중"
            status_msg = "조금씩 익숙해지고 있어요. 꾸준히 연습해 보세요."

        tag_obj = self.registry.get(tag_key)
        name_ko = tag_obj.name_ko if tag_obj else tag_key
        domain = tag_obj.domain if tag_obj else "수와 연산"
        desc = tag_obj.description if tag_obj else ""

        return {
            "key": tag_key,
            "name_ko": name_ko,
            "domain": domain,
            "description": desc,
            "score": round(score, 2),
            "raw_accuracy": round(raw_accuracy, 2),
            "attempt_count": n,
            "correct_count": correct_count,
            "confidence": round(confidence, 2),
            "status": status,
            "status_label": status_label,
            "status_message": status_msg,
            "avg_elapsed_ms": int(total_elapsed / n) if n > 0 else 0,
            "avg_hint_count": round(total_hints / n, 1) if n > 0 else 0.0,
            "avg_retry_count": round(total_retries / n, 1) if n > 0 else 0.0,
        }

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        attempts = (
            Attempt.objects.filter(user=self.user)
            .select_related("problem", "problem__tagging")
            .order_by("-created_at")[:limit]
        )

        history_list = []
        for a in attempts:
            concepts = a.problem.effective_concepts or a.problem.concepts
            skills = a.problem.effective_skills or a.problem.skills
            history_list.append({
                "id": a.id,
                "problem_id": a.problem.problem_id,
                "problem_title": a.problem.semantic_data.get("metadata", {}).get("title")
                or a.problem.problem_id,
                "language": a.problem.language,
                "grade": a.problem.grade,
                "is_correct": a.is_correct,
                "submitted_answer": a.submitted_answer,
                "elapsed_ms": a.elapsed_ms,
                "hint_count": a.hint_count,
                "retry_count": a.retry_count,
                "concepts": [self.registry.get_name_ko(c) for c in concepts],
                "skills": [self.registry.get_name_ko(s) for s in skills],
                "session_id": a.session_id,
                "created_at": a.created_at.isoformat(),
            })
        return history_list
