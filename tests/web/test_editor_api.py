from __future__ import annotations

import json
import os
from pathlib import Path

import django
from django.conf import settings
from django.test import Client


def _setup_django(tmp_path: Path) -> Client:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
    os.environ["MODU_PROBLEMS_ROOT"] = str(tmp_path / "examples" / "problems")
    os.environ["MODU_GOLDEN_PROBLEMS_ROOT"] = str(tmp_path / "examples" / "golden")
    django.setup()
    settings.PROBLEMS_ROOT = Path(os.environ["MODU_PROBLEMS_ROOT"])
    settings.GOLDEN_PROBLEMS_ROOT = Path(os.environ["MODU_GOLDEN_PROBLEMS_ROOT"])
    return Client()


def _write_problem(base: Path, problem_id: str, dsl: str) -> Path:
    p = base / "examples" / "problems" / problem_id
    p.mkdir(parents=True, exist_ok=True)
    (p / "problem.dsl.py").write_text(dsl, encoding="utf-8")
    return p


def _write_golden_dsl(base: Path, problem_id: str, dsl: str) -> Path:
    p = base / "examples" / "golden"
    p.mkdir(parents=True, exist_ok=True)
    dsl_path = p / f"{problem_id}.dsl.py"
    dsl_path.write_text(dsl, encoding="utf-8")
    return dsl_path


def test_path_traversal_rejected(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    response = client.get("/api/editor/problems/..%2fsecret/")
    assert response.status_code in (400, 404)


def test_list_endpoint_includes_0001_if_present(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    _write_problem(tmp_path, "0001", "PROBLEM_TEMPLATE = None\n")
    response = client.get("/api/editor/problems/")
    assert response.status_code == 200
    body = response.json()
    ids = {p["problem_id"] for p in body["problems"]}
    assert "0001" in ids


def test_detail_reads_dsl_and_missing_artifact_is_null(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = "from modu_math.dsl import TextSlot\n"
    _write_problem(tmp_path, "0001", dsl_text)
    response = client.get("/api/editor/problems/0001/")
    assert response.status_code == 200
    body = response.json()
    assert body["dsl"] == dsl_text
    assert body["semantic"] is None
    assert body["solvable"] is None


def test_list_and_detail_include_golden_dsl_files(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = "from modu_math.dsl import TextSlot\n"
    _write_golden_dsl(tmp_path, "S3_초등_3_008540", dsl_text)

    response = client.get("/api/editor/problems/")
    assert response.status_code == 200
    body = response.json()
    ids = {p["problem_id"] for p in body["problems"]}
    assert "golden/S3_초등_3_008540.dsl.py" in ids

    detail = client.get("/api/editor/problems/golden/S3_초등_3_008540.dsl.py/")
    assert detail.status_code == 200
    assert detail.json()["dsl"] == dsl_text


def test_layout_patch_updates_textslot_fields(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import TextSlot

SLOTS = (
    TextSlot(id="slot.q1", text="A", x=10.0, y=20.0, font_size=12),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.q1",
                "op": "update",
                "value": {"x": 120.0, "y": 80.0, "font_size": 28},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "x = 120.0" in updated
    assert "y = 80.0" in updated
    assert "font_size = 28" in updated


def test_layout_patch_updates_rectslot_size_fields(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import RectSlot

SLOTS = (
    RectSlot(id="slot.box", x=10.0, y=20.0, width=30.0, height=40.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.box",
                "op": "update",
                "value": {"x": 5.0, "y": 15.0, "width": 120.0, "height": 80.0},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "x = 5.0" in updated
    assert "y = 15.0" in updated
    assert "width = 120.0" in updated
    assert "height = 80.0" in updated


def test_layout_patch_updates_person_slots_helper_anchor(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import CircleSlot

def person_slots(prefix: str, *, cx: float, head_cy: float):
    return (
        CircleSlot(id=f"{prefix}.head", cx=cx, cy=head_cy, r=28),
        CircleSlot(id=f"{prefix}.eye1", cx=cx - 8, cy=head_cy - 3, r=3.5),
    )

SLOTS = (
    *person_slots("slot.figure.left", cx=200.0, head_cy=70.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.figure.left.head",
                "op": "update",
                "value": {"cx": 220.0, "cy": 85.0, "r": 28},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'person_slots("slot.figure.left", cx = 220.0, head_cy = 85.0)' in updated


def test_layout_patch_adds_copied_slot_to_slots_and_region(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="0001",
    title="copy",
    canvas=Canvas(width=100, height=100),
    regions=(Region(id="region.main", role="diagram", flow="absolute", slot_ids=("slot.a",)),),
    slots=(TextSlot(id="slot.a", prompt="", text="A", x=10, y=20, font_size=12),),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.a.copy1",
                "op": "add",
                "value": {
                    "kind": "text",
                    "region_id": "region.main",
                    "content": {"text": "A", "x": 20, "y": 30, "font_size": 12, "fill": "#111111"},
                },
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "slot.a.copy1" in updated
    assert "TextSlot" in updated
    assert "fill = '#111111'" in updated


def test_layout_patch_updates_canvas_size(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate

PROBLEM_TEMPLATE = ProblemTemplate(
    id="0001",
    title="canvas",
    canvas=Canvas(width=100, height=120),
    regions=(),
    slots=(),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "__canvas__",
                "op": "update",
                "value": {"width": 180, "height": 160},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "Canvas(width = 180, height = 160)" in updated
