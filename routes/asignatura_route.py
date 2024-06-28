from database.database import db, TBL_ASIGNATURAS
from flask import Blueprint, jsonify, request

user_asignatura_routes = Blueprint('user_asignatura_routes',__name__)

@user_asignatura_routes.route('/asignaturas',methods=['GET'])
def get_all_asignaturas():
 asignaturas = TBL_ASIGNATURAS.query.all()
 result = [{'id_asignatura': asignatura.id_asignatura, 
            'nombre_asignatura': asignatura.nombre_asignatura} 
           for asignatura in asignaturas]
 return jsonify({'asignaturas': result})

@user_asignatura_routes.route('/asignaturas/insert', methods=['POST'])
def add_asignatura():
    data = request.json
    nombre_asignatura = data.get('nombre_asignatura')

    if not nombre_asignatura:
        return jsonify({'message': 'El nombre de la asignatura es requerido'}), 400

    nueva_asignatura = TBL_ASIGNATURAS(nombre_asignatura=nombre_asignatura)

    try:
        db.session.add(nueva_asignatura)
        db.session.commit()
        return jsonify({'message': 'Asignatura registrada exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al registrar la asignatura: {str(e)}'}), 500
    
@user_asignatura_routes.route('/asignaturas/update/<int:id_asignatura>', methods=['PUT'])
def update_asignatura(id_asignatura):
    data = request.json
    asignatura = TBL_ASIGNATURAS.query.get(id_asignatura)

    if not asignatura:
        return jsonify({'message': 'Asignatura no encontrada'}), 404

    nombre_asignatura = data.get('nombre_asignatura')

    if not nombre_asignatura:
        return jsonify({'message': 'El nombre de la asignatura es requerido'}), 400

    try:
        asignatura.nombre_asignatura = nombre_asignatura
        db.session.commit()
        return jsonify({'message': 'Asignatura actualizada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar la asignatura: {str(e)}'}), 500
    
@user_asignatura_routes.route('/asignaturas/delete/<int:id_asignatura>', methods=['DELETE'])
def delete_asignatura(id_asignatura):
    asignatura = TBL_ASIGNATURAS.query.get(id_asignatura)
    if not asignatura:
        return jsonify({'message': 'Asignatura no encontrada'}), 404

    try:
        db.session.delete(asignatura)
        db.session.commit()
        return jsonify({'message': 'Asignatura eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar la asignatura: {str(e)}'}), 500