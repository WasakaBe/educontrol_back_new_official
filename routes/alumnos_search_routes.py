from flask import Blueprint, jsonify, request, abort
from database.database import db, TBL_ALUMNOS, TBL_SEXOS, TBL_USUARIOS, TBL_CLINICAS, TBL_GRADOS, TBL_GRUPOS, TBL_TRASLADO, TBL_TRASLADO_TRANSPORTE, TBL_CARRERAS_TECNICAS, TBL_PAISES, TBL_ESTADOS, TBL_RELACION_FAMILIAR
from sqlalchemy.exc import SQLAlchemyError

alumnos_search_routes = Blueprint('alumnos_search_routes', __name__)

@alumnos_search_routes.route('/alumnos/search', methods=['GET'])
def search_alumnos():
    try:
        nombre = request.args.get('nombre', '')
        grado = request.args.get('grado', '')
        grupo = request.args.get('grupo', '')
        carrera = request.args.get('carrera', '')
        nocontrol = request.args.get('nocontrol', '')
        sexo = request.args.get('sexo', '')
        seguro_social = request.args.get('seguroSocial', '')

        query = TBL_ALUMNOS.query

        if nombre:
            query = query.filter(TBL_ALUMNOS.nombre_alumnos.ilike(f"%{nombre}%"))
        if grado:
            query = query.filter(TBL_ALUMNOS.idgrado == grado)
        if grupo:
            query = query.filter(TBL_ALUMNOS.idgrupo == grupo)
        if carrera:
            query = query.filter(TBL_ALUMNOS.idcarreratecnica == carrera)
        if nocontrol:
            query = query.filter(TBL_ALUMNOS.nocontrol_alumnos.ilike(f"%{nocontrol}%"))
        if sexo:
            query = query.filter(TBL_ALUMNOS.idsexo == sexo)
        if seguro_social:
            query = query.filter(TBL_ALUMNOS.seguro_social_alumnos.ilike(f"%{seguro_social}%"))

        alumnos = query.all()
        result = []
        for alumno in alumnos:
            sexo = TBL_SEXOS.query.get(alumno.idsexo).nombre_sexo
            usuario_alumno = TBL_USUARIOS.query.get(alumno.idusuario).correo_usuario
            clinica_alumno = TBL_CLINICAS.query.get(alumno.idclinica).nombre_clinicas
            grado_alumnos = TBL_GRADOS.query.get(alumno.idgrado).nombre_grado
            grupo_alumnos = TBL_GRUPOS.query.get(alumno.idgrupo).nombre_grupos
            traslado_alumnos = TBL_TRASLADO.query.get(alumno.idtraslado).nombre_traslado
            trasladotransporte_alumnos = TBL_TRASLADO_TRANSPORTE.query.get(alumno.idtrasladotransporte).nombre_traslado_transporte
            carrera_tecnica_alumnos = TBL_CARRERAS_TECNICAS.query.get(alumno.idcarreratecnica).nombre_carrera_tecnica
            pais_alumnos = TBL_PAISES.query.get(alumno.idpais).nombre_pais
            estado_alumnos = TBL_ESTADOS.query.get(alumno.idestado).nombre_estado
            relacionfamiliar = TBL_RELACION_FAMILIAR.query.get(alumno.idrelacionfamiliar).nombre_relacion_familiar
            result.append({
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
                'sexo': sexo,
                'usuario_alumno': usuario_alumno,
                'clinica_alumno': clinica_alumno,
                'grado_alumnos': grado_alumnos,
                'grupo_alumnos': grupo_alumnos,
                'traslado_alumnos': traslado_alumnos,
                'trasladotransporte_alumnos': trasladotransporte_alumnos,
                'carrera_tecnica_alumnos': carrera_tecnica_alumnos,
                'pais_alumnos': pais_alumnos,
                'estado_alumnos': estado_alumnos,
                'municipio_alumnos': alumno.municipio_alumnos,
                'comunidad_alumnos': alumno.comunidad_alumnos,
                'calle_alumnos': alumno.calle_alumnos,
                'proc_sec_alumno': alumno.proc_sec_alumno,
                'nombre_familiar_alumno': alumno.nombre_familiar_alumno,
                'app_familiar_alumno': alumno.app_familiar_alumno,
                'apm_familiar_alumno': alumno.apm_familiar_alumno,
                'relacionfamiliar': relacionfamiliar,
                'numero_telefono_familiar_alumno': alumno.numero_telefono_familiar_alumno,
            })
        return jsonify({'alumnos': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
