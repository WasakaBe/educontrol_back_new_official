from flask import Blueprint, jsonify, request
from database.database import db, TBL_CREDENCIALES_ESCOLARES

# Crear un blueprint para las rutas de credenciales escolares
credencial_escolar_routes = Blueprint('credencial_escolar_routes', __name__)

# Ruta para obtener todas las credenciales escolares
@credencial_escolar_routes.route('/credenciales_escolares', methods=['GET'])
def get_all_credenciales_escolares():
    credenciales = TBL_CREDENCIALES_ESCOLARES.query.all()
    result = [
        {
            'id_credencial_escolar': cred.id_credencial_escolar,
            'nombre_credencial_escolar': cred.nombre_credencial_escolar,
            'app_credencial_escolar': cred.app_credencial_escolar,
            'apm_credencial_escolar': cred.apm_credencial_escolar,
            'carrera_credencial_escolar': cred.carrera_credencial_escolar,
            'grupo_credencial_escolar': cred.grupo_credencial_escolar,
            'curp_credencial_escolar': cred.curp_credencial_escolar,
            'nocontrol_credencial_escolar': cred.nocontrol_credencial_escolar,
            'segsocial_credencial_escolar': cred.segsocial_credencial_escolar,
            'idalumnocrede': cred.idalumnocrede
        } for cred in credenciales
    ]
    return jsonify({'credenciales_escolares': result})


@credencial_escolar_routes.route('/credenciales_escolares/insert', methods=['POST'])
def insert_credencial_escolar():
    try:
        data = request.get_json()
        nueva_credencial = TBL_CREDENCIALES_ESCOLARES(
            nombre_credencial_escolar=data['nombre_credencial_escolar'],
            app_credencial_escolar=data['app_credencial_escolar'],
            apm_credencial_escolar=data['apm_credencial_escolar'],
            carrera_credencial_escolar=data['carrera_credencial_escolar'],
            grupo_credencial_escolar=data['grupo_credencial_escolar'],
            curp_credencial_escolar=data['curp_credencial_escolar'],
            nocontrol_credencial_escolar=data['nocontrol_credencial_escolar'],
            segsocial_credencial_escolar=data['segsocial_credencial_escolar'],
            idalumnocrede=data['idalumnocrede']
        )
        db.session.add(nueva_credencial)
        db.session.commit()
        return jsonify({'message': 'Credencial escolar añadida exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@credencial_escolar_routes.route('/credenciales_escolares/delete/<int:id>', methods=['DELETE'])
def delete_credencial_escolar(id):
    try:
        credencial = TBL_CREDENCIALES_ESCOLARES.query.get(id)
        if credencial:
            db.session.delete(credencial)
            db.session.commit()
            return jsonify({'message': 'Credencial escolar eliminada exitosamente'}), 200
        else:
            return jsonify({'error': 'Credencial escolar no encontrada'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
