from app.db import db

class Facultad(db.Model):
    __tablename__ = "facultades"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Facultad {self.codigo} - {self.nombre}>"
