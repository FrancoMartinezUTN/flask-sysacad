# 🧠 SysAcad

## 🔧 Flask SysAcad

Este es un sistema base desarrollado en Flask para la gestión de estudiantes, utilizando arquitectura multicapa, PostgreSQL y SQLAlchemy. Preparado para trabajo colaborativo y con entorno virtual configurado.

---

## 🧱 Requisitos previos

### ✅ Generales

- Python 3.12+
- Git
- PostgreSQL 16+
- Visual Studio Code o cualquier IDE compatible

---

## 💻 Instalación (Windows / Linux)

### 🧩 1. Clonar el repositorio

```bash
git clone https://github.com/FrancoMartinezUTN/flask-sysacad.git
cd flask-sysacad

🧰 2. Crear y activar entorno virtual
- python -m venv venv
.\venv\Scripts\Activate     # Windows
- source venv/bin/activate    # Linux/macOS

📦 3. Instalar dependencias

pip install -r requirements.txt

📥 Importación de alumnos desde CSV / Student CSV Import

Este módulo adicional permite importar grandes volúmenes de datos de alumnos desde un archivo .csv a la base de datos PostgreSQL. Está desarrollado siguiendo los principios DRY, YAGNI, KISS, con soporte para detección de duplicados y escritura eficiente.

This additional module allows importing large volumes of student data from a .csv file into the PostgreSQL database. It is built following DRY, YAGNI, KISS principles, with duplicate detection and efficient batch insertion.

⚙️ Ejecución / Run

🧱 1. Crear las tablas necesarias

python crear_tablas.py

📤 2. Ejecutar el importador de alumnos

python -m importacion_csv.importar_alumnos "ruta/alumnos.csv"

💡 Ejemplo real:


python -m importacion_csv.importar_alumnos "E:\1 Ingeniería...\alumnos.csv"

📌 Características / Features
Lectura eficiente con pandas

Inserción masiva (bulk_save_objects)

Evita duplicados por dni

Inserta solo registros nuevos

Generación automática de emails

Preparado para escalar a millones de filas

📝 Consideraciones

Se requiere tener la base de datos sysacaddb activa

La tabla alumnos se crea con crear_tablas.py

La columna dni debe ser única

La carrera se fija por defecto como "Ingeniería en Sistemas"

El año de ingreso se extrae de fecha_ingreso en el CSV

📁 Estructura relevante

├── app/
│   ├── models/alumno.py
│   ├── database.py
├── importacion_csv/
│   └── importar_alumnos.py
├── crear_tablas.py
├── alumnos.csv
├── requirements.txt
├── README.md
