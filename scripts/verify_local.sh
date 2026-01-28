#!/bin/bash
#
# Script de verificación local del microservicio Alumno.
# Ejecuta pytest con configuración de testing (SQLite en memoria)
# y verifica que no queden referencias a módulos no-alumno.
#
# Uso: ./scripts/verify_local.sh
# Exit code: 0 = OK, != 0 = ERROR
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo " Verificación Local - Microservicio Alumno"
echo "========================================"
echo ""

cd "$PROJECT_ROOT"

# 1. Configurar variables de entorno para testing
echo "[1/3] Configurando entorno de testing..."
export FLASK_CONTEXT="testing"
export FLASK_SKIP_DOTENV="1"
export SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"

# 2. Ejecutar pytest
echo "[2/3] Ejecutando pytest..."
if python -m pytest -q; then
    echo "✅ Pytest OK"
else
    echo ""
    echo "❌ PYTEST FALLÓ"
    exit 1
fi

# 3. Verificar que no queden módulos no-alumno
echo ""
echo "[3/3] Verificando que no queden imports/archivos de módulos no-alumno..."

# Buscar referencias problemáticas (excluyendo .md, campos legítimos del modelo)
if git grep -n -E "import_materias|import_planes|archivados_xml" -- . 2>/dev/null; then
    echo "❌ Se encontraron referencias a módulos no-alumno"
    exit 1
fi
echo "✅ No se encontraron referencias a módulos no-alumno"

# Limpiar variables de entorno
unset FLASK_CONTEXT
unset FLASK_SKIP_DOTENV
unset SQLALCHEMY_DATABASE_URI

echo ""
echo "========================================"
echo " ✅ VERIFICACIÓN LOCAL COMPLETADA OK"
echo "========================================"
exit 0
