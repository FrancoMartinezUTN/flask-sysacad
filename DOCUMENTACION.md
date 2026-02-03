# 📜 Documentación Técnica - Microservicio Alumno

Este documento contiene la información técnica detallada del **Microservicio Alumno** del sistema Flask-Sysacad de la UTN.

---

## 📁 Estructura del Proyecto

```text
flask-sysacad/
├── app/                        # Código principal de la aplicación
│   ├── __init__.py             # App factory (create_app)
│   ├── db.py                   # Instancias de SQLAlchemy y Migrate
│   ├── cli.py                  # Comandos CLI personalizados
│   ├── models/                 # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   └── alumno.py           # Modelo Alumno
│   ├── routes/                 # Endpoints REST (Blueprints)
│   │   └── alumno_routes.py    # Rutas de /alumnos
│   ├── services/               # Lógica de negocio
│   │   └── alumno_service.py
│   ├── repositories/           # Capa de acceso a datos
│   │   └── alumno_repository.py
│   ├── dto/                    # Data Transfer Objects
│   │   └── alumno_ficha.py
│   ├── importers/              # Importadores de datos
│   │   └── importar_alumnos.py # Importador CSV
│   ├── validators/             # Validaciones de entrada
│   ├── renderers/              # Renderizadores (PDF, etc)
│   ├── mapping/                # Mapeos de datos
│   ├── resources/              # Recursos estáticos
│   └── utils/                  # Utilidades generales
├── test/                       # Tests automatizados
│   ├── __init__.py
│   ├── test_app.py             # Test de app factory
│   ├── test_db.py              # Test de conexión DB
│   └── test_alumno_api.py      # Tests de endpoints API
├── scripts/                    # Scripts auxiliares
│   ├── init_db.py              # Inicialización DB (Docker)
│   ├── verify_local.ps1        # Verificación local (Windows)
│   └── verify_local.sh         # Verificación local (Linux)
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI
├── docker/                     # Configuración Docker adicional
├── .env.example                # Plantilla de variables de entorno
├── docker-compose.yml          # Orquestación de contenedores
├── Dockerfile                  # Imagen del microservicio
├── requirements.txt            # Dependencias Python
├── run.py                      # Punto de entrada local
├── crear_tablas.py             # Script para crear tablas
└── wsgi.py                     # Punto de entrada WSGI (Gunicorn)
```

---

## 📦 Modelo de Datos

### `Alumno` (`app/models/alumno.py`)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | Integer | PK, autoincremental | Identificador único |
| `legajo` | String(50) | Unique, nullable | Número de legajo |
| `nombre` | String(100) | Not null | Nombre del alumno |
| `apellido` | String(100) | Not null | Apellido del alumno |
| `dni` | String(20) | Unique, nullable | Documento de identidad |
| `email` | String(120) | Unique, nullable | Correo electrónico |
| `facultad` | String(120) | Nullable | Facultad (ej: "FRC - UTN") |
| `fecha_nacimiento` | Date | Nullable | Fecha de nacimiento |
| `carrera` | String(120) | Nullable | Carrera que cursa |
| `anio_ingreso` | Integer | Nullable | Año de ingreso |

```python
# Ejemplo de uso
alumno = Alumno(
    dni="40123456",
    nombre="Ana",
    apellido="Pérez",
    email="ana@example.com",
    facultad="FRC - UTN",
    legajo="2025-0001"
)

# Serialización
alumno.to_dict()  # Devuelve diccionario JSON-serializable
```

---

## 🌐 API REST

### Endpoints Implementados

| Método | Ruta | Descripción | Response |
|--------|------|-------------|----------|
| `GET` | `/alumnos` | Lista todos los alumnos (paginado) | `{"items": [...], "total": N}` |
| `GET` | `/alumnos/<id>` | Obtiene un alumno por ID | `{alumno}` o `404` |
| `POST` | `/alumnos` | Crea un nuevo alumno | `201` o `409` (duplicado) |
| `GET` | `/alumnos/<id>/ficha` | Ficha del alumno (JSON) | `{ficha}` |
| `GET` | `/alumnos/<id>/ficha.pdf` | Ficha del alumno (PDF) | Archivo PDF |

