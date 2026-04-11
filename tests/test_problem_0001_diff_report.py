from pathlib import Path
import runpy


def test_generate_0001_outputs_and_reports() -> None:
    runpy.run_path("tests/problem/0001/output_0001.py", run_name="__main__")

    base = Path("tests/problem/0001")
    expected_files = [
        base / "generated/0001.semantic.generated.json",
        base / "generated/0001.layout.generated.json",
        base / "generated/0001.semantic.generated.svg",
        base / "report/semantic_diff.json",
        base / "report/layout_diff.json",
        base / "report/semantic_diff.md",
        base / "report/layout_diff.md",
        base / "report/svg_diff.md",
        base / "report/run_summary.json",
    ]

    for path in expected_files:
        assert path.exists(), f"Missing expected output: {path}"
