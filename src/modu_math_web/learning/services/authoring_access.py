"""Map file-backed editor sources to durable problem ownership."""

from uuid import uuid4

from django.db import transaction

from ..models import Problem, ProblemPublication
from .problem_access import is_admin


def source_key(paths):
    relative = paths.dsl_path.relative_to(paths.root_dir).as_posix()
    return f"{paths.root_alias}/{relative}" if paths.root_alias else relative


def source_publication(paths):
    key = source_key(paths)
    publication = ProblemPublication.objects.filter(source_path=key).first()
    if publication:
        return publication
    # Legacy entries may only have catalog directory + file prefix.
    for problem in Problem.objects.filter(
        problem_id=paths.artifact_base
    ).select_related("publication"):
        directory = str(
            problem.catalog_data.get("path") or f"examples/problems/{problem.language}"
        ).removeprefix("examples/problems/")
        if (
            paths.root_dir
            / directory
            / f"{problem.catalog_data.get('filePrefix') or problem.problem_id}.dsl.py"
        ).resolve() == paths.dsl_path.resolve():
            return getattr(problem, "publication", None)
    return None


def may_author(user, paths):
    if is_admin(user):
        return True
    publication = source_publication(paths)
    return bool(publication and publication.owner_id == user.pk)


def filter_authoring_rows(user, rows):
    if is_admin(user):
        return rows
    allowed = set()
    for publication in ProblemPublication.objects.filter(owner=user).select_related(
        "problem"
    ):
        key = publication.source_path
        if not key:
            problem = publication.problem
            directory = (
                str(
                    problem.catalog_data.get("path")
                    or f"examples/problems/{problem.language}"
                )
                .removeprefix("examples/problems/")
                .rstrip("/")
            )
            key = f"{directory}/{problem.catalog_data.get('filePrefix') or problem.problem_id}.dsl.py"
        allowed.add(key)
        if key.endswith("/problem.dsl.py"):
            allowed.add(key.removesuffix("/problem.dsl.py"))
    return [row for row in rows if row["problem_id"] in allowed]


@transaction.atomic
def register_source(user, paths, title=""):
    language = paths.dsl_path.relative_to(paths.root_dir).parts[0]
    if language not in {"ko", "uk", "en", "ja", "zh", "km"}:
        language = "ko"
    # Stable database id independent of teacher-entered folder/file names.
    problem = Problem.objects.create(
        problem_id=f"authored_{uuid4().hex}",
        language=language,
        answer={},
        catalog_data={
            "title": title or paths.artifact_base,
            "path": "examples/problems/"
            + paths.dsl_path.parent.relative_to(paths.root_dir).as_posix(),
            "filePrefix": paths.artifact_base,
        },
    )
    return ProblemPublication.objects.create(
        problem=problem, owner=user, source_path=source_key(paths)
    )


def sync_authored_artifacts(paths, artifacts):
    publication = (
        ProblemPublication.objects.filter(source_path=source_key(paths))
        .select_related("problem")
        .first()
    )
    if (
        not publication
        or not artifacts.get("semantic")
        or not artifacts.get("renderer")
    ):
        return
    problem = publication.problem
    semantic = artifacts["semantic"]
    metadata = semantic.get("metadata") or {}
    problem.semantic_data = semantic
    problem.answer = semantic.get("answer") or {}
    problem.solvable_data = artifacts.get("solvable") or {}
    problem.layout_data = artifacts.get("layout") or {}
    problem.renderer_data = artifacts["renderer"]
    problem.problem_type = semantic.get("problem_type") or ""
    problem.grade = metadata.get("grade") or problem.grade
    problem.concepts = metadata.get("concepts") or []
    problem.skills = metadata.get("skills") or []
    problem.catalog_data = {
        **problem.catalog_data,
        "title": metadata.get("title")
        or problem.catalog_data.get("title", problem.problem_id),
    }
    problem.save()
