param(
  [string]$ListFile = "txt/problems_list.txt",
  [ValidateSet("openai", "google")]
  [string]$Provider = "openai",
  [ValidateSet("openai", "google")]
  [string]$Phase1Provider,
  [ValidateSet("openai", "google")]
  [string]$Phase2Provider,
  [ValidateSet("api", "prompt")]
  [string]$Mode = "api",
  [int]$DslMaxAttempts = 1,
  [switch]$RunMb,
  [string]$Model,
  [ValidateSet("low", "high", "auto")]
  [string]$VisionDetail = "low",
  [ValidateSet("low", "high", "auto")]
  [string]$DslImageDetail = "low",
  [switch]$CompactDslPrompt,
  [switch]$UseVisionStructured
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$PythonExe = "python"
$RepoVenvPython = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $RepoVenvPython) {
  $PythonExe = $RepoVenvPython
}
Write-Host "Python=$PythonExe"

function Invoke-Step {
  param(
    [Parameter(Mandatory = $true)][string]$Title,
    [Parameter(Mandatory = $true)][scriptblock]$Action
  )
  Write-Host ""
  Write-Host "=== $Title ===" -ForegroundColor Cyan
  & $Action
}

function Invoke-Python {
  param([Parameter(Mandatory = $true)][string[]]$Args)
  & $PythonExe @Args
  if ($LASTEXITCODE -ne 0) {
    throw "$PythonExe command failed: $($Args -join ' ')"
  }
}

if (!(Test-Path -LiteralPath $ListFile)) {
  throw "List file not found: $ListFile"
}

$rows = @(Get-Content -LiteralPath $ListFile -Encoding UTF8)
if (!$rows -or $rows.Count -eq 0) {
  throw "List file is empty: $ListFile"
}

$validRows = @()
foreach ($line in $rows) {
  $trim = $line.Trim()
  if ($trim -eq "" -or $trim.StartsWith("#")) { continue }
  $dir = ""
  $probId = ""

  $parts = $trim -split ",", 2
  if ($parts.Count -eq 2) {
    # Legacy format: dir,prob_id
    $dir = $parts[0].Trim()
    $probId = $parts[1].Trim()
    if ($dir -eq "" -or $probId -eq "") {
      throw "Invalid line format: '$line'. dir/prob_id cannot be empty."
    }
  } else {
    # Base-path format: examples/problems/.../PROB_ID (no extension)
    $base = $trim -replace "\\", "/"
    $base = $base -replace "\.(png|json)$", ""
    $base = $base.Trim()
    if ($base -eq "") {
      throw "Invalid line format: '$line'. Base path cannot be empty."
    }
    $dir = Split-Path -Path $base -Parent
    $probId = Split-Path -Path $base -Leaf
    if ($dir -eq "" -or $probId -eq "") {
      throw "Invalid base path format: '$line'. Expected: .../<prob_id> or dir,prob_id"
    }
  }

  $validRows += [PSCustomObject]@{
    Dir = $dir
    ProbId = $probId
  }
}

if ($validRows.Count -eq 0) {
  throw "No executable rows in list file: $ListFile"
}

Write-Host "Provider=$Provider, Mode=$Mode, Items=$($validRows.Count), UseVisionStructured=$UseVisionStructured"

$resolvedPhase1Provider = if ($Phase1Provider) { $Phase1Provider } else { $Provider }
$resolvedPhase2Provider = if ($Phase2Provider) { $Phase2Provider } else { $Provider }
Write-Host "Phase1Provider=$resolvedPhase1Provider (vision/refine), Phase2Provider=$resolvedPhase2Provider (dsl)"

