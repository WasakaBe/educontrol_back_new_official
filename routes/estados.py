from database.database import db, TBL_ESTADOS
from flask import Blueprint, jsonify, request

user_estados_routes = Blueprint('user_estados_routes', __name__)

@user_estados_routes.route('/estados', methods=['GET'])
def get_all_estados():
    estados = TBL_ESTADOS.query.all()
    result = [{'id_estado': estado.id_estado, 'nombre_estado': estado.nombre_estado, 'foto_estado': estado.foto_estado} for estado in estados]
    return jsonify({'estados': result})

@user_estados_routes.route('/estados', methods=['POST'])
def insert_estado():
    try:
        data = request.json
        nuevo_estado = TBL_ESTADOS(nombre_estado=data['nombre_estado'])
        db.session.add(nuevo_estado)
        db.session.commit()
        return jsonify({'message': 'Estado insertado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_estados_routes.route('/estados/<int:id>', methods=['PUT'])
def update_estado(id):
    try:
        data = request.json
        estado = TBL_ESTADOS.query.get(id)
        if estado:
            estado.nombre_estado = data['nombre_estado']
            db.session.commit()
            return jsonify({'message': 'Estado actualizado correctamente'})
        else:
            return jsonify({'error': 'El estado no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_estados_routes.route('/estados/<int:id>', methods=['DELETE'])
def delete_estado(id):
    try:
        estado = TBL_ESTADOS.query.get(id)
        if estado:
            db.session.delete(estado)
            db.session.commit()
            return jsonify({'message': 'Estado eliminado correctamente'})
        else:
            return jsonify({'error': 'El estado no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
