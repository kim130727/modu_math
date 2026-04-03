from __future__ import annotations

from typing import Callable

from modu_math.core.base_problem import BaseProblemBuilder


_BUILDER_REGISTRY: dict[str, type[BaseProblemBuilder]] = {}


def register_builder(problem_type: str) -> Callable[[type[BaseProblemBuilder]], type[BaseProblemBuilder]]:
    def _decorator(cls: type[BaseProblemBuilder]) -> type[BaseProblemBuilder]:
        _BUILDER_REGISTRY[problem_type] = cls
        return cls

    return _decorator


def get_builder(problem_type: str) -> BaseProblemBuilder:
    cls = _BUILDER_REGISTRY.get(problem_type)
    if cls is None:
        raise KeyError(f"builder not registered for problem_type={problem_type}")
    return cls()


def registered_problem_types() -> list[str]:
    return sorted(_BUILDER_REGISTRY.keys())
