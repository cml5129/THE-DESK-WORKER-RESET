param(
    [string]$Destination = "github-upload"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$destRoot = Join-Path $repoRoot $Destination

if (Test-Path $destRoot) {
    Write-Host "Removing existing folder: $destRoot" -ForegroundColor Yellow
    Remove-Item -Path $destRoot -Recurse -Force
}

New-Item -ItemType Directory -Path $destRoot | Out-Null

$excludeDirs = @(
    ".git",
    ".venv",
    "dist",
    "build/windows-work",
    "build/mac-work",
    "__pycache__"
)

$excludeFiles = @(
    "*.pyc",
    "*.pyo",
    "*.tmp",
    "*.log"
)

Write-Host "Copying repository to clean upload directory..." -ForegroundColor Cyan

$allItems = Get-ChildItem -Path $repoRoot -Force
foreach ($item in $allItems) {
    if ($item.Name -eq (Split-Path $destRoot -Leaf)) { continue }

    $relative = $item.FullName.Substring($repoRoot.Path.Length + 1).Replace('\\','/')

    $skip = $false
    foreach ($ex in $excludeDirs) {
        if ($relative -eq $ex -or $relative.StartsWith($ex + "/")) {
            $skip = $true
            break
        }
    }
    if ($skip) { continue }

    if ($item.PSIsContainer) {
        Copy-Item -Path $item.FullName -Destination $destRoot -Recurse -Force
    } else {
        $isExcludedFile = $false
        foreach ($pattern in $excludeFiles) {
            if ($item.Name -like $pattern) {
                $isExcludedFile = $true
                break
            }
        }
        if (-not $isExcludedFile) {
            Copy-Item -Path $item.FullName -Destination $destRoot -Force
        }
    }
}

Write-Host "Done. Clean upload directory created:" -ForegroundColor Green
Write-Host "  $destRoot" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1) cd $destRoot"
Write-Host "  2) git init"
Write-Host "  3) git add ."
Write-Host "  4) git commit -m \"Initial commit\""
Write-Host "  5) git branch -M main"
Write-Host "  6) git remote add origin https://github.com/<your-user>/<your-repo>.git"
Write-Host "  7) git push -u origin main"
