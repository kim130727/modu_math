from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from modu_math.taxonomy.tagger import ProblemAutoTagger
from modu_math_web.learning.models import Problem, ProblemTagging


class Command(BaseCommand):
    help = "Tag problems using explainable rule-based concept and skill extraction."

    def add_arguments(self, parser):
        parser.add_argument(
            "--problem-id",
            type=str,
            help="Tag only the specified problem ID.",
        )
        parser.add_argument(
            "--low-confidence",
            type=float,
            nargs="?",
            const=0.8,
            default=None,
            help="List problems with confidence strictly below the threshold (default: 0.8) without modifying them.",
        )
        parser.add_argument(
            "--overwrite-confirmed",
            action="store_true",
            help="Overwrite human-confirmed tags (default: false).",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        tagger = ProblemAutoTagger()
        low_confidence_threshold = options.get("low_confidence")
        problem_id_filter = options.get("problem_id")
        overwrite_confirmed = options.get("overwrite_confirmed", False)

        queryset = Problem.objects.select_related("tagging").all()
        if problem_id_filter:
            queryset = queryset.filter(problem_id=problem_id_filter)
            if not queryset.exists():
                self.stdout.write(
                    self.style.WARNING(f"Problem not found with id: {problem_id_filter}")
                )
                return

        # If --low-confidence is set, just list problems below threshold
        if low_confidence_threshold is not None:
            self.stdout.write(
                f"Scanning for problems with confidence < {low_confidence_threshold}..."
            )
            low_list = []
            for problem in queryset:
                tagging = getattr(problem, "tagging", None)
                if tagging:
                    conf = tagging.confidence
                else:
                    res = tagger.tag(
                        problem_id=problem.problem_id,
                        problem_type=problem.problem_type,
                        semantic_data=problem.semantic_data,
                        solvable_data=problem.solvable_data,
                        grade=problem.grade,
                        language=problem.language,
                    )
                    conf = res.confidence

                if conf < low_confidence_threshold:
                    low_list.append((problem.problem_id, problem.language, conf))

            self.stdout.write(f"Found {len(low_list)} problems with low confidence:")
            for pid, lang, conf in low_list:
                self.stdout.write(f"  - [{lang}] {pid}: confidence={conf:.2f}")
            return

        # Perform tagging
        tagged_count = 0
        skipped_confirmed_count = 0

        with transaction.atomic():
            for problem in queryset:
                existing_tagging = getattr(problem, "tagging", None)
                if (
                    existing_tagging
                    and existing_tagging.review_status == "confirmed"
                    and not overwrite_confirmed
                ):
                    skipped_confirmed_count += 1
                    continue

                res = tagger.tag(
                    problem_id=problem.problem_id,
                    problem_type=problem.problem_type,
                    semantic_data=problem.semantic_data,
                    solvable_data=problem.solvable_data,
                    grade=problem.grade,
                    language=problem.language,
                )

                tagging, _ = ProblemTagging.objects.update_or_create(
                    problem=problem,
                    defaults={
                        "auto_concepts": res.concepts,
                        "auto_skills": res.skills,
                        "rule_version": res.rule_version,
                        "source": res.source,
                        "confidence": res.confidence,
                        # If existing status was not confirmed, keep pending
                        "review_status": existing_tagging.review_status
                        if existing_tagging and existing_tagging.review_status != "pending"
                        else "pending",
                    },
                )
                tagged_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully tagged {tagged_count} problems "
                f"(skipped {skipped_confirmed_count} confirmed problems)."
            )
        )
