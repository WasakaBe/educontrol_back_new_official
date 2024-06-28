from database.database import TBL_CUENTA_CREDENCIAL
from flask import Blueprint,jsonify

user_cuenta_credencial_routes=Blueprint('user_cuenta_credencial_routes',__name__)

@user_cuenta_credencial_routes.route('/cuenta_credencial',methods=['GET'])
def get_all_cuenta_credencial():
 cuenta_credenciales = TBL_CUENTA_CREDENCIAL.query.all()
 result =[{'id_cuenta_credencial':cuenta_credencial.id_cuenta_credencial,'nombre_cuenta_credencial':cuenta_credencial.nombre_cuenta_credencial}for cuenta_credencial in cuenta_credenciales]
 return jsonify({'cuenta_credenciales':result})
  