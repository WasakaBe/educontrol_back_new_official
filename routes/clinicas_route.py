from database.database import db, TBL_CLINICAS
from flask import Blueprint, jsonify, request

user_clinicas_routes = Blueprint('user_clinicas_routes',__name__)

@user_clinicas_routes.route('/clinicas', methods=['GET'])
def get_all_clinicas():
    clinicas = TBL_CLINICAS.query.all()
    result = [{'id_clinicas': clinica.id_clinicas,
               'nombre_clinicas': clinica.nombre_clinicas
               } for clinica in clinicas]
    return jsonify({'clinicas': result})

@user_clinicas_routes.route('/clinicas', methods=['POST'])
def insert_clinica():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nueva_clinica = TBL_CLINICAS(
            nombre_clinicas=data.get('nombre_clinicas')
        )
        db.session.add(nueva_clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica insertada exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al insertar la clínica', 'error': str(e)}), 500

@user_clinicas_routes.route('/clinicas/<int:id>', methods=['DELETE'])
def delete_clinica(id):
    clinica = TBL_CLINICAS.query.get(id)
    if not clinica:
        return jsonify({'message': 'Clínica no encontrada'}), 404

    try:
        db.session.delete(clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica eliminada exitosamente'})
    except Exception as e:
        return jsonify({'message': 'Error al eliminar la clínica', 'error': str(e)}), 500

@user_clinicas_routes.route('/clinicas/<int:id>', methods=['PUT'])
def update_clinica(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

    clinica = TBL_CLINICAS.query.get(id)
    if not clinica:
        return jsonify({'message': 'Clínica no encontrada'}), 404

    try:
        clinica.nombre_clinicas = data.get('nombre_clinicas', clinica.nombre_clinicas)
        
        db.session.commit()
        return jsonify({'message': 'Clínica actualizada exitosamente'})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar la clínica', 'error': str(e)}), 500
