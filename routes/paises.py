from database.database import TBL_PAISES
from flask import Blueprint,jsonify

user_paises_routes = Blueprint('user_paises_routes',__name__)

@user_paises_routes.route('/paises',methods=['GET'])
def get_all_paises():
 paises = TBL_PAISES.query.all()
 result =[{'id_pais':pais.id_pais,'nombre_pais':pais.nombre_pais,'foto_pais':pais.foto_pais} for pais in paises]
 return jsonify({'paises':result})