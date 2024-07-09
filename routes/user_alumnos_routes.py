from flask import Blueprint, jsonify, request
from database.database import db, TBL_USUARIOS, TBL_ALUMNOS, TBL_SEXOS, TBL_GRUPOS, TBL_CARRERAS_TECNICAS, TBL_RELACION_FAMILIAR, TBL_PAISES, TBL_ESTADOS, TBL_TRASLADO, TBL_TRASLADO_TRANSPORTE, TBL_CLINICAS
from datetime import datetime

user_alumnos_routes = Blueprint('user_alumnos_routes', __name__)

@user_alumnos_routes.route('/user/info/<int:user_id>', methods=['GET'])
def get_user_and_alumno_info(user_id):
    try:
        # Obtener la información del usuario
        tbl_user = TBL_USUARIOS.query.get(user_id)
        if not tbl_user:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        
        user_info = {
            'id_usuario': tbl_user.id_usuario,
            'nombre_usuario': tbl_user.nombre_usuario,
            'app_usuario': tbl_user.app_usuario,
            'apm_usuario': tbl_user.apm_usuario,
            'fecha_nacimiento_usuario': tbl_user.fecha_nacimiento_usuario,
            'token_usuario': tbl_user.token_usuario,
            'correo_usuario': tbl_user.correo_usuario,
            'phone_usuario': tbl_user.phone_usuario,
            'idRol': tbl_user.idRol,
            'idSexo': tbl_user.idSexo,
            'idCuentaActivo': tbl_user.idCuentaActivo,
            'idPregunta': tbl_user.idPregunta,
            'respuestaPregunta': tbl_user.respuestaPregunta
        }

        # Verificar si el rol del usuario es "alumno"
        if tbl_user.idRol == 2:  # Asumiendo que el rol de "alumno" es 2
            alumno = TBL_ALUMNOS.query.filter_by(idusuario=user_id).first()
            if not alumno:
                return jsonify({'message': 'Alumno no encontrado'}), 404
            
            alumno_info = {
                'id_alumnos': alumno.id_alumnos,
                'nombre_alumnos': alumno.nombre_alumnos,
                'app_alumnos': alumno.app_alumnos,
                'apm_alumnos': alumno.apm_alumnos,
                'fecha_nacimiento_alumnos': alumno.fecha_nacimiento_alumnos.strftime("%Y-%m-%d"),
                'curp_alumnos': alumno.curp_alumnos,
                'nocontrol_alumnos': alumno.nocontrol_alumnos,
                'telefono_alumnos': alumno.telefono_alumnos,
                'seguro_social_alumnos': alumno.seguro_social_alumnos,
                'cuentacredencial_alumnos': alumno.cuentacredencial_alumnos,
                'sexo': TBL_SEXOS.query.get(alumno.idsexo).nombre_sexo if alumno.idsexo else None,
                'usuario_alumno': tbl_user.correo_usuario,
                'clinica_alumno': TBL_CLINICAS.query.get(alumno.idclinica).nombre_clinicas if alumno.idclinica else None,
                'grado_alumnos': alumno.idgrado,
                'grupo_alumnos': TBL_GRUPOS.query.get(alumno.idgrupo).nombre_grupos if alumno.idgrupo else None,
                'traslado_alumnos': TBL_TRASLADO.query.get(alumno.idtraslado).nombre_traslado if alumno.idtraslado else None,
                'trasladotransporte_alumnos': TBL_TRASLADO_TRANSPORTE.query.get(alumno.idtrasladotransporte).nombre_traslado_transporte if alumno.idtrasladotransporte else None,
                'carrera_tecnica_alumnos': TBL_CARRERAS_TECNICAS.query.get(alumno.idcarreratecnica).nombre_carrera_tecnica if alumno.idcarreratecnica else None,
                'pais_alumnos': TBL_PAISES.query.get(alumno.idpais).nombre_pais if alumno.idpais else None,
                'estado_alumnos': TBL_ESTADOS.query.get(alumno.idestado).nombre_estado if alumno.idestado else None,
                'municipio_alumnos': alumno.municipio_alumnos,
                'comunidad_alumnos': alumno.comunidad_alumnos,
                'calle_alumnos': alumno.calle_alumnos,
                'proc_sec_alumno': alumno.proc_sec_alumno,
                'nombre_familiar_alumno': alumno.nombre_familiar_alumno,
                'app_familiar_alumno': alumno.app_familiar_alumno,
                'apm_familiar_alumno': alumno.apm_familiar_alumno,
                'relacionfamiliar': TBL_RELACION_FAMILIAR.query.get(alumno.idrelacionfamiliar).nombre_relacion_familiar if alumno.idrelacionfamiliar else None,
                'numero_telefono_familiar_alumno': alumno.numero_telefono_familiar_alumno
            }

            return jsonify({'user': user_info, 'alumno': alumno_info}), 200

        return jsonify({'user': user_info}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
