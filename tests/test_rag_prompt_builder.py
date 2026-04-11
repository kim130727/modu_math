import json
from pathlib import Path

from modu_semantic.rag.prompt_builder import build_few_shot_prompt


def test_prompt_builder_includes_examples_and_paths(tmp_path: Path) -> None:
    root = tmp_path / "examples" / "problem"
    problem_dir = root / "p100"
    problem_dir.mkdir(parents=True)

    py_rel = "p100/p100.py"
    semantic_rel = "p100/output/json/p100.semantic.json"

    (root / py_rel).parent.mkdir(parents=True, exist_ok=True)
    (root / py_rel).write_text("def build():\n    return None\n", encoding="utf-8")

    semantic_doc = {
        "problem_type": "demo",
        "render": {"elements": [{"type": "rect"}, {"type": "text"}]},
    }
    (root / semantic_rel).parent.mkdir(parents=True, exist_ok=True)
    (root / semantic_rel).write_text(json.dumps(semantic_doc, ensure_ascii=False), encoding="utf-8")

    retrieved = [
        {
            "entry": {
                "problem_id": "p100",
                "py_path": py_rel,
                "semantic_path": semantic_rel,
                "tags": ["demo"],
                "visual_primitives": ["rect", "text"],
            },
            "score": 8.5,
        }
    ]

    prompt = build_few_shot_prompt(
        input_meta={"problem_type": "demo", "tags": ["demo"]},
        retrieved_examples=retrieved,
        examples_root=root,
    )

    assert "Current Input Features" in prompt
    assert "Example 1: p100" in prompt
    assert "py_path: p100/p100.py" in prompt
    assert "semantic_path: p100/output/json/p100.semantic.json" in prompt
    assert "Return only Python code with build() -> Problem." in prompt
