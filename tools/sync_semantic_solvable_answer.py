from __future__ import annotations

import argparse
import ast
import importlib.util
import sys
from pathlib import Path
from typing import Any

from modu_math.dsl.models.exporter import compile_problem_template_to_semantic


def deep_merge_dict(base: Any, override: Any) -> Any:
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def normalize_answer(value: Any) -> Any:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for k, v in value.items():
            if k == "confidence":
                continue
            out[k] = normalize_answer(v)
        return out
    if isinstance(value, list):
        return [normalize_answer(item) for item in value]
    return value


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("dsl_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module from: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_top_level_assignment(tree: ast.Module, name: str, value: Any) -> bool:
    replacement = ast.parse(repr(value), mode="eval").body
    for idx, stmt in enumerate(tree.body):
        if not isinstance(stmt, ast.Assign):
            continue
        for target in stmt.targets:
            if isinstance(target, ast.Name) and target.id == name:
                tree.body[idx] = ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=replacement)
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync SEMANTIC_OVERRIDE['answer'] and SOLVABLE['answer'] for mb/watch_build compatibility."
    )
    parser.add_argument("--dsl", required=True, help="Path to *.dsl.py")
    args = parser.parse_args()

    dsl_path = Path(args.dsl)
    if not dsl_path.exists():
        raise SystemExit(f"DSL not found: {dsl_path}")

    try:
        module = load_module(dsl_path)
    except Exception as exc:
        print(f"Skip sync (load failed): {dsl_path} :: {exc}")
        return 0
    semantic_override = getattr(module, "SEMANTIC_OVERRIDE", None)
    solvable = getattr(module, "SOLVABLE", None)
    problem_template = getattr(module, "PROBLEM_TEMPLATE", None)
    if not isinstance(semantic_override, dict) or not isinstance(solvable, dict) or problem_template is None:
        print(f"Skip sync (missing structures): {dsl_path}")
        return 0

    semantic = compile_problem_template_to_semantic(problem_template, problem_type="diagram_problem")
    merged_semantic = deep_merge_dict(semantic, semantic_override)
    semantic_answer = normalize_answer(merged_semantic.get("answer", {}))
    if not isinstance(semantic_answer, dict):
        raise SystemExit("Merged semantic answer is not a dict.")

    new_semantic_override = dict(semantic_override)
    new_semantic_override["answer"] = semantic_answer

    new_solvable = dict(solvable)
    new_solvable["answer"] = semantic_answer

    source = dsl_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    ok_sem = replace_top_level_assignment(tree, "SEMANTIC_OVERRIDE", new_semantic_override)
    ok_sol = replace_top_level_assignment(tree, "SOLVABLE", new_solvable)
    if not ok_sem or not ok_sol:
        raise SystemExit("Failed to locate top-level SEMANTIC_OVERRIDE/SOLVABLE assignments.")

    ast.fix_missing_locations(tree)
    output = ast.unparse(tree) + "\n"
    dsl_path.write_text(output, encoding="utf-8", newline="\n")
    print(f"Synchronized answers: {dsl_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

