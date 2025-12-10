# Imagen base oficial de uv + Python 3.12 (requisito de la cátedra)
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo requirements primero para aprovechar cache de capas
COPY requirements.txt .

# Instalamos dependencias usando uv (modo recomendado)
RUN uv pip install --system -r requirements.txt

# Copiamos el resto del código de la app
COPY . .

# Exponemos el puerto donde va a escuchar el microservicio
EXPOSE 5000

# Comando de arranque:
#   - gunicorn como servidor de aplicaciones
#   - bindea a 0.0.0.0:5000
#   - usa el WSGI "wsgi:app" que definimos en wsgi.py
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
