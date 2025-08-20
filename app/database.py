import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Leer la URI de la base de datos desde el .env
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

if not DATABASE_URL:
    raise ValueError("❌ No se encontró la variable SQLALCHEMY_DATABASE_URI en el .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()