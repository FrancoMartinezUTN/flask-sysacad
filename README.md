# ​ flask-sysacad

Sistema académico desarrollado con Flask para la gestión de entidades como **alumnos, materias, grados, facultades** y más.  
Proyecto colaborativo de Ingeniería en Sistemas – **UTN San Rafael**.  
Arquitectura **multicapa**, **PostgreSQL** y **SQLAlchemy**. Preparado para trabajo colaborativo y con entorno virtual configurado.

---

## ​ Tecnologías utilizadas / Stack
- Python 3.13+
- Flask
- SQLAlchemy
- PostgreSQL
- Pytest
- PowerShell / Bash
- Git + GitHub

---

## ​ Requisitos
- Python 3.13 o superior
- PostgreSQL funcionando (por ejemplo, base `sysacaddb`)
- Entorno virtual con dependencias del `requirements.txt`
- Archivo `.env` configurado (ver `.env.example`)

---
## ​ Integrantes
- Martinez Franco
- Mulena Adrian
- Ochoa Camila
## ​Uso de IA: Chat GPT, GROK

### 1) Clonar el repositorio
```bash
git clone https://github.com/FrancoMartinezUTN/flask-sysacad.git
cd flask-sysacad

2) Crear y activar entorno virtual

Windows
python -m venv venv
.\venv\Scripts\Activate

Linux/macOS
python -m venv venv
source venv/bin/activate

3) Instalar dependencias
pip install -r requirements.txt

4) Variables de entorno

No subas credenciales reales al repositorio. Usá un archivo local .env basado en:
cp .env.example .env

5) Ejecutar aplicación (modo simple)
python run.py

Importación de alumnos desde CSV

Este módulo adicional permite importar grandes volúmenes de datos de alumnos desde un archivo .csv a la base de datos PostgreSQL.
Sigue principios DRY, YAGNI, KISS, con detección de duplicados y inserción eficiente.

Ejecución

1. Crear las tablas necesarias:
python crear_tablas.py

2. ecutar el importador de alumnos:
python -m importacion_csv.importar_alumnos "ruta/alumnos.csv"

Ejemplo (Windows):
python -m importacion_csv.importar_alumnos "E:\1 Ingeniería...\alumnos.csv"

Características

Lectura eficiente con pandas

Inserción masiva (bulk_save_objects)

Evita duplicados por DNI

Inserta solo registros nuevos

Generación automática de emails

Preparado para escalar a millones de filas

Consideraciones

La base de datos sysacaddb debe estar activa

La tabla alumnos se crea con crear_tablas.py

La columna dni debe ser única

La carrera se fija por defecto como “Ingeniería en Sistemas”

El año de ingreso se extrae de fecha_ingreso en el CSV

Estructura relevante

├── app/
│   ├── models/alumno.py
│   ├── database.py
├── importacion_csv/
│   └── importar_alumnos.py
├── crear_tablas.py
├── alumnos.csv
├── requirements.txt
├── README.md


---

### Contexto adicional  
Según las mejores prácticas examinadas (por ejemplo, Real Python), un README de calidad claramente explica el propósito del proyecto, tecnologías usadas, cómo instalarlo y cómo contribuir. También sirve como **landing page** del repo y facilita que otros lo entiendan y usen fácilmente. :contentReference[oaicite:17]{index=17}

Pegalo y luego hacé clic en **Mark as resolved** para seguir con los demás conflictos.
::contentReference[oaicite:18]{index=18}
