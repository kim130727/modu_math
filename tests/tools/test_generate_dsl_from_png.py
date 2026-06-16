from __future__ import annotations

from pathlib import Path

import pytest

from tools.generate_dsl_from_png import (
    _normalize_answer_alignment_block,
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

SEMANTIC_OVERRIDE = {
    "problem_id": "x",
    "domain": {"objects": [], "relations": []},
    "answer": {"value": 1},
}

SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "x",
    "answer": {"value": 1},
}
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

    monkeypatch.setattr("tools.generate_dsl_from_png.call_llm_for_dsl", _should_not_be_called)

    exit_code = main(
        [
            "--image",
            str(image_path),
            "--problem-id",
            "0001",
            "--out",
            str(out_path),
            "--provider",
            "openai",
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
            "\n"
            "SEMANTIC_OVERRIDE = {\n"
            "    'problem_id': '0001',\n"
            "    'domain': {'objects': [], 'relations': []},\n"
            "    'answer': {'value': 1, 'unit': ''},\n"
            "}\n"
            "\n"
            "SOLVABLE = {\n"
            "    'schema': 'modu.solvable.v1',\n"
            "    'problem_id': '0001',\n"
            "    'problem_type': 'test',\n"
            "    'inputs': {\n"
            "        'total_ticks': 0,\n"
            "        'target_label': 'x',\n"
            "        'target_ticks': 0,\n"
            "        'target_count': 0,\n"
            "        'unit': '',\n"
            "    },\n"
            "    'given': [{'ref': 'input.x', 'value': 1}],\n"
            "    'target': {'ref': 'answer.value', 'type': 'number'},\n"
            "    'method': 'test method',\n"
            "    'plan': ['p'],\n"
            "    'steps': [{'id': 'step.1', 'expr': 'x', 'value': 1}],\n"
            "    'checks': [],\n"
            "    'answer': {'value': 1, 'unit': ''},\n"
            "}\n"
        )

    monkeypatch.setattr("tools.generate_dsl_from_png.call_llm_for_dsl", _fake_call_openai_for_dsl)

    exit_code = main(
        [
            "--image",
            str(image_path),
            "--problem-id",
            "0001",
            "--out",
            str(out_path),
            "--provider",
            "openai",
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

    monkeypatch.setattr("tools.generate_dsl_from_png.call_llm_for_dsl", lambda **_: "print('bad')")

    with pytest.raises(ValueError):
        main(
            [
                "--image",
                str(image_path),
                "--problem-id",
                "0001",
                "--out",
                str(out_path),
                "--provider",
                "openai",
                "--system-prompt",
                str(system_prompt),
                "--user-template",
                str(user_template),
                "--max-attempts",
                "2",
            ]
        )


def test_normalize_answer_alignment_block_rewrites_to_canonical_form() -> None:
    source = (
        "SEMANTIC_OVERRIDE = {'answer': {'value': 1}}\n"
        "SOLVABLE = {'answer': {'value': 2}}\n"
        "SEMANTIC_OVERRIDE['answer'] = SOLVABLE['answer']\n"
        "# answer contract alignment (do not touch Korean text content)\n"
        "if isinstance(SEMANTIC_OVERRIDE.get('answer'), dict) and isinstance(SOLVABLE.get('answer'), dict):\n"
        "    _answer = dict(SEMANTIC_OVERRIDE['answer'])\n"
        "    _answer.setdefault('blanks', [])\n"
        "    _answer.setdefault('choices', [])\n"
        "    _answer.setdefault('answer_key', [])\n"
        "    SOLVABLE['answer'] = _answer\n"
    )
    normalized = _normalize_answer_alignment_block(source)
    assert "SEMANTIC_OVERRIDE['answer'] = SOLVABLE['answer']" not in normalized
    assert '# answer contract alignment' in normalized
    assert 'SEMANTIC_OVERRIDE.get("answer")' in normalized
    assert 'SOLVABLE["answer"] = _answer' in normalized


def test_normalize_answer_alignment_block_preserves_korean_text() -> None:
    source = (
        "SEMANTIC_OVERRIDE = {'answer': {'value': 1}}\n"
        "SOLVABLE = {'answer': {'value': 1}}\n"
        "text = '한글 문장 보존 테스트'\n"
    )
    normalized = _normalize_answer_alignment_block(source)
    assert "한글 문장 보존 테스트" in normalized
