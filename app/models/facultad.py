from app import db

class Facultad(db.Model):
    __tablename__ = 'facultad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Facultad {self.id} - {self.nombre}>"
