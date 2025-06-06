# 📚 flask-sysacad

Sistema académico desarrollado con Flask para la gestión de entidades como alumnos, materias, grados, facultades y más.  
Proyecto colaborativo de Ingeniería en Sistemas – UTN San Rafael.

---

## 🚀 Tecnologías utilizadas

- Python 3.13+
- Flask
- SQLAlchemy
- PostgreSQL
- Pytest
- PowerShell / Bash
- Git + GitHub

---

## ⚙️ Requisitos

- Python 3.13 o superior
- PostgreSQL funcionando (ej: base `sysacaddb`)
- Entorno virtual con dependencias del `requirements.txt`
- Archivo `.env` configurado

---

## 🛠️ Instalación y ejecución local

```bash
git clone https://github.com/FrancoMartinezUTN/flask-sysacad.git
cd flask-sysacad

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Ejecutar aplicación
python run.py
