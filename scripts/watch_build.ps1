param(
    [Parameter(Mandatory=$true)]
    [string]$ProblemId,
    [string]$DslPath,
    [switch]$Once,
    [int]$IntervalSec = 1
)

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

    Write-Host "Searching for DSL file for problem: $ProblemIdValue..." -ForegroundColor Gray
    $root = Join-Path $RepoRootPath "examples\problems"
    $matches = @(Get-ChildItem -Path $root -Filter "*$ProblemIdValue*.dsl.py" -Recurse)
    if ($matches.Count -eq 0) {
        throw "DSL file for problem $ProblemIdValue not found in examples\problems"
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
$OutPrefix = $DslPath.Replace(".dsl.py", "")
Write-Host "[watch_build] Target DSL: $DslPath" -ForegroundColor Gray

function Invoke-Build {
    Write-Host "[watch_build] Building from DSL: $ProblemId" -ForegroundColor Cyan
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
from modu_math.renderer.compiler import compile_renderer_json
from modu_math.renderer.svg.render import render_svg

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
renderer = compile_renderer_json(layout)
svg = render_svg(renderer)

def deep_merge_dict(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = deep_merge_dict(out[key], value)
        else:
            out[key] = value
    return out

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

# Validation
semantic_schema = json.loads((repo / "schema/semantic/semantic.v1.json").read_text(encoding="utf-8-sig"))
layout_schema = json.loads((repo / "schema/layout/layout.v1.json").read_text(encoding="utf-8-sig"))
renderer_schema = json.loads((repo / "schema/renderer/renderer.v1.json").read_text(encoding="utf-8-sig"))

Draft202012Validator(semantic_schema).validate(semantic)
Draft202012Validator(layout_schema).validate(layout)
Draft202012Validator(renderer_schema).validate(renderer)

# Save Outputs
base.with_suffix(".semantic.json").write_text(json.dumps(semantic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".renderer.json").write_text(json.dumps(renderer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
base.with_suffix(".svg").write_text(svg, encoding="utf-8")

if solvable:
    solvable_schema = json.loads((repo / "schema/solvable/solvable.v1.json").read_text(encoding="utf-8-sig"))
    Draft202012Validator(solvable_schema).validate(solvable)
    base.with_suffix(".solvable.v1.json").write_text(json.dumps(solvable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
