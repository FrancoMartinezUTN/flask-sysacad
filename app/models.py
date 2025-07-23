# app/models.py
from app import db

class Grado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Grado '{self.nombre}'>"