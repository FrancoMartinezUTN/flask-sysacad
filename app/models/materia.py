from app.db import db

class Materia(db.Model):
    __tablename__ = "materias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f"<Materia {self.codigo} - {self.nombre}>"