### Ejemplos de Uso

```bash
# Listar alumnos
curl http://localhost:5000/alumnos

# Obtener alumno por ID
curl http://localhost:5000/alumnos/1

# Crear alumno
curl -X POST http://localhost:5000/alumnos \
  -H "Content-Type: application/json" \
  -d '{"dni":"40123456","nombre":"Ana","apellido":"Pérez","email":"ana@example.com"}'
```

---

## ⚙️ Configuración

### Variables de Entorno

| Variable | Obligatoria | Entorno | Default | Descripción |
|----------|-------------|---------|---------|-------------|
| `SECRET_KEY` | Sí (prod) | Todos | (testing: auto) | Clave secreta de Flask |
| `SQLALCHEMY_DATABASE_URI` | Sí (prod) | Todos | - | URI de conexión principal |
| `DEV_DATABASE_URI` | No | Dev | `sqlite:///sysacad_dev.db` | URI para desarrollo |
| `TEST_DATABASE_URI` | No | Test | `sqlite:///:memory:` | URI para tests |
| `FLASK_CONTEXT` | No | Todos | `development` | Contexto de ejecución |
| `FLASK_SKIP_DOTENV` | No | CI | `0` | `1` para no cargar `.env` |
| `FLASK_DEBUG` | No | Dev | `False` | Modo debug |

### Lógica de Conexión a Base de Datos

```python
# Prioridad de configuración en create_app():
# 1. SQLALCHEMY_DATABASE_URI (si está definida)
# 2. Según FLASK_CONTEXT:
#    - testing: TEST_DATABASE_URI → fallback sqlite:///:memory:
#    - development: DEV_DATABASE_URI → fallback sqlite:///sysacad_dev.db
#    - production: FALLA si no hay URI
```

### Archivo `.env.example`

```env
POSTGRES_DB=sysacaddb
POSTGRES_USER=franco
POSTGRES_PASSWORD=CHANGE_ME

FLASK_CONTEXT=production
SECRET_KEY=CHANGE_ME

SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://franco:CHANGE_ME@postgres-sysacad:5432/sysacaddb
REDIS_URL=redis://redis-sysacad:6379/0
```

> ⚠️ **IMPORTANTE:** `.env` está en `.gitignore`. Nunca commitear credenciales reales.

---

## 🧪 Testing

### Estructura de Tests

```text
test/
├── __init__.py
├── test_app.py          # Verifica que create_app() funciona
├── test_db.py           # Verifica conexión a base de datos
└── test_alumno_api.py   # Tests de endpoints /alumnos
```

### Ejecutar Tests (Modo CI)

**Windows (PowerShell):**

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Configurar variables
$env:FLASK_CONTEXT='testing'
$env:FLASK_SKIP_DOTENV='1'
$env:SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'

# Ejecutar
python -m pytest -q

# O usar script automatizado
.\scripts\verify_local.ps1
```

**Linux/macOS (bash):**

```bash
# Activar entorno virtual
source .venv/bin/activate

# Configurar variables
export FLASK_CONTEXT=testing
export FLASK_SKIP_DOTENV=1
export SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'

# Ejecutar
python -m pytest -q

# O usar script automatizado
./scripts/verify_local.sh
```

### Tests Disponibles

| Test | Archivo | Descripción |
|------|---------|-------------|
| `test_app` | `test_app.py` | Verifica que la app se crea correctamente |
| `test_db_connection` | `test_db.py` | Verifica conexión a DB |
| `test_get_alumnos_ok` | `test_alumno_api.py` | GET /alumnos retorna 200 |
| `test_get_alumno_por_id_ok` | `test_alumno_api.py` | GET /alumnos/<id> retorna 200 |
| `test_get_alumno_por_id_not_found` | `test_alumno_api.py` | GET /alumnos/<id> inexistente retorna 404 |
| `test_post_alumno_crea_ok` | `test_alumno_api.py` | POST /alumnos crea correctamente |
| `test_post_alumno_dni_duplicado` | `test_alumno_api.py` | POST /alumnos con DNI duplicado retorna 409 |

---

## 🐳 Docker

### docker-compose.yml

Servicios definidos:

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| `sysacad-alumno` | 5000 | Microservicio Flask |
| `sysacad-alumno-init` | - | Job de inicialización DB |
| `postgres-sysacad` | 5432 | Base de datos PostgreSQL |
| `traefik` | 80 | Reverse proxy / Load balancer |

### Comandos Útiles

```bash
# Levantar todo
docker compose up -d --build

