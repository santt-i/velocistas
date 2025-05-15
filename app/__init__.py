from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'dev-key-very-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///robots_competencia.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
