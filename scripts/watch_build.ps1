param(
    [string]$ProblemId,
    [string]$DslPath,
    [switch]$Once,
    [int]$IntervalSec = 1
)

if (-not $ProblemId -and -not $DslPath) {
    Write-Host "Error: Either -ProblemId or -DslPath must be provided." -ForegroundColor Red
    exit 1
}

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Resolve-DslPath {
    param(
        [string]$RepoRootPath,
        [string]$ProblemIdValue,
        [string]$DslPathValue
    )

    if ($DslPathValue) {
        $resolved = (Resolve-Path -LiteralPath $DslPathValue).Path
        if (-not (Test-Path -LiteralPath $resolved)) {
            throw "DSL file not found: $DslPathValue"
        }
        return $resolved
    }

    if (-not $ProblemIdValue) {
        throw "ProblemId must be provided if DslPath is not specified."
    }

    Write-Host "Searching for DSL file for problem: $ProblemIdValue..." -ForegroundColor Gray
    $searchRoots = @(
        (Join-Path $RepoRootPath "examples\problems"),
        (Join-Path $RepoRootPath "examples\golden")
    )
    $matches = @(
        foreach ($root in $searchRoots) {
            if (Test-Path -LiteralPath $root) {
                Get-ChildItem -Path $root -Filter "*$ProblemIdValue*.dsl.py" -Recurse
            }
        }
    )
    if ($matches.Count -eq 0) {
        throw "DSL file for problem $ProblemIdValue not found in examples\problems or examples\golden"
    }

    # Prefer exact basename match first, then fallback to first partial match.
    $exactName = "$ProblemIdValue.dsl.py"
    $exact = $matches | Where-Object { $_.Name -eq $exactName } | Select-Object -First 1
    if ($exact) {
        return $exact.FullName
    }
    return ($matches | Select-Object -First 1).FullName
}

function Get-FileFingerprint {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash
    return "$($item.Length)|$($item.LastWriteTimeUtc.Ticks)|$hash"
}

$DslPath = Resolve-DslPath -RepoRootPath $RepoRoot -ProblemIdValue $ProblemId -DslPathValue $DslPath

if (-not $ProblemId) {
    # Infer ProblemId from filename (e.g., Hpdf_xxx.dsl.py -> Hpdf_xxx)
    $ProblemId = [System.IO.Path]::GetFileNameWithoutExtension($DslPath).Replace(".dsl", "")
}

$OutPrefix = $DslPath.Replace(".dsl.py", "")
Write-Host "[watch_build] Target DSL: $DslPath" -ForegroundColor Gray

