from database.database import db, TBL_VISION
from flask import Blueprint, jsonify, request

vision_routes = Blueprint('vision_routes',__name__)

@vision_routes.route('/vision/view',methods=['GET'])
def get_all_vision():
    try:
        # Aquí puedes limitar los campos específicos que deseas recuperar
        visiones = TBL_VISION.query.with_entities(TBL_VISION.id_vision, TBL_VISION.vision_text).all()
        if not visiones:
            # Retorna una respuesta vacía con un código 204 (No Content)
            return jsonify({'message': 'No visiones found'}), 204
        
        result = [{'id_vision': vision.id_vision, 'vision_text': vision.vision_text} for vision in visiones]
        return jsonify({'visiones': result})
    except Exception as e:
        # Manejar errores genéricos
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
       
@vision_routes.route('/vision/update/<int:id_vision>', methods=['PATCH'])
def update_welcome(id_vision):
    try:
        vision = TBL_VISION.query.get(id_vision)
        if not vision:
            return jsonify({'message': 'VISION not found'}), 404
        
        data = request.get_json()
        vision_text = data.get('vision_text')
        if vision_text:
            vision.vision_text = vision_text
            db.session.commit()
            return jsonify({'message': 'VISION updated successfully', 'id_vision': vision.id_vision, 'vision_text': vision.vision_text})
        else:
            return jsonify({'message': 'No update data vision provided'}), 400
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500