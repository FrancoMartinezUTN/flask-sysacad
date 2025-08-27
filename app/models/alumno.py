from app.db import db

class Alumno(db.Model):
    __tablename__ = "alumnos"
    id = db.Column(db.Integer, primary_key=True)
    legajo = db.Column(db.String(50), unique=True, nullable=True)  # <- debe existir
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    facultad = db.Column(db.String(120), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    carrera = db.Column(db.String(120), nullable=True)
    anio_ingreso = db.Column(db.Integer, nullable=True)

