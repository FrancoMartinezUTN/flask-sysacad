from app.db import db
from app.models.mixins import ToDictMixin

class Alumno(db.Model, ToDictMixin):
    __tablename__ = "alumnos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    carrera = db.Column(db.String(50), nullable=True)
    anio_ingreso = db.Column(db.Integer, nullable=True)
