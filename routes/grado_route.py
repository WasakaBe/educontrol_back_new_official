from database.database import db, TBL_GRADOS
from flask import Blueprint, jsonify, request

user_grado_routes = Blueprint('user_grado_routes',__name__)

@user_grado_routes.route('/grados',methods=['GET'])
def get_all_grados():
 grados = TBL_GRADOS.query.all()
 result = [{'id_grado': grado.id_grado, 'nombre_grado': grado.nombre_grado} for grado in grados]
 return jsonify({'grados': result})