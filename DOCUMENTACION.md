# 📜 Documentación del Sistema Flask-Sysacad

Este archivo tiene como objetivo dejar asentada toda la información técnica necesaria para comprender cómo funciona el sistema actual de gestión de alumnos de la UTN llamado **Flask-Sysacad**. Esta documentación servirá para colaborar en equipo, escalar el proyecto y facilitar el ingreso de nuevos desarrolladores.

---

## 📁 Estructura del Proyecto

```
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
id: int                  # Identificador único, autoincremental
nombre: str             # Nombre completo del alumno
email: str              # Correo electrónico único
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

> ✅ **¿Qué hace este archivo?** Arranca la aplicación. Crea las tablas si no existen y lanza el servidor local ([http://127.0.0.1:5000](http://127.0.0.1:5000)).

---

## 📄 Documentación Adicional

El proyecto incluye un directorio `docs/` donde se almacena el archivo `Documentacion Sysacad.pdf` como referencia complementaria. Este material:

* Sirve como respaldo de decisiones técnicas
* Puede ser consultado offline
* No contiene contraseñas ni datos sensibles

> ✅ **Recomendación:** mantener la versión más reciente de este PDF en el repositorio, pero sin sustituir la documentación Markdown colaborativa.

---

Con esto queda documentado el estado actual del sistema. A partir de aquí, el equipo puede continuar desarrollando nuevas funcionalidades con claridad.

