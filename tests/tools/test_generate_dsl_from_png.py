from __future__ import annotations

from pathlib import Path

import pytest

from tools.generate_dsl_from_png import (
    ensure_output_writable,
    main,
    render_user_prompt,
    strip_markdown_code_fence,
    validate_dsl_source,
)


def test_render_user_prompt_inserts_problem_id() -> None:
    template = "Problem ID: {problem_id}"
    assert render_user_prompt(template, "0001") == "Problem ID: 0001"


def test_strip_markdown_code_fence_handles_python_fence() -> None:
    raw = "desc\n```python\nprint('hello')\n```\nmore"
    assert strip_markdown_code_fence(raw) == "print('hello')"


def test_strip_markdown_code_fence_leaves_plain_code_unchanged() -> None:
    raw = "print('plain code')\n"
    assert strip_markdown_code_fence(raw) == raw


def test_validate_dsl_source_accepts_problem_template_contract() -> None:
    source = """
from modu_math.dsl import ProblemTemplate

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(id='x', title='t', canvas=None, regions=(), slots=())
""".strip()
    assert validate_dsl_source(source) == []


def test_validate_dsl_source_rejects_missing_contract() -> None:
    source = "print('bad')"
    errors = validate_dsl_source(source)
    assert errors
    assert any("build_problem_template" in err for err in errors)


def test_ensure_output_writable_refuses_overwrite_without_force(tmp_path: Path) -> None:
    out_path = tmp_path / "problem.dsl.py"
    out_path.write_text("# existing\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        ensure_output_writable(out_path, force=False)


def test_ensure_output_writable_allows_overwrite_with_force(tmp_path: Path) -> None:
    out_path = tmp_path / "problem.dsl.py"
    out_path.write_text("# existing\n", encoding="utf-8")
    ensure_output_writable(out_path, force=True)


def test_dry_run_does_not_call_openai(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    image_path = tmp_path / "input.png"
    system_prompt = tmp_path / "system.md"
    user_template = tmp_path / "user.md"
    out_path = tmp_path / "problem.dsl.py"

    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    system_prompt.write_text("system", encoding="utf-8")
    user_template.write_text("Problem ID: {problem_id}", encoding="utf-8")

    def _should_not_be_called(**_: object) -> str:
        raise AssertionError("OpenAI call should not happen in dry-run")

    monkeypatch.setattr("tools.generate_dsl_from_png.call_openai_for_dsl", _should_not_be_called)

    exit_code = main(
        [
            "--image",
            str(image_path),
            "--problem-id",
            "0001",
            "--out",
            str(out_path),
            "--system-prompt",
            str(system_prompt),
            "--user-template",
            str(user_template),
            "--dry-run",
        ]
    )
    assert exit_code == 0
    assert not out_path.exists()


def test_generate_retries_until_valid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    image_path = tmp_path / "input.png"
    system_prompt = tmp_path / "system.md"
    user_template = tmp_path / "user.md"
    out_path = tmp_path / "problem.dsl.py"

    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    system_prompt.write_text("system", encoding="utf-8")
    user_template.write_text("Problem ID: {problem_id}", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    calls = {"n": 0}

    def _fake_call_openai_for_dsl(**_: object) -> str:
        calls["n"] += 1
        if calls["n"] == 1:
            return "print('bad')"
        return (
            "from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot\n\n"
            "def build_problem_template() -> ProblemTemplate:\n"
            "    return ProblemTemplate(\n"
            "        id='0001',\n"
            "        title='t',\n"
            "        canvas=Canvas(width=100, height=100),\n"
            "        regions=(Region(id='region.stem', role='stem', slot_ids=('slot.q',)),),\n"
            "        slots=(TextSlot(id='slot.q', text='q', style_role='question'),),\n"
            "    )\n"
        )

    monkeypatch.setattr("tools.generate_dsl_from_png.call_openai_for_dsl", _fake_call_openai_for_dsl)

    exit_code = main(
        [
            "--image",
            str(image_path),
            "--problem-id",
            "0001",
            "--out",
            str(out_path),
            "--system-prompt",
            str(system_prompt),
            "--user-template",
            str(user_template),
            "--max-attempts",
            "2",
        ]
    )
    assert exit_code == 0
    assert calls["n"] == 2
    assert out_path.exists()


def test_generate_fails_after_attempt_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    image_path = tmp_path / "input.png"
    system_prompt = tmp_path / "system.md"
    user_template = tmp_path / "user.md"
    out_path = tmp_path / "problem.dsl.py"

    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    system_prompt.write_text("system", encoding="utf-8")
    user_template.write_text("Problem ID: {problem_id}", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    monkeypatch.setattr("tools.generate_dsl_from_png.call_openai_for_dsl", lambda **_: "print('bad')")

    with pytest.raises(ValueError):
        main(
            [
                "--image",
                str(image_path),
                "--problem-id",
                "0001",
                "--out",
                str(out_path),
                "--system-prompt",
                str(system_prompt),
                "--user-template",
                str(user_template),
                "--max-attempts",
                "2",
            ]
        )
