from __future__ import annotations

from typing import Any

from modu_semantic.normalizer import normalize_semantic
from modu_semantic.orderer import order_semantic
from modu_semantic.validator import validate_semantic


def canonicalize_and_validate(semantic: dict[str, Any]) -> dict[str, Any]:
    canonical = normalize_semantic(semantic)
    canonical = order_semantic(canonical)
    validate_semantic(canonical)
    return canonical

