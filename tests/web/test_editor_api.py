from __future__ import annotations

import json
import os
from pathlib import Path

import django
import pytest
from django.conf import settings
from django.test import Client

from modu_math.layout.editor_overrides import apply_editor_overrides


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


def test_editor_index_uses_static_assets_without_inline_script(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)

    response = client.get("/editor/")

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert 'href="/static/editor/css/editor.css"' in html
    assert 'type="module" src="/static/editor/js/editor-app.js"' in html
    assert "<script>" not in html
    assert "<style>" not in html
    css_response = client.get("/static/editor/css/editor.css")
    assert css_response.status_code == 200
    assert b".ppt-shell" in b"".join(css_response.streaming_content)
    static_root = Path("src/modu_math_web/editor/static/editor")
    assert (static_root / "css" / "editor.css").exists()
    for name in [
        "editor-state.js",
        "editor-api.js",
        "editor-commands.js",
        "editor-canvas.js",
        "editor-properties.js",
        "editor-app.js",
    ]:
        assert (static_root / "js" / name).exists()

    canvas_js = (static_root / "js" / "editor-canvas.js").read_text(encoding="utf-8")
    assert "export function beginMarqueeBox" in canvas_js
    assert "export function updateMarqueeBox" in canvas_js
    assert "export function finishMarqueeBox" in canvas_js
    assert "export function capturePointer" in canvas_js
    assert "export function releasePointerCapture" in canvas_js
    assert "export function ensureDrawPreview" in canvas_js
    assert "export function removeDrawPreview" in canvas_js
    assert "export function formatPathPoint" in canvas_js
    assert "export function curvePathFromPoints" in canvas_js
    assert "export function freeformPathFromPoints" in canvas_js
    assert "export function drawPathFromState" in canvas_js
    assert "export function createDrawState" in canvas_js
    assert "export function updateDrawStatePoint" in canvas_js
    assert "export function editablePathFromD" in canvas_js
    assert "export function pathPointPatchFromHandle" in canvas_js
    assert "export function parsePolygonPoints" in canvas_js
    assert "export function formatPolygonPoints" in canvas_js
    assert "export function transformPathD" in canvas_js
    assert "export function shiftPathD" in canvas_js
    assert "export function scalePathD" in canvas_js
    assert "export function appendStrokeHitProxy" in canvas_js
    assert "export function appendTextHitProxy" in canvas_js
    assert "export function syncSlotHitProxies" in canvas_js
    assert "export function bindCanvasSlotInteractionEvents" in canvas_js
    assert "export function createSlotDragSnapshot" in canvas_js
    assert "export function scheduleDragFrame" in canvas_js
    assert "export function consumePendingDragDelta" in canvas_js
    assert "export function ensureSelectionOverlay" in canvas_js
    assert "export function updateSelectionOverlay" in canvas_js
    assert "export function translateSelectionOverlay" in canvas_js
    assert "export function renderTableAdjustmentHandles" in canvas_js
    assert "export function renderPathPointHandles" in canvas_js
    assert "export function adjustedBBox" in canvas_js
    assert "export function pointInRotatedFrame" in canvas_js
    assert "export function linePatchFromEndpoint" in canvas_js
    assert "export function linePatchFromRotation" in canvas_js
    assert "export function pointToSegmentDistance" in canvas_js


def test_editor_next_index_uses_separate_solid_assets(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)

    response = client.get("/editor-next/")

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert 'id="editor-next-root"' in html
    assert 'href="/static/editor_next/assets/editor-next.css' in html
    assert 'type="module" src="/static/editor_next/assets/editor-next.js' in html
    assert 'src="/static/editor/js/editor-app.js"' not in html
    assert 'href="/static/editor/css/editor.css"' not in html
    css_response = client.get("/static/editor_next/assets/editor-next.css")
    assert css_response.status_code == 200
    assert b".editor-next-shell" in b"".join(css_response.streaming_content)
    js_response = client.get("/static/editor_next/assets/editor-next.js")
    assert js_response.status_code == 200
    assert b"ModuMath Editor Next" in b"".join(js_response.streaming_content)


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
    assert "x=120.0" in updated
    assert "y=80.0" in updated
    assert "font_size=28" in updated


