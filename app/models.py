from datetime import datetime
from app import db

class Robot(db.Model):
    __tablename__ = 'robots'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    intentos = db.relationship('Intento', backref='robot', lazy=True)

class Intento(db.Model):
    __tablename__ = 'intentos'
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.Integer, db.ForeignKey('robots.id'), nullable=False)
    intento_numero = db.Column(db.Integer, nullable=False)
    tiempo = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
