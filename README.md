# 🎓 Microservicio Alumno - Flask-Sysacad

## 👥 Equipo

- Martinez, Franco  
- Mulena, Adrián  
- Ochoa, Camila  
- Asistencia IAs: GPT, Grok, Google Antigravity

---

## 📋 Descripción

**Microservicio de Gestión de Alumnos** desarrollado en Flask, parte del sistema Sysacad de la UTN.

### Características

- Arquitectura multicapa (routes → services → repositories → models)
- Base de datos **PostgreSQL** (producción) / **SQLite** (desarrollo/testing)
- Importación masiva de alumnos desde CSV
- API REST con endpoints CRUD para alumnos
- CI/CD con GitHub Actions (Python 3.12 y 3.13)
- Containerizado con Docker y Docker Compose

---

## 🧱 Requisitos Previos

| Requisito | Versión Mínima |
|-----------|----------------|
| Python | 3.12+ |
| Git | 2.x |
| Docker (opcional) | 24.x |
| Docker Compose (opcional) | 2.x |
| PostgreSQL (producción) | 16+ |

---

## ⚡ Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/FrancoMartinezUTN/flask-sysacad.git
cd flask-sysacad
```

### 2. Crear entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux/macOS (bash):**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar el archivo de ejemplo y editar:

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

> ⚠️ **Importante:** `.env` está en `.gitignore` y nunca debe commitearse con credenciales reales.

### 4. Ejecutar la aplicación

```powershell
python run.py
```

La API estará disponible en: `http://127.0.0.1:5000`

---

## 🐳 Ejecución con Docker Compose

```bash
# Construir y levantar todos los servicios
docker compose up -d --build

# Verificar estado
docker compose ps

# Ver logs
docker compose logs -f sysacad-alumno

# Detener
docker compose down
```

### Endpoints disponibles

| Endpoint | Puerto | Descripción |
|----------|--------|-------------|
| `http://localhost/alumnos` | 80 (Traefik) | API de alumnos (producción) |
| `http://localhost:5000/alumnos` | 5000 | API de alumnos (directo) |

### Verificar base de datos

```bash
# Conectar a PostgreSQL
docker exec -it postgres-sysacad psql -U franco -d sysacaddb

# Listar tablas
\dt

# Ver datos de alumnos
SELECT * FROM alumnos LIMIT 5;

# Salir
\q
```

---

## 🧪 Tests

### Ejecutar tests localmente (modo CI-like)

Los tests usan SQLite en memoria para no depender de PostgreSQL.

**Windows (PowerShell):**

```powershell
# Opción 1: Configurar variables y ejecutar
$env:FLASK_CONTEXT='testing'
$env:FLASK_SKIP_DOTENV='1'
$env:SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
python -m pytest -q

# Opción 2: Usar el script de verificación
.\scripts\verify_local.ps1
```

**Linux/macOS (bash):**

```bash
# Opción 1: Configurar variables y ejecutar
export FLASK_CONTEXT=testing
export FLASK_SKIP_DOTENV=1
export SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
python -m pytest -q

# Opción 2: Usar el script de verificación
./scripts/verify_local.sh
```

### GitHub Actions (CI)

El workflow `.github/workflows/ci.yml` ejecuta automáticamente:

- Tests en Python 3.12 y 3.13
- Variables de entorno para testing (sin necesidad de `.env`)

---

## ⚙️ Variables de Entorno

| Variable | Obligatoria | Entorno | Descripción |
|----------|-------------|---------|-------------|
| `SECRET_KEY` | Sí (prod) | Todos | Clave secreta de Flask |
| `SQLALCHEMY_DATABASE_URI` | Sí (prod) | Producción | URI de conexión PostgreSQL |
| `DEV_DATABASE_URI` | No | Desarrollo | URI de desarrollo (fallback: SQLite file) |
| `TEST_DATABASE_URI` | No | Testing | URI de testing (fallback: SQLite memory) |
| `FLASK_CONTEXT` | No | Todos | `development` / `testing` / `production` |
| `FLASK_SKIP_DOTENV` | No | CI | `1` para no cargar `.env` |

---

## 📁 Estructura del Proyecto

```
flask-sysacad/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── db.py                 # SQLAlchemy + Migrate
│   ├── models/               # Modelos ORM
│   │   └── alumno.py
│   ├── routes/               # Endpoints REST
│   │   └── alumno_routes.py
│   ├── services/             # Lógica de negocio
│   │   └── alumno_service.py
│   ├── repositories/         # Acceso a datos
│   │   └── alumno_repository.py
│   ├── dto/                  # Data Transfer Objects
│   ├── importers/            # Importadores CSV
│   │   └── importar_alumnos.py
│   └── ...
├── test/
│   ├── test_app.py           # Test de app factory
│   ├── test_db.py            # Test de conexión DB
│   └── test_alumno_api.py    # Tests de API
├── scripts/
│   ├── init_db.py            # Inicialización DB (Docker)
│   ├── verify_local.ps1      # Verificación local (Windows)
│   └── verify_local.sh       # Verificación local (Linux)
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI
├── .env.example              # Ejemplo de variables
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ✅ Checklist de Verificación

Antes de hacer push o crear un PR, verificar:

```bash
# 1. Git status limpio (sin cambios pendientes)
git status

# 2. Tests pasan
python -m pytest -q

# 3. No hay referencias a módulos no-alumno
git grep -n -E "import_materias|import_planes|archivados_xml" -- .
# (debe estar vacío)

# 4. Docker funciona (si aplica)
docker compose ps

# 5. Endpoints responden
curl http://localhost:5000/alumnos
```

O usar el script automatizado:

```powershell
.\scripts\verify_local.ps1   # Windows
./scripts/verify_local.sh    # Linux
```

---

## 📥 Importación de Alumnos desde CSV

```bash
# Crear tablas
python crear_tablas.py

# Importar desde CSV
python -m app.importers.importar_alumnos "alumnos.csv"
```

---

## 📊 Pruebas de Carga (k6)

```powershell
# Levantar la app
python run.py

# En otra terminal
$env:SYSACAD_BASE_URL = "http://127.0.0.1:5000"
k6 run spike_tests.js
```

Ver `ANALISIS_TEST_CARGA_K6.md` para resultados detallados.

---

## 🔐 Seguridad

- `.env` está en `.gitignore` - nunca commitear credenciales reales
- Usar `.env.example` como plantilla
- En producción, usar siempre variables de entorno del sistema
- Script de verificación: `python verify_security_fixes.py`

---

## 📜 Licencia

Proyecto académico - UTN FRSR
