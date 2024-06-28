from flask import Blueprint, jsonify,request
from database.database import db, TBL_MENSAJES_MOTIVO_CREDENCIAL, TBL_ALUMNOS, TBL_MOTIVO_CREDENCIAL
from datetime import datetime

mensajes_motivo_credencial_routes = Blueprint('mensajes_motivo_credencial_routes', __name__)

@mensajes_motivo_credencial_routes.route('/ver-mensaje-solicitud', methods=['GET'])
def get_all_mensajes_motivo():
    # Realiza un join de las tablas necesarias para obtener los nombres y detalles adicionales
    mensajes = db.session.query(
        TBL_MENSAJES_MOTIVO_CREDENCIAL.id_mensajes_motivo_credencial,
        TBL_ALUMNOS.nombre_alumnos,
        TBL_ALUMNOS.app_alumnos,  # Apellido paterno
        TBL_ALUMNOS.apm_alumnos,  # Apellido materno
        TBL_ALUMNOS.nocontrol_alumnos,  # Número de control
        TBL_MOTIVO_CREDENCIAL.nombre_motivo_credencial,
        TBL_MENSAJES_MOTIVO_CREDENCIAL.fecha_motivo_credencial
    ).join(
        TBL_ALUMNOS, TBL_MENSAJES_MOTIVO_CREDENCIAL.idalumno == TBL_ALUMNOS.id_alumnos
    ).join(
        TBL_MOTIVO_CREDENCIAL, TBL_MENSAJES_MOTIVO_CREDENCIAL.idmotivo == TBL_MOTIVO_CREDENCIAL.id_motivo_credencial
    ).all()

    # Formatea los resultados para la respuesta JSON
    result = [{
        'id_mensajes_motivo_credencial': mensaje.id_mensajes_motivo_credencial,
        'nombre_completo_alumno': f"{mensaje.nombre_alumnos} {mensaje.app_alumnos} {mensaje.apm_alumnos}",
        'no_control_alumno': mensaje.nocontrol_alumnos,
        'nombre_motivo': mensaje.nombre_motivo_credencial,
        'fecha_motivo_credencial': mensaje.fecha_motivo_credencial
    } for mensaje in mensajes]
    
    return jsonify({'mensajes': result})

@mensajes_motivo_credencial_routes.route('/mensajes-motivos', methods=['POST'])
def insert_mensaje_motivo():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    idalumno = data.get('idalumno')
    idmotivo = data.get('idmotivo')
    fecha_motivo_credencial = data.get('fecha_motivo_credencial', datetime.utcnow())

    # Validaciones básicas de los datos
    if not idalumno or not idmotivo:
        return jsonify({'message': 'Falta información necesaria para insertar el mensaje motivo'}), 400

    try:
        nuevo_mensaje_motivo = TBL_MENSAJES_MOTIVO_CREDENCIAL(
            idalumno=idalumno,
            idmotivo=idmotivo,
            fecha_motivo_credencial=fecha_motivo_credencial
        )
        db.session.add(nuevo_mensaje_motivo)
        db.session.commit()
        return jsonify({'message': 'Mensaje motivo insertado exitosamente', 'id': nuevo_mensaje_motivo.id_mensajes_motivo_credencial}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al insertar el mensaje motivo', 'error': str(e)}), 500
    
    
@mensajes_motivo_credencial_routes.route('/mensajes-motivos/delete/<int:id>', methods=['DELETE'])
def delete_mensaje_motivo(id):
    try:
        mensaje_motivo = TBL_MENSAJES_MOTIVO_CREDENCIAL.query.get(id)
        if not mensaje_motivo:
            return jsonify({'message': 'Mensaje motivo no encontrado'}), 404

        db.session.delete(mensaje_motivo)
        db.session.commit()
        return jsonify({'message': 'Mensaje motivo eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar el mensaje motivo', 'error': str(e)}), 500
