from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from modu_math_web.learning.models import Problem, ProblemPublication


def _read_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CommandError(f"Expected a JSON object in {path}")
    return data


def _unique_strings(values: list[Any]) -> list[str]:
    return list(
        dict.fromkeys(str(value).strip() for value in values if str(value).strip())
    )


class Command(BaseCommand):
    help = (
        "Synchronize existing examples/problems JSON artifacts into the Problem table."
    )

    def add_arguments(self, parser):
        parser.add_argument("--root", type=Path, default=settings.PROBLEMS_ROOT)
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument(
            "--new-status",
            choices=("draft", "review", "published", "archived"),
            default="draft",
            help="State of new imports; existing review states are preserved.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        root = options["root"].resolve()
        if not root.is_dir():
            raise CommandError(f"Problems root does not exist: {root}")

        manifest = _read_json(root / "manifest.json")
        manifest_by_id = {
            str(item.get("id")): item
            for item in manifest.get("problems", [])
            if isinstance(item, dict) and item.get("id")
        }
        created = updated = 0
        synced_keys: set[tuple[str, str]] = set()

        from modu_math_web.editor.services.content_store import (
            list_content,
            read_content,
            source_files,
        )

        for paths in list_content(root):
            language = paths.dsl_path.relative_to(root).parts[0]
            prefix = paths.artifact_base
            bundle = read_content(paths)
            semantic = dict(bundle.get("semantic") or {})
            problem_id = prefix
            semantic["problem_id"] = problem_id
            synced_keys.add((problem_id, language))
            metadata = (
                semantic.get("metadata")
                if isinstance(semantic.get("metadata"), dict)
                else {}
            )
            catalog = dict(manifest_by_id.get(problem_id, {}))
            if not catalog:
                text = (
                    str(metadata.get("title", ""))
                    + " "
                    + str(metadata.get("question", ""))
                    + " "
                    + str(metadata.get("instruction", ""))
                    + " "
                    + str(semantic.get("problem_type", ""))
                )
                if any(
                    k in text
                    for k in ["원", "circle", "지름", "반지름", "중심", "컴퍼스"]
                ):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "2학기",
                        3,
                        "원",
                    )
                elif any(k in text for k in ["들이", "무게", "capacity", "weight"]):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "2학기",
                        5,
                        "들이와 무게",
                    )
                elif any(k in text for k in ["분수", "소수", "fraction"]):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "1학기",
                        6,
                        "분수와 소수",
                    )
                elif any(k in text for k in ["곱셈", "multiplication"]):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "1학기",
                        4,
                        "곱셈",
                    )
                elif any(k in text for k in ["나눗셈", "division"]):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "1학기",
                        3,
                        "나눗셈",
                    )
                elif any(
                    k in text for k in ["평면도형", "직각", "선분", "반직선", "직선"]
                ):
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "1학기",
                        2,
                        "평면도형",
                    )
                else:
                    default_grade, default_sem, default_unit_num, default_topic = (
                        3,
                        "1학기",
                        1,
                        "덧셈과 뺄셈",
                    )

                unit_topic = str(
                    metadata.get("unitTopic") or metadata.get("unit") or default_topic
                )
                sub_unit = str(
                    metadata.get("subUnit")
                    or metadata.get("subTopic")
                    or metadata.get("topic")
                    or "기본 학습"
                )
                catalog = {
                    "id": problem_id,
                    "grade": metadata.get("grade") or default_grade,
                    "subject": "math",
                    "unit": unit_topic,
                    "unitTopic": unit_topic,
                    "subUnit": sub_unit,
                    "topic": sub_unit,
                    "semester": str(metadata.get("semester") or default_sem),
                    "unitNumber": int(metadata.get("unitNumber") or default_unit_num),
                    "filePrefix": problem_id,
                }

            solvable = bundle.get("solvable") or {}
            artifact_paths = source_files(paths)

            concepts = _unique_strings(
                list(metadata.get("concepts", []))
                + list(metadata.get("tags", []))
                + [
                    catalog.get("domain", ""),
                    catalog.get("unit", ""),
                    catalog.get("topic", ""),
                ]
            )
            skills = _unique_strings(
                list(metadata.get("skills", []))
                + list(solvable.get("skills", []))
                + [solvable.get("method", "")]
            )
            grade = catalog.get("grade")
            if grade is None:
                grade = metadata.get("grade")

            defaults = {
                "grade": int(grade) if grade not in (None, "") else None,
                "problem_type": str(
                    semantic.get("problem_type") or catalog.get("problemType") or ""
                ),
                "concepts": concepts,
                "skills": skills,
                "catalog_data": catalog,
                "answer": (
                    semantic.get("answer")
                    if isinstance(semantic.get("answer"), dict)
                    else {}
                ),
                "semantic_data": semantic,
                "solvable_data": solvable,
                "layout_data": bundle.get("layout") or {},
                "renderer_data": bundle.get("renderer") or {},
                "source_updated_at": datetime.fromtimestamp(
                    max(
                        path.stat().st_mtime for path in artifact_paths if path.exists()
                    ),
                    tz=timezone.utc,
                ),
            }
            if options["dry_run"]:
                exists = Problem.objects.filter(
                    problem_id=problem_id, language=language
                ).exists()
                updated += int(exists)
                created += int(not exists)
                continue
            problem, was_created = Problem.objects.update_or_create(
                problem_id=problem_id,
                language=language,
                defaults=defaults,
            )
            if was_created:
                ProblemPublication.objects.create(
                    problem=problem, status=options["new_status"]
                )
            created += int(was_created)
            updated += int(not was_created)

        # Partial imports/renamed sources must not delete learning history.
        # Retire records explicitly through ProblemPublication instead.

        if options["dry_run"]:
            transaction.set_rollback(True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Problems synchronized: created={created}, updated={updated}, total={created + updated}"
                + (" (dry run)" if options["dry_run"] else "")
            )
        )
