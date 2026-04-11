from pathlib import Path

from modu_semantic.rag.logger import append_run_log, load_run_logs


def test_rag_run_logger_appends_and_loads(tmp_path: Path) -> None:
    runs_path = tmp_path / "runs.jsonl"

    append_run_log(
        runs_path=runs_path,
        run_id="run_1",
        input_meta={"problem_type": "demo"},
        retrieved_examples=["0001", "0002"],
        generated_py_path="tmp/generated.py",
        build_success=True,
        validation_success=False,
        error_message="validation failed",
    )

    append_run_log(
        runs_path=runs_path,
        run_id="run_2",
        input_meta={"problem_type": "geometry"},
        retrieved_examples=["0003"],
        generated_py_path="tmp/generated2.py",
        build_success=True,
        validation_success=True,
    )

    rows = load_run_logs(runs_path)
    assert len(rows) == 2
    assert rows[0]["run_id"] == "run_1"
    assert rows[0]["validation_success"] is False
    assert rows[1]["run_id"] == "run_2"
    assert rows[1]["validation_success"] is True
