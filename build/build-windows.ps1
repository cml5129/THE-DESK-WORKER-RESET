# Build Exerset for Windows
# Prerequisites: 
#   - Python 3.9+ with venv activated
#   - pip install pyinstaller
#   - (Optional) Inno Setup for creating installer
# 
# Usage:
#   From PowerShell in the Exerset root directory:
#   .\build\build-windows.ps1

param(
    [switch]$CreateInstaller = $false
)

Write-Host "Building Exerset for Windows..." -ForegroundColor Green

# Clean previous build
if (Test-Path "dist\windows") {
    Remove-Item "dist\windows" -Recurse -Force
    Write-Host "Cleaned previous build artifacts"
}

# Create dist directory
New-Item -ItemType Directory -Force -Path "dist\windows" | Out-Null

# Run PyInstaller
Write-Host "Running PyInstaller..." -ForegroundColor Cyan
pyinstaller exerset.spec --distpath dist\windows --workpath build\windows-work

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller failed!" -ForegroundColor Red
    exit 1
}

Write-Host "PyInstaller completed successfully" -ForegroundColor Green
Write-Host ""
Write-Host "Build output: dist\windows\Exerset" -ForegroundColor Yellow
Write-Host ""
Write-Host "To create an installer, install Inno Setup and run:" -ForegroundColor Cyan
Write-Host "  iscc build\exerset-installer.iss" -ForegroundColor Yellow
Write-Host ""
Write-Host "The installer will be created at: dist\windows\Exerset-Setup.exe" -ForegroundColor Yellow
