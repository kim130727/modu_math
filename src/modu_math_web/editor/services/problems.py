from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

from django.conf import settings

from .dsl_format import format_dsl_source

ARTIFACT_FILES = {
    "semantic": ".semantic.json",
    "solvable": ".solvable.json",
    "layout": ".layout.json",
    "renderer": ".renderer.json",
    "svg": ".svg",
}


BLANK_PROBLEM_DSL = '''from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region


PROBLEM_ID = "{problem_id}"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title="{title}",
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=()),
        ),
        slots=(),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("draft",),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {{
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "metadata": {{
        "language": "ko",
        "question": "",
        "instruction": "",
    }},
    "domain": {{
        "objects": [],
        "relations": [],
    }},
    "answer": {{
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": "",
        "unit": "",
    }},
}}

SOLVABLE = {{
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "inputs": {{
        "target_label": "",
        "unit": "",
        "quantities": {{}},
        "conditions": [],
    }},
    "given": [],
    "target": {{
        "ref": "answer.value",
        "type": "unknown",
    }},
    "method": "",
    "plan": [],
    "steps": [],
    "checks": [],
    "answer": {{
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "value": "",
        "unit": "",
    }},
}}
'''


@dataclass(frozen=True)
class ProblemPaths:
    problem_id: str
    root_alias: str
    root_dir: Path
    base_dir: Path
    dsl_path: Path
    artifact_base: str

    def artifact_path(self, key: str) -> Path:
        return self.base_dir / f"{self.artifact_base}{ARTIFACT_FILES[key]}"


def problems_root() -> Path:
    return Path(settings.PROBLEMS_ROOT).resolve()


def problem_roots() -> list[tuple[str, Path]]:
    roots = [("", problems_root())]
    golden_root = Path(
        getattr(settings, "GOLDEN_PROBLEMS_ROOT", Path(settings.BASE_DIR) / "examples" / "golden")
    ).resolve()
    if golden_root != roots[0][1]:
        roots.append(("golden", golden_root))
    return roots


def validate_problem_id(problem_id: str) -> str:
    if not problem_id:
        raise ValueError("problem_id is required")
    normalized = problem_id.replace("\\", "/")
    if normalized.startswith("/"):
        raise ValueError("invalid problem_id")
    parts = PurePosixPath(normalized).parts
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("invalid problem_id")
    return "/".join(parts)


def _split_problem_root(problem_id: str) -> tuple[str, str, Path]:
    parts = problem_id.split("/")
    for alias, root in problem_roots():
        if alias and parts[0] == alias:
            relative_id = "/".join(parts[1:])
            if not relative_id:
                raise ValueError("problem_id is required")
            return alias, relative_id, root
    return "", problem_id, problems_root()


def _display_problem_id(alias: str, relative_id: str) -> str:
    return f"{alias}/{relative_id}" if alias else relative_id


def resolve_problem_paths(problem_id: str) -> ProblemPaths:
    safe_problem_id = validate_problem_id(problem_id)
    alias, relative_id, root = _split_problem_root(safe_problem_id)
    target = (root / relative_id).resolve()
    if target != root and root not in target.parents:
        raise ValueError("invalid problem path")

    if target.exists() and target.is_dir():
        dsl_path = target / "problem.dsl.py"
        if not dsl_path.exists():
            raise FileNotFoundError(f"dsl file not found in folder: {safe_problem_id}")
        return ProblemPaths(
            problem_id=_display_problem_id(alias, relative_id),
            root_alias=alias,
            root_dir=root,
            base_dir=target,
            dsl_path=dsl_path,
            artifact_base="problem",
        )

    if target.exists() and target.is_file() and target.name.endswith(".dsl.py"):
        artifact_base = target.name[: -len(".dsl.py")]
        rel = target.relative_to(root).as_posix()
        return ProblemPaths(
            problem_id=_display_problem_id(alias, rel),
            root_alias=alias,
            root_dir=root,
            base_dir=target.parent,
            dsl_path=target,
            artifact_base=artifact_base,
        )

    raise FileNotFoundError(f"problem not found: {safe_problem_id}")


def _find_solvable_path(base_dir: Path, artifact_base: str) -> Path | None:
    canonical = base_dir / f"{artifact_base}{ARTIFACT_FILES['solvable']}"
    if canonical.exists():
        return canonical
    versioned = sorted(base_dir.glob(f"{artifact_base}.solvable.v*.json"))
    if not versioned:
        return None
    return versioned[-1]


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _is_external_href(value: str) -> bool:
    return (
        not value
        or value.startswith("#")
        or value.startswith("/")
        or value.startswith("data:")
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) is not None
    )


def _asset_url(problem_id: str, filename: str) -> str:
    return f"/api/editor/assets/{quote(problem_id, safe='')}/{quote(filename)}"


