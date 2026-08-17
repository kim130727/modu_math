from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

import pytest

from tools.apply_dsl_localization import main
from tools.extract_dsl_localization import load_dsl_module
from tests.tools.test_extract_dsl_localization import _write_dsl


def _locale_with_translations(dsl_path: Path, locale_path: Path) -> None:
    from tools.extract_dsl_localization import main as extract_main

    assert extract_main(["--dsl", str(dsl_path), "--locale", "en-US", "--out", str(locale_path)]) == 0
    data = json.loads(locale_path.read_text(encoding="utf-8"))
    data["template.title"]["translation"] = "Addition"
    data["template.title"]["status"] = "translated"
    data["template.slots.slot.question.text"]["translation"] = "Add all numbers."
    data["template.slots.slot.question.text"]["status"] = "translated"
    data["template.slots.slot.answer.prompt"]["translation"] = "Answer"
    data["template.slots.slot.answer.prompt"]["status"] = "translated"
    data["semantic.metadata.subject"]["translation"] = "Mathematics"
    data["semantic.metadata.subject"]["status"] = "translated"
    data["solvable.steps.step.add.goal"]["translation"] = "Find the sum."
    data["solvable.steps.step.add.goal"]["status"] = "translated"
    locale_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_apply_creates_localized_dsl_without_modifying_source(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    locale_path = tmp_path / "p_localize.locale.json"
    out_path = tmp_path / "problem.en-US.dsl.py"
    _write_dsl(dsl_path, slot_text="Add the numbers.")
    _locale_with_translations(dsl_path, locale_path)
    before = sha256(dsl_path.read_bytes()).hexdigest()

    assert (
        main(
            [
                "--dsl",
                str(dsl_path),
                "--locale-json",
                str(locale_path),
                "--out",
                str(out_path),
            ]
        )
        == 0
    )

    assert sha256(dsl_path.read_bytes()).hexdigest() == before
    module = load_dsl_module(out_path)
    assert module.PROBLEM_TEMPLATE.title == "Addition"
    assert module.PROBLEM_TEMPLATE.slots[0].text == "Add all numbers."
    assert module.PROBLEM_TEMPLATE.slots[2].prompt == "Answer"
    assert module.SEMANTIC_OVERRIDE["metadata"]["subject"] == "Mathematics"
    assert module.SOLVABLE["steps"][0]["goal"] == "Find the sum."
    assert module.SOLVABLE["steps"][0]["expr"] == "2 + 3"


def test_apply_does_not_overwrite_existing_output_without_force(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    locale_path = tmp_path / "p_localize.locale.json"
    out_path = tmp_path / "problem.en-US.dsl.py"
    _write_dsl(dsl_path)
    _locale_with_translations(dsl_path, locale_path)
    out_path.write_text("# existing\n", encoding="utf-8")

    with pytest.raises(FileExistsError):
        main(["--dsl", str(dsl_path), "--locale-json", str(locale_path), "--out", str(out_path)])

    assert out_path.read_text(encoding="utf-8") == "# existing\n"


def test_apply_skips_needs_review_by_default(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    locale_path = tmp_path / "p_localize.locale.json"
    out_path = tmp_path / "problem.en-US.dsl.py"
    _write_dsl(dsl_path)
    _locale_with_translations(dsl_path, locale_path)

    data = json.loads(locale_path.read_text(encoding="utf-8"))
    data["template.slots.slot.question.text"]["status"] = "needs_review"
    locale_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert main(["--dsl", str(dsl_path), "--locale-json", str(locale_path), "--out", str(out_path)]) == 0
    module = load_dsl_module(out_path)
    assert module.PROBLEM_TEMPLATE.slots[0].text == "Add the numbers."


def test_apply_preserves_korean_choice_and_symbol_markers(tmp_path: Path) -> None:
    dsl_path = tmp_path / "problem.dsl.py"
    locale_path = tmp_path / "p_symbol_locale.locale.json"
    out_path = tmp_path / "problem.en-US.dsl.py"
    dsl_path.write_text(
        '''
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

PROBLEM_ID = "p_symbol_locale"
PROBLEM_TEMPLATE = ProblemTemplate(
    id=PROBLEM_ID,
    title="Symbol Locale",
    canvas=Canvas(width=300, height=120),
    regions=(Region(id="region.body", role="body", slot_ids=("slot.choice", "slot.symbol")),),
    slots=(
        TextSlot(id="slot.choice", text="(\\uac00)", style_role="choice"),
        TextSlot(id="slot.symbol", text="\\u3131", semantic_role="symbol_label"),
    ),
)
'''.lstrip(),
        encoding="utf-8",
    )
    locale_path.write_text(
        json.dumps(
            {
                "template.slots.slot.choice.text": {
                    "source": "(\uac00)",
                    "translation": "A",
                    "status": "translated",
                },
                "template.slots.slot.symbol.text": {
                    "source": "\u3131",
                    "translation": "A",
                    "status": "translated",
                },
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    assert main(["--dsl", str(dsl_path), "--locale-json", str(locale_path), "--out", str(out_path)]) == 0

    module = load_dsl_module(out_path)
    assert module.PROBLEM_TEMPLATE.slots[0].text == "(\uac00)"
    assert module.PROBLEM_TEMPLATE.slots[1].text == "\u3131"