foreach ($row in $validRows) {
  try {
  $dir = $row.Dir
  $probId = $row.ProbId
  $img = Join-Path $dir "$probId.png"
  $sourceProblemJson = Join-Path $dir "$probId.json"

  Write-Host ""
  Write-Host "########################################" -ForegroundColor Yellow
  Write-Host "Processing: dir=$dir, prob_id=$probId" -ForegroundColor Yellow
  Write-Host "########################################" -ForegroundColor Yellow

  if (!(Test-Path -LiteralPath $dir)) {
    throw "Directory not found: $dir"
  }
  if (!(Test-Path -LiteralPath $img)) {
    throw "Image not found: $img"
  }
  if (Test-Path -LiteralPath $sourceProblemJson) {
    Write-Host "Reference source problem json found: $sourceProblemJson" -ForegroundColor DarkGray
  } else {
    Write-Host "Reference source problem json not found (optional): $sourceProblemJson" -ForegroundColor DarkGray
  }

  $visionDraft = Join-Path $dir "$probId.vision_draft.md"
  $visionPrompt = Join-Path $dir "$probId.vision_prompt.md"
  $visionLlm = Join-Path $dir "$probId.vision_llm_output.txt"
  $visionStructured = Join-Path $dir "$probId.vision_structured.json"
  $visionStructuredPrompt = Join-Path $dir "$probId.vision_structured_prompt.md"
  $visionStructuredLlm = Join-Path $dir "$probId.vision_structured_llm_output.txt"

  $refinedDraft = Join-Path $dir "$probId.refined_draft.md"
  $refinePrompt = Join-Path $dir "$probId.refine_prompt.md"
  $refineLlm = Join-Path $dir "$probId.refine_llm_output.txt"

  $dslPy = Join-Path $dir "$probId.dsl.py"
  $dslPrompt = Join-Path $dir "$probId.dsl_prompt.md"
  $dslLlm = Join-Path $dir "$probId.dsl_llm_output.txt"
  $dslFailureReport = Join-Path $dir "$probId.dsl_failure_report.json"
  $report = Join-Path $dir "$probId.build_report.json"
  $visualReport = Join-Path $dir "$probId.visual_alignment_report.json"

  $commonModelArgs = @()
  if ($Model) {
    $commonModelArgs = @("--model", $Model)
  }
  $sourceJsonArgs = @()
  if (Test-Path -LiteralPath $sourceProblemJson) {
    $sourceJsonArgs = @("--source-problem-json", $sourceProblemJson)
  }

  Invoke-Step "1) Generate vision prompt bundle" {
    $args = @(
      "tools/generate_vision_draft.py",
      "--image", $img,
      "--problem-id", $probId,
      "--out", $visionDraft,
      "--mode", "prompt",
      "--provider", $resolvedPhase1Provider,
      "--detail", $VisionDetail,
      "--prompt-out", $visionPrompt,
      "--force"
    ) + $commonModelArgs
    Invoke-Python -Args $args
  }

  if ($Mode -eq "api") {
    Invoke-Step "2) Generate vision draft via API" {
      $args = @(
        "tools/generate_vision_draft.py",
        "--image", $img,
        "--problem-id", $probId,
        "--out", $visionDraft,
        "--mode", "api",
        "--provider", $resolvedPhase1Provider,
        "--detail", $VisionDetail,
        "--force"
      ) + $commonModelArgs
      Invoke-Python -Args $args
    }
  } else {
    if (!(Test-Path -LiteralPath $visionLlm)) {
      throw "Missing file for prompt mode: $visionLlm"
    }
    Invoke-Step "2) Generate vision draft from llm output file" {
      $args = @(
        "tools/generate_vision_draft.py",
        "--image", $img,
        "--problem-id", $probId,
        "--out", $visionDraft,
        "--mode", "prompt",
        "--provider", $resolvedPhase1Provider,
        "--detail", $VisionDetail,
        "--llm-output-file", $visionLlm,
        "--force"
      ) + $commonModelArgs
      Invoke-Python -Args $args
    }
  }

  if ($UseVisionStructured) {
    Invoke-Step "3) Generate structured vision JSON prompt bundle" {
      $args = @(
        "tools/generate_vision_structured.py",
        "--image", $img,
        "--problem-id", $probId,
        "--out", $visionStructured,
        "--vision-draft", $visionDraft,
        "--mode", "prompt",
        "--provider", $resolvedPhase1Provider,
        "--detail", $VisionDetail,
        "--prompt-out", $visionStructuredPrompt,
        "--force"
      ) + $commonModelArgs
      Invoke-Python -Args $args
    }

    if ($Mode -eq "api") {
      Invoke-Step "4) Generate structured vision JSON via API" {
        $args = @(
          "tools/generate_vision_structured.py",
          "--image", $img,
          "--problem-id", $probId,
          "--out", $visionStructured,
          "--vision-draft", $visionDraft,
          "--mode", "api",
          "--provider", $resolvedPhase1Provider,
          "--detail", $VisionDetail,
          "--force"
        ) + $commonModelArgs
        Invoke-Python -Args $args
      }
    } else {
      if (!(Test-Path -LiteralPath $visionStructuredLlm)) {
        throw "Missing file for prompt mode: $visionStructuredLlm"
      }
      Invoke-Step "4) Generate structured vision JSON from llm output file" {
        $args = @(
          "tools/generate_vision_structured.py",
          "--image", $img,
          "--problem-id", $probId,
          "--out", $visionStructured,
          "--vision-draft", $visionDraft,
          "--mode", "prompt",
          "--provider", $resolvedPhase1Provider,
          "--detail", $VisionDetail,
          "--llm-output-file", $visionStructuredLlm,
          "--force"
        ) + $commonModelArgs
        Invoke-Python -Args $args
      }
    }
  } else {
    Write-Host "Skipping structured vision JSON (pass -UseVisionStructured to enable)." -ForegroundColor DarkGray
  }

  Invoke-Step "5) Generate refine prompt bundle" {
    $args = @(
      "tools/refine_vision_draft.py",
      "--vision-draft", $visionDraft,
      "--problem-id", $probId,
      "--image", $img,
      "--out", $refinedDraft,
      "--mode", "prompt",
      "--provider", $resolvedPhase1Provider,
      "--detail", $VisionDetail,
      "--prompt-out", $refinePrompt,
      "--force"
    ) + $commonModelArgs
    Invoke-Python -Args $args
  }

  if ($Mode -eq "api") {
    Invoke-Step "6) Generate refined draft via API" {
      $args = @(
        "tools/refine_vision_draft.py",
        "--vision-draft", $visionDraft,
        "--problem-id", $probId,
        "--image", $img,
        "--out", $refinedDraft,
        "--mode", "api",
        "--provider", $resolvedPhase1Provider,
        "--detail", $VisionDetail,
        "--force"
      ) + $commonModelArgs
      Invoke-Python -Args $args
    }
  } else {
    if (!(Test-Path -LiteralPath $refineLlm)) {
      throw "Missing file for prompt mode: $refineLlm"
    }
    Invoke-Step "6) Generate refined draft from llm output file" {
      $args = @(
        "tools/refine_vision_draft.py",
        "--vision-draft", $visionDraft,
        "--problem-id", $probId,
        "--image", $img,
        "--out", $refinedDraft,
        "--mode", "prompt",
        "--provider", $resolvedPhase1Provider,
        "--detail", $VisionDetail,
        "--llm-output-file", $refineLlm,
        "--force"
      ) + $commonModelArgs
      Invoke-Python -Args $args
    }
  }

  Invoke-Step "7) Generate DSL prompt bundle" {
    $args = @(
      "tools/generate_dsl_from_refined_draft.py",
      "--draft", $refinedDraft,
      "--image", $img,
      "--problem-id", $probId,
      "--out", $dslPy,
      "--mode", "prompt",
      "--provider", $resolvedPhase2Provider,
      "--system-prompt", "prompts/dsl_agent_system.md",
      "--rules-md", "prompts/dsl_generation_rules.md",
      "--max-attempts", "$DslMaxAttempts",
      "--image-detail", $DslImageDetail,
      "--write-on-fail",
      "--failure-report", $dslFailureReport,
      "--prompt-out", $dslPrompt,
      "--force"
    ) + $sourceJsonArgs + $commonModelArgs
    if ($UseVisionStructured) { $args += @("--vision-structured", $visionStructured) }
    if ($CompactDslPrompt) { $args += "--compact-prompt" }
    Invoke-Python -Args $args
  }

  if ($Mode -eq "api") {
    Invoke-Step "8) Generate DSL via API" {
      $args = @(
        "tools/generate_dsl_from_refined_draft.py",
        "--draft", $refinedDraft,
        "--image", $img,
        "--problem-id", $probId,
        "--out", $dslPy,
        "--mode", "api",
        "--provider", $resolvedPhase2Provider,
        "--system-prompt", "prompts/dsl_agent_system.md",
        "--rules-md", "prompts/dsl_generation_rules.md",
        "--max-attempts", "$DslMaxAttempts",
        "--image-detail", $DslImageDetail,
        "--write-on-fail",
        "--failure-report", $dslFailureReport,
        "--force"
      ) + $sourceJsonArgs + $commonModelArgs
      if ($UseVisionStructured) { $args += @("--vision-structured", $visionStructured) }
      if ($CompactDslPrompt) { $args += "--compact-prompt" }
      Invoke-Python -Args $args
    }
  } else {
    if (!(Test-Path -LiteralPath $dslLlm)) {
      throw "Missing file for prompt mode: $dslLlm"
    }
    Invoke-Step "8) Generate DSL from llm output file" {
      $args = @(
        "tools/generate_dsl_from_refined_draft.py",
        "--draft", $refinedDraft,
        "--image", $img,
        "--problem-id", $probId,
        "--out", $dslPy,
        "--mode", "prompt",
        "--provider", $resolvedPhase2Provider,
        "--llm-output-file", $dslLlm,
        "--system-prompt", "prompts/dsl_agent_system.md",
        "--rules-md", "prompts/dsl_generation_rules.md",
        "--max-attempts", "$DslMaxAttempts",
        "--image-detail", $DslImageDetail,
        "--write-on-fail",
        "--failure-report", $dslFailureReport,
        "--force"
      ) + $sourceJsonArgs + $commonModelArgs
      if ($UseVisionStructured) { $args += @("--vision-structured", $visionStructured) }
      if ($CompactDslPrompt) { $args += "--compact-prompt" }
      Invoke-Python -Args $args
    }
  }

  Invoke-Step "8.5) Normalize generated DSL (import/object-shape guard)" {
    $args = @(
      "tools/normalize_generated_dsl.py",
      "--dsl", $dslPy,
      "--failure-report", $dslFailureReport
    )
    Invoke-Python -Args $args
  }

  Invoke-Step "9) Sync semantic/solvable answer" {
    $args = @(
      "tools/sync_semantic_solvable_answer.py",
      "--dsl", $dslPy
    )
    Invoke-Python -Args $args
  }

  Invoke-Step "10) Format generated DSL layout" {
    $args = @(
      "tools/format_dsl_layout.py",
      "--dsl", $dslPy
    )
    Invoke-Python -Args $args
  }

  Invoke-Step "11) Validate generated DSL" {
    $args = @(
      "tools/validate_generated_dsl.py",
      "--dsl", $dslPy,
      "--out-prefix", (Join-Path $dir $probId),
      "--strict",
      "--emit-solvable",
      "--report", $report
    ) + $sourceJsonArgs
    Invoke-Python -Args $args
  }

  Invoke-Step "11.5) Validate visual alignment (vision draft vs layout)" {
    $layoutJson = Join-Path $dir "$probId.layout.json"
    $args = @(
      "tools/validate_visual_alignment.py",
      "--vision-draft", $visionDraft,
      "--layout-json", $layoutJson,
      "--report", $visualReport,
      "--min-text-hit-ratio", "0.55"
    )
    Invoke-Python -Args $args
  }

  if ($RunMb) {
    Invoke-Step "12) Run mb" {
      & mb $probId
      if ($LASTEXITCODE -ne 0) {
        throw "mb failed for $probId"
      }
    }
  }
  } catch {
    Write-Host "FAILED: $($row.ProbId) :: $($_.Exception.Message)" -ForegroundColor Red
    continue
  }
}

Write-Host ""
Write-Host "All items processed successfully." -ForegroundColor Green