def _rewrite_svg_asset_hrefs(svg: str | None, paths: ProblemPaths) -> str | None:
    if svg is None:
        return None

    def replace(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote_char = match.group("quote")
        href = match.group("href")
        if _is_external_href(href):
            return match.group(0)
        if "/" in href or "\\" in href:
            return match.group(0)
        if not (paths.base_dir / href).exists():
            return match.group(0)
        return f"{attr}={quote_char}{_asset_url(paths.problem_id, href)}{quote_char}"

    return re.sub(
        r"(?P<attr>\b(?:href|xlink:href))=(?P<quote>['\"])(?P<href>.*?)(?P=quote)",
        replace,
        svg,
    )


def list_problem_directories() -> list[dict[str, Any]]:
    problems: list[dict[str, Any]] = []
    for alias, root in problem_roots():
        if not root.exists():
            continue
        for dsl_path in sorted(root.rglob("problem.dsl.py")):
            child = dsl_path.parent
            artifact_base = "problem"
            solvable_path = _find_solvable_path(child, artifact_base)
            relative_id = child.relative_to(root).as_posix()
            problems.append(
                {
                    "problem_id": _display_problem_id(alias, relative_id),
                    "root": alias or "problems",
                    "path": str(child.relative_to(root.parent)).replace("\\", "/"),
                    "has_input_png": (child / "input.png").exists(),
                    "has_dsl": True,
                    "has_semantic": (child / f"{artifact_base}{ARTIFACT_FILES['semantic']}").exists(),
                    "has_solvable": solvable_path is not None,
                    "has_layout": (child / f"{artifact_base}{ARTIFACT_FILES['layout']}").exists(),
                    "has_renderer": (child / f"{artifact_base}{ARTIFACT_FILES['renderer']}").exists(),
                    "has_svg": (child / f"{artifact_base}{ARTIFACT_FILES['svg']}").exists(),
                }
            )

        for dsl_path in sorted(root.rglob("*.dsl.py")):
            if dsl_path.name == "problem.dsl.py":
                continue
            child = dsl_path.parent
            artifact_base = dsl_path.name[: -len(".dsl.py")]
            solvable_path = _find_solvable_path(child, artifact_base)
            relative_id = dsl_path.relative_to(root).as_posix()
            problems.append(
                {
                    "problem_id": _display_problem_id(alias, relative_id),
                    "root": alias or "problems",
                    "path": str(child.relative_to(root.parent)).replace("\\", "/"),
                    "has_input_png": (child / "input.png").exists(),
                    "has_dsl": True,
                    "has_semantic": (child / f"{artifact_base}{ARTIFACT_FILES['semantic']}").exists(),
                    "has_solvable": solvable_path is not None,
                    "has_layout": (child / f"{artifact_base}{ARTIFACT_FILES['layout']}").exists(),
                    "has_renderer": (child / f"{artifact_base}{ARTIFACT_FILES['renderer']}").exists(),
                    "has_svg": (child / f"{artifact_base}{ARTIFACT_FILES['svg']}").exists(),
                }
            )
    return sorted(problems, key=lambda p: p["problem_id"])


def read_problem_detail(problem_id: str) -> dict[str, Any]:
    paths = resolve_problem_paths(problem_id)
    dsl = paths.dsl_path.read_text(encoding="utf-8")
    solvable_path = _find_solvable_path(paths.base_dir, paths.artifact_base)
    svg_path = paths.artifact_path("svg")
    return {
        "problem_id": paths.problem_id,
        "base_dir": str(paths.base_dir),
        "dsl": dsl,
        "semantic": _read_json(paths.artifact_path("semantic")),
        "solvable": _read_json(solvable_path) if solvable_path else None,
        "layout": _read_json(paths.artifact_path("layout")),
        "renderer": _read_json(paths.artifact_path("renderer")),
        "svg": _rewrite_svg_asset_hrefs(_read_text(svg_path), paths),
        "svg_url": _asset_url(paths.problem_id, svg_path.name) if svg_path.exists() else None,
    }


def create_blank_problem(problem_id: str, title: str | None = None) -> dict[str, Any]:
    safe_problem_id = validate_problem_id(problem_id)
    alias, relative_id, root = _split_problem_root(safe_problem_id)
    if alias:
        raise ValueError("new problems can only be created under the main problems root")

    target = (root / relative_id).resolve()
    if target != root and root not in target.parents:
        raise ValueError("invalid problem path")

    if target.name.endswith(".dsl.py"):
        dsl_path = target
        base_dir = target.parent
        display_id = relative_id
        template_problem_id = target.name[: -len(".dsl.py")]
        create_parent_only = True
    else:
        base_dir = target
        dsl_path = base_dir / "problem.dsl.py"
        display_id = relative_id
        template_problem_id = PurePosixPath(relative_id).name
        create_parent_only = False

    if dsl_path.exists():
        raise FileExistsError(f"problem already exists: {display_id}")

    base_dir.mkdir(parents=True, exist_ok=create_parent_only)
    clean_title = (title or template_problem_id or "New problem").replace('"', '\\"')
    dsl_path.write_text(
        BLANK_PROBLEM_DSL.format(problem_id=template_problem_id, title=clean_title),
        encoding="utf-8",
    )
    return read_problem_detail(display_id)


def save_problem_dsl(problem_id: str, dsl: str) -> tuple[ProblemPaths, str]:
    paths = resolve_problem_paths(problem_id)
    formatted = format_dsl_source(dsl)
    paths.dsl_path.write_text(formatted, encoding="utf-8")
    return paths, formatted


def format_problem_dsl(problem_id: str) -> tuple[ProblemPaths, str]:
    paths = resolve_problem_paths(problem_id)
    dsl = paths.dsl_path.read_text(encoding="utf-8")
    formatted = format_dsl_source(dsl)
    paths.dsl_path.write_text(formatted, encoding="utf-8")
    return paths, formatted


def read_artifacts(problem_id: str) -> dict[str, Any]:
    paths = resolve_problem_paths(problem_id)
    solvable_path = _find_solvable_path(paths.base_dir, paths.artifact_base)
    svg_path = paths.artifact_path("svg")
    return {
        "semantic": _read_json(paths.artifact_path("semantic")),
        "solvable": _read_json(solvable_path) if solvable_path else None,
        "layout": _read_json(paths.artifact_path("layout")),
        "renderer": _read_json(paths.artifact_path("renderer")),
        "svg": _rewrite_svg_asset_hrefs(_read_text(svg_path), paths),
        "svg_url": _asset_url(paths.problem_id, svg_path.name) if svg_path.exists() else None,
    }
