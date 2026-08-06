from __future__ import annotations

import json
from pathlib import Path

from tools.repair_localized_editor_artifacts import main


def _write_dsl(path: Path, *, title: str, prompt: str, text: str) -> None:
    path.write_text(
        f"""
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextBoxSlot

PROBLEM_TEMPLATE = ProblemTemplate(
    id="p",
    title={title!r},
    canvas=Canvas(width=260, height=120),
    regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.question", "slot.answer")),),
    slots=(
        TextBoxSlot(
            id="slot.question",
            text={text!r},
            x=10,
            y=10,
            width=110,
            height=28,
            font_size=24,
            line_height=1.25,
        ),
        RectSlot(id="slot.answer", prompt={prompt!r}, x=150, y=70, width=28, height=28),
    ),
)
""".lstrip(),
        encoding="utf-8",
    )


def test_repair_copies_answer_interaction_without_overwriting_translation(tmp_path: Path) -> None:
    source_dsl = tmp_path / "problem.dsl.py"
    localized_dsl = tmp_path / "problem.uk.dsl.py"
    _write_dsl(source_dsl, title="Add", prompt="Answer", text="Write.")
    _write_dsl(
        localized_dsl,
        title="Додавання",
        prompt="Відповідь",
        text="Впишіть у клітинки відповідні числа.",
    )
    (tmp_path / "problem.editor_overrides.json").write_text(
        json.dumps(
            {
                "slots": {
                    "slot.question": {
                        "text": "Write.",
                        "x": 20,
                        "y": 10,
                        "width": 120,
                        "height": 30,
                        "font_size": 24,
                    },
                    "slot.answer": {
                        "x": 160,
                        "interaction": {
                            "type": "input",
                            "role": "answer",
                            "value_type": "digit",
                            "max_length": 1,
                            "order": 0,
                        },
                        "input_style": {"font_size_mode": "auto"},
                    },
                },
                "version": 1,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    assert (
        main(
            [
                "--localized-dsl",
                str(localized_dsl),
                "--source-dsl",
                str(source_dsl),
                "--no-build",
            ]
        )
        == 0
    )

    repaired = json.loads((tmp_path / "problem.uk.editor_overrides.json").read_text(encoding="utf-8"))
    assert repaired["slots"]["slot.question"]["text"] == "Впишіть у клітинки відповідні числа."
    assert repaired["slots"]["slot.question"]["font_size"] < 24
    assert repaired["slots"]["slot.answer"]["interaction"]["role"] == "answer"
    assert repaired["slots"]["slot.answer"]["input_style"]["font_size_mode"] == "auto"
