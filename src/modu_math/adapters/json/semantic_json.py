from typing import Any
from ...semantic.models.problem import SemanticProblem

def problem_to_semantic_json(problem: SemanticProblem) -> dict[str, Any]:
    """Converts a SemanticProblem model into the canonical JSON dictionary."""
    from ...semantic.normalize import normalize_semantic
    
    data = problem.to_dict()
    return normalize_semantic(data)

def semantic_json_to_problem(data: dict[str, Any]) -> SemanticProblem:
    """Parses a canonical JSON dictionary into a SemanticProblem model."""
    from ...semantic.validate import validate_semantic_json
    validate_semantic_json(data)
    
    return SemanticProblem(
        problem_id=data.get("problem_id"),
        problem_type=data.get("problem_type", "generic"),
        metadata=data.get("metadata", {}),
        domain=data.get("domain", {"objects": [], "relations": []}),
        answer=data.get("answer", {"blanks": [], "choices": [], "answer_key": []})
    )
