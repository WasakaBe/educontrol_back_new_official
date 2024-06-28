from database.database import db, TBL_MISION
from flask import Blueprint, jsonify, request

mision_routes = Blueprint('mision_routes',__name__)

@mision_routes.route('/mision/view',methods=['GET'])
def get_all_mision():
    try:
        # Aquí puedes limitar los campos específicos que deseas recuperar
        misiones = TBL_MISION.query.with_entities(TBL_MISION.id_mision, TBL_MISION.mision_text).all()
        if not misiones:
            # Retorna una respuesta vacía con un código 204 (No Content)
            return jsonify({'message': 'No misiones found'}), 204
        
        result = [{'id_mision': mision.id_mision, 'mision_text': mision.mision_text} for mision in misiones]
        return jsonify({'misiones': result})
    except Exception as e:
        # Manejar errores genéricos
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
       
@mision_routes.route('/mision/update/<int:id_mision>', methods=['PATCH'])
def update_welcome(id_mision):
    try:
        mision = TBL_MISION.query.get(id_mision)
        if not mision:
            return jsonify({'message': 'MISION not found'}), 404
        
        data = request.get_json()
        mision_text = data.get('mision_text')
        if mision_text:
            mision.mision_text = mision_text
            db.session.commit()
            return jsonify({'message': 'MISION updated successfully', 'id_mision': mision.id_mision, 'mision_text': mision.mision_text})
        else:
            return jsonify({'message': 'No update data mision provided'}), 400
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500