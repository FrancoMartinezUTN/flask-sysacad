from app import db

class Grado(db.Model):
    __tablename__ = 'grado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
def __repr__(self):
    return f"<Grado id={self.id} nombre={self.nombre}>"