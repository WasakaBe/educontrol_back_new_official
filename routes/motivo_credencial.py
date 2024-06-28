from flask import Blueprint,jsonify,request
from database.database import TBL_MOTIVO_CREDENCIAL

motivos_credencial_routes = Blueprint('motivos_credencial_routes',__name__)

@motivos_credencial_routes.route('/motivo/credencial',methods=['GET'])
def get_all_motivos_credencial():
 try:
  motivos = TBL_MOTIVO_CREDENCIAL.query.all()
  result = []
  
  for motivo in motivos:
   result.append({
    'id_motivo_credencial':motivo.id_motivo_credencial,
    'nombre_motivo_credencial':motivo.nombre_motivo_credencial,
   })
  return jsonify({'motivos':result})
 except Exception as e:
  return jsonify({'error':str(e)}), 500