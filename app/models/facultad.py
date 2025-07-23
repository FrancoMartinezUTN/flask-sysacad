from app import db

class Facultad(db.Model):
    __tablename__ = 'facultades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)