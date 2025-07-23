from app import db  # Cambiar de from app.db import db

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'
    
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)