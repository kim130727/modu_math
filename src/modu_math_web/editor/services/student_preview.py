"""Use the deployed student's presentation and grader without saving attempts."""
import hashlib
import json
from django.utils import timezone
from modu_math_web.learning.models import Problem
from modu_math_web.learning.services.assignments import student_problem
from modu_math_web.learning.services.assignment_content import freeze_images
from modu_math_web.learning.services.authoring_access import source_publication
from .problems import read_problem_detail, resolve_problem_paths


def saved_student_preview(problem_id):
    paths = resolve_problem_paths(problem_id)
    detail = read_problem_detail(problem_id)
    if not detail.get("semantic") or not detail.get("renderer"):
        raise ValueError("문제를 저장하고 화면 반영한 뒤 다시 열어주세요.")
    semantic = detail["semantic"]
    publication = source_publication(paths)
    problem = Problem(
        pk=0, problem_id=paths.artifact_base,
        language=paths.dsl_path.relative_to(paths.root_dir).parts[0],
        problem_type=semantic.get("problem_type", ""),
        answer=semantic.get("answer") or {},
        semantic_data=semantic, solvable_data=detail.get("solvable") or {},
        layout_data=detail.get("layout") or {}, renderer_data=detail["renderer"],
        catalog_data={"path": paths.dsl_path.parent.relative_to(paths.root_dir).as_posix()},
        updated_at=timezone.now(),
    )
    if publication:
        problem.publication = publication
    revision = hashlib.sha256(json.dumps(
        [problem.semantic_data, problem.solvable_data, problem.layout_data, problem.renderer_data],
        sort_keys=True, ensure_ascii=False,
    ).encode()).hexdigest()
    return problem, paths, revision


def preview_content(problem_id):
    problem, paths, revision = saved_student_preview(problem_id)
    content = freeze_images(student_problem(problem), problem, root=paths.root_dir)
    content["revision"] = revision
    return content
