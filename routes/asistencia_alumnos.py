from flask import Blueprint,jsonify,request
from database.database import db, TBL_ASISTENCIAS
from datetime import datetime
asistencia_alumnos_routes = Blueprint('asistencia_alumnos_routes',__name__)

@asistencia_alumnos_routes.route('/asistencias', methods=['GET'])
def get_all_asistencias():
    asistencias = TBL_ASISTENCIAS.query.all()
    result = [{
        'id_asistencia': asistencia.id_asistencia,
        'id_alumno': asistencia.id_alumno,
        'id_horario': asistencia.id_horario,
        'fecha': asistencia.fecha.strftime('%Y-%m-%d %H:%M:%S'),  # Formateando la fecha a string
        'estado_asistencia': asistencia.estado_asistencia,
        'comentarios': asistencia.comentarios
    } for asistencia in asistencias]
    return jsonify({'asistencias': result})

@asistencia_alumnos_routes.route('/asistencias/insert', methods=['POST'])
def insert_asistencias():
    if not request.is_json:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser JSON'}), 400

    registros = request.get_json()
    if not isinstance(registros, list):  # Asegúrate de que recibes una lista
        return jsonify({'error': 'Expected a list of items'}), 400

    try:
        for registro in registros:
            if not isinstance(registro, dict):  # Asegúrate de que cada item sea un diccionario
                return jsonify({'error': 'All items must be dictionaries'}), 400
            nueva_asistencia = TBL_ASISTENCIAS(
                id_alumno=registro['id_alumno'],
                id_horario=registro['id_horario'],
                fecha=datetime.strptime(registro['fecha'], '%Y-%m-%d %H:%M:%S'),
                estado_asistencia=registro['estado_asistencia'],
                comentarios=registro['comentarios']
            )
            db.session.add(nueva_asistencia)
        db.session.commit()
        return jsonify({'message': 'Asistencias creadas exitosamente'}), 201
    except KeyError as e:
        db.session.rollback()  # Asegurarse de no dejar la DB en un estado inconsistente
        return jsonify({'error': f'Missing mandatory data: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500