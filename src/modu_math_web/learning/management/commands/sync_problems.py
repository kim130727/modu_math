from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from modu_math_web.learning.models import Problem


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

        semantic_paths = sorted(root.glob("*/*.semantic.json"))
        for semantic_path in semantic_paths:
            language = semantic_path.parent.name
            prefix = semantic_path.name[: -len(".semantic.json")]
            semantic = _read_json(semantic_path)
            problem_id = str(semantic.get("problem_id") or prefix)
            metadata = (
                semantic.get("metadata")
                if isinstance(semantic.get("metadata"), dict)
                else {}
            )
            catalog = manifest_by_id.get(problem_id, {})

            solvable_candidates = sorted(
                semantic_path.parent.glob(f"{prefix}.solvable*.json")
            )
            solvable_path = solvable_candidates[-1] if solvable_candidates else None
            layout_path = semantic_path.parent / f"{prefix}.layout.json"
            renderer_path = semantic_path.parent / f"{prefix}.renderer.json"
            solvable = _read_json(solvable_path)
            artifact_paths = [semantic_path, layout_path, renderer_path]
            if solvable_path:
                artifact_paths.append(solvable_path)

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
                "layout_data": _read_json(layout_path),
                "renderer_data": _read_json(renderer_path),
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
            _, was_created = Problem.objects.update_or_create(
                problem_id=problem_id,
                language=language,
                defaults=defaults,
            )
            created += int(was_created)
            updated += int(not was_created)

        if options["dry_run"]:
            transaction.set_rollback(True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Problems synchronized: created={created}, updated={updated}, total={created + updated}"
                + (" (dry run)" if options["dry_run"] else "")
            )
        )
