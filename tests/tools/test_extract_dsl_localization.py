from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from tools.extract_dsl_localization import main


def _write_dsl(path: Path, *, slot_text: str = "Add the numbers.") -> None:
    path.write_text(
        f'''
from modu_math.dsl import BlankSlot, Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_ID = "p_localize"

PROBLEM_TEMPLATE = ProblemTemplate(
    id=PROBLEM_ID,
    title="Addition",
    canvas=Canvas(width=300, height=120),
    regions=(Region(id="region.stem", role="stem", slot_ids=("slot.question", "slot.expr", "slot.answer")),),
    slots=(
        TextSlot(id="slot.question", text="{slot_text}", font_family="Noto Sans KR"),
        TextSlot(id="slot.expr", text="2 + 3 = 5"),
        BlankSlot(id="slot.answer", prompt="Answer", placeholder="units", answer_key="5"),
    ),
)

SEMANTIC_OVERRIDE = {{
    "problem_id": PROBLEM_ID,
    "problem_type": "addition",
    "metadata": {{"subject": "Math", "topic": "Addition"}},
    "domain": {{
        "objects": [
            {{"id": "object.apple", "type": "countable_object", "label": "apple", "unit": "piece"}},
        ],
    }},
    "answer": {{"value": 5, "unit": "piece"}},
}}

SOLVABLE = {{
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "addition",
    "inputs": {{"conditions": ["There are 2 apples.", "There are 3 more apples."]}},
    "steps": [{{"id": "step.add", "goal": "Find the total.", "expr": "2 + 3", "value": 5}}],
    "answer": {{"value": 5, "unit": "piece"}},
}}
'''.lstrip(),
        encoding="utf-8",
    )


def test_extract_uses_stable_keys_and_skips_non_translatable_fields(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    out_path = tmp_path / "p_localize.locale.json"
    _write_dsl(dsl_path)

    assert main(["--dsl", str(dsl_path), "--locale", "en-US", "--out", str(out_path)]) == 0

    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["template.slots.slot.question.text"]["source"] == "Add the numbers."
    assert data["template.slots.slot.question.text"] == {
        "source": "Add the numbers.",
        "translation": "",
    }
    assert data["semantic.domain.objects.object.apple.label"]["source"] == "apple"
    assert data["solvable.steps.step.add.goal"]["source"] == "Find the total."
    assert data["solvable.inputs.conditions.0"]["source"] == "There are 2 apples."
    assert "template.slots.0.text" not in data
    assert "template.slots.slot.expr.text" not in data
    assert all(not key.startswith(("semantic.answer.", "solvable.answer.")) for key in data)
    assert all(not key.endswith(".font_family") for key in data)


def test_extract_drops_stale_translation_and_obsolete_entries(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    out_path = tmp_path / "p_localize.locale.json"
    _write_dsl(dsl_path)
    assert main(["--dsl", str(dsl_path), "--locale", "en-US", "--out", str(out_path)]) == 0

    data = json.loads(out_path.read_text(encoding="utf-8"))
    data["template.slots.slot.question.text"]["translation"] = "Addiere die Zahlen."
    data["old.key"] = {
        "source": "gone",
        "source_hash": sha256(b"gone").hexdigest(),
        "translation": "weg",
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    _write_dsl(dsl_path, slot_text="Add all numbers.")
    assert main(["--dsl", str(dsl_path), "--locale", "en-US", "--out", str(out_path)]) == 0

    updated = json.loads(out_path.read_text(encoding="utf-8"))
    question = updated["template.slots.slot.question.text"]
    assert question == {"source": "Add all numbers.", "translation": ""}
    assert "old.key" not in updated
    assert all("source_hash" not in entry and "status" not in entry for entry in updated.values())


def test_extract_does_not_modify_existing_dsl(tmp_path: Path) -> None:
    dsl_path = Path("examples/problems/ko/P3_1_01_00040_00469.dsl.py")
    before = sha256(dsl_path.read_bytes()).hexdigest()

    assert (
        main(
            [
                "--dsl",
                str(dsl_path),
                "--locale",
                "en-US",
                "--out",
                str(tmp_path / "representative.locale.json"),
            ]
        )
        == 0
    )

    assert sha256(dsl_path.read_bytes()).hexdigest() == before
