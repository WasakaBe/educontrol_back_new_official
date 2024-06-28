from database.database import db, TBL_GRUPOS
from flask import Blueprint, jsonify, request

user_grupos_routes = Blueprint('user_grupos_routes',__name__)

@user_grupos_routes.route('/grupos',methods=['GET'])
def get_all_grupos():
 grupos = TBL_GRUPOS.query.all()
 result = [{'id_grupos': grupo.id_grupos, 'nombre_grupos': grupo.nombre_grupos} for grupo in grupos]
 return jsonify({'grupos': result})