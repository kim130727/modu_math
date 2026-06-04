from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import batch_generate_dsl


def test_batch_discovery_finds_problem_dirs_with_input_png(tmp_path: Path) -> None:
    root = tmp_path / "examples" / "problems"
    (root / "0001").mkdir(parents=True)
    (root / "0001" / "input.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (root / "0002").mkdir(parents=True)
    (root / "0002" / "input.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (root / "9999").mkdir(parents=True)  # no input.png, should be ignored

    found = batch_generate_dsl._problem_dirs(root)
    assert [path.name for path in found] == ["0001", "0002"]


def test_agent_trace_shape_is_stable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "examples" / "problems"
    problem_dir = root / "0001"
    problem_dir.mkdir(parents=True)
    (problem_dir / "input.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    def _fake_generate_dsl_from_png(**kwargs: object) -> dict[str, str]:
        out_path = Path(str(kwargs["out_path"]))
        out_path.write_text("print('ok')\n", encoding="utf-8")
        return {
            "image": str(kwargs["image_path"]),
            "problem_id": str(kwargs["problem_id"]),
            "out": str(kwargs["out_path"]),
            "model": "test-model",
            "system_prompt": str(kwargs["system_prompt_path"]),
            "user_template": str(kwargs["user_template_path"]),
        }

    monkeypatch.setattr(batch_generate_dsl, "generate_dsl_from_png", _fake_generate_dsl_from_png)
    monkeypatch.setattr(batch_generate_dsl, "resolve_model_name", lambda _: "test-model")

    exit_code = batch_generate_dsl.main(
        [
            "--root",
            str(root),
            "--force",
        ]
    )
    assert exit_code == 0

    trace_path = problem_dir / "agent_trace.json"
    payload = json.loads(trace_path.read_text(encoding="utf-8"))
    assert set(payload.keys()) >= {
        "problem_id",
        "image_path",
        "output_path",
        "model",
        "prompt_files",
        "success",
    }
    assert payload["problem_id"] == "0001"
    assert payload["success"] is True
    assert isinstance(payload["prompt_files"], dict)
    assert set(payload["prompt_files"].keys()) == {"system_prompt", "user_template"}
