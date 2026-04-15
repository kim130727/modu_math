import json
from pathlib import Path

from modu_semantic import Problem, Rect
from modu_semantic.rag.indexer import build_and_write_index, build_index_entries, load_index_jsonl


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_build_rag_index_entries_and_jsonl(tmp_path: Path) -> None:
    root = tmp_path / "examples" / "problem"
    problem_dir = root / "p001"
    problem_dir.mkdir(parents=True)

    (problem_dir / "p001.py").write_text(
        "from modu_semantic import Problem, Rect\n\ndef build():\n    p=Problem(width=100,height=100,problem_id='p001')\n    p.add(Rect(id='r1',x=1,y=2,width=3,height=4))\n    return p\n",
        encoding="utf-8",
    )

    p = Problem(width=100, height=100, problem_id="p001", problem_type="demo")
    p.add(Rect(id="r1", x=1, y=2, width=3, height=4))
    p.save(problem_dir, include_layout_diff=False)

    semantic = json.loads((problem_dir / "json" / "semantic_final" / "semantic_final.json").read_text(encoding="utf-8"))
    _write_json(problem_dir / "output" / "json" / "p001.semantic.json", semantic)

    entries = build_index_entries(examples_root=root)
    assert len(entries) == 1

    entry = entries[0]
    assert entry["problem_id"] == "p001"
    assert entry["py_path"] == "p001/p001.py"
    assert entry["semantic_path"] == "p001/output/json/p001.semantic.json"
    assert "layout_path" not in entry
    assert entry["validation_passed"] is True
    assert isinstance(entry["visual_primitives"], list)

    index_path = tmp_path / "index.jsonl"
    build_and_write_index(examples_root=root, index_path=index_path)
    loaded = load_index_jsonl(index_path)
    assert len(loaded) == 1
    assert loaded[0]["problem_id"] == "p001"
