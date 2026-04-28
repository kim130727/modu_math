from __future__ import annotations

from pathlib import Path

import pytest

from tools.generate_dsl_from_png import (
    ensure_output_writable,
    main,
    render_user_prompt,
    strip_markdown_code_fence,
)


def test_render_user_prompt_inserts_problem_id() -> None:
    template = "Problem ID: {problem_id}"
    assert render_user_prompt(template, "0001") == "Problem ID: 0001"


def test_strip_markdown_code_fence_handles_python_fence() -> None:
    raw = "설명\n```python\nprint('안녕하세요')\n```\n추가"
    assert strip_markdown_code_fence(raw) == "print('안녕하세요')"


def test_strip_markdown_code_fence_leaves_plain_code_unchanged() -> None:
    raw = "print('plain code')\n"
    assert strip_markdown_code_fence(raw) == raw


def test_ensure_output_writable_refuses_overwrite_without_force(tmp_path: Path) -> None:
    out_path = tmp_path / "problem.dsl.py"
    out_path.write_text("# existing\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        ensure_output_writable(out_path, force=False)


def test_ensure_output_writable_allows_overwrite_with_force(tmp_path: Path) -> None:
    out_path = tmp_path / "problem.dsl.py"
    out_path.write_text("# existing\n", encoding="utf-8")
    # Should not raise when force is enabled.
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


def test_korean_utf8_text_is_preserved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    image_path = tmp_path / "input.png"
    system_prompt = tmp_path / "system.md"
    user_template = tmp_path / "user.md"
    out_path = tmp_path / "problem.dsl.py"

    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    system_prompt.write_text("system", encoding="utf-8")
    user_template.write_text("Problem ID: {problem_id}", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def _fake_call_openai_for_dsl(**_: object) -> str:
        return "```python\nprint('한글 유지 테스트')\n```"

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
        ]
    )
    assert exit_code == 0
    written = out_path.read_text(encoding="utf-8")
    assert "한글 유지 테스트" in written
    assert "```" not in written
