# 🧠 

## 👬🙋  Equipo 
Martinez, Franco
Mulena, Adrián
Ochoa, Camila
Asistencia IAs: GPT, Grok, Google Antigravity


## 🔧 Descripción general

Este proyecto es un **microservicio de Gestión de Alumnos** desarrollado en **Flask**, con:

- Arquitectura multicapa (routes → services → repositories → models).
- Base de datos **PostgreSQL** usando **SQLAlchemy**.
- Soporte para **importación masiva de alumnos desde CSV**.
- Preparado para trabajo colaborativo con ramas `feature/*` y PR en GitHub.
- Entorno virtual aislado para facilitar instalación y despliegue.

---

## 🧱 Requisitos previos

### ✅ Generales

- Python **3.12+**
- Git
- PostgreSQL **16+**
- Visual Studio Code (o cualquier IDE similar)
- (Opcional / futuro) Redis o DragonflyDB para cache/rate limit
- k6 instalado para pruebas de carga (`k6 version` debe funcionar)

---

## ⚙️ Configuración por variables de entorno (12-Factor)

El microservicio usa **variables de entorno** para su configuración, siguiendo buenas prácticas de 12-Factor App.

Variables principales:

| Variable                 | Obligatoria | Entorno     | Descripción                                                   |
|--------------------------|------------|-------------|---------------------------------------------------------------|
| SECRET_KEY               | Sí         | Todos       | Clave secreta de Flask (cookies, sesiones).                  |
| SQLALCHEMY_DATABASE_URI  | Sí         | Producción  | Cadena de conexión a la base PostgreSQL.                     |
| DEV_DATABASE_URI         | No         | Desarrollo  | Cadena de conexión en modo desarrollo.                       |
| FLASK_CONTEXT            | No         | Todos       | `development` / `production` (por defecto `development`).     |
| FLASK_DEBUG              | No         | Desarrollo  | `True` solo en local, vacío/False en producción.             |
| REDIS_URL                | No         | Todos       | URL de Redis/Dragonfly (para cache/rate limit en el futuro). |

### Verificación rápida de configuración y seguridad

Antes de levantar la app o hacer deploy:

```bash
python verify_security_fixes.py
```

Este script valida que:

- Exista `SECRET_KEY`.
- `DEBUG` no esté forzado a activo en producción.
- La app pueda iniciar con configuración válida.

---

## 💻 Instalación local (Windows / Linux)

### 🧩 1. Clonar el repositorio

```bash
git clone https://github.com/FrancoMartinezUTN/flask-sysacad.git
cd flask-sysacad
```

### 🧰 2. Crear y activar entorno virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS (bash):**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 📦 3. Instalar dependencias

```bash
pip install -r requirements.txt
python -m pip install pandas
```

> `pandas` se utiliza para la importación masiva de alumnos desde CSV.

---

## 🚀 Ejecución local (sin Docker)

Con el entorno virtual activado y las variables de entorno configuradas:

```powershell
python run.py
```

La aplicación queda disponible en:

- `http://127.0.0.1:5000`

---

## 🐳 Ejecución y compilación en Docker

> Ajustar si se dispone de un `docker-compose.yml` específico. A modo general:

### 1. Build de la imagen

Desde la raíz del proyecto (donde está el `Dockerfile`):

```bash
docker build -t sysacad-alumno .
```

### 2. Ejecución del contenedor

```bash
docker run -d   --name sysacad-alumno   -p 5000:5000   -e SECRET_KEY="prod-secret"   -e SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://user:pass@host:5432/sysacaddb"   sysacad-alumno
```

El microservicio quedará expuesto en `http://localhost:5000`.

Si se utiliza `docker compose`, el flujo típico es:

```bash
docker compose build
docker compose up
```

---

## 📥 Importación de alumnos desde CSV

Este módulo permite **importar grandes volúmenes de alumnos** desde un archivo `.csv` a la base de datos PostgreSQL.

Características principales:

- Lectura eficiente con **pandas**.
- Inserción masiva con `bulk_save_objects`.
- Evita **duplicados por DNI**.
- Inserta solo registros nuevos.
- Generación automática de emails.
- Preparado para escalar a **miles/millones de filas**.
- Desarrollado siguiendo principios **DRY, KISS, YAGNI**.

### 🧱 1. Crear las tablas necesarias

```bash
python crear_tablas.py
```

### 📤 2. Ejecutar el importador de alumnos

```bash
python -m app.importers.importar_alumnos "alumnos.csv"
```

### 📝 Consideraciones

- Se requiere tener la base de datos `sysacaddb` activa.
- La tabla `alumnos` se crea con `crear_tablas.py`.
- La columna `dni` debe ser única.
- La carrera por defecto es **"Ingeniería en Sistemas"** (configurable en código).
- El año de ingreso se extrae de `fecha_ingreso` en el CSV.

### 📁 Estructura relevante

```text
├── app/
│   ├── models/alumno.py
│   ├── database.py
│   ├── importers/
│   │   └── importar_alumnos.py
├── crear_tablas.py
├── alumnos.csv
├── requirements.txt
├── README.md
```

---

## 🧪 Tests automatizados (pytest)

Este proyecto incluye **tests automatizados** con `pytest` para:

- Importación de alumnos desde CSV.
- Conexión a la base de datos.
- Comportamiento básico de la aplicación.

### ⚡ Requisitos previos para los tests

- Entorno virtual (`.venv`) creado y activado.
- Base de datos PostgreSQL levantada (`sysacaddb`).
- Tablas creadas con:

  ```bash
  python crear_tablas.py
  ```

### ▶️ Ejecutar todos los tests

```bash
pytest test/ -v
```

### ▶️ Ejecutar un test específico

Ejemplo:

```bash
pytest test/test_importar_alumnos.py -v
```

---

## 📊 Pruebas de carga con k6 (spike test)

El proyecto incluye un script de prueba de carga `spike_tests.js` para el endpoint de alumnos.

### Requisitos

- k6 instalado y en el PATH (`k6 version`).
- Microservicio corriendo en `http://127.0.0.1:5000` (por defecto).

### Ejecución

1. Levantar la aplicación:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python run.py
   ```

2. En otra terminal, desde la raíz del proyecto:

   ```powershell
   $env:SYSACAD_BASE_URL = "http://127.0.0.1:5000"
   k6 run spike_tests.js
   ```

El script:

- Ejecuta un **spike de carga** contra `GET /alumnos`.
- Verifica:
  - `status 200` en las respuestas.
  - Que la respuesta tenga `Content-Type: application/json`.
- Aplica umbrales (`thresholds`):
  - `p(95) < 500 ms` en `http_req_duration`.
  - Tasa de error `< 1%` en `http_req_failed`.

El análisis detallado de resultados se documenta en  
**`ANALISIS_TEST_CARGA_K6.md`** (cuando corresponda).

---

## ✅ Notas de buenas prácticas

- Arquitectura multicapa → facilita aplicar principios **SOLID** y **DRY**.
- Configuración por variables de entorno → alineado con **12-Factor App**.
- Proyecto preparado para:
  - Incorporar **Circuit Breaker**, **Retry**, **Rate Limit** y **cache en Redis/Dragonfly**.
  - Extender tests con enfoque **TDD** en nuevas funcionalidades.
