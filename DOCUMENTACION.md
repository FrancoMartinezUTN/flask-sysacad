# 📜 Documentación del Sistema Flask-Sysacad

Este archivo tiene como objetivo dejar asentada toda la información técnica necesaria para comprender cómo funciona el sistema actual de gestión de alumnos de la UTN llamado **Flask-Sysacad**. Esta documentación servirá para colaborar en equipo, escalar el proyecto y facilitar el ingreso de nuevos desarrolladores.

---

## 📁 Estructura del Proyecto

```text
flask-sysacad/
├── app/                    # Contiene la lógica principal de la aplicación
│   ├── models/             # Modelos de datos (ORM SQLAlchemy)
│   ├── routes/             # Rutas o endpoints de la API REST
│   ├── services/           # Lógica de negocio separada de las rutas
│   ├── validators/         # Validaciones de datos de entrada (opcional)
│   ├── __init__.py         # Punto de entrada para crear la app Flask
│   └── config.py           # Configuración de entornos (dev, prod)
├── run.py                  # Script principal que levanta el servidor
├── requirements.txt        # Dependencias del sistema
├── .env                    # Variables de entorno (usuario y BD)
├── README.md               # Documentación general del proyecto
└── docs/                   # Documentación técnica complementaria (.md)
```

> ✅ **¿Por qué esta estructura?** Para mantener una arquitectura limpia y escalable (multicapa). Cada carpeta cumple un rol específico que permite separar responsabilidades.

---

## 📦 Modelos Definidos

### `Alumno` (en `app/models/alumno_model.py`)

```python
id: int          # Identificador único, autoincremental
nombre: str      # Nombre completo del alumno
email: str       # Correo electrónico único
```

También incluye el método `to_dict()` que devuelve un diccionario con los datos del alumno. Esto facilita el trabajo en las respuestas JSON de la API.

> ✅ **¿Para qué sirven los modelos?** Representan las tablas de la base de datos. Permiten interactuar con PostgreSQL como si trabajáramos con objetos de Python (ORM).

---

## 🌐 Rutas Definidas

### Archivo: `app/routes/alumno_routes.py`

| Método | Ruta     | Función           | Descripción                           |
| ------ | -------- | ----------------- | ------------------------------------- |
| GET    | /alumnos | `get_alumnos()`   | Lista todos los alumnos               |
| POST   | /alumnos | `create_alumno()` | Crea un nuevo alumno con JSON enviado |

> ✅ **¿Qué son las rutas?** Son los endpoints HTTP que puede consumir un cliente (navegador o frontend). Se conectan con los servicios para responder solicitudes.

---

## ⚙️ Configuración del Entorno

### `.env`

Contiene las variables de entorno necesarias para la conexión a la base de datos. **Advertencia:** este archivo NUNCA debe subirse a GitHub si contiene credenciales reales.

```env
FLASK_CONTEXT=development
DEV_DATABASE_URI=postgresql://usuario:password@localhost:5432/sysacaddb
```

> ⚠️ **IMPORTANTE:** reemplazar `usuario` y `password` por los propios de cada desarrollador en su entorno local. Nunca exponer contraseñas reales en repositorios.

> ✅ **Recomendación de seguridad:** configurar el archivo `.gitignore` para que excluya automáticamente el archivo `.env` del control de versiones:

```gitignore
# Ignorar variables de entorno
.env
```

### `app/config.py`

Lee estas variables de entorno y configura la app según el entorno activo (desarrollo, producción, etc).

> ✅ **¿Por qué usamos `.env`?** Para separar las credenciales del código fuente y facilitar la configuración por usuario.

---

## 🚀 Inicialización del sistema

### `run.py`

Contiene:

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()

