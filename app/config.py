# app/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:segura_2025@localhost:5432/sysacaddb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False