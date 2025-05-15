from flask import Blueprint, jsonify, request, render_template
from app.models import db, Robot, Intento

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registrar_robot', methods=['POST'])
def registrar_robot():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre no proporcionado.'})
    
    if Robot.query.filter_by(nombre=nombre).first():
        return jsonify({'success': False, 'error': 'Robot ya registrado.'})
    
    nuevo_robot = Robot(nombre=nombre)
    db.session.add(nuevo_robot)
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al registrar robot.'})

@main.route('/guardar_intento', methods=['POST'])
def guardar_intento():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    tiempo = data.get('tiempo')
    
    robot = Robot.query.filter_by(nombre=nombre).first()
    if not robot:
        return jsonify({'success': False, 'error': 'Robot no registrado.'})
    
    intentos_count = Intento.query.filter_by(robot_id=robot.id).count()
    if intentos_count >= 3:
        return jsonify({'success': False, 'error': 'Máximo de 3 intentos alcanzado.'})
    
    nuevo_intento = Intento(
        robot_id=robot.id,
        intento_numero=intentos_count + 1,
        tiempo=tiempo
    )
    db.session.add(nuevo_intento)
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al guardar intento.'})

@main.route('/obtener_resultados')
def obtener_resultados():
    resultados = db.session.query(Robot, Intento)\
        .join(Intento)\
        .order_by(Robot.nombre, Intento.intento_numero)\
        .all()
    return render_template('resultados.html', resultados=resultados)
