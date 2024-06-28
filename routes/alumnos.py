from flask import Blueprint, jsonify, request, abort
from database.database import db, TBL_ALUMNOS,TBL_SEXOS,TBL_USUARIOS,TBL_CLINICAS,TBL_GRADOS,TBL_GRUPOS,TBL_TRASLADO,TBL_TRASLADO_TRANSPORTE,TBL_CARRERAS_TECNICAS,TBL_PAISES,TBL_ESTADOS,TBL_RELACION_FAMILIAR,TBL_HORARIO_ALUMNOS,TBL_HORARIOS_ESCOLARES,TBL_ASIGNATURAS,TBL_DOCENTES
from routes.asistencia_alumnos import get_all_asistencias
import json
from sqlalchemy.exc import SQLAlchemyError

alumnos_routes = Blueprint('alumnos_routes', __name__)

@alumnos_routes.route('/alumnos', methods=['GET'])
def get_all_alumnos():
    try:
        alumnos = TBL_ALUMNOS.query.all()
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
                'trasladotransporte_alumnos':trasladotransporte_alumnos,
                'carrera_tecnica_alumnos':carrera_tecnica_alumnos,
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

# Nueva ruta para buscar por número de control
@alumnos_routes.route('/alumnos/nocontrol/<int:no_control>', methods=['GET'])
def get_alumno_by_nocontrol(no_control):
    alumno = TBL_ALUMNOS.query.filter_by(nocontrol_alumnos=no_control).first()
    if alumno:
        grupo_alumnos = TBL_GRUPOS.query.get(alumno.idgrupo).nombre_grupos
        carrera_tecnica_alumnos = TBL_CARRERAS_TECNICAS.query.get(alumno.idcarreratecnica).nombre_carrera_tecnica
        return jsonify({
            'id_alumnos': alumno.id_alumnos,
            'nombre_alumnos': alumno.nombre_alumnos,
            'app_alumnos': alumno.app_alumnos,
            'apm_alumnos': alumno.apm_alumnos,
            'fecha_nacimiento_alumnos': alumno.fecha_nacimiento_alumnos.strftime("%Y-%m-%d"),
            'curp_alumnos': alumno.curp_alumnos,
            'nocontrol_alumnos': alumno.nocontrol_alumnos,
            'telefono_alumnos': alumno.telefono_alumnos,
            'seguro_social_alumnos': alumno.seguro_social_alumnos,
            'grupo_alumnos': grupo_alumnos,
            'carrera_tecnica_alumnos':carrera_tecnica_alumnos,
        })
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    
# Nueva ruta para buscar por CURP

