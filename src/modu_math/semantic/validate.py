import json
from pathlib import Path
from typing import Any


class SemanticValidationError(Exception):
    pass


def _require_non_empty_string(data: dict[str, Any], key: str) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SemanticValidationError(f"Missing or invalid '{key}' (expected non-empty string)")


def _require_object(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise SemanticValidationError(f"Missing or invalid '{key}' (expected object)")
    return value


def _require_list(obj: dict[str, Any], key: str, path: str) -> list[Any]:
    value = obj.get(key)
    if not isinstance(value, list):
        raise SemanticValidationError(f"Missing or invalid '{path}.{key}' (expected array)")
    return value


def _validate_domain(domain: dict[str, Any]) -> None:
    objects = _require_list(domain, "objects", "domain")
    relations = _require_list(domain, "relations", "domain")

    object_ids: set[str] = set()
    for index, item in enumerate(objects):
        if not isinstance(item, dict):
            raise SemanticValidationError(f"domain.objects[{index}] must be an object")
        object_id = item.get("id")
        object_type = item.get("type")
        if not isinstance(object_id, str) or not object_id.strip():
            raise SemanticValidationError(f"domain.objects[{index}].id must be a non-empty string")
        if object_id in object_ids:
            raise SemanticValidationError(f"Duplicate domain.objects id '{object_id}'")
        object_ids.add(object_id)
        if not isinstance(object_type, str) or not object_type.strip():
            raise SemanticValidationError(f"domain.objects[{index}].type must be a non-empty string")

        if "refs" in item:
            refs = item["refs"]
            if not isinstance(refs, list):
                raise SemanticValidationError(f"domain.objects[{index}].refs must be an array")
            for ref_index, ref in enumerate(refs):
                if not isinstance(ref, dict):
                    raise SemanticValidationError(
                        f"domain.objects[{index}].refs[{ref_index}] must be an object"
                    )
                ref_id = ref.get("id")
                ref_kind = ref.get("kind")
                if not isinstance(ref_id, str) or not ref_id.strip():
                    raise SemanticValidationError(
                        f"domain.objects[{index}].refs[{ref_index}].id must be a non-empty string"
                    )
                if not isinstance(ref_kind, str) or not ref_kind.strip():
                    raise SemanticValidationError(
                        f"domain.objects[{index}].refs[{ref_index}].kind must be a non-empty string"
                    )

    relation_ids: set[str] = set()
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            raise SemanticValidationError(f"domain.relations[{index}] must be an object")

        relation_id = relation.get("id")
        relation_type = relation.get("type")
        from_id = relation.get("from_id")
        to_id = relation.get("to_id")

        if not isinstance(relation_id, str) or not relation_id.strip():
            raise SemanticValidationError(f"domain.relations[{index}].id must be a non-empty string")
        if relation_id in relation_ids:
            raise SemanticValidationError(f"Duplicate domain.relations id '{relation_id}'")
        relation_ids.add(relation_id)

        if not isinstance(relation_type, str) or not relation_type.strip():
            raise SemanticValidationError(f"domain.relations[{index}].type must be a non-empty string")
        if not isinstance(from_id, str) or not from_id.strip():
            raise SemanticValidationError(f"domain.relations[{index}].from_id must be a non-empty string")
        if not isinstance(to_id, str) or not to_id.strip():
            raise SemanticValidationError(f"domain.relations[{index}].to_id must be a non-empty string")


def _validate_answer(answer: dict[str, Any]) -> None:
    blanks = _require_list(answer, "blanks", "answer")
    choices = _require_list(answer, "choices", "answer")
    answer_key = _require_list(answer, "answer_key", "answer")

    for index, blank in enumerate(blanks):
        if not isinstance(blank, dict):
            raise SemanticValidationError(f"answer.blanks[{index}] must be an object")

    for index, choice in enumerate(choices):
        if not isinstance(choice, dict):
            raise SemanticValidationError(f"answer.choices[{index}] must be an object")

    for index, key in enumerate(answer_key):
        if not isinstance(key, dict):
            raise SemanticValidationError(f"answer.answer_key[{index}] must be an object")


def validate_semantic_json(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise SemanticValidationError("semantic payload must be an object")

    _require_non_empty_string(data, "problem_id")
    _require_non_empty_string(data, "problem_type")

    metadata = _require_object(data, "metadata")
    domain = _require_object(data, "domain")
    answer = _require_object(data, "answer")

    if "required_layout_ids" in metadata and not isinstance(metadata.get("required_layout_ids"), list):
        raise SemanticValidationError("metadata.required_layout_ids must be an array when present")

    _validate_domain(domain)
    _validate_answer(answer)


def load_and_validate(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    validate_semantic_json(data)
    return data
