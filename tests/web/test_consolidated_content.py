import importlib.util
import json
from pathlib import Path
import threading
from urllib.request import urlopen
from http.server import ThreadingHTTPServer

import pytest

from modu_math.dsl.problem_store import document_path, section
from modu_math.dsl.variants import save_variant, snapshot, read_source, write_source
from modu_math_web.editor.services import artifact_cache, build
from modu_math_web.editor.services.problems import (
    invalidate_problem_list_cache, list_problem_directories, read_problem_detail,
    resolve_problem_paths,
)
from tools.consolidate_problem_json import consolidate
from tools.export_problem_content import export

SOURCE = '''from modu_math.dsl import Canvas, ProblemTemplate, TextSlot, Region
PROBLEM_TEMPLATE = ProblemTemplate(id="sample", title="한국어", canvas=Canvas(width=400, height=200),
    regions=(Region(id="region.main", role="prompt", slot_ids=("slot.q",)),),
    slots=(TextSlot(id="slot.q", text="문제", x=10, y=20, width=300, height=50),))
'''


@pytest.fixture
def content(tmp_path, settings):
    root = tmp_path / "problems"
    canonical = root / "ko" / "sample.dsl.py"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(SOURCE, encoding="utf-8")
    translated = root / "en" / "sample.dsl.py"
    translated.parent.mkdir()
    save_variant(translated, canonical, snapshot(SOURCE.replace("문제", "Question"), translated))
    settings.PROBLEMS_ROOT = root
    settings.GOLDEN_PROBLEMS_ROOT = tmp_path / "golden"
    invalidate_problem_list_cache()
    result = consolidate(root, delete=True)
    assert result["verified_renders"] == 2
    return root, canonical, translated


def test_one_authored_json_and_lazy_assets(content, client):
    root, canonical, translated = content
    assert sorted(path.name for path in root.rglob("*.json")) == ["sample.i18n.json"]
    assert len(list_problem_directories()) == 2
    detail = read_problem_detail("en/sample.dsl.py")
    assert "Question" in detail["svg"]
    assert not translated.exists()
    # Use the canonical URL returned by the editor, including its trailing slash.
    response = client.get(detail["svg_url"])
    assert response.status_code == 200
    assert b"Question" in response.content
    document = document_path(canonical).read_bytes()
    out = root.parent / "exported"
    assert export(root, out) == 2
    assert (out / "en" / "sample.renderer.json").exists()
    assert document_path(canonical).read_bytes() == document
    with pytest.raises(ValueError, match="outside"):
        export(root, root)


def test_cache_hit_invalidation_and_recovery(content, monkeypatch):
    root, canonical, translated = content
    paths = resolve_problem_paths("en/sample.dsl.py")
    ko = resolve_problem_paths("ko/sample.dsl.py")
    original = build.compile_problem_artifacts
    calls = []
    def counted(paths):
        calls.append(paths.problem_id)
        return original(paths)
    monkeypatch.setattr(build, "compile_problem_artifacts", counted)
    artifact_cache.get_artifacts(paths)
    assert calls == []
    ko_cache = artifact_cache.cache_path(ko).read_bytes()
    write_source(translated, read_source(translated).replace("Question", "Edited"))
    assert "Edited" in artifact_cache.get_artifacts(paths)["svg"]
    artifact_cache.get_artifacts(ko)
    assert calls == ["en/sample.dsl.py"]
    assert artifact_cache.cache_path(ko).read_bytes() == ko_cache
    canonical.write_text(SOURCE.replace("x=10", "x=70"), encoding="utf-8")
    assert artifact_cache.get_artifacts(paths)["layout"]["slots"][0]["content"]["x"] == 70
    artifact_cache.cache_path(paths).write_bytes(b"broken")
    assert "Edited" in artifact_cache.get_artifacts(paths)["svg"]
    assert len(calls) == 3


def test_editor_fast_save_uses_single_json(content):
    root, canonical, _ = content
    from modu_math_web.editor.services.dsl_patch import apply_layout_patches
    apply_layout_patches("en/sample.dsl.py", [
        {"target": "slot.q", "op": "update", "value": {"x": 77, "text": "Changed"}},
    ], fast_overrides=True)
    detail = read_problem_detail("en/sample.dsl.py")
    assert detail["layout"]["slots"][0]["content"]["x"] == 77
    assert "Changed" in detail["svg"]
    assert not list(root.rglob("*.editor_overrides.json"))
    assert not list(root.rglob("*.locale-delta.json"))
    assert canonical.read_text(encoding="utf-8") == SOURCE


def test_simultaneous_language_sections_preserved(content):
    _, canonical, translated = content
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(section(path, "editor_overrides").write_text, json.dumps({"version": 1, "canvas": {"width": width}}))
                   for path, width in ((canonical, 500), (translated, 600))]
        for future in futures:
            future.result()
    data = json.loads(document_path(canonical).read_text(encoding="utf-8"))
    assert data["editor_overrides"]["canvas"]["width"] == 500
    assert data["languages"]["en"]["editor_overrides"]["canvas"]["width"] == 600


def test_stale_same_language_save_is_rejected(content):
    _, _, translated = content
    first = section(translated, "editor_overrides")
    second = section(translated, "editor_overrides")
    first.read_text()
    second.read_text()
    first.write_text('{"version":1,"canvas":{"width":600}}')
    with pytest.raises(ValueError, match="concurrently"):
        second.write_text('{"version":1,"canvas":{"width":700}}')


def test_translation_tools_use_integrated_catalog(content):
    from tools.extract_dsl_localization import main as extract
    from tools.apply_dsl_localization import main as apply
    root, canonical, translated = content
    assert extract(["--dsl", str(canonical), "--locale", "en"]) == 0
    stored = section(translated, "translation_catalog")
    entries = json.loads(stored.read_text())
    entries["template.slots.slot.q.text"]["translation"] = "New translation"
    stored.write_text(json.dumps(entries, ensure_ascii=False))
    assert apply(["--dsl", str(canonical), "--locale", "en", "--locale-json", str(document_path(canonical)), "--force"]) == 0
    assert "New translation" in read_source(translated)
    assert len(list(root.rglob("*.json"))) == 1


def test_mobile_server_without_generated_json(content):
    root, _, _ = content
    script = Path(__file__).resolve().parents[2] / "apps/mobile/scripts/problem_dev_server.py"
    spec = importlib.util.spec_from_file_location("problem_dev_test", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ProblemDevHandler.root = root
    server = ThreadingHTTPServer(("127.0.0.1", 0), module.ProblemDevHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base + "/api/problems?locale=en") as response:
            assert len(json.load(response)["problems"]) == 1
        with urlopen(base + "/api/problem-bundle/sample?locale=en") as response:
            assert "Question" in json.load(response)["svg"]
        with urlopen(base + "/files/en/sample.renderer.json") as response:
            assert json.load(response)["elements"]
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.django_db
def test_learning_sync_renders_consolidated_source(content):
    from django.core.management import call_command
    from modu_math_web.learning.models import Problem
    root, _, _ = content
    call_command("sync_problems", root=root, verbosity=0)
    assert Problem.objects.count() == 2
    assert Problem.objects.get(problem_id="sample", language="en").renderer_data["elements"]