def test_layout_patch_removes_textslot_max_width(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import TextSlot

SLOTS = (
    TextSlot(id="slot.q1", text="A", x=10.0, y=20.0, font_size=12, max_width=30),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.q1",
                "op": "update",
                "value": {"x": 120.0, "max_width": None},
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
    assert "x=120.0" in updated
    assert "max_width" not in updated


def test_layout_patch_ignores_polygon_path_d_compat_field(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import PolygonSlot

SLOTS = (
    PolygonSlot(id="slot.poly", points=((0, 0), (10, 0), (0, 10)), stroke="#111111"),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.poly",
                "op": "update",
                "value": {
                    "points": [[1, 2], [11, 2], [1, 12]],
                    "d": "M 1 2 L 11 2 L 1 12 Z",
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
    assert "points=[[1, 2], [11, 2], [1, 12]]" in updated
    assert "d=\"M 1 2 L 11 2 L 1 12 Z\"" not in updated


def test_layout_patch_can_skip_formatting_for_fast_drag_save(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import TextSlot

SLOTS = (
    TextSlot(id="slot.q1", text="A", x=10.0, y=20.0, font_size=12),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    from modu_math_web.editor.services import dsl_patch

    def fail_format(_: str) -> str:
        raise AssertionError("formatter should be skipped")

    monkeypatch.setattr(dsl_patch, "format_dsl_source", fail_format)

    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(
            {
                "format": False,
                "patches": [
                    {
                        "target": "slot.q1",
                        "op": "update",
                        "value": {"x": 15.0, "y": 25.0},
                    }
                ],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "x = 15.0" in updated
    assert "y = 25.0" in updated


def test_layout_patch_reports_dsl_syntax_error_as_bad_request(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    _write_problem(
        tmp_path,
        "0001",
        """
from modu_math.dsl import TextSlot

SLOTS = (
    TextSlot(id="slot.q1", text="A", x=10.0, y=20.0, font_size=12),
)
00123
""".lstrip(),
    )

    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(
            {
                "patches": [
                    {
                        "target": "slot.q1",
                        "op": "update",
                        "value": {"x": 15.0},
                    }
                ],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["ok"] is False
    assert "DSL syntax error" in payload["error"]


def test_layout_patch_add_slot_falls_back_to_first_region_when_no_diagram_region(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(
        tmp_path,
        "0001",
        """
from modu_math.dsl import ProblemTemplate, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p",
    title="p",
    regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),),
    slots=(TextSlot(id="slot.q1", text="A", x=10, y=20, font_size=12),),
)
""".lstrip(),
    )

    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(
            {
                "patches": [
                    {
                        "target": "slot.editor_next.rect.1",
                        "op": "add",
                        "value": {
                            "kind": "rect",
                            "content": {
                                "x": 30,
                                "y": 40,
                                "width": 50,
                                "height": 60,
                                "fill": "none",
                                "stroke": "#111827",
                            },
                        },
                    }
                ],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "slot.editor_next.rect.1" in updated
    assert '"slot.q1", "slot.editor_next.rect.1"' in updated


def test_layout_patch_add_polygon_ignores_path_d_compat_field(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(
        tmp_path,
        "0001",
        """
from modu_math.dsl import Canvas, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p",
    title="p",
    canvas=Canvas(width=100, height=100),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),),
    slots=(),
)
""".lstrip(),
    )

    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(
            {
                "patches": [
                    {
                        "target": "slot.poly",
                        "op": "add",
                        "value": {
                            "kind": "polygon",
                            "region_id": "region.diagram",
                            "content": {
                                "points": [[1, 2], [11, 2], [1, 12]],
                                "d": "M 1 2 L 11 2 L 1 12 Z",
                                "stroke": "#111111",
                            },
                        },
                    }
                ]
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "PolygonSlot" in updated
    assert "points=[[1, 2], [11, 2], [1, 12]]" in updated
    assert "d=\"M 1 2 L 11 2 L 1 12 Z\"" not in updated


def test_build_endpoint_generates_artifacts_without_shell_script(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_build",
    title="build",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.stem", role="stem", slot_ids=("slot.q",)),),
    slots=(TextSlot(id="slot.q", text="2 + 3 = ?", x=20, y=40),),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    response = client.post("/api/editor/problems/0001/build/")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert "build_ok" in body["stdout"]
    assert (problem_dir / "problem.layout.json").exists()
    assert (problem_dir / "problem.renderer.json").exists()
    assert (problem_dir / "problem.svg").exists()


def test_build_endpoint_normalizes_solvable_plan_string(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_plan",
    title="build",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.stem", role="stem", slot_ids=("slot.q",)),),
    slots=(TextSlot(id="slot.q", text="2 + 3 = ?", x=20, y=40),),
)

SEMANTIC_OVERRIDE = {
    "problem_id": "p_plan",
    "answer": {"blanks": [], "choices": [], "answer_key": [], "value": 5, "unit": ""},
}

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": "p_plan",
    "problem_type": "addition",
    "inputs": {"target_label": "sum", "unit": ""},
    "given": [{"ref": "input.a", "value": 2}, {"ref": "input.b", "value": 3}],
    "target": {"ref": "answer.value", "type": "number"},
    "understanding": {
        "summary": "Find the total by adding two given numbers.",
        "facts": [
            {"ref": "input.a", "label": "first number", "value": 2, "unit": "", "source": "explicit"},
            {"ref": "input.b", "label": "second number", "value": 3, "unit": "", "source": "explicit"},
        ],
        "unknowns": [
            {"ref": "answer.value", "label": "sum", "unit": ""}
        ],
        "relation": {
            "type": "part_part_whole",
            "statement": "Add the two parts to get the whole.",
            "symbolic": "input.a + input.b = answer.value",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "What should we find?",
                "choices": ["first number", "second number", "sum"],
                "answer_index": 2,
            }
        ],
    },
    "method": "addition",
    "plan": "Add the two numbers.",
    "steps": [{"id": "step.1", "expr": "2 + 3", "value": 5}],
    "checks": [{"id": "check.1", "expr": "5 == 5", "expected": True, "actual": True, "pass": True}],
    "answer": {"blanks": [], "choices": [], "answer_key": [], "value": 5, "unit": ""},
}
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    response = client.post("/api/editor/problems/0001/build/")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    solvable = json.loads((problem_dir / "problem.solvable.v1.2.json").read_text(encoding="utf-8"))
    assert solvable["plan"] == ["Add the two numbers."]


def test_detail_rewrites_relative_svg_image_assets(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = "from modu_math.dsl import TextSlot\n"
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)
    (problem_dir / "local.png").write_bytes(b"png")
    (problem_dir / "problem.svg").write_text(
        '<svg><image href="local.png" /><image href="data:image/png;base64,AAA" /></svg>',
        encoding="utf-8",
    )

    response = client.get("/api/editor/problems/0001/")

    assert response.status_code == 200
    svg = response.json()["svg"]
    assert 'href="/api/editor/assets/0001/local.png"' in svg
    assert 'href="data:image/png;base64,AAA"' in svg


def test_problem_asset_serves_file_from_problem_folder(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(tmp_path, "0001", "from modu_math.dsl import TextSlot\n")
    (problem_dir / "local.png").write_bytes(b"png")

    response = client.get("/api/editor/assets/0001/local.png")

    assert response.status_code == 200
    assert b"".join(response.streaming_content) == b"png"


def test_layout_patch_updates_textboxslot_box_fields(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import TextBoxSlot

SLOTS = (
    TextBoxSlot(id="slot.tb", text="A", x=10.0, y=20.0, width=80.0, height=30.0, font_size=12),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.tb",
                "op": "update",
                "value": {"x": 12.0, "y": 24.0, "width": 120.0, "height": 48.0},
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
    assert "x=12.0" in updated
    assert "y=24.0" in updated
    assert "width=120.0" in updated
    assert "height=48.0" in updated


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
    assert "x=5.0" in updated
    assert "y=15.0" in updated
    assert "width=120.0" in updated
    assert "height=80.0" in updated


def test_layout_patch_adds_image_slot_and_import(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_image_add",
    title="image add",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),),
    slots=(TextSlot(id="slot.title", text="A"),),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.image_1",
                "op": "add",
                "value": {
                    "kind": "image",
                    "region_id": "region.diagram",
                    "content": {
                        "href": "data:image/png;base64,AAAA",
                        "x": 10.0,
                        "y": 20.0,
                        "width": 80.0,
                        "height": 60.0,
                        "preserve_aspect_ratio": "xMidYMid meet",
                    },
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
    assert "ImageSlot" in updated
    assert "ImageSlot(" in updated
    assert "slot.image_1" in updated
    assert "data:image/png;base64,AAAA" in updated
    namespace: dict[str, object] = {}
    exec(updated, namespace)


def test_layout_patch_add_clears_conflicting_deleted_slot_override(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_fraction_restore",
    title="fraction restore",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),),
    slots=(),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)
    overrides_path = problem_dir / "problem.editor_overrides.json"
    overrides_path.write_text(
        json.dumps({"deleted_slots": ["slot.math.fraction"], "version": 1}, ensure_ascii=False),
        encoding="utf-8",
    )

    payload = {
        "patches": [
            {
                "target": "slot.math.fraction.num",
                "op": "add",
                "value": {
                    "kind": "text",
                    "region_id": "region.diagram",
                    "content": {"text": "1", "x": 100.0, "y": 80.0, "font_size": 30},
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
    overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    assert "deleted_slots" not in overrides


def test_layout_patch_add_clears_stale_slot_override_for_same_target(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_image_restore",
    title="image restore",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),),
    slots=(),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)
    overrides_path = problem_dir / "problem.editor_overrides.json"
    overrides_path.write_text(
        json.dumps(
            {
                "slots": {
                    "slot.inserted.image.1": {
                        "href": "data:image/png;base64,OLD",
                        "x": 1,
                        "y": 2,
                    }
                },
                "version": 1,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    payload = {
        "patches": [
            {
                "target": "slot.inserted.image.1",
                "op": "add",
                "value": {
                    "kind": "image",
                    "region_id": "region.diagram",
                    "content": {
                        "href": "data:image/png;base64,NEW",
                        "x": 10.0,
                        "y": 20.0,
                        "width": 80.0,
                        "height": 60.0,
                    },
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
    assert "data:image/png;base64,NEW" in updated
    overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    assert "slots" not in overrides


def test_layout_patch_adds_table_slots_and_imports(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_table_add",
    title="table add",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),),
    slots=(),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.table.outer",
                "op": "add",
                "value": {
                    "kind": "rect",
                    "region_id": "region.diagram",
                    "content": {"x": 10.0, "y": 20.0, "width": 120.0, "height": 80.0},
                },
            },
            {
                "target": "slot.table.v1",
                "op": "add",
                "value": {
                    "kind": "line",
                    "region_id": "region.diagram",
                    "content": {"x1": 70.0, "y1": 20.0, "x2": 70.0, "y2": 100.0},
                },
            },
            {
                "target": "slot.table.r1c1",
                "op": "add",
                "value": {
                    "kind": "text",
                    "region_id": "region.diagram",
                    "content": {"text": "", "x": 20.0, "y": 45.0, "style_role": "table"},
                },
            },
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "RectSlot" in updated
    assert "LineSlot" in updated
    assert "TextSlot" in updated
    assert "slot.table.outer" in updated
    assert "slot.table.v1" in updated
    assert "slot.table.r1c1" in updated
    namespace: dict[str, object] = {}
    exec(updated, namespace)


def test_layout_patch_moves_table_group(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_table_move",
    title="table move",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.table.outer", "slot.table.v1", "slot.table.r1c1")),),
    slots=(
        RectSlot(id="slot.table.outer", prompt="", x=10.0, y=20.0, width=120.0, height=80.0),
        LineSlot(id="slot.table.v1", prompt="", x1=70.0, y1=20.0, x2=70.0, y2=100.0),
        TextSlot(id="slot.table.r1c1", prompt="", text="", x=20.0, y=45.0, style_role="table"),
    ),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.table",
                "op": "update",
                "value": {"move_dx": 5.0, "move_dy": -3.0},
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
    assert "x=(10.0) + (5.0)" in updated
    assert "y=(20.0) + (-3.0)" in updated
    assert "x1=(70.0) + (5.0)" in updated
    assert "y1=(20.0) + (-3.0)" in updated
    assert "x=(20.0) + (5.0)" in updated
    assert "y=(45.0) + (-3.0)" in updated


def test_layout_patch_moves_direct_path_slot_with_delta(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, PathSlot, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p_path_move",
    title="path move",
    canvas=Canvas(width=300, height=200),
    regions=(Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.path",)),),
    slots=(
        PathSlot(id="slot.path", prompt="", d="M 10 20 Q 30 40 50 60", fill="none", stroke="#111111"),
    ),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.path",
                "op": "update",
                "value": {"move_dx": 5.0, "move_dy": -3.0},
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
    assert 'd="M 15 17 Q 35 37 55 57"' in updated


def test_layout_patch_falls_back_to_editor_overrides_for_generated_slot(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import ProblemTemplate
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.generated.body",
                "op": "update",
                "value": {"x": 15.0, "y": 25.0, "width": 40.0, "height": 50.0},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    overrides = json.loads((problem_dir / "problem.editor_overrides.json").read_text(encoding="utf-8"))
    assert overrides["slots"]["slot.generated.body"] == {"x": 15.0, "y": 25.0, "width": 40.0, "height": 50.0}


def test_layout_patch_rejects_empty_dsl_before_saving_overrides(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(tmp_path, "0001", "")

    payload = {
        "patches": [
            {
                "target": "slot.q.num",
                "op": "delete",
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "DSL file is empty" in response.json()["error"]
    assert not (problem_dir / "problem.editor_overrides.json").exists()


def test_save_dsl_rejects_empty_dsl(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(tmp_path, "0001", "from modu_math.dsl import TextSlot\n")

    response = client.post(
        "/api/editor/problems/0001/dsl/",
        data=json.dumps({"dsl": "   \n"}),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "must not be empty" in response.json()["error"]
    assert (problem_dir / "problem.dsl.py").read_text(encoding="utf-8") == "from modu_math.dsl import TextSlot\n"


def test_save_dsl_formats_python_source(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(tmp_path, "0001", "VALUE=1\n")
    dsl = (
        "VALUE=Foo(alpha=1,beta=2,gamma=3,delta=4,epsilon=5,"
        "zeta=6,eta=7,theta=8,iota=9,kappa=10)\n"
    )

    response = client.post(
        "/api/editor/problems/0001/dsl/",
        data=json.dumps({"dsl": dsl}),
        content_type="application/json",
    )

    assert response.status_code == 200
    saved = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "VALUE = Foo(" in saved
    assert "alpha=1, beta=2" in saved
    assert response.json()["dsl"] == saved


def test_format_dsl_endpoint_formats_existing_source(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    problem_dir = _write_problem(
        tmp_path,
        "0001",
        "VALUE=Foo(alpha=1,beta=2,gamma=3,delta=4,epsilon=5,zeta=6,eta=7,theta=8,iota=9,kappa=10)\n",
    )

    response = client.post("/api/editor/problems/0001/dsl/format/")

    assert response.status_code == 200
    saved = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "VALUE = Foo(" in saved
    assert "iota=9, kappa=10" in saved
    assert response.json()["dsl"] == saved


def test_apply_editor_overrides_updates_layout_slot_content() -> None:
    layout = {
        "canvas": {"width": 100, "height": 100},
        "slots": [
            {"id": "slot.generated.body", "kind": "rect", "content": {"x": 1.0, "y": 2.0, "width": 3.0}},
            {"id": "slot.other", "kind": "text", "content": {"x": 9.0}},
        ],
    }
    overrides = {"slots": {"slot.generated.body": {"x": 15.0, "height": 50.0}}}

    apply_editor_overrides(layout, overrides)

    assert layout["slots"][0]["content"] == {"x": 15.0, "y": 2.0, "width": 3.0, "height": 50.0}
    assert layout["slots"][1]["content"] == {"x": 9.0}


def test_apply_editor_overrides_adds_missing_override_slot_to_matching_region() -> None:
    layout = {
        "regions": [
            {"id": "region.stem", "role": "stem", "slot_ids": ["slot.q.text"]},
            {"id": "region.choices", "role": "diagram", "slot_ids": ["slot.choice.box"]},
        ],
        "slots": [
            {"id": "slot.q.text", "kind": "text", "content": {"text": "Question"}},
            {"id": "slot.choice.box", "kind": "rect", "content": {"x": 1.0, "y": 2.0}},
        ],
        "reading_order": ["region.stem", "slot.q.text", "region.choices", "slot.choice.box"],
    }
    overrides = {"slots": {"slot.choice.a.text": {"text": "①", "x": 105.0, "y": 146.0, "font_size": 28}}}

    apply_editor_overrides(layout, overrides)

    added = next(slot for slot in layout["slots"] if slot["id"] == "slot.choice.a.text")
    assert added["kind"] == "text"
    assert added["content"]["text"] == "①"
    assert "slot.choice.a.text" in layout["regions"][1]["slot_ids"]
    assert layout["reading_order"][-1] == "slot.choice.a.text"


def test_layout_patch_delete_falls_back_to_editor_overrides(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import ProblemTemplate
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {"patches": [{"target": "slot.generated.body", "op": "delete"}]}
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    overrides = json.loads((problem_dir / "problem.editor_overrides.json").read_text(encoding="utf-8"))
    assert overrides["deleted_slots"] == ["slot.generated.body"]


def test_layout_patch_delete_accepts_renderer_element_id(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, Region

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p",
    canvas=Canvas(width=100, height=100),
    regions=(Region(id="region.diagram", role="diagram", slot_ids=("slot.editor_next.circle.1",)),),
    slots=(CircleSlot(id="slot.editor_next.circle.1", cx=20, cy=20, r=10),),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {"patches": [{"target": "slot.editor_next.circle.1.circle", "op": "delete"}]}
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "slot.editor_next.circle.1" not in updated


def test_apply_editor_overrides_removes_deleted_slots() -> None:
    layout = {
        "regions": [{"id": "region.diagram", "slot_ids": ["slot.keep", "slot.delete"]}],
        "slots": [
            {"id": "slot.keep", "kind": "rect", "content": {}},
            {"id": "slot.delete", "kind": "circle", "content": {}},
        ],
        "reading_order": ["region.diagram", "slot.keep", "slot.delete"],
    }
    overrides = {"deleted_slots": ["slot.delete"]}

    apply_editor_overrides(layout, overrides)

    assert [slot["id"] for slot in layout["slots"]] == ["slot.keep"]
    assert layout["regions"][0]["slot_ids"] == ["slot.keep"]
    assert layout["reading_order"] == ["region.diagram", "slot.keep"]


def test_apply_editor_overrides_removes_deleted_prefix_when_exact_slot_missing() -> None:
    layout = {
        "regions": [{"id": "region.stem", "slot_ids": ["slot.q.num", "slot.q.text", "slot.other"]}],
        "slots": [
            {"id": "slot.q.num", "kind": "text", "content": {"text": "81."}},
            {"id": "slot.q.text", "kind": "text", "content": {"text": "Question"}},
            {"id": "slot.other", "kind": "text", "content": {}},
        ],
        "reading_order": ["region.stem", "slot.q.num", "slot.q.text", "slot.other"],
    }
    overrides = {"deleted_slots": ["slot.q"]}

    apply_editor_overrides(layout, overrides)

    assert [slot["id"] for slot in layout["slots"]] == ["slot.other"]
    assert layout["regions"][0]["slot_ids"] == ["slot.other"]
    assert layout["reading_order"] == ["region.stem", "slot.other"]


def test_apply_editor_overrides_keeps_children_when_exact_deleted_slot_exists() -> None:
    layout = {
        "regions": [{"id": "region.stem", "slot_ids": ["slot.q", "slot.q.num"]}],
        "slots": [
            {"id": "slot.q", "kind": "text", "content": {}},
            {"id": "slot.q.num", "kind": "text", "content": {}},
        ],
        "reading_order": ["region.stem", "slot.q", "slot.q.num"],
    }
    overrides = {"deleted_slots": ["slot.q"]}

    apply_editor_overrides(layout, overrides)

    assert [slot["id"] for slot in layout["slots"]] == ["slot.q.num"]
    assert layout["regions"][0]["slot_ids"] == ["slot.q.num"]
    assert layout["reading_order"] == ["region.stem", "slot.q.num"]


def test_layout_patch_layer_order_falls_back_to_editor_overrides(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = "from modu_math.dsl import ProblemTemplate\n"
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "__layer__",
                "op": "layer",
                "value": {"region_id": "region.diagram", "slot_ids": ["slot.back", "slot.front"]},
            }
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    overrides = json.loads((problem_dir / "problem.editor_overrides.json").read_text(encoding="utf-8"))
    assert overrides["region_slot_orders"]["region.diagram"] == ["slot.back", "slot.front"]


def test_apply_editor_overrides_reorders_region_slots() -> None:
    layout = {
        "regions": [{"id": "region.diagram", "slot_ids": ["slot.a", "slot.b", "slot.c"]}],
        "slots": [{"id": "slot.a"}, {"id": "slot.b"}, {"id": "slot.c"}],
        "reading_order": ["region.diagram", "slot.a", "slot.b", "slot.c"],
    }
    overrides = {"region_slot_orders": {"region.diagram": ["slot.c", "slot.a", "slot.b"]}}

    apply_editor_overrides(layout, overrides)

    assert layout["regions"][0]["slot_ids"] == ["slot.c", "slot.a", "slot.b"]


def test_layout_patch_updates_opened_circle_helper_size(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import opened_circle_with_fold_slots

SLOTS = (
    *opened_circle_with_fold_slots("slot.opened", cx=612.0, cy=153.0, r=59.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.opened.paper",
                "op": "update",
                "value": {"cx": 620.0, "cy": 160.0, "r": 72.0},
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
    assert "cx=620.0" in updated
    assert "cy=160.0" in updated
    assert "r=72.0" in updated


def test_layout_patch_updates_folded_half_helper_size_from_path(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import folded_half_circle_slots

SLOTS = (
    *folded_half_circle_slots("slot.folded", cx=345.0, cy=153.0, r=59.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.folded.paper",
                "op": "update",
                "value": {"d": "M 280 150 C 290 220, 400 220, 420 150 L 280 150 Z"},
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
    assert "cx=350.0" in updated
    assert "cy=150.0" in updated
    assert "r=70.0" in updated


def test_layout_patch_overrides_folded_edge_generated_by_wrapper(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from dataclasses import replace

from modu_math.dsl import folded_half_circle_slots


def _folded_half_slots() -> tuple:
    slots = folded_half_circle_slots("slot.folded", cx=345.0, cy=153.0, r=59.0)
    return tuple(replace(slot, transform="rotate(180 345 153)") for slot in slots)


SLOTS = (*_folded_half_slots(),)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.folded.edge",
                "op": "update",
                "value": {
                    "d": "M 290 160 C 320 230, 390 225, 410 160",
                    "transform": "rotate(180 345 153)",
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
    assert 'slot.id == "slot.folded.edge"' in updated
    assert 'd="M 290 160 C 320 230, 390 225, 410 160"' in updated
    assert 'transform="rotate(180 345 153)"' in updated

    payload["patches"][0]["value"]["d"] = "M 300 170 C 330 240, 395 230, 420 170"
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert updated.count('slot.id == "slot.folded.edge"') == 1
    assert "M 300 170 C 330 240, 395 230, 420 170" in updated
    assert "M 290 160 C 320 230, 390 225, 410 160" not in updated


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
    assert 'transform="rotate(25 45 20)"' in updated


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
    assert 'person_slots("slot.figure.left", cx=220.0, head_cy=85.0)' in updated


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
    assert "character_body_slots(" in updated
    assert '"slot.person_left"' in updated
    assert "cx=(100.0) + (7.0)" in updated
    assert "head_cy=(70.0) + (11.0)" in updated
    assert "character_hand_slots(" in updated
    assert "card_x=(80.0) + (7.0)" in updated
    assert "card_y=(120.0) + (11.0)" in updated
    assert 'RectSlot(id="slot.card_left", x=(80.0) + (7.0), y=(120.0) + (11.0)' in updated


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
    assert '_base_ten_model("slot.figure.top", x=(100.0) + (15.0), y=(50.0) + (25.0)' in updated
    assert '_partition_box("slot.figure.group1", x=(200.0) + (-5.0), y=(150.0) + (10.0))' in updated


def test_layout_patch_moves_one_bar_model_bar(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import LineSlot, RectSlot

SLOTS = (
    RectSlot(id="slot.figure.bar_model_1.bar1.shade1", x=10.0, y=20.0, width=50, height=30),
    RectSlot(id="slot.figure.bar_model_1.bar1.outline", x=10.0, y=20.0, width=150, height=30, fill="none"),
    LineSlot(id="slot.figure.bar_model_1.bar1.div1", x1=60.0, y1=20.0, x2=60.0, y2=50.0),
    RectSlot(id="slot.figure.bar_model_1.bar2.shade1", x=10.0, y=70.0, width=50, height=30),
    RectSlot(id="slot.figure.bar_model_1.bar2.outline", x=10.0, y=70.0, width=150, height=30, fill="none"),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.figure.bar_model_1.bar1",
                "op": "update",
                "value": {"move_dx": 12.0, "move_dy": -5.0},
            },
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'id="slot.figure.bar_model_1.bar1.shade1"' in updated
    assert "x=(10.0) + (12.0)" in updated
    assert "y=(20.0) + (-5.0)" in updated
    assert 'id="slot.figure.bar_model_1.bar1.div1"' in updated
    assert "x1=(60.0) + (12.0)" in updated
    assert "y1=(20.0) + (-5.0)" in updated
    assert 'RectSlot(id="slot.figure.bar_model_1.bar2.shade1", x=10.0, y=70.0' in updated


def test_layout_patch_moves_one_tick_bar_row(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import LineSlot, TextSlot

SLOTS = (
    TextSlot(id="slot.figure.tick_bar_1.row1.label", text="9/7 m", x=10.0, y=20.0),
    LineSlot(id="slot.figure.tick_bar_1.row1.axis", x1=120.0, y1=30.0, x2=300.0, y2=30.0),
    LineSlot(id="slot.figure.tick_bar_1.row1.fill", x1=120.0, y1=30.0, x2=240.0, y2=30.0, stroke="#2563eb"),
    LineSlot(id="slot.figure.tick_bar_1.row1.tick0", x1=120.0, y1=20.0, x2=120.0, y2=40.0),
    TextSlot(id="slot.figure.tick_bar_1.row2.label", text="1 3/7 m", x=10.0, y=80.0),
    LineSlot(id="slot.figure.tick_bar_1.row2.axis", x1=120.0, y1=90.0, x2=300.0, y2=90.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {
                "target": "slot.figure.tick_bar_1.row1",
                "op": "update",
                "value": {"move_dx": 6.0, "move_dy": 8.0},
            },
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert 'id="slot.figure.tick_bar_1.row1.axis"' in updated
    assert "x1=(120.0) + (6.0)" in updated
    assert "y1=(30.0) + (8.0)" in updated
    assert 'TextSlot(id="slot.figure.tick_bar_1.row2.label", text="1 3/7 m", x=10.0, y=80.0)' in updated


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
    assert 'circle_fold_sequence_slots(' in updated
    assert '"slot.fold"' in updated
    assert "x=(40.0) + (12.0)" in updated
    assert "y=(245.0) + (-8.0)" in updated


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
    assert '_grid_slots("slot.grid", x=(100.0) + (11.0), y=(50.0) + (-7.0), step=30.0)' in updated
    assert '_candidate_slots(' in updated
    assert '"slot.pt.rieul"' in updated
    assert "origin_x=(140.0) + (-5.0)" in updated
    assert "origin_y=(80.0) + (13.0)" in updated


def test_layout_patch_moves_compass_on_ruler_helper(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import compass_on_ruler_slots

SLOTS = (
    *compass_on_ruler_slots(
        "slot.choice1",
        x=198.0,
        y=181.0,
        unit_width=30.0,
        needle_mark=0,
        pencil_mark=3,
    ),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {"target": "slot.choice1", "op": "update", "value": {"move_dx": 10.0, "move_dy": -5.0}},
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    updated = (problem_dir / "problem.dsl.py").read_text(encoding="utf-8")
    assert "x=(198.0) + (10.0)" in updated
    assert "y=(181.0) + (-5.0)" in updated


def test_layout_patch_rejects_compass_on_ruler_child_override(tmp_path: Path) -> None:
    client = _setup_django(tmp_path)
    dsl_text = """
from modu_math.dsl import compass_on_ruler_slots

SLOTS = (
    *compass_on_ruler_slots("slot.choice1", x=198.0, y=181.0, unit_width=30.0),
)
""".lstrip()
    problem_dir = _write_problem(tmp_path, "0001", dsl_text)

    payload = {
        "patches": [
            {"target": "slot.choice1.ruler.body", "op": "update", "value": {"x": 115.0, "y": 235.0}},
        ]
    }
    response = client.post(
        "/api/editor/problems/0001/layout-patch/",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert not (problem_dir / "problem.editor_overrides.json").exists()


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
    assert "SpeakerSpec(" in updated
    assert 'key="left"' in updated
    assert "cx=(245.0) + (7.0)" in updated
    assert "bubble_cy=(211.0) + (11.0)" in updated
    assert "head_cy=(322.0) + (11.0)" in updated
    assert "tail_y=(267.0) + (11.0)" in updated
    assert "name_y=394.0" in updated


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
    assert 'fill="#111111"' in updated


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
    assert "Canvas(width=180, height=160)" in updated
