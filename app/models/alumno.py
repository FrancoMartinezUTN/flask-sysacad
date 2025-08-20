from app.db import db

class Alumno(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(db.Integer, primary_key=True, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    carrera = db.Column(db.String(50), nullable=True)
    año_ingreso = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Alumno {self.dni} - {self.apellido}, {self.nombre}>"
