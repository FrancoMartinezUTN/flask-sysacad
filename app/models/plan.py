from app.db import db

class Plan(db.Model):
    __tablename__ = "planes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Plan {self.id} - {self.nombre}>"
