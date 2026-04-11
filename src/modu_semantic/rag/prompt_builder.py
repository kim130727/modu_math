from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _safe_read(path: Path, max_chars: int = 1200) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    if len(text) > max_chars:
        return text[:max_chars] + "\n# ...truncated..."
    return text


def _semantic_summary(path: Path) -> str:
    if not path.exists():
        return "semantic summary unavailable"
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return "semantic summary unavailable"

    problem_type = doc.get("problem_type", "unknown")
    render = doc.get("render") if isinstance(doc, dict) else {}
    elements = render.get("elements", []) if isinstance(render, dict) else []
    element_types = sorted({str(el.get("type")) for el in elements if isinstance(el, dict) and el.get("type")})
    return f"problem_type={problem_type}, element_types={element_types}, element_count={len(elements)}"


def build_few_shot_prompt(
    *,
    input_meta: dict[str, Any],
    retrieved_examples: list[dict[str, Any]],
    examples_root: str | Path = "examples/problem",
) -> str:
    root = Path(examples_root)

    lines: list[str] = []
    lines.append("# Role")
    lines.append("You generate Python DSL for modu_semantic. Reuse patterns from retrieved examples.")
    lines.append("")
    lines.append("# Current Input Features")
    lines.append(json.dumps(input_meta, ensure_ascii=False, indent=2))
    lines.append("")
    lines.append("# Contract Rules")
    lines.append("- Keep semantic/layout canonical contract valid.")
    lines.append("- Prefer simple, readable DSL composition.")
    lines.append("- Do not invent unsupported primitives.")
    lines.append("")
    lines.append("# Retrieved Few-Shot Examples")

    if not retrieved_examples:
        lines.append("- No retrieved examples. Use generic minimal Problem/Rect/Text pattern.")
    else:
        for index, item in enumerate(retrieved_examples, start=1):
            entry = item.get("entry", {})
            score = item.get("score", 0.0)
            problem_id = entry.get("problem_id", "unknown")
            py_path = root / str(entry.get("py_path", ""))
            semantic_path = root / str(entry.get("semantic_path", ""))

            lines.append(f"## Example {index}: {problem_id} (score={score:.2f})")
            lines.append(f"- py_path: {entry.get('py_path', '')}")
            lines.append(f"- semantic_path: {entry.get('semantic_path', '')}")
            lines.append(f"- tags: {entry.get('tags', [])}")
            lines.append(f"- primitives: {entry.get('visual_primitives', [])}")
            lines.append(f"- semantic_summary: {_semantic_summary(semantic_path)}")
            lines.append("- py_dsl_snippet:")
            snippet = _safe_read(py_path)
            if snippet:
                lines.append("```python")
                lines.append(snippet)
                lines.append("```")
            else:
                lines.append("  (missing)")
            lines.append("")

    lines.append("# Output Requirement")
    lines.append("Return only Python code with build() -> Problem.")
    lines.append("Ensure Problem.save/build path can pass validation.")

    return "\n".join(lines).strip() + "\n"
