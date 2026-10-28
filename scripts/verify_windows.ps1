# NEX Windows verification script
# Run from the repository root in PowerShell: .\scripts\verify_windows.ps1
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$pythonCommand = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCommand = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
} else {
    throw "Python was not found. Install Python 3 and enable the Python launcher or PATH, then retry."
}

Write-Host "NEX verification root: $repoRoot"
Write-Host "Python command: $pythonCommand"
Write-Host ""

Write-Host "=== 1/3 Unit tests ==="
if ($pythonCommand -eq "py") {
    & py -3 -m unittest discover -v
} else {
    & python -m unittest discover -v
}
if ($LASTEXITCODE -ne 0) {
    throw "Unit tests failed (exit code $LASTEXITCODE)."
}

Write-Host ""
Write-Host "=== 2/3 Python compilation ==="
if ($pythonCommand -eq "py") {
    & py -3 -m compileall -q scripts tests
} else {
    & python -m compileall -q scripts tests
}
if ($LASTEXITCODE -ne 0) {
    throw "Python compilation failed (exit code $LASTEXITCODE)."
}

Write-Host ""
Write-Host "=== 3/3 Agent Factory smoke test ==="
$tempOutput = Join-Path ([System.IO.Path]::GetTempPath()) ("nex-verify-" + [guid]::NewGuid().ToString("N"))
try {
    if ($pythonCommand -eq "py") {
        & py -3 scripts/agent_factory.py --input examples/agent-factory-request.json --output $tempOutput
    } else {
        & python scripts/agent_factory.py --input examples/agent-factory-request.json --output $tempOutput
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Agent Factory smoke test failed (exit code $LASTEXITCODE)."
    }

    $expected = @(
        "agent-spec.md",
        "system-instructions.md",
        "tool-manifest.md",
        "test-plan.md",
        "setup.md",
        "checkpoint.md"
    )
    foreach ($name in $expected) {
        $artifact = Join-Path $tempOutput $name
        if (-not (Test-Path -LiteralPath $artifact -PathType Leaf)) {
            throw "Expected artifact missing: $name"
        }
    }

    $actualCount = @(Get-ChildItem -LiteralPath $tempOutput -File).Count
    if ($actualCount -ne $expected.Count) {
        throw "Expected $($expected.Count) Markdown artifacts; found $actualCount."
    }
    Write-Host "PASS: all six expected artifacts generated in a temporary directory."
}
finally {
    if (Test-Path -LiteralPath $tempOutput) {
        Remove-Item -LiteralPath $tempOutput -Recurse -Force
    }
}

Write-Host ""
Write-Host "PASS: all three verification stages completed."
