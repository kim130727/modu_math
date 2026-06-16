from __future__ import annotations

import json
from pathlib import Path

from tools.generate_dsl_from_refined_draft import (
    build_user_prompt,
    generate_dsl_from_refined_draft,
)


def test_build_user_prompt_includes_structured_vision_constraints() -> None:
    prompt = build_user_prompt(
        problem_id="p1",
        refined_draft_text="refined details",
        source_answer_refs=[],
        compact_prompt=False,
        vision_structured_text='{"source_image":{"width_px":100,"height_px":200},"elements":[]}',
    )

    assert "<vision_structured_json>" in prompt
    assert "primary layout constraint source" in prompt
    assert "Convert each bbox" in prompt
    assert '"width_px":100' in prompt


def test_prompt_mode_writes_dsl_prompt_with_structured_vision_json(tmp_path: Path) -> None:
    image = tmp_path / "input.png"
    draft = tmp_path / "problem.refined_draft.md"
    structured = tmp_path / "problem.vision_structured.json"
    system_prompt = tmp_path / "system.md"
    rules = tmp_path / "rules.md"
    out = tmp_path / "problem.dsl.py"
    prompt_out = tmp_path / "problem.dsl_prompt.md"

    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    draft.write_text("[DSL 힌트]\n- place a box\n", encoding="utf-8")
    system_prompt.write_text("system", encoding="utf-8")
    rules.write_text("rules", encoding="utf-8")
    structured.write_text(
        json.dumps(
            {
                "schema": "modu.vision_structured.v1",
                "problem_id": "p1",
                "source_image": {
                    "path": str(image),
                    "width_px": 100,
                    "height_px": 200,
                    "coordinate_system": "normalized_0_1",
                },
                "elements": [
                    {
                        "id": "el.1",
                        "type": "box",
                        "bbox": {"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4},
                        "details": "box",
                        "confidence": "high",
                    }
                ],
                "groups": [],
                "math_structure": {},
                "dsl_hints": ["Use RectSlot."],
                "uncertain": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = generate_dsl_from_refined_draft(
        draft_path=draft,
        image_path=image,
        problem_id="p1",
        vision_structured_path=structured,
        out_path=out,
        provider="openai",
        mode="prompt",
        prompt_out=prompt_out,
        system_prompt_path=system_prompt,
        rules_md_path=rules,
        force=True,
    )

    assert result["prompt_only"] == "true"
    assert result["has_vision_structured"] == "True"
    prompt_text = prompt_out.read_text(encoding="utf-8")
    assert "<vision_structured_json>" in prompt_text
    assert '"coordinate_system": "normalized_0_1"' in prompt_text
    assert '"id": "el.1"' in prompt_text
