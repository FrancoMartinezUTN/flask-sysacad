from app.db import db

class Universidad(db.Model):
    __tablename__ = 'universidad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Universidad {self.id} - {self.nombre}>"
