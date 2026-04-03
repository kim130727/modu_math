from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ProblemRecord:
    problem_id: str
    problem_type: str
    grade_band: str
    problem_json_path: Path


def infer_problem_record(problem_dir: Path, problem_type: str, grade_band: str = "unknown") -> ProblemRecord:
    problem_id = problem_dir.name
    return ProblemRecord(
        problem_id=problem_id,
        problem_type=problem_type,
        grade_band=grade_band,
        problem_json_path=problem_dir / "input" / "problem.json",
    )
