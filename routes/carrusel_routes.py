from flask import Blueprint, jsonify, request
from database.database import db
from database.database import TBL_CARRUSEL_IMG
import base64

carrusel_routes = Blueprint('carrusel_routes', __name__)

# Ruta para obtener todas las imágenes del carrusel
@carrusel_routes.route('/carrusel', methods=['GET'])
def get_all_carrusel_images():
    carrusels = TBL_CARRUSEL_IMG.query.all()
    result = [{'id_carrusel': carrusel.id_carrusel, 
               'carrusel': base64.b64encode(carrusel.carrusel).decode('utf-8') if carrusel.carrusel else ''} 
              for carrusel in carrusels]
    return jsonify({'carrusels': result})

# Ruta para añadir una nueva imagen al carrusel
@carrusel_routes.route('/carrusel/insert', methods=['POST'])
def add_carrusel_image():
    carrusel_image = request.files.get('carrusel')
    if carrusel_image:
        new_carrusel = TBL_CARRUSEL_IMG(carrusel=carrusel_image.read())
        db.session.add(new_carrusel)
        db.session.commit()
        return jsonify({'message': 'Imagen añadida exitosamente'}), 201
    return jsonify({'message': 'No se proporcionó ninguna imagen'}), 400

# Ruta para obtener una imagen específica del carrusel por ID
@carrusel_routes.route('/carrusel/<int:id>', methods=['GET'])
def get_carrusel_image(id):
    carrusel = TBL_CARRUSEL_IMG.query.get(id)
    if carrusel:
        result = {'id_carrusel': carrusel.id_carrusel, 
                  'carrusel': base64.b64encode(carrusel.carrusel).decode('utf-8') if carrusel.carrusel else ''}
        return jsonify(result)
    return jsonify({'message': 'Imagen no encontrada'}), 404

# Ruta para eliminar una imagen del carrusel por ID
@carrusel_routes.route('/carrusel/<int:id>', methods=['DELETE'])
def delete_carrusel_image(id):
    carrusel = TBL_CARRUSEL_IMG.query.get(id)
    if carrusel:
        db.session.delete(carrusel)
        db.session.commit()
        return jsonify({'message': 'Imagen eliminada exitosamente'})
    return jsonify({'message': 'Imagen no encontrada'}), 404
