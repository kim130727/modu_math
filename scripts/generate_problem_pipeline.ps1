[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProblemId,

    [Parameter(Mandatory = $true)]
    [string]$Dir,

    [string]$Provider = "openai",
    [string]$Mode = "api",
    [int]$DslMaxAttempts = 8
)

$ErrorActionPreference = "Stop"

if ($env:PYTHONUTF8 -ne "1") { $env:PYTHONUTF8 = "1" }
if ($env:PYTHONIOENCODING -ne "utf-8") { $env:PYTHONIOENCODING = "utf-8" }

$img = Join-Path $Dir "$ProblemId.png"
$visionDraft = Join-Path $Dir "$ProblemId.vision_draft.md"
$visionPrompt = Join-Path $Dir "$ProblemId.vision_prompt.md"
$visionLlm = Join-Path $Dir "$ProblemId.vision_llm_output.txt"

$refinedDraft = Join-Path $Dir "$ProblemId.refined_draft.md"
$refinePrompt = Join-Path $Dir "$ProblemId.refine_prompt.md"
$refineLlm = Join-Path $Dir "$ProblemId.refine_llm_output.txt"

$dslPath = Join-Path $Dir "$ProblemId.dsl.py"
$dslPrompt = Join-Path $Dir "$ProblemId.dsl_prompt.md"
$dslLlm = Join-Path $Dir "$ProblemId.dsl_llm_output.txt"
$buildReport = Join-Path $Dir "$ProblemId.build_report.json"

if (-not (Test-Path $img)) {
    throw "Image not found: $img"
}

Write-Host "[1/6] Generate vision draft (+prompt, +llm output)"
python tools/generate_vision_draft.py `
  --image "$img" `
  --problem-id "$ProblemId" `
  --out "$visionDraft" `
  --mode "$Mode" `
  --provider "$Provider" `
  --prompt-out "$visionPrompt" `
  --llm-output-file "$visionLlm" `
  --force

Write-Host "[2/6] Refine vision draft (+prompt, +llm output)"
python tools/refine_vision_draft.py `
  --vision-draft "$visionDraft" `
  --problem-id "$ProblemId" `
  --image "$img" `
  --out "$refinedDraft" `
  --mode "$Mode" `
  --provider "$Provider" `
  --prompt-out "$refinePrompt" `
  --llm-output-file "$refineLlm" `
  --force

Write-Host "[3/6] Generate DSL (+prompt, +llm output)"
python tools/generate_dsl_from_refined_draft.py `
  --draft "$refinedDraft" `
  --image "$img" `
  --problem-id "$ProblemId" `
  --out "$dslPath" `
  --mode "$Mode" `
  --provider "$Provider" `
  --llm-output-file "$dslLlm" `
  --system-prompt "prompts/dsl_agent_system.md" `
  --rules-md "prompts/dsl_generation_rules.md" `
  --prompt-out "$dslPrompt" `
  --max-attempts $DslMaxAttempts `
  --force

Write-Host "[4/6] Validate generated DSL (strict + solvable)"
python tools/validate_generated_dsl.py `
  --dsl "$dslPath" `
  --out-prefix "$Dir/$ProblemId" `
  --strict `
  --emit-solvable `
  --report "$buildReport"

Write-Host "[5/6] Final mb check"
mb $ProblemId

Write-Host "[6/6] Done"