app.run(debug=True)
```

> ✅ **¿Qué hace este archivo?** Arranca la aplicación. Crea las tablas si no existen y lanza el servidor local (<http://127.0.0.1:5000>).

---

## 📄 Documentación Adicional

El proyecto incluye un directorio `docs/` donde se almacena el archivo `Documentacion Sysacad.pdf` como referencia complementaria. Este material:

- Sirve como respaldo de decisiones técnicas
- Puede ser consultado offline
- No contiene contraseñas ni datos sensibles

> ✅ **Recomendación:** mantener la versión más reciente de este PDF en el repositorio, pero sin sustituir la documentación Markdown colaborativa.

---

## 🧩 Alcance del microservicio_alumno

El **microservicio_alumno** se encarga de centralizar la lógica relacionada con los datos básicos de los alumnos del sistema Sysacad.

### Responsabilidades principales

- Gestionar el **ciclo de vida** de un alumno:
  - Alta (creación)
  - Consulta
  - Actualización
  - Baja (eliminación lógica o física, según se defina)
- Exponer endpoints **REST** que devuelven y reciben información de alumnos en formato **JSON**.
- Validar datos básicos antes de persistirlos (por ejemplo: formato de email, unicidad de DNI).
- Servir como **fuente de verdad** de los datos de alumno para otros módulos o microservicios.

### Fuera de alcance (otros módulos / microservicios)

- Gestión de inscripciones a materias y cursadas.
- Gestión de carreras, planes de estudio y correlatividades.
- Procesos administrativos generales (pagos, estados de deuda, legajos administrativos).
- Reportes globales que combinen alumnos + materias + notas + pagos.

> 🧠 En resumen: este microservicio se focaliza en “**quién es**” el alumno (sus datos maestros), no en “**qué hace**” en el sistema.

---

## 🔗 Endpoints principales del microservicio_alumno

A continuación se describen los endpoints clave asociados a alumnos.  
Se distinguen los **ya implementados** y los **previstos** para futuras iteraciones.

### ✅ Endpoints actualmente implementados

> Basados en `app/routes/alumno_routes.py`.

| Método | Ruta       | Descripción                                      | Estado        |
|--------|-----------|--------------------------------------------------|---------------|
| GET    | `/alumnos` | Devuelve el listado de alumnos.                 | Implementado  |
| POST   | `/alumnos` | Crea un nuevo alumno a partir de un JSON válido.| Implementado  |

### 🚧 Endpoints previstos / roadmap

> Estos endpoints sirven como guía de evolución del microservicio.

| Método | Ruta                       | Descripción                                                                    |
|--------|----------------------------|--------------------------------------------------------------------------------|
| GET    | `/alumnos/<id>`           | Obtiene el detalle de un alumno por su identificador interno.                 |
| PUT    | `/alumnos/<id>`           | Actualiza los datos básicos de un alumno existente.                           |
| DELETE | `/alumnos/<id>`           | Elimina (lógica o físicamente) un alumno.                                     |
| GET    | `/alumnos/<id>/ficha`     | Devuelve la ficha del alumno en formato JSON (datos consolidados).           |
| GET    | `/alumnos/<id>/ficha.pdf` | Devuelve la ficha del alumno en formato PDF (para impresión o descarga).     |

> 🔎 Aunque algunos endpoints aún no estén desarrollados, dejarlos documentados alinea al equipo con la visión de arquitectura y facilita el diseño de otros microservicios.

---

## ⚙️ Configuración y variables de entorno para el microservicio_alumno

El comportamiento del microservicio depende de variables de entorno, leídas desde `.env` en desarrollo o desde el entorno del sistema en producción.

| Variable                  | Obligatoria | Entorno      | Descripción                                                                 |
|---------------------------|------------|--------------|-----------------------------------------------------------------------------|
| `FLASK_CONTEXT`           | No         | Todos        | Indica el contexto: `development` / `production`. Default: `development`.  |
| `DEV_DATABASE_URI`        | No         | Desarrollo   | URI de conexión a la base de datos de desarrollo (PostgreSQL local).       |
| `SQLALCHEMY_DATABASE_URI` | Sí (prod)  | Producción   | URI de conexión a la base principal en entorno productivo.                 |
| `SECRET_KEY`              | Sí         | Todos        | Clave secreta de Flask para firmar cookies y sesiones.                     |
| `FLASK_DEBUG`             | No         | Desarrollo   | `True` para debug en local; debe estar desactivado en producción.          |

> 🔐 Buenas prácticas:
> - Nunca commitear valores reales de `SECRET_KEY` ni credenciales de base de datos.
> - En producción, usar siempre variables de entorno o un gestor de secretos.
> - Mantener `.env` fuera del control de versiones (ya configurado en `.gitignore`).

---

## 🔐 Verificación rápida de seguridad

El proyecto incluye un script auxiliar para validar aspectos mínimos de seguridad en la configuración de Flask.

### Script: `verify_security_fixes.py`

Este script verifica que:

- La aplicación **no arranca** si falta `SECRET_KEY`.
- El modo **debug está desactivado por defecto**.
- La aplicación **arranca correctamente** con una configuración válida.

### Cómo ejecutarlo

En la raíz del proyecto, con el entorno virtual activo:

```bash
python verify_security_fixes.py
```

Si todas las pruebas pasan, se mostrará un resumen con mensajes `PASS` indicando que:

- La app falla correctamente cuando falta `SECRET_KEY`.
- El modo debug por defecto es `False`.
- Con una configuración válida, la app inicia sin problemas.

---

## 📈 Prueba de carga con k6 para `/alumnos`

Esta sección documenta la prueba de carga sobre el endpoint `GET /alumnos` utilizando **k6**, basada en el script `spike_tests.js` brindado por la cátedra y adaptado al proyecto Flask-Sysacad.

### ✅ Requisitos previos

- k6 instalado y accesible desde la consola (`k6 version`).
- Entorno virtual de Python creado y activado (`.venv`).
- Variables de entorno configuradas correctamente (especialmente `SECRET_KEY` y la URI de base de datos).
- Base de datos PostgreSQL `sysacaddb` levantada.
- Aplicación Flask ejecutándose en:

```text
http://localhost:5000
```

### 🧩 Pasos para ejecutar la prueba de carga

1. **Activar el entorno virtual** en la raíz del proyecto:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Levantar la aplicación Flask**:

   ```powershell
   python run.py
   ```

   Esto deja la API escuchando en `http://localhost:5000`.

