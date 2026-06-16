from __future__ import annotations

import json
from pathlib import Path

from tools.generate_vision_structured import (
    generate_vision_structured,
    parse_json_output,
    read_image_size,
)


def _write_png(path: Path, width: int = 2, height: int = 3) -> None:
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\r"
        b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x06\x00\x00\x00"
        + b"\x00\x00\x00\x00"
    )


def test_read_image_size_reads_png_header(tmp_path: Path) -> None:
    image = tmp_path / "input.png"
    _write_png(image, width=640, height=480)

    assert read_image_size(image) == (640.0, 480.0)


def test_parse_json_output_handles_fenced_json() -> None:
    payload = parse_json_output('```json\n{"schema":"x","visible_text":[]}\n```')

    assert payload["schema"] == "x"
    assert payload["visible_text"] == []


def test_generate_vision_structured_prompt_mode_normalizes_and_writes(tmp_path: Path) -> None:
    image = tmp_path / "input.png"
    out = tmp_path / "problem.vision_structured.json"
    llm_output = tmp_path / "problem.vision_structured_llm_output.txt"
    schema = Path("schema/vision/vision_structured.v1.json")
    _write_png(image, width=100, height=200)
    llm_output.write_text(
        json.dumps(
            {
                "schema": "wrong",
                "problem_id": "wrong",
                "source_image": {},
                "visible_text": [
                    {
                        "id": "t1",
                        "text": "문제",
                        "bbox": {"x": -1, "y": 0.1, "w": 2, "h": 0.2},
                        "confidence": "certain",
                    }
                ],
                "elements": [
                    {
                        "id": "e1",
                        "type": "blank",
                        "bbox": {"x": 0.2, "y": 0.3, "w": 0.1, "h": 0.05},
                        "details": "empty answer box",
                        "confidence": "high",
                    }
                ],
                "groups": [],
                "math_structure": {"blanks": [{"element_id": "e1"}]},
                "dsl_hints": ["Use RectSlot for the blank."],
                "uncertain": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = generate_vision_structured(
        image_path=image,
        problem_id="p1",
        out_path=out,
        provider="openai",
        mode="prompt",
        llm_output_file=llm_output,
        force=True,
        schema_path=schema,
    )

    assert result["out"] == str(out)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema"] == "modu.vision_structured.v1"
    assert payload["problem_id"] == "p1"
    assert payload["source_image"]["width_px"] == 100.0
    assert payload["source_image"]["height_px"] == 200.0
    assert payload["visible_text"][0]["confidence"] == "medium"
    assert payload["visible_text"][0]["bbox"] == {"x": 0.0, "y": 0.1, "w": 1.0, "h": 0.2}
