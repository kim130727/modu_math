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
    django.setup()
    settings.PROBLEMS_ROOT = Path(os.environ["MODU_PROBLEMS_ROOT"])
    return Client()


def _write_problem(base: Path, problem_id: str, dsl: str) -> Path:
    p = base / "examples" / "problems" / problem_id
    p.mkdir(parents=True, exist_ok=True)
    (p / "problem.dsl.py").write_text(dsl, encoding="utf-8")
    return p


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
