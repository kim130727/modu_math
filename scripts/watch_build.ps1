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
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $Utf8NoBom
[Console]::OutputEncoding = $Utf8NoBom
$OutputEncoding = $Utf8NoBom
if ($env:PYTHONUTF8 -ne "1") { $env:PYTHONUTF8 = "1" }
if ($env:PYTHONIOENCODING -ne "utf-8") { $env:PYTHONIOENCODING = "utf-8" }

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

    # Prefer exact basename match first. If only split copies exist, forcing an
    # explicit suffix avoids building one artifact with another artifact's id.
    $exactName = "$ProblemIdValue.dsl.py"
    $exact = $matches | Where-Object { $_.Name -eq $exactName } | Select-Object -First 1
    if ($exact) {
        return $exact.FullName
    }
    if ($matches.Count -gt 1) {
        $candidateNames = ($matches | Select-Object -ExpandProperty Name) -join ", "
        throw "Exact DSL file not found for $ProblemIdValue. Multiple partial matches exist; use one explicit problem id: $candidateNames"
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
from modu_math.layout.sanitizer import sanitize_layout
from modu_math.pipeline.answer_contracts import normalize_answer_for_deleted_slots, normalize_answer_for_submit_slots, validate_answer_slot_contract
from modu_math.pipeline.semantic_normalizer import normalize_semantic_for_schema
from modu_math.pipeline.subproblem_projection import project_suffixed_subproblem
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
editor_override_slot_ids = set()
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
    override_slots = editor_overrides.get("slots") if isinstance(editor_overrides, dict) else None
    if isinstance(override_slots, dict):
        editor_override_slot_ids = {slot_id for slot_id in override_slots if isinstance(slot_id, str)}
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
    return [slot["slot_id"] for slot in submitted_answer_slots(layout)]

def submitted_answer_slots(layout: dict) -> list[dict]:
    slots = []
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
            slots.append({
                "slot_id": slot_id,
                "answer_key_index": interaction.get("answer_key_index"),
                "answer_ref": interaction.get("answer_ref"),
                "order": interaction.get("order"),
            })
    return slots

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

def attach_submit_slot_answers(layout: dict, semantic: dict, solvable):
    submit_slots = submitted_answer_slots(layout)
    if not submit_slots:
        return semantic, solvable
    semantic_answer, semantic_changed = normalize_answer_for_submit_slots(semantic.get("answer"), submit_slots)
    if semantic_changed:
        semantic = dict(semantic)
        semantic["answer"] = semantic_answer
    if isinstance(solvable, dict):
        solvable_answer, solvable_changed = normalize_answer_for_submit_slots(solvable.get("answer"), submit_slots)
        if solvable_changed:
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

semantic, _semantic_normalized = normalize_semantic_for_schema(semantic)

layout, semantic, solvable, projected_deleted_slots = project_suffixed_subproblem(
    artifact_id=base.name,
    template_id=getattr(problem, "id", None),
    layout=layout,
    semantic=semantic,
    solvable=solvable if isinstance(solvable, dict) else None,
    protected_slot_ids=editor_override_slot_ids,
)
deleted_answer_slots.update(projected_deleted_slots)

layout, auto_deleted_answer_slots = prune_legacy_answer_blank_slots(layout, semantic.get("answer"))
deleted_answer_slots.update(auto_deleted_answer_slots)
layout = sanitize_layout(
    layout,
    deleted_slots=deleted_answer_slots,
    protected_slot_ids=editor_override_slot_ids,
)
semantic, solvable = attach_submit_slot_answers(layout, semantic, solvable if isinstance(solvable, dict) else None)
semantic_answer, removed_semantic_answer_slots = normalize_answer_for_deleted_slots(
    semantic.get("answer"),
    deleted_answer_slots,
)
if removed_semantic_answer_slots:
    semantic = dict(semantic)
    semantic["answer"] = semantic_answer
if isinstance(solvable, dict):
    solvable_answer, removed_solvable_answer_slots = normalize_answer_for_deleted_slots(
        solvable.get("answer"),
        deleted_answer_slots,
    )
    if removed_solvable_answer_slots:
        solvable = dict(solvable)
        solvable["answer"] = solvable_answer

semantic, _semantic_normalized = normalize_semantic_for_schema(semantic)

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
    solvable, _solvable_normalized = normalize_semantic_for_schema(solvable)
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
    
    # Sync generated artifacts to Flutter assets build directories
    $dslDir = [System.IO.Path]::GetDirectoryName($DslPath)
    $relDir = $dslDir.Substring($RepoRoot.Length).TrimStart('\', '/')
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($DslPath).Replace(".dsl", "")
    $destDirs = @(
        (Join-Path $RepoRoot "apps\mobile\build\flutter_assets\$relDir"),
        (Join-Path $RepoRoot "apps\mobile\build\unit_test_assets\$relDir")
    )
    foreach ($dest in $destDirs) {
        if (Test-Path $dest) {
            Get-ChildItem -Path $dslDir -Filter "$baseName.*" | ForEach-Object {
                Copy-Item -Path $_.FullName -Destination $dest -Force
            }
        }
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
