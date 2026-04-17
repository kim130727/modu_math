import json
from pathlib import Path
from typing import Any

class SemanticValidationError(Exception):
    pass

def validate_semantic_json(data: dict[str, Any]) -> None:
    if "problem_id" not in data:
        raise SemanticValidationError("Missing 'problem_id'")
    if "problem_type" not in data:
        raise SemanticValidationError("Missing 'problem_type'")
    
    # Check domain
    domain = data.get("domain", {})
    if not isinstance(domain, dict):
        raise SemanticValidationError("'domain' must be an object")
    if "objects" not in domain or "relations" not in domain:
        raise SemanticValidationError("'domain' must contain 'objects' and 'relations'")

    # Check answer
    answer = data.get("answer", {})
    if not isinstance(answer, dict):
        raise SemanticValidationError("'answer' must be an object")

def load_and_validate(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_semantic_json(data)
    return data
