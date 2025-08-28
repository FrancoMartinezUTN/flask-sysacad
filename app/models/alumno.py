from app.db import db

class Alumno(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(db.Integer, primary_key=True)
    legajo = db.Column(db.String(50), unique=True, nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    facultad = db.Column(db.String(120), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    carrera = db.Column(db.String(120), nullable=True)
    anio_ingreso = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "legajo": self.legajo,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "email": self.email,
            "facultad": self.facultad,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "carrera": self.carrera,
            "anio_ingreso": self.anio_ingreso,
        }
