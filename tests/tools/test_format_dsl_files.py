from __future__ import annotations

from pathlib import Path

from tools.format_dsl_files import format_path, iter_dsl_paths, main


def test_iter_dsl_paths_finds_only_dsl_files(tmp_path: Path) -> None:
    (tmp_path / "a.dsl.py").write_text("A=1\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("B=1\n", encoding="utf-8")
    child = tmp_path / "child"
    child.mkdir()
    (child / "c.dsl.py").write_text("C=1\n", encoding="utf-8")

    assert [p.name for p in iter_dsl_paths(tmp_path, recursive=False)] == ["a.dsl.py"]
    assert [p.name for p in iter_dsl_paths(tmp_path, recursive=True)] == ["a.dsl.py", "c.dsl.py"]


def test_format_path_check_does_not_write(tmp_path: Path) -> None:
    path = tmp_path / "problem.dsl.py"
    path.write_text("VALUE=1\n", encoding="utf-8")

    assert format_path(path, write=False) is True
    assert path.read_text(encoding="utf-8") == "VALUE=1\n"


def test_format_path_write_updates_file(tmp_path: Path) -> None:
    path = tmp_path / "problem.dsl.py"
    path.write_text("VALUE=1\n", encoding="utf-8")

    assert format_path(path, write=True) is True
    assert path.read_text(encoding="utf-8") == "VALUE = 1\n"


def test_main_check_returns_one_when_changes_needed(tmp_path: Path) -> None:
    path = tmp_path / "problem.dsl.py"
    path.write_text("VALUE=1\n", encoding="utf-8")

    assert main([str(tmp_path), "--quiet"]) == 1
    assert path.read_text(encoding="utf-8") == "VALUE=1\n"


def test_main_write_returns_zero_after_formatting(tmp_path: Path) -> None:
    path = tmp_path / "problem.dsl.py"
    path.write_text("VALUE=1\n", encoding="utf-8")

    assert main([str(tmp_path), "--write", "--quiet"]) == 0
    assert path.read_text(encoding="utf-8") == "VALUE = 1\n"