# Ver estado
docker compose ps

# Ver logs del microservicio
docker compose logs -f sysacad-alumno

# Conectar a PostgreSQL
docker exec -it postgres-sysacad psql -U franco -d sysacaddb

# Dentro de psql:
\dt                          # Listar tablas
SELECT * FROM alumnos LIMIT 5;  # Ver alumnos
\q                           # Salir

# Detener todo
docker compose down

# Limpiar volúmenes (⚠️ borra datos)
docker compose down -v
```

---

## 🔄 GitHub Actions CI

### Workflow: `.github/workflows/ci.yml`

```yaml
name: CI
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"
      - run: pip install -r requirements.txt && pip install pytest
      - name: Run tests
        env:
          FLASK_CONTEXT: testing
          FLASK_SKIP_DOTENV: "1"
          SQLALCHEMY_DATABASE_URI: "sqlite:///:memory:"
        run: pytest -q
```

---

## 📥 Importación de Alumnos

### Desde CSV

```bash
# Crear tablas (si no existen)
python crear_tablas.py

# Importar alumnos
python -m app.importers.importar_alumnos "alumnos.csv"
```

### Formato CSV Esperado

```csv
nro_documento,nro_legajo,nombre,apellido,fecha_nacimiento,fecha_ingreso
40123456,2025-0001,Ana,Pérez,1995-05-15,2020-03-01
```

El importador:
- Evita duplicados por DNI
- Extrae año de ingreso desde `fecha_ingreso`
- Usa inserción en bloque para performance

---

## 🔐 Seguridad

### Verificación de Configuración

```bash
python verify_security_fixes.py
```

Verifica:
- `SECRET_KEY` está definida
- `DEBUG` no está forzado en producción
- La app arranca correctamente

### Buenas Prácticas

1. **`.env` nunca se commitea** - está en `.gitignore`
2. **Usar `.env.example`** como plantilla
3. **En producción**: usar variables de entorno del sistema o gestor de secretos
4. **SECRET_KEY diferente** en cada entorno

---

## ✅ Checklist de Verificación

```bash
# 1. Git status limpio
git status

# 2. Tests pasan
python -m pytest -q

# 3. No hay módulos no-alumno
git grep -n -E "import_materias|import_planes|archivados_xml" -- .

# 4. Docker funciona (opcional)
docker compose ps
curl http://localhost/alumnos

# 5. Endpoint directo funciona
curl http://localhost:5000/alumnos
```

### Script Automatizado

```powershell
# Windows
.\scripts\verify_local.ps1

# Linux
./scripts/verify_local.sh
```

---

## 🔍 Alcance del Microservicio

### ✅ Responsabilidades

- CRUD de datos básicos de alumnos
- Importación masiva desde CSV
- Generación de ficha de alumno (JSON/PDF)
- Validación de datos (DNI único, email válido)
- API REST para consumo por otros servicios

### ❌ Fuera de Alcance

- Gestión de materias y cursadas
- Gestión de planes de estudio
- Procesos administrativos (pagos, deudas)
- Autenticación/autorización (delegado a API Gateway)

---

## 📊 Pruebas de Carga (k6)

```bash
# Levantar la app
python run.py

# Ejecutar spike test
k6 run spike_tests.js
```

El script `spike_tests.js`:
- Ramp-up a 100 VUs en 10s
- Mantiene 100 VUs por 20s
- Ramp-down a 0 VUs en 10s
- Verifica status 200 y latencia p95 < 500ms

Ver `ANALISIS_TEST_CARGA_K6.md` para resultados.

---

*Última actualización: Enero 2026*