function Invoke-Build {
    Write-Host "[watch_build] Building: $ProblemId" -ForegroundColor Cyan
    $env:PYTHONPATH = Join-Path $RepoRoot "src"
    
    # We pass the paths as environment variables to the Python script
    $env:MODU_DSL_PATH = $DslPath
    $env:MODU_BASE_PATH = $OutPrefix
    $env:MODU_REPO_ROOT = $RepoRoot

    @'
import os
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from modu_math.dsl import (
    ProblemTemplate,
    compile_problem_template_to_layout,
    compile_problem_template_to_semantic,
)
from modu_math.layout.editor_overrides import (
    apply_editor_overrides,
    prune_deleted_legacy_answer_slots,
    prune_editor_overrides,
    prune_legacy_answer_blank_slots,
)
from modu_math.pipeline.answer_contracts import validate_answer_slot_contract
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import inline_local_image_hrefs, render_svg
from modu_math.pipeline.validate_contracts import validate_semantic_solvable_answer_match
from modu_math.pipeline.tutor_renderer_flow import attach_tutor_renderer_flow, validate_tutor_renderer_flow

repo = Path(os.environ["MODU_REPO_ROOT"])
dsl_path = Path(os.environ["MODU_DSL_PATH"])
base = Path(os.environ["MODU_BASE_PATH"])

# Load DSL module
spec = importlib.util.spec_from_file_location("problem_dsl_module", dsl_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

# Get PROBLEM_TEMPLATE
if hasattr(module, "PROBLEM_TEMPLATE") and isinstance(module.PROBLEM_TEMPLATE, ProblemTemplate):
    problem = module.PROBLEM_TEMPLATE
elif hasattr(module, "build_problem_template"):
    problem = module.build_problem_template()
else:
    raise ValueError(f"DSL file {dsl_path} does not define PROBLEM_TEMPLATE or build_problem_template()")

# Compilation
semantic = compile_problem_template_to_semantic(problem, problem_type="diagram_problem")
layout = compile_problem_template_to_layout(problem)

deleted_answer_slots = set()
editor_overrides_path = base.with_suffix(".editor_overrides.json")
if editor_overrides_path.exists():
    editor_overrides = json.loads(editor_overrides_path.read_text(encoding="utf-8-sig"))
    editor_overrides, pruned = prune_editor_overrides(layout, editor_overrides)
    editor_overrides, answer_pruned = prune_deleted_legacy_answer_slots(
        layout,
        editor_overrides,
        semantic.get("answer"),
    )
    pruned = pruned or answer_pruned
    deleted_slots = editor_overrides.get("deleted_slots") if isinstance(editor_overrides, dict) else None
    if isinstance(deleted_slots, list):
        deleted_answer_slots = {slot_id for slot_id in deleted_slots if isinstance(slot_id, str)}
    if pruned:
        editor_overrides_path.write_text(
            json.dumps(editor_overrides, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    layout = apply_editor_overrides(layout, editor_overrides)

def deep_merge_dict(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = deep_merge_dict(out[key], value)
        else:
            out[key] = value
    return out

def parse_solvable_schema_tag(solvable: dict) -> str:
    schema_value = solvable.get("schema")
    if not isinstance(schema_value, str):
        raise ValueError("SOLVABLE['schema'] must be a string like 'modu.solvable.v1.1', 'modu.solvable.v1.2', or 'modu.solvable.v1.3'.")
    prefix = "modu.solvable."
    if not schema_value.startswith(prefix):
        raise ValueError(f"Unsupported solvable schema format: {schema_value}")
    tag = schema_value[len(prefix):]
    if not tag:
        raise ValueError(f"Invalid solvable schema tag: {schema_value}")
    return tag

def normalize_solvable_for_schema(solvable: dict) -> dict:
    normalized = dict(solvable)
    if isinstance(normalized.get("plan"), str):
        normalized["plan"] = [normalized["plan"]]
    return normalized

def submitted_answer_slot_ids(layout: dict) -> list[str]:
    slot_ids = []
    for slot in layout.get("slots", []):
        if not isinstance(slot, dict):
            continue
        slot_id = slot.get("id")
        content = slot.get("content")
        interaction = content.get("interaction") if isinstance(content, dict) else None
        if (
            isinstance(slot_id, str)
            and isinstance(interaction, dict)
            and interaction.get("role") == "answer"
            and interaction.get("type") == "input"
            and interaction.get("include_in_submission") is not False
        ):
            slot_ids.append(slot_id)
    return slot_ids

def answer_slot_ids(answer) -> set[str]:
    if not isinstance(answer, dict):
        return set()
    out = set()
    for key in ("blanks", "answer_key"):
        items = answer.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            slot_id = item.get("slot_id") or item.get("id") or item.get("blank_id")
            if isinstance(slot_id, str) and slot_id.strip():
                out.add(slot_id)
    return out

def with_single_submit_slot_answer(answer, slot_id: str):
    if not isinstance(answer, dict):
        return answer
    value = answer.get("value")
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return answer
    if answer_slot_ids(answer) == {slot_id}:
        return answer
    normalized = dict(answer)
    normalized["blanks"] = [{"id": slot_id, "slot_id": slot_id, "expected": value}]
    normalized["answer_key"] = [{"slot_id": slot_id, "value": value}]
    return normalized

def attach_single_submit_slot_answer(layout: dict, semantic: dict, solvable):
    submit_slot_ids = submitted_answer_slot_ids(layout)
    if len(submit_slot_ids) != 1:
        return semantic, solvable
    slot_id = submit_slot_ids[0]
    semantic_answer = with_single_submit_slot_answer(semantic.get("answer"), slot_id)
    if semantic_answer is not semantic.get("answer"):
        semantic = dict(semantic)
        semantic["answer"] = semantic_answer
    if isinstance(solvable, dict):
        solvable_answer = with_single_submit_slot_answer(solvable.get("answer"), slot_id)
        if solvable_answer is not solvable.get("answer"):
            solvable = dict(solvable)
            solvable["answer"] = solvable_answer
    return semantic, solvable

# Optional: Semantic override (inject/replace selected semantic fields from DSL)
if hasattr(module, "SEMANTIC_OVERRIDE"):
    semantic_override = module.SEMANTIC_OVERRIDE
    if isinstance(semantic_override, dict):
        semantic = deep_merge_dict(semantic, semantic_override)
    else:
        raise ValueError("SEMANTIC_OVERRIDE must be a dict when provided.")

# Optional: Semantic Answer (inject if defined in DSL)
if hasattr(module, "SEMANTIC_ANSWER"):
    semantic["answer"] = module.SEMANTIC_ANSWER

# Optional: Solvable JSON (inject if defined in DSL)
solvable = None
if hasattr(module, "SOLVABLE"):
    solvable = module.SOLVABLE
elif hasattr(module, "build_solvable"):
    solvable = module.build_solvable()

layout, auto_deleted_answer_slots = prune_legacy_answer_blank_slots(layout, semantic.get("answer"))
deleted_answer_slots.update(auto_deleted_answer_slots)
semantic, solvable = attach_single_submit_slot_answer(layout, semantic, solvable if isinstance(solvable, dict) else None)

renderer = compile_renderer_json(layout)
if hasattr(module, "TUTOR_RENDERER_FLOW"):
    renderer = attach_tutor_renderer_flow(renderer, module.TUTOR_RENDERER_FLOW)
svg = inline_local_image_hrefs(render_svg(renderer), base.parent)

# Validation
semantic_schema = json.loads((repo / "schema/semantic/semantic.v1.json").read_text(encoding="utf-8-sig"))
layout_schema = json.loads((repo / "schema/layout/layout.v1.json").read_text(encoding="utf-8-sig"))
renderer_schema = json.loads((repo / "schema/renderer/renderer.v1.json").read_text(encoding="utf-8-sig"))

Draft202012Validator(semantic_schema).validate(semantic)
Draft202012Validator(layout_schema).validate(layout)
Draft202012Validator(renderer_schema).validate(renderer)
validate_tutor_renderer_flow(renderer, solvable if isinstance(solvable, dict) else None)

if solvable:
    if not isinstance(solvable, dict):
        raise ValueError("SOLVABLE must be a dict when provided.")
    solvable = normalize_solvable_for_schema(solvable)
    solvable_tag = parse_solvable_schema_tag(solvable)
    solvable_schema_path = repo / "schema/solvable" / f"solvable.{solvable_tag}.json"
    if not solvable_schema_path.exists():
        raise FileNotFoundError(
            f"Solvable schema file not found for '{solvable.get('schema')}': {solvable_schema_path}"
        )
    solvable_schema = json.loads(solvable_schema_path.read_text(encoding="utf-8-sig"))
    Draft202012Validator(solvable_schema).validate(solvable)
    validate_semantic_solvable_answer_match(semantic, solvable)

validate_answer_slot_contract(
    layout=layout,
    semantic=semantic,
    solvable=solvable if isinstance(solvable, dict) else None,
    deleted_slots=deleted_answer_slots,
)

# Save Outputs
base.with_suffix(".semantic.json").write_text(json.dumps(semantic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".renderer.json").write_text(json.dumps(renderer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".svg").write_text(svg, encoding="utf-8")

if solvable:
    solvable_tag = parse_solvable_schema_tag(solvable)
    base.with_suffix(f".solvable.{solvable_tag}.json").write_text(
        json.dumps(solvable, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

print("build_ok")
'@ | & $PythonExe -

    if ($LASTEXITCODE -ne 0) {
        throw "Build failed (exit code: $LASTEXITCODE)"
    }
    Write-Host "[watch_build] Build complete." -ForegroundColor Green
}

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Python not found: $PythonExe"
}

if ($Once) {
    Invoke-Build
    exit 0
}

Write-Host "[watch_build] Watching: $DslPath" -ForegroundColor Yellow
Write-Host "[watch_build] Press Ctrl+C to stop." -ForegroundColor Yellow

$lastFingerprint = Get-FileFingerprint -Path $DslPath
Invoke-Build

while ($true) {
    Start-Sleep -Seconds $IntervalSec
    $currentFingerprint = Get-FileFingerprint -Path $DslPath
    if ($currentFingerprint -ne $lastFingerprint) {
        $lastFingerprint = $currentFingerprint
        Invoke-Build
    }
}
