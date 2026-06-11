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


def test_layout_patch_updates_transform_field(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import LineSlot

SLOTS = (
    LineSlot(id="slot.line", x1=10.0, y1=20.0, x2=80.0, y2=20.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.line",
                "op": "update",
                "value": {"transform": "rotate(25 45 20)"},
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
    assert "transform = 'rotate(25 45 20)'" in updated


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


def test_layout_patch_moves_card_character_group(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import RectSlot, TextSlot, character_body_slots, character_hand_slots

SLOTS = (
    *character_body_slots("slot.person_left", cx=100.0, head_cy=70.0, hair="#111", shirt="#eee"),
    RectSlot(id="slot.name_left_box", x=20.0, y=30.0, width=50.0, height=20.0),
    TextSlot(id="slot.name_left", text="A", x=25.0, y=45.0),
    RectSlot(id="slot.card_left", x=80.0, y=120.0, width=70.0, height=30.0),
    *character_hand_slots("slot.person_left", card_x=80.0, card_y=120.0, card_width=70.0),
    TextSlot(id="slot.card_left_text", text="1", x=90.0, y=140.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {"patches": [{"target": "slot.character.left", "op": "update", "value": {"move_dx": 7.0, "move_dy": 11.0}}]}
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'character_body_slots("slot.person_left", cx = (100.0) + (7.0), head_cy = (70.0) + (11.0)' in updated
    assert 'character_hand_slots("slot.person_left", card_x = (80.0) + (7.0), card_y = (120.0) + (11.0)' in updated
    assert 'RectSlot(id="slot.card_left", x = (80.0) + (7.0), y = (120.0) + (11.0)' in updated


def test_layout_patch_moves_base_ten_figure_helper(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import RectSlot

def _base_ten_model(slot_id: str, *, x: float, y: float, rods: int, ones: int):
    return (
        RectSlot(id=f"{slot_id}.rod.1.front", x=x, y=y, width=10, height=80),
    )

def _partition_box(slot_id: str, *, x: float, y: float):
    return (
        RectSlot(id=f"{slot_id}.box", x=x, y=y, width=80, height=100),
    )

SLOTS = (
    *_base_ten_model("slot.figure.top", x=100.0, y=50.0, rods=6, ones=9),
    *_partition_box("slot.figure.group1", x=200.0, y=150.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {"target": "slot.figure.top", "op": "update", "value": {"move_dx": 15.0, "move_dy": 25.0}},
            {"target": "slot.figure.group1", "op": "update", "value": {"move_dx": -5.0, "move_dy": 10.0}},
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert '_base_ten_model("slot.figure.top", x = (100.0) + (15.0), y = (50.0) + (25.0)' in updated
    assert '_partition_box("slot.figure.group1", x = (200.0) + (-5.0), y = (150.0) + (10.0))' in updated


def test_layout_patch_moves_circle_fold_sequence_helper(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import circle_fold_sequence_slots

SLOTS = (
    *circle_fold_sequence_slots("slot.fold", x=40.0, y=245.0, r=56.0, gap=105.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {"target": "slot.fold", "op": "update", "value": {"move_dx": 12.0, "move_dy": -8.0}},
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'circle_fold_sequence_slots("slot.fold", x = (40.0) + (12.0), y = (245.0) + (-8.0)' in updated


def test_layout_patch_moves_grid_and_candidate_helpers(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import CircleSlot, LineSlot, TextSlot

def _grid_slots(prefix: str, *, x: float, y: float, step: float = 30.0):
    return (
        LineSlot(id=f"{prefix}.v0", x1=x, y1=y, x2=x, y2=y + step),
    )

def _candidate_slots(prefix: str, *, origin_x: float, origin_y: float, step: float = 30.0):
    return (
        CircleSlot(id=f"{prefix}.point", cx=origin_x, cy=origin_y, r=4),
        TextSlot(id=f"{prefix}.label", text="ㄹ", x=origin_x + 8, y=origin_y + 18),
    )

SLOTS = (
    *_grid_slots("slot.grid", x=100.0, y=50.0, step=30.0),
    *_candidate_slots("slot.pt.rieul", origin_x=140.0, origin_y=80.0, step=30.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {"target": "slot.grid", "op": "update", "value": {"move_dx": 11.0, "move_dy": -7.0}},
            {"target": "slot.pt.rieul", "op": "update", "value": {"move_dx": -5.0, "move_dy": 13.0}},
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert '_grid_slots("slot.grid", x = (100.0) + (11.0), y = (50.0) + (-7.0), step=30.0)' in updated
    assert '_candidate_slots("slot.pt.rieul", origin_x = (140.0) + (-5.0), origin_y = (80.0) + (13.0), step=30.0)' in updated


def test_layout_patch_moves_speaker_character_group(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import SpeakerSpec

SPEAKERS = (
    SpeakerSpec(key="left", cx=245.0, bubble_cy=211.0, head_cy=322.0, text="A", name="B", hair="#111", shirt="#eee", tail_y=267.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {"patches": [{"target": "slot.character.left", "op": "update", "value": {"move_dx": 7.0, "move_dy": 11.0}}]}
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'SpeakerSpec(key="left", cx = (245.0) + (7.0), bubble_cy = (211.0) + (11.0), head_cy = (322.0) + (11.0)' in updated
    assert "tail_y = (267.0) + (11.0)" in updated
    assert "name_y = 394.0" in updated


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
