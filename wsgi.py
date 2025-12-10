from app import create_app

# Esta es la aplicación WSGI que usará gunicorn dentro del contenedor
app = create_app()

if __name__ == "__main__":
    # Solo para correr local si quisieras: python wsgi.py
    app.run(host="0.0.0.0", port=5000)
