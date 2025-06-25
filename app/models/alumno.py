
from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    carrera = Column(String(50), nullable=True)
    año_ingreso = Column(Integer, nullable=True)
