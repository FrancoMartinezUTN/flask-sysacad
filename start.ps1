# start.ps1

# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias si no están
pip install -r requirements.txt

# 3. Ejecutar el sistema
python run.py
