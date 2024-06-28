from database.database import db, TBL_WELCOME
from flask import Blueprint, jsonify, request

welcome_routes = Blueprint('welcome_routes', __name__)

@welcome_routes.route('/welcomes/view', methods=['GET'])
def get_all_welcomes():
    try:
        # Aquí puedes limitar los campos específicos que deseas recuperar
        welcomes = TBL_WELCOME.query.with_entities(TBL_WELCOME.id_welcome, TBL_WELCOME.welcome_text).all()
        if not welcomes:
            # Retorna una respuesta vacía con un código 204 (No Content)
            return jsonify({'message': 'No welcomes found'}), 204
        
        result = [{'id_welcome': welcome.id_welcome, 'welcome_text': welcome.welcome_text} for welcome in welcomes]
        return jsonify({'welcomes': result})
    except Exception as e:
        # Manejar errores genéricos
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@welcome_routes.route('/welcomes/update/<int:id_welcome>', methods=['PATCH'])
def update_welcome(id_welcome):
    try:
        welcome = TBL_WELCOME.query.get(id_welcome)
        if not welcome:
            return jsonify({'message': 'Welcome not found'}), 404
        
        data = request.get_json()
        welcome_text = data.get('welcome_text')
        if welcome_text:
            welcome.welcome_text = welcome_text
            db.session.commit()
            return jsonify({'message': 'Welcome updated successfully', 'id_welcome': welcome.id_welcome, 'welcome_text': welcome.welcome_text})
        else:
            return jsonify({'message': 'No update data provided'}), 400
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500