from __future__ import annotations

from typing import Any

from django.db.models import Q

from modu_math.taxonomy import get_taxonomy_registry
from modu_math_web.learning.models import Attempt, Problem
from .diagnostics_service import DiagnosticService


class ProblemRecommendationService:
    def __init__(self, user: Any) -> None:
        self.user = user
        self.diagnostic_service = DiagnosticService(user)
        self.registry = get_taxonomy_registry()

    def get_recommendations(self, limit: int = 10, language: str = "ko") -> list[dict[str, Any]]:
        # Retrieve all candidate problems in the specified language
        candidates = list(
            Problem.objects.filter(language=language)
            .select_related("tagging")
            .order_by("id")
        )
        if not candidates:
            # Fallback to any language if requested not found
            candidates = list(Problem.objects.select_related("tagging").all())

        concept_metrics = {
            m["key"]: m
            for m in self.diagnostic_service.get_tag_diagnostics(tag_type="concept")
        }
        skill_metrics = {
            m["key"]: m
            for m in self.diagnostic_service.get_tag_diagnostics(tag_type="skill")
        }

        # Recent attempts by the user
        user_attempts = list(
            Attempt.objects.filter(user=self.user)
            .select_related("problem")
            .order_by("-created_at")[:20]
        )
        recently_solved_ids = {a.problem.problem_id for a in user_attempts[:5]}
        all_solved_ids = {a.problem.problem_id for a in user_attempts}

        # Recent incorrect problems
        recent_incorrect = [a for a in user_attempts if not a.is_correct][:3]
        recent_incorrect_concepts: set[str] = set()
        for inc in recent_incorrect:
            recent_incorrect_concepts.update(inc.problem.effective_concepts or inc.problem.concepts)

        ranked: list[tuple[int, int, Problem, str, dict[str, Any]]] = []

        for p in candidates:
            concepts = p.effective_concepts or p.concepts
            skills = p.effective_skills or p.skills

            # Find weakest concept and skill metric
            c_items = [concept_metrics.get(c) for c in concepts if c in concept_metrics]
            s_items = [skill_metrics.get(s) for s in skills if s in skill_metrics]

            weakest_concept = min(c_items, key=lambda x: x["score"]) if c_items else None
            high_hint_skill = next(
                (s for s in s_items if s["avg_hint_count"] >= 1.0 or s["avg_retry_count"] >= 1.0),
                None,
            )

            priority = 5
            reason = "기본 다지기를 위한 학습 추천 문제예요."
            ref_metric = weakest_concept or (s_items[0] if s_items else None)

            # Rule 1: Weak concept with sufficient history (attempts >= 2, score < 0.6)
            if weakest_concept and weakest_concept["attempt_count"] >= 2 and weakest_concept["score"] < 0.60:
                priority = 1
                reason = f"취약했던 '{weakest_concept['name_ko']}' 개념을 확실하게 보완하는 문제예요."

            # Rule 2: Skill with repeated hints / retries
            elif high_hint_skill and high_hint_skill["attempt_count"] >= 1:
                priority = 2
                reason = f"힌트나 재시도가 잦았던 '{high_hint_skill['name_ko']}' 역량을 스스로 해결해 보는 문제예요."

            # Rule 3: Related to recently incorrect problem
            elif any(c in recent_incorrect_concepts for c in concepts):
                priority = 3
                matched_c = next(c for c in concepts if c in recent_incorrect_concepts)
                c_name = self.registry.get_name_ko(matched_c)
                reason = f"최근 오답이 발생한 '{c_name}' 개념과 연결된 유사 연습 문제예요."

            # Rule 4: Concepts not practiced enough yet (unpracticed or attempt_count < 2)
            elif any(not concept_metrics.get(c) or concept_metrics[c]["attempt_count"] < 2 for c in concepts):
                priority = 4
                reason = "아직 충분히 풀어보지 않은 새로운 유형에 도전해 보세요."

            # Rule 5: Recently solved problems go to the lowest priority
            if p.problem_id in recently_solved_ids:
                priority = max(priority, 5)
                reason = "이미 최근에 해결한 문제예요. 복습을 위해 다시 풀어볼 수 있어요."

            # Score for sorting within the same priority: lower mastery score first, unattempted first
            tie_breaker = 100 if p.problem_id in all_solved_ids else 0
            if ref_metric:
                tie_breaker += int(ref_metric["score"] * 100)

            ranked.append((priority, tie_breaker, p, reason, ref_metric or {}))

        # Sort by (priority asc, tie_breaker asc)
        ranked.sort(key=lambda x: (x[0], x[1]))

        # Format output
        seen_problem_ids: set[str] = set()
        recommendations: list[dict[str, Any]] = []

        for priority, _, p, reason, ref_metric in ranked:
            if p.problem_id in seen_problem_ids:
                continue
            seen_problem_ids.add(p.problem_id)

            metadata = p.semantic_data.get("metadata", {}) if isinstance(p.semantic_data, dict) else {}
            title = metadata.get("title") or p.problem_id

            recommendations.append({
                "problem": {
                    "id": p.id,
                    "problem_id": p.problem_id,
                    "title": title,
                    "grade": p.grade,
                    "problem_type": p.problem_type,
                    "language": p.language,
                    "unit": metadata.get("unit") or "",
                    "domain": metadata.get("domain") or "",
                },
                "reason": reason,
                "concepts": [
                    {"key": c, "name_ko": self.registry.get_name_ko(c)}
                    for c in (p.effective_concepts or p.concepts)
                ],
                "skills": [
                    {"key": s, "name_ko": self.registry.get_name_ko(s)}
                    for s in (p.effective_skills or p.skills)
                ],
                "current_mastery": {
                    "score": ref_metric.get("score", 0.0),
                    "confidence": ref_metric.get("confidence", 0.0),
                    "status": ref_metric.get("status", "insufficient"),
                    "status_label": ref_metric.get("status_label", "기록 부족"),
                },
                "priority": priority,
            })

            if len(recommendations) >= limit:
                break

        return recommendations
