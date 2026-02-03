<#
.SYNOPSIS
    Script de verificacion local del microservicio Alumno.
.DESCRIPTION
    Ejecuta pytest con configuracion de testing (SQLite en memoria)
    y verifica que no queden referencias a modulos no-alumno.
.NOTES
    Uso: .\scripts\verify_local.ps1
    Exit code: 0 = OK, != 0 = ERROR
#>

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

Write-Host "========================================"
Write-Host " Verificacion Local - Microservicio Alumno"
Write-Host "========================================"
Write-Host ""

# Cambiar al directorio raiz del proyecto
Set-Location $projectRoot

# 1. Configurar variables de entorno para testing
Write-Host "[1/4] Configurando entorno de testing..."
$env:FLASK_CONTEXT = "testing"
$env:FLASK_SKIP_DOTENV = "1"
$env:SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# 2. Ejecutar pytest
Write-Host "[2/4] Ejecutando pytest..."
python -m pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "PYTEST FALLO (exit code: $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}
Write-Host "Pytest OK" -ForegroundColor Green

# 3. Verificar que no queden imports de modulos no-alumno en app/ y test/
Write-Host ""
Write-Host "[3/4] Verificando imports en app/ y test/..."

$grepResult = git grep -n -E "import_materias|import_planes|archivados_xml" -- app test 2>$null
if ($grepResult) {
    Write-Host "Se encontraron referencias a modulos no-alumno en codigo:" -ForegroundColor Red
    Write-Host $grepResult
    exit 1
}
Write-Host "No se encontraron referencias en app/ ni test/" -ForegroundColor Green

# 4. Verificar que no existan archivos prohibidos en el repo
Write-Host ""
Write-Host "[4/4] Verificando que no existan archivos de modulos no-alumno..."

$forbiddenPaths = @(
    "archivados_xml/",
    "scripts/import_materias.py",
    "scripts/import_planes.py",
    "scripts/import_all.py",
    "scripts/materias.xml"
)

$trackedFiles = git ls-files 2>$null
$foundForbidden = @()

foreach ($pattern in $forbiddenPaths) {
    foreach ($file in $trackedFiles) {
        if ($file -like "$pattern*" -or $file -eq $pattern.TrimEnd('/')) {
            $foundForbidden += $file
        }
    }
}

if ($foundForbidden.Count -gt 0) {
    Write-Host "Se encontraron archivos prohibidos en el repo:" -ForegroundColor Red
    $foundForbidden | ForEach-Object { Write-Host "  - $_" }
    exit 1
}
Write-Host "No se encontraron archivos prohibidos" -ForegroundColor Green

# Limpiar variables de entorno
Remove-Item Env:FLASK_CONTEXT -ErrorAction SilentlyContinue
Remove-Item Env:FLASK_SKIP_DOTENV -ErrorAction SilentlyContinue
Remove-Item Env:SQLALCHEMY_DATABASE_URI -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================"
Write-Host " VERIFICACION LOCAL COMPLETADA OK" -ForegroundColor Green
Write-Host "========================================"
exit 0
