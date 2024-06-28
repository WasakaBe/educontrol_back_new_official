from flask import Blueprint, jsonify, request
from database.database import db, TBL_HORARIO_ALUMNOS, TBL_ALUMNOS

horario_alumnos = Blueprint('horario_alumnos', __name__)

@horario_alumnos.route('/horario_alumnos/<int:idHorario>', methods=['GET'])
def get_alumnos_por_horario(idHorario):
    try:
        # Recuperar todos los horarios de alumnos para el id_horario dado
        horarios = TBL_HORARIO_ALUMNOS.query.filter_by(id_horario=idHorario).all()
        
        # Lista para almacenar la información de los alumnos
        alumnos_info = []
        
        # Para cada horario, buscar el alumno correspondiente
        for horario in horarios:
            alumno = TBL_ALUMNOS.query.filter_by(id_alumnos=horario.id_alumno).first()
            if alumno:
                # Si el alumno existe, añadir sus datos al resultado
                alumnos_info.append({'id_alumno': alumno.id_alumnos, 'nombre': f"{alumno.nombre_alumnos} {alumno.app_alumnos} {alumno.apm_alumnos}"})
        
        return jsonify(alumnos_info), 200
    except Exception as e:
        # En caso de error, devolver un mensaje con el error
        return jsonify({'message': 'Error al recuperar alumnos', 'error': str(e)}), 500


@horario_alumnos.route('/horarios_alumnos/insert', methods=['POST'])
def insert_horario_alumnos():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nuevo_horario_alumno = TBL_HORARIO_ALUMNOS(
            id_horario=data.get('id_horario'),
            id_alumno=data.get('id_alumno'),
            fecha_inscripcion=data.get('fecha_inscripcion')
        )
        db.session.add(nuevo_horario_alumno)
        db.session.commit()
        return jsonify({'message': 'HORARIO ALUMNO insertada exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al insertar la HORARIO ALUMNO', 'error': str(e)}), 500
