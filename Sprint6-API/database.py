# ARCHIVO: database.py
from sqlmodel import create_engine, Session, SQLModel

# Configuración de la base de datos (SQLite)
DATABASE_URL = "sqlite:///./fit_express.db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Crea las tablas en la BD si no existen"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependencia para obtener la sesión de BD"""
    with Session(engine) as session:
        yield session