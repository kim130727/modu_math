"""Disposable browser-test fixture. Refuse to run against a user's database."""

import json
import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
import django

django.setup()
from django.core.management import call_command
from django.db import connection

root = Path(os.environ["MODU_BROWSER_TEST_ROOT"]).resolve()
if connection.vendor != "sqlite" or not Path(
    connection.settings_dict["NAME"]
).resolve().is_relative_to(root):
    raise RuntimeError("Browser fixtures require a disposable SQLite database")
call_command("migrate", interactive=False, verbosity=0)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    compile_problem_template_to_layout,
)
from modu_math.renderer.compiler import compile_renderer_json
from modu_math_web.learning.models import Problem, ProblemPublication, StudentProfile

teacher = get_user_model().objects.create_user(
    "browser_teacher", password="browser-teacher-password"
)
group, _ = Group.objects.get_or_create(name="modu_teachers")
teacher.groups.add(group)
for i in (1, 2):
    user = get_user_model().objects.create_user(
        f"browser_student_{i}", password="browser-student-password"
    )
    StudentProfile.objects.create(user=user, created_by=teacher)

directory = Path(os.environ["MODU_PROBLEMS_ROOT"]) / "ko" / "day_01"
directory.mkdir(parents=True)
for i in range(10):
    problem_id = f"browser_{i + 1:02d}"
    question = f"고구마 {10 + i}개와 {20 + i}개를 모았습니다. 모두 몇 개인가요?"
    semantic = {
        "problem_id": problem_id,
        "metadata": {"title": f"덧셈 연습 {i + 1:02d}", "question": question},
        "answer": {"value": 30 + 2 * i},
    }
    solvable = {
        "schema": "modu.solvable.v1.3",
        "problem_id": problem_id,
        "steps": [{"expr": f"{10 + i} + {20 + i}", "value": 30 + 2 * i}],
        "answer": semantic["answer"],
    }
    template = ProblemTemplate(
        id=problem_id,
        title=semantic["metadata"]["title"],
        canvas=Canvas(width=900, height=220),
        regions=(
            Region(
                id="stem",
                role="stem",
                slot_ids=("slot.question", "slot.expression", "slot.answer"),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                text=question,
                x=32,
                y=20,
                width=836,
                height=70,
                font_size=28,
            ),
            TextBoxSlot(
                id="slot.expression",
                text=f"{10 + i} + {20 + i} =",
                x=230,
                y=120,
                width=270,
                height=60,
                font_size=36,
            ),
            RectSlot(
                id="slot.answer",
                x=515,
                y=120,
                width=110,
                height=60,
                interaction={"type": "input", "role": "answer"},
            ),
        ),
    )
    layout = compile_problem_template_to_layout(template)
    renderer = compile_renderer_json(layout)
    problem = Problem.objects.create(
        problem_id=problem_id,
        grade=3,
        problem_type="addition",
        concepts=["addition"],
        catalog_data={
            "title": semantic["metadata"]["title"],
            "unit": "덧셈",
            "path": "examples/problems/ko/day_01",
        },
        answer=semantic["answer"],
        semantic_data=semantic,
        solvable_data=solvable,
        layout_data=layout,
        renderer_data=renderer,
    )
    ProblemPublication.objects.create(
        problem=problem, owner=teacher, source_path=f"ko/day_01/{problem_id}.dsl.py",
        status="published", visibility="public", allow_classroom_use=True,
        rights_confirmed=True,
    )
    # The real editor can open these sources, not just fixture API responses.
    source = "from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextBoxSlot\n"
    source += f"PROBLEM_TEMPLATE = {template!r}\nSEMANTIC_OVERRIDE = {semantic!r}\nSOLVABLE = {solvable!r}\n"
    (directory / f"{problem_id}.dsl.py").write_text(source, encoding="utf-8")
    for key, content in {
        "layout": layout,
        "renderer": renderer,
        "semantic": semantic,
        "solvable.v1.3": solvable,
    }.items():
        (directory / f"{problem_id}.{key}.json").write_text(
            json.dumps(content, ensure_ascii=False), encoding="utf-8"
        )
print("Disposable teacher browser fixtures ready")

if os.environ.get("MODU_BROWSER_STUDENT_ASSIGNMENT") == "1":
    from modu_math_web.learning.models import (
        Assignment,
        AssignmentRecipient,
        ProblemSet,
        ProblemSetItem,
    )
    from modu_math_web.learning.services.assignments import snapshot_item

    problem_set = ProblemSet.objects.create(owner=teacher, title="학생 브라우저 10문항")
    assignment = Assignment.objects.create(
        owner=teacher,
        problem_set=problem_set,
        source_version=1,
        title="학생 브라우저 10문항",
        max_attempts=1,
    )
    for position, problem in enumerate(Problem.objects.order_by("problem_id")):
        ProblemSetItem.objects.create(
            problem_set=problem_set, problem=problem, position=position
        )
        snapshot_item(assignment, problem, position)
    for student in StudentProfile.objects.all():
        AssignmentRecipient.objects.create(assignment=assignment, student=student)
