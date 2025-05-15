import os
from pathlib import Path

class Config:
    # Obtiene el directorio base del proyecto
    BASE_DIR = Path(__file__).resolve().parent
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/instance/robots_competencia.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para sesiones
    SECRET_KEY = 'dev-key-very-secret'  # Cambiar en producción
