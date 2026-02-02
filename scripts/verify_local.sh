#!/bin/bash
#
# Script de verificacion local del microservicio Alumno.
# Ejecuta pytest con configuracion de testing (SQLite en memoria)
# y verifica que no queden referencias a modulos no-alumno.
#
# Uso: ./scripts/verify_local.sh
# Exit code: 0 = OK, != 0 = ERROR
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo " Verificacion Local - Microservicio Alumno"
echo "========================================"
echo ""

cd "$PROJECT_ROOT"

# 1. Configurar variables de entorno para testing
echo "[1/4] Configurando entorno de testing..."
export FLASK_CONTEXT="testing"
export FLASK_SKIP_DOTENV="1"
export SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"

# 2. Ejecutar pytest
echo "[2/4] Ejecutando pytest..."
if python -m pytest -q; then
    echo "Pytest OK"
else
    echo ""
    echo "PYTEST FALLO"
    exit 1
fi

# 3. Verificar que no queden imports de modulos no-alumno en app/ y test/
echo ""
echo "[3/4] Verificando imports en app/ y test/..."

if git grep -n -E "import_materias|import_planes|archivados_xml" -- app test 2>/dev/null; then
    echo "Se encontraron referencias a modulos no-alumno en codigo"
    exit 1
fi
echo "No se encontraron referencias en app/ ni test/"

# 4. Verificar que no existan archivos prohibidos en el repo
echo ""
echo "[4/4] Verificando que no existan archivos de modulos no-alumno..."

FORBIDDEN_PATTERNS=(
    "archivados_xml/"
    "scripts/import_materias.py"
    "scripts/import_planes.py"
    "scripts/import_all.py"
    "scripts/materias.xml"
)

FOUND_FORBIDDEN=0
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
    if git ls-files | grep -q "^${pattern}"; then
        echo "Archivo prohibido encontrado: $pattern"
        FOUND_FORBIDDEN=1
    fi
done

if [ $FOUND_FORBIDDEN -eq 1 ]; then
    echo "Se encontraron archivos prohibidos en el repo"
    exit 1
fi
echo "No se encontraron archivos prohibidos"

# Limpiar variables de entorno
unset FLASK_CONTEXT
unset FLASK_SKIP_DOTENV
unset SQLALCHEMY_DATABASE_URI

echo ""
echo "========================================"
echo " VERIFICACION LOCAL COMPLETADA OK"
echo "========================================"
exit 0
