from database.database import db, TBL_PREGUNTAS
from flask import Blueprint,jsonify,request

user_preguntas = Blueprint('user_preguntas',__name__)

@user_preguntas.route('/preguntas',methods=['GET'])
def get_all_pregunts():
 preguntas = TBL_PREGUNTAS.query.all()
 result = [{'id_preguntas':pregunta.id_preguntas,'nombre_preguntas':pregunta.nombre_preguntas} for pregunta in preguntas]
 return jsonify({'preguntas':result})

@user_preguntas.route('/preguntas', methods=['POST'])
def insert_pregunta():
    try:
        data = request.json
        nueva_pregunta = TBL_PREGUNTAS(nombre_preguntas=data['nombre_preguntas']) # Suponiendo que 'nombre_preguntas' es el nombre del campo en el JSON recibido
        db.session.add(nueva_pregunta)
        db.session.commit()
        return jsonify({'message': 'Pregunta insertada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_preguntas.route('/preguntas/<int:id>', methods=['PUT'])
def update_pregunta(id):
    try:
        data = request.json
        pregunta = TBL_PREGUNTAS.query.get(id)
        if pregunta:
            pregunta.nombre_preguntas = data['nombre_preguntas'] # Actualiza el nombre de la pregunta con el valor recibido en el JSON
            db.session.commit()
            return jsonify({'message': 'Pregunta actualizada correctamente'})
        else:
            return jsonify({'error': 'La pregunta no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_preguntas.route('/preguntas/<int:id>', methods=['DELETE'])
def delete_pregunta(id):
    try:
        pregunta = TBL_PREGUNTAS.query.get(id)
        if pregunta:
            db.session.delete(pregunta)
            db.session.commit()
            return jsonify({'message': 'Pregunta eliminada correctamente'})
        else:
            return jsonify({'error': 'La pregunta no existe'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500