3. **En otra terminal**, ubicarse en la raíz del proyecto y ejecutar k6:

   ```powershell
   k6 run spike_tests.js
   ```

### 🔍 Descripción del escenario de carga

El archivo `spike_tests.js` define el siguiente escenario:

- Ramp-up hasta **100 usuarios virtuales (VUs)** en **10 segundos**.
- Mantiene **100 VUs** durante **20 segundos**.
- Ramp-down a **0 VUs** en **10 segundos**.

Cada VU realiza solicitudes `GET` al endpoint:

```text
http://localhost:5000/alumnos
```

El script registra:

- Códigos de estado HTTP (200, 400, 404, 409, 429, 500).
- Tiempos de respuesta (`http_req_duration`).
- Porcentaje de requests fallidas (`http_req_failed`).
- Métrica personalizada `status_codes` (Trend) para analizar la distribución de respuestas.

### ✅ Resultado esperado

En condiciones normales de funcionamiento:

- La mayoría de los checks deben aparecer como `"status is 200"`.
- La métrica `http_req_failed` debería ser `0.00%`.
- El promedio de `http_req_duration` debe mantenerse en valores razonables para el entorno local.

### 🔄 Ejecución en entorno Docker (opcional)

Si el proyecto se ejecuta dentro de **Docker** y el servicio Flask se expone con otro nombre (por ejemplo `web`), se puede ajustar la constante `BASE_URL` en `spike_tests.js` para apuntar a:

```js
const BASE_URL = "http://web:5000/alumnos";
```

Esto permite que el contenedor de k6 golpee al servicio Flask dentro de la misma red de Docker.

---

Con esto queda documentado el estado actual del sistema. A partir de aquí, el equipo puede continuar desarrollando nuevas funcionalidades con claridad.
