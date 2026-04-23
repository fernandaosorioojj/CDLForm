param(
    [string]$Python = "python",
    [string]$DistPath = "dist\exe",
    [string]$WorkPath = "build\pyinstaller"
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

& $Python -m PyInstaller --version *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller no esta instalado para este Python." -ForegroundColor Yellow
    Write-Host "Instale con: $Python -m pip install pyinstaller"
    exit 1
}

$dataArgs = @(
    "--add-data", "$root\assets;assets",
    "--add-data", "$root\styles;styles",
    "--add-data", "$root\config\jobtrack.ini;config",
    "--add-data", "$root\config\sql_server.example.json;config",
    "--add-data", "$root\config\gestion_login.example.json;config",
    "--add-data", "$root\config\admin_login.example.json;config",
    "--add-data", "$root\docs;docs"
)

function Initialize-SharedDataLayout {
    param(
        [string]$BaseDistPath
    )

    $sharedDataDir = Join-Path $BaseDistPath "data"
    $logsDir = Join-Path $sharedDataDir "logs"
    New-Item -ItemType Directory -Force -Path $sharedDataDir *> $null
    New-Item -ItemType Directory -Force -Path $logsDir *> $null

    Copy-Item "$root\config\sql_server.example.json" (Join-Path $sharedDataDir "sql_server.example.json") -Force
    Copy-Item "$root\config\gestion_login.example.json" (Join-Path $sharedDataDir "gestion_login.example.json") -Force
    Copy-Item "$root\config\admin_login.example.json" (Join-Path $sharedDataDir "admin_login.example.json") -Force

    $jobtrackExample = @"
[JOBTRACK]
Estacao=ESTACION-XX
idioma=1
"@
    Set-Content -Path (Join-Path $sharedDataDir "jobtrack.example.ini") -Value $jobtrackExample -Encoding UTF8
}

function Write-WorkerLauncher {
    param(
        [string]$BaseDistPath
    )

    $workerDir = Join-Path $BaseDistPath "CDLformWorker"
    $launcherPath = Join-Path $workerDir "run_worker.bat"
    $launcherContent = @"
@echo off
cd /d %~dp0

if not exist ..\data mkdir ..\data
if not exist ..\data\logs mkdir ..\data\logs

echo ==== %date% %time% ====>> ..\data\logs\worker.log
CDLformWorker.exe >> ..\data\logs\worker.log 2>&1
"@

    Set-Content -Path $launcherPath -Value $launcherContent -Encoding ASCII
}

function Build-App {
    param(
        [string]$Name,
        [string]$EntryPoint,
        [switch]$Console
    )

    $modeArg = "--windowed"
    if ($Console) {
        $modeArg = "--console"
    }

    & $Python -m PyInstaller `
        --noconfirm `
        --clean `
        --onedir `
        --contents-directory "." `
        $modeArg `
        --name $Name `
        --distpath $DistPath `
        --workpath $WorkPath `
        --specpath "build\spec" `
        @dataArgs `
        $EntryPoint

    if ($LASTEXITCODE -ne 0) {
        throw "Fallo el build de $Name"
    }
}

Build-App -Name "CDLformGestion" -EntryPoint "packaging\entrypoints\gestion.py"
Build-App -Name "CDLformOperario" -EntryPoint "packaging\entrypoints\operario.py"
Build-App -Name "CDLformWorker" -EntryPoint "packaging\entrypoints\worker.py" -Console
Initialize-SharedDataLayout -BaseDistPath (Join-Path $root $DistPath)
Write-WorkerLauncher -BaseDistPath (Join-Path $root $DistPath)

Write-Host ""
Write-Host "Build finalizado en $DistPath" -ForegroundColor Green
Write-Host "No se copian credenciales locales sensibles al build."
Write-Host "Configure manualmente data\\sql_server.local.json y data\\jobtrack.ini en el equipo destino."
