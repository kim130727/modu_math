from pathlib import Path

from modu_semantic.rag.pipeline import build_generation_scaffold, persist_generated_outputs


def test_rag_pipeline_persist_generated_outputs(tmp_path: Path) -> None:
    out_dir = tmp_path / "generated"
    run_id = "rag_test"
    py_path = build_generation_scaffold(
        output_dir=out_dir,
        run_id=run_id,
        input_meta={"problem_id": "p_test", "problem_type": "demo"},
        file_stem="p_test_readable",
    )

    out_prefix = out_dir / "p_test_readable_built"
    ok, error = persist_generated_outputs(py_path, out_prefix=out_prefix, validate=True)

    assert ok is True
    assert error == ""
    assert (out_dir / "p_test_readable.generated.py").exists()
    assert (out_dir / "p_test_readable_built.semantic.json").exists()
    assert (out_dir / "p_test_readable_built.layout.json").exists()
    assert (out_dir / "p_test_readable_built.svg").exists()
