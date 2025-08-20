from app.db import db

class Grado(db.Model):
    __tablename__ = "grados"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Grado {self.codigo} - {self.nombre}>"