@alumnos_routes.route('/alumnos/curp/<string:curp>', methods=['GET'])
def get_alumno_by_curp(curp):
    if not curp or len(curp) != 18:
        abort(400, description="CURP inválido")

    alumno = TBL_ALUMNOS.query.filter_by(curp_alumnos=curp.upper()).first()
    if alumno:
        # Completamos la información del alumno con todos los campos relevantes
        response = {
            'id_alumnos': alumno.id_alumnos,
            'nombre_alumnos': alumno.nombre_alumnos,
            'app_alumnos': alumno.app_alumnos,
            'apm_alumnos': alumno.apm_alumnos,
            'fecha_nacimiento_alumnos': alumno.fecha_nacimiento_alumnos.strftime("%Y-%m-%d"),
            'curp_alumnos': alumno.curp_alumnos,
            'nocontrol_alumnos': alumno.nocontrol_alumnos,
            'telefono_alumnos': alumno.telefono_alumnos,
            'seguro_social_alumnos': alumno.seguro_social_alumnos,
            'grupo_alumnos': TBL_GRUPOS.query.get(alumno.idgrupo).nombre_grupos if alumno.idgrupo else "No asignado",
            'carrera_tecnica_alumnos': TBL_CARRERAS_TECNICAS.query.get(alumno.idcarreratecnica).nombre_carrera_tecnica if alumno.idcarreratecnica else "No asignada"
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    
# Nueva ruta para buscar alumno por ID de usuario
@alumnos_routes.route('/alumnos/user/<int:user_id>', methods=['GET'])
def get_alumno_by_user_id(user_id):
    alumno = TBL_ALUMNOS.query.filter_by(idusuario=user_id).first()
    if alumno:
        return jsonify({
            'id_alumnos': alumno.id_alumnos,
            'nombre_alumnos': alumno.nombre_alumnos,
            'app_alumnos': alumno.app_alumnos,
            'apm_alumnos': alumno.apm_alumnos,
            'curp_alumnos': alumno.curp_alumnos,
            'nocontrol_alumnos': alumno.nocontrol_alumnos,
            # Agrega otros campos necesarios aquí
        })
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404


@alumnos_routes.route('/alumnos/<int:no_control>/horarios', methods=['GET'])
def get_horarios_by_no_control(no_control):
    try:
        # Buscar el alumno por número de control
        alumno = TBL_ALUMNOS.query.filter_by(nocontrol_alumnos=no_control).first()
        if not alumno:
            return jsonify({'message': 'Alumno no encontrado'}), 404

        # Buscar horarios asociados al alumno
        horarios = TBL_HORARIO_ALUMNOS.query.filter_by(id_alumno=alumno.id_alumnos).all()

        # Obtener información de los horarios
        result = []
        for horario in horarios:
            horario_escolar = TBL_HORARIOS_ESCOLARES.query.get(horario.id_horario)
            if horario_escolar:
                asignatura = TBL_ASIGNATURAS.query.get(horario_escolar.id_asignatura).nombre_asignatura if horario_escolar.id_asignatura else None
                docente = TBL_DOCENTES.query.get(horario_escolar.id_docente)
                docente_nombre_completo = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}" if horario_escolar.id_docente and docente else None
                grado = TBL_GRADOS.query.get(horario_escolar.id_grado).nombre_grado if horario_escolar.id_grado else None
                grupo = TBL_GRUPOS.query.get(horario_escolar.id_grupo).nombre_grupos if horario_escolar.id_grupo else None
                carrera_tecnica = TBL_CARRERAS_TECNICAS.query.get(horario_escolar.id_carrera_tecnica).nombre_carrera_tecnica if horario_escolar.id_carrera_tecnica else None
                # Asumiendo que el campo dias_horarios es un campo de texto que contiene JSON
                # Asumiendo que el campo dias_horarios es un campo de texto que contiene JSON
                try:
                    dias_horarios = json.loads(horario_escolar.dias_horarios) if horario_escolar.dias_horarios else []
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON para el horario {horario_escolar.id_horario}: {e}")
                    dias_horarios = []  # Continuar con una lista vacía en caso de error

                result.append({
                    'id_horario': horario_escolar.id_horario,
                    'asignatura': asignatura,
                    'docente': docente_nombre_completo,
                    'grado': grado,
                    'grupo': grupo,
                    'carrera_tecnica': carrera_tecnica,
                    'ciclo_escolar': horario_escolar.ciclo_escolar,
                    'dias_horarios': dias_horarios
                })

        return jsonify(result), 200
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({'error': str(e)}), 500



@alumnos_routes.route('/alumnos/<int:no_control>/horarios/<int:id_horario>/detalle', methods=['GET'])
def get_detalle_horario(no_control, id_horario):
    try:
        # Obtener todas las asistencias relacionadas con el alumno y el horario
        response = get_all_asistencias()
        if response.status_code != 200:
            abort(response.status_code, description='Error al obtener las asistencias del alumno')

        # Obtener las asistencias, tardíos y faltas del alumno para el horario específico
        asistencias = 0
        tardios = 0
        faltas = 0
        asistencias_data = response.json.get('asistencias')
        for asistencia in asistencias_data:
            if asistencia['id_horario'] == id_horario and asistencia['id_alumno'] == no_control:
                if asistencia['estado_asistencia'] == 'Asistencia':
                    asistencias += 1
                elif asistencia['estado_asistencia'] == 'Tardio':
                    tardios += 1
                elif asistencia['estado_asistencia'] == 'Falta':
                    faltas += 1

        return jsonify({
            'asistencias': asistencias,
            'tardios': tardios,
            'faltas': faltas
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
