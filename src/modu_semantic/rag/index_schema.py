from __future__ import annotations

from typing import Any, TypedDict


class RagIndexEntry(TypedDict):
    problem_id: str
    py_path: str
    semantic_path: str
    layout_path: str
    tags: list[str]
    validation_passed: bool
    updated_at: str
    problem_type: str
    grade: str
    topic: str
    visual_primitives: list[str]
    layout_pattern: str
    answer_style: str
    failure_notes: str
    source_image_hash: str


class RagRunLog(TypedDict):
    run_id: str
    input_meta: dict[str, Any]
    retrieved_examples: list[str]
    generated_py_path: str
    build_success: bool
    validation_success: bool
    error_message: str
    created_at: str
