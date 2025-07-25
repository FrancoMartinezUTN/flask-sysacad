from app import db

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), nullable=False)

    def __repr__(self):
        return f"<Materia '{self.nombre}'>"