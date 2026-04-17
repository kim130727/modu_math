from __future__ import annotations

import importlib.util
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from ..problem import Problem


SCAFFOLD_TEMPLATE = """from modu_semantic import Problem, Rect, Text\n\n\ndef build() -> Problem:\n    p = Problem(width=800, height=600, problem_id=\"{problem_id}\", problem_type=\"{problem_type}\")\n    p.add(Rect(id=\"box\", x=80, y=80, width=640, height=420, stroke=\"#333333\", fill=\"none\"))\n{instruction_lines}\n    return p\n"""


def _build_instruction_lines(input_meta: dict[str, Any]) -> str:
    raw_lines = input_meta.get("ocr_text_lines") or []
    lines = [str(line).strip() for line in raw_lines if str(line).strip()]
    if not lines:
        lines = ["TODO: 문제 문장을 입력하세요."]

    rendered: list[str] = []
    base_y = 130
    step = 36
    for idx, line in enumerate(lines[:6]):
        safe_line = line.replace("\\", "\\\\").replace("\"", "\\\"")
        rendered.append(
            f'    p.add(Text(id="instruction_{idx+1}", x=100, y={base_y + idx * step}, text="{safe_line}", font_size=24))'
        )
    return "\n".join(rendered)


def make_run_id(prefix: str = "rag") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def build_generation_scaffold(
    *,
    output_dir: str | Path,
    run_id: str,
    input_meta: dict[str, Any],
    file_stem: str | None = None,
) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    problem_id = str(input_meta.get("problem_id") or run_id)
    problem_type = str(input_meta.get("problem_type") or "unknown")

    stem = file_stem or run_id
    py_path = out_dir / f"{stem}.generated.py"
    instruction_lines = _build_instruction_lines(input_meta)
    py_path.write_text(
        SCAFFOLD_TEMPLATE.format(
            problem_id=problem_id,
            problem_type=problem_type,
            instruction_lines=instruction_lines,
        ),
        encoding="utf-8",
    )
    return py_path


def _load_problem_from_python_file(path: str | Path) -> Problem:
    path_obj = Path(path)
    spec = importlib.util.spec_from_file_location("rag_generated_problem_module", path_obj)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path_obj}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "build"):
        raise RuntimeError("Generated file must define build() returning Problem")

    problem = module.build()
    if not isinstance(problem, Problem):
        raise RuntimeError("build() must return modu_semantic.Problem")
    return problem


def validate_generated_python(py_path: str | Path) -> tuple[bool, bool, str]:
    try:
        problem = _load_problem_from_python_file(py_path)
    except Exception as exc:  # noqa: BLE001
        return False, False, str(exc)

    try:
        with TemporaryDirectory() as tmp_dir:
            out_prefix = Path(tmp_dir) / "generated_check"
            problem.save(out_prefix, validate=True)
        return True, True, ""
    except Exception as exc:  # noqa: BLE001
        return True, False, str(exc)


def persist_generated_outputs(
    py_path: str | Path,
    *,
    out_prefix: str | Path,
    validate: bool = True,
) -> tuple[bool, str]:
    try:
        problem = _load_problem_from_python_file(py_path)
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)

    try:
        problem.save(Path(out_prefix), validate=validate)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
