from flask import Blueprint, jsonify, request
from database.database import db, TBL_DOCENTES,TBL_SEXOS,TBL_USUARIOS,TBL_CLINICAS
from datetime import datetime

user_docentes_routes = Blueprint('user_docentes_routes', __name__)

@user_docentes_routes.route('/docentes', methods=['GET'])
def get_all_docentes():
    docentes = TBL_DOCENTES.query.all()
    
    result = []
    for docente in docentes:
        # Obtener nombres asociados a los IDs
        sexo = TBL_SEXOS.query.get(docente.idsexo).nombre_sexo if docente.idsexo else None
        usuariocorreo = TBL_USUARIOS.query.get(docente.idusuario).correo_usuario if docente.idusuario else None
        clinica = TBL_CLINICAS.query.get(docente.idclinica).nombre_clinicas if docente.idclinica else None
        
        result.append({
            'id_docentes': docente.id_docentes,
            'nombre_docentes': docente.nombre_docentes,
            'app_docentes': docente.app_docentes,
            'apm_docentes': docente.apm_docentes,
            'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.strftime('%Y-%m-%d'),
            'noconttrol_docentes': docente.noconttrol_docentes,
            'telefono_docentes': docente.telefono_docentes,
            'foto_docentes': docente.foto_docentes.decode('utf-8') if docente.foto_docentes else None,
            'seguro_social_docentes': docente.seguro_social_docentes,
            'sexo_docente': sexo,
            'usuario_docente': usuariocorreo,
            'clinica_docente': clinica
        })
    return jsonify({'docentes': result})

@user_docentes_routes.route('/docentes/<int:id>', methods=['GET'])
def get_docente_by_id(id):
    docente = TBL_DOCENTES.query.get(id)
    if not docente:
        return jsonify({'message': 'Docente no encontrado'}), 404
    
    result = {'id_docentes': docente.id_docentes,
              'nombre_docentes': docente.nombre_docentes,
              'app_docentes': docente.app_docentes,
              'apm_docentes': docente.apm_docentes,
              'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.strftime('%Y-%m-%d'),
              'noconttrol_docentes': docente.noconttrol_docentes,
              'telefono_docentes': docente.telefono_docentes,
              'foto_docentes': docente.foto_docentes.decode('utf-8') if docente.foto_docentes else None,
              'seguro_social_docentes': docente.seguro_social_docentes,
              'idsexo': docente.idsexo,
              'idusuario': docente.idusuario,
              'idclinica': docente.idclinica
              }
    return jsonify({'docente': result})

@user_docentes_routes.route('/docentes', methods=['POST'])
def insert_docente():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400
    
    try:
        nueva_docente = TBL_DOCENTES(
            nombre_docentes=data.get('nombre_docentes'),
            app_docentes=data.get('app_docentes'),
            apm_docentes=data.get('apm_docentes'),
            fecha_nacimiento_docentes=datetime.strptime(data.get('fecha_nacimiento_docentes'), '%Y-%m-%d'),
            noconttrol_docentes=data.get('noconttrol_docentes'),
            telefono_docentes=data.get('telefono_docentes'),
            foto_docentes=data.get('foto_docentes').encode('utf-8') if data.get('foto_docentes') else None,
            seguro_social_docentes=data.get('seguro_social_docentes'),
            idsexo=data.get('idsexo'),
            idusuario=data.get('idusuario'),
            idclinica=data.get('idclinica')
        )
        db.session.add(nueva_docente)
        db.session.commit()
        return jsonify({'message': 'Docente insertado exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al insertar el docente', 'error': str(e)}), 500

@user_docentes_routes.route('/docentes/<int:id>', methods=['PUT'])
def update_docente(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400
    
    docente = TBL_DOCENTES.query.get(id)
    if not docente:
        return jsonify({'message': 'Docente no encontrado'}), 404
    
    try:
        docente.nombre_docentes = data.get('nombre_docentes', docente.nombre_docentes)
        docente.app_docentes = data.get('app_docentes', docente.app_docentes)
        docente.apm_docentes = data.get('apm_docentes', docente.apm_docentes)
        docente.fecha_nacimiento_docentes = datetime.strptime(data.get('fecha_nacimiento_docentes'), '%Y-%m-%d')
        docente.noconttrol_docentes = data.get('noconttrol_docentes', docente.noconttrol_docentes)
        docente.telefono_docentes = data.get('telefono_docentes', docente.telefono_docentes)
        foto_docentes = data.get('foto_docentes')
        if foto_docentes:
            docente.foto_docentes = foto_docentes.encode('utf-8')
        docente.seguro_social_docentes = data.get('seguro_social_docentes', docente.seguro_social_docentes)
        docente.idsexo = data.get('idsexo', docente.idsexo)
        docente.idusuario = data.get('idusuario', docente.idusuario)
        docente.idclinica = data.get('idclinica', docente.idclinica)

        db.session.commit()
        return jsonify({'message': 'Docente actualizado exitosamente'})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el docente', 'error': str(e)}), 500

@user_docentes_routes.route('/docentes/<int:id>', methods=['DELETE'])
def delete_docente(id):
    docente = TBL_DOCENTES.query.get(id)
    if not docente:
        return jsonify({'message': 'Docente no encontrado'}), 404
    
    try:
        db.session.delete(docente)
        db.session.commit()
        return jsonify({'message': 'Docente eliminado exitosamente'})
    except Exception as e:
        return jsonify({'message': 'Error al eliminar el docente', 'error': str(e)}), 500

@user_docentes_routes.route('/docentes/nocontrol/<string:noconttrol>', methods=['GET'])
def get_docente_by_noconttrol(noconttrol):
    docente = TBL_DOCENTES.query.filter_by(noconttrol_docentes=noconttrol).first()
    if not docente:
        return jsonify({'message': 'Docente no encontrado'}), 404
    
    result = {
        'id_docentes': docente.id_docentes,
        'nombre_docentes': docente.nombre_docentes,
        'app_docentes': docente.app_docentes,
        'apm_docentes': docente.apm_docentes,
        'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.strftime('%Y-%m-%d'),
        'noconttrol_docentes': docente.noconttrol_docentes,
        'telefono_docentes': docente.telefono_docentes,
        'foto_docentes': docente.foto_docentes.decode('utf-8') if docente.foto_docentes else None,
        'seguro_social_docentes': docente.seguro_social_docentes,
        'sexo_docente': TBL_SEXOS.query.get(docente.idsexo).nombre_sexo if docente.idsexo else None,
        'usuario_docente': TBL_USUARIOS.query.get(docente.idusuario).correo_usuario if docente.idusuario else None,
        'clinica_docente': TBL_CLINICAS.query.get(docente.idclinica).nombre_clinicas if docente.idclinica else None
    }
    return jsonify(result)
