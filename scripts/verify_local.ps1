<#
.SYNOPSIS
    Script de verificación local del microservicio Alumno.
.DESCRIPTION
    Ejecuta pytest con configuración de testing (SQLite en memoria)
    y verifica que no queden referencias a módulos no-alumno.
.NOTES
    Uso: .\scripts\verify_local.ps1
    Exit code: 0 = OK, != 0 = ERROR
#>

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

Write-Host "========================================"
Write-Host " Verificación Local - Microservicio Alumno"
Write-Host "========================================"
Write-Host ""

# Cambiar al directorio raíz del proyecto
Set-Location $projectRoot

# 1. Configurar variables de entorno para testing
Write-Host "[1/3] Configurando entorno de testing..."
$env:FLASK_CONTEXT = "testing"
$env:FLASK_SKIP_DOTENV = "1"
$env:SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# 2. Ejecutar pytest
Write-Host "[2/3] Ejecutando pytest..."
python -m pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "PYTEST FALLO (exit code: $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}
Write-Host "Pytest OK" -ForegroundColor Green

# 3. Verificar que no queden módulos no-alumno
Write-Host ""
Write-Host "[3/3] Verificando que no queden imports/archivos de modulos no-alumno..."

$grepResult = git grep -n -E "import_materias|import_planes|archivados_xml" -- . 2>$null
if ($grepResult) {
    Write-Host "Se encontraron referencias a modulos no-alumno:" -ForegroundColor Red
    Write-Host $grepResult
    exit 1
}
Write-Host "No se encontraron referencias a modulos no-alumno" -ForegroundColor Green

# Limpiar variables de entorno
Remove-Item Env:FLASK_CONTEXT -ErrorAction SilentlyContinue
Remove-Item Env:FLASK_SKIP_DOTENV -ErrorAction SilentlyContinue
Remove-Item Env:SQLALCHEMY_DATABASE_URI -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================"
Write-Host " VERIFICACION LOCAL COMPLETADA OK" -ForegroundColor Green
Write-Host "========================================"
exit 0
