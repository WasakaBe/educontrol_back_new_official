from flask import Blueprint, jsonify, request
from database.database import db, TBL_HORARIOS_ESCOLARES, TBL_ASIGNATURAS, TBL_DOCENTES, TBL_GRADOS, TBL_GRUPOS, TBL_CARRERAS_TECNICAS
import json
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

horarios_escolares_routes = Blueprint('horarios_escolares_routes', __name__)

@horarios_escolares_routes.route('/horarios_escolares/views', methods=['GET'])
def get_all_horarios():
    horarios = TBL_HORARIOS_ESCOLARES.query.all()
    
    result = []
    for horario in horarios:
        # Obtener nombres asociados a los IDs
        asignatura = TBL_ASIGNATURAS.query.get(horario.id_asignatura).nombre_asignatura if horario.id_asignatura else None
        docente = TBL_DOCENTES.query.get(horario.id_docente)
        docente_nombre_completo = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}" if horario.id_docente and docente else None
        grado = TBL_GRADOS.query.get(horario.id_grado).nombre_grado if horario.id_grado else None
        grupo = TBL_GRUPOS.query.get(horario.id_grupo).nombre_grupos if horario.id_grupo else None
        carrera_tecnica = TBL_CARRERAS_TECNICAS.query.get(horario.id_carrera_tecnica).nombre_carrera_tecnica if horario.id_carrera_tecnica else None
         # Asignar dias_horarios si existe en la base de datos
        dias_horarios = json.loads(horario.dias_horarios) if horario.dias_horarios else []
        result.append({
            'id_horario': horario.id_horario,
            'asignatura': asignatura,
            'docente': docente_nombre_completo,
            'grado': grado,
            'grupo': grupo,
            'carrera_tecnica': carrera_tecnica,
            'ciclo_escolar': horario.ciclo_escolar,
            'dias_horarios': dias_horarios,
        })
    return jsonify(result)  # Directly return the list of results


def time_conflicts(new_time, existing_time):
    # Comprueba si dos periodos de tiempo se solapan
    new_start, new_end = [datetime.strptime(t, "%H:%M") for t in new_time]
    existing_start, existing_end = [datetime.strptime(t, "%H:%M") for t in existing_time]
    return new_start < existing_end and new_end > existing_start

@horarios_escolares_routes.route('/horarios_escolares/insert', methods=['POST'])
def insert_horario():
    try:
        data = request.get_json()
        dias_horarios_json = json.dumps(data['scheduleDays'])

        # Convertir los días y horas de JSON a objeto
        new_schedule_days = json.loads(dias_horarios_json)

        # Verificar si el horario ya existe en la base de datos
        existing_horarios = TBL_HORARIOS_ESCOLARES.query.filter_by(
            id_grupo=data['id_grupo'],  # Filtrar por grupo para validar solapamientos en el mismo grupo
            ciclo_escolar=data['ciclo_escolar']
        ).all()

        # Verificar conflictos de horario específicamente por día y horas
        for existing in existing_horarios:
            existing_days = json.loads(existing.dias_horarios)
            for new_day in new_schedule_days:
                for existing_day in existing_days:
                    if new_day['day'] == existing_day['day'] and \
                        time_conflicts((new_day['startTime'], new_day['endTime']), (existing_day['startTime'], existing_day['endTime'])):
                        return jsonify({'message': 'Conflicto de horario: otro horario ocupa este slot'}), 409

        # Si no hay conflictos, procede a insertar el nuevo horario
        new_horario = TBL_HORARIOS_ESCOLARES(
            id_asignatura=data['id_asignatura'],
            id_docente=data['id_docente'],
            id_grado=data['id_grado'],
            id_grupo=data['id_grupo'],
            id_carrera_tecnica=data['id_carrera_tecnica'],
            ciclo_escolar=data['ciclo_escolar'],
            dias_horarios=dias_horarios_json
        )
        db.session.add(new_horario)
        db.session.commit()
        return jsonify({'message': 'Horario created successfully'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print("SQLAlchemy Error:", e)  # Imprimir errores específicos de SQLAlchemy
        return jsonify({'error': 'Database error'}), 400
    except Exception as e:
        db.session.rollback()
        print("General Error:", e)  # Imprimir otros tipos de errores
        return jsonify({'error': str(e)}), 400



    
@horarios_escolares_routes.route('/horarios_escolares/search', methods=['GET'])
def search_horarios():
    query = TBL_HORARIOS_ESCOLARES.query

    # Obtener parámetros de consulta
    id_asignatura = request.args.get('id_asignatura')
    id_docente = request.args.get('id_docente')
    id_grado = request.args.get('id_grado')
    id_grupo = request.args.get('id_grupo')
    id_carrera_tecnica = request.args.get('id_carrera_tecnica')
    ciclo_escolar = request.args.get('ciclo_escolar')

    # Aplicar filtros basados en los parámetros existentes
    if id_asignatura:
        query = query.filter(TBL_HORARIOS_ESCOLARES.id_asignatura == id_asignatura)
    if id_docente:
        query = query.filter(TBL_HORARIOS_ESCOLARES.id_docente == id_docente)
    if id_grado:
        query = query.filter(TBL_HORARIOS_ESCOLARES.id_grado == id_grado)
    if id_grupo:
        query = query.filter(TBL_HORARIOS_ESCOLARES.id_grupo == id_grupo)
    if id_carrera_tecnica:
        query = query.filter(TBL_HORARIOS_ESCOLARES.id_carrera_tecnica == id_carrera_tecnica)
    if ciclo_escolar:
        query = query.filter(TBL_HORARIOS_ESCOLARES.ciclo_escolar.like(f"%{ciclo_escolar}%"))

    horarios = query.all()
    result = []
    for horario in horarios:
        asignatura = TBL_ASIGNATURAS.query.get(horario.id_asignatura).nombre_asignatura if horario.id_asignatura else None
        docente = TBL_DOCENTES.query.get(horario.id_docente)
        docente_nombre_completo = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}" if horario.id_docente and docente else None
        grado = TBL_GRADOS.query.get(horario.id_grado).nombre_grado if horario.id_grado else None
        grupo = TBL_GRUPOS.query.get(horario.id_grupo).nombre_grupos if horario.id_grupo else None
        carrera_tecnica = TBL_CARRERAS_TECNICAS.query.get(horario.id_carrera_tecnica).nombre_carrera_tecnica if horario.id_carrera_tecnica else None
        
        result.append({
            'id_horario': horario.id_horario,
            'asignatura': asignatura,
            'docente': docente_nombre_completo,
            'grado': grado,
            'grupo': grupo,
            'carrera_tecnica': carrera_tecnica,
            'ciclo_escolar': horario.ciclo_escolar,
        })
    return jsonify(result)  # Devolver los resultados filtrados

@horarios_escolares_routes.route('/horarios_escolares/views/<int:id_docente>', methods=['GET'])
def get_horarios_by_docente(id_docente):
    # Filtrar los horarios por id_docente
    horarios = TBL_HORARIOS_ESCOLARES.query.filter_by(id_docente=id_docente).all()
    
    result = []
    for horario in horarios:
        result.append({
            'id_horario': horario.id_horario,
            'id_asignatura': horario.id_asignatura,
            'id_docente': horario.id_docente,
            'id_grado': horario.id_grado,
            'id_grupo': horario.id_grupo,
            'id_carrera_tecnica': horario.id_carrera_tecnica,
            'ciclo_escolar': horario.ciclo_escolar,
        })
    return jsonify(result)

@horarios_escolares_routes.route('/horarios_escolares/views/control/<no_control>', methods=['GET'])
def get_horarios_by_no_control(no_control):
    # Buscar primero el docente por número de control para obtener su ID
    docente = TBL_DOCENTES.query.filter_by(noconttrol_docentes=no_control).first()
    if not docente:
        return jsonify({'message': 'Docente no encontrado'}), 404

    # Usar el ID del docente encontrado para filtrar los horarios
    horarios = TBL_HORARIOS_ESCOLARES.query.filter_by(id_docente=docente.id_docentes).all()
    
    result = []
    for horario in horarios:
        asignatura = TBL_ASIGNATURAS.query.get(horario.id_asignatura).nombre_asignatura if horario.id_asignatura else None
        docente = TBL_DOCENTES.query.get(horario.id_docente)
        docente_nombre_completo = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}" if horario.id_docente and docente else None
        grado = TBL_GRADOS.query.get(horario.id_grado).nombre_grado if horario.id_grado else None
        grupo = TBL_GRUPOS.query.get(horario.id_grupo).nombre_grupos if horario.id_grupo else None
        carrera_tecnica = TBL_CARRERAS_TECNICAS.query.get(horario.id_carrera_tecnica).nombre_carrera_tecnica if horario.id_carrera_tecnica else None
        
        # Asumiendo que el campo dias_horarios es un campo de texto que contiene JSON
        dias_horarios = json.loads(horario.dias_horarios) if horario.dias_horarios else []

        result.append({
            'id_horario': horario.id_horario,
            'asignatura': asignatura,
            'docente': docente_nombre_completo,
            'grado': grado,
            'grupo': grupo,
            'carrera_tecnica': carrera_tecnica,
            'ciclo_escolar': horario.ciclo_escolar,
            'dias_horarios': dias_horarios  # Incluir los días y horas de clase
        })
    return jsonify(result)



@horarios_escolares_routes.route('/horarios_escolares/docente/<int:id_docente>', methods=['GET'])
def get_horarios_por_docente(id_docente):
    try:
        # Consultar los horarios asociados al ID del docente
        horarios = TBL_HORARIOS_ESCOLARES.query.filter_by(id_docente=id_docente).all()
        result = []
        for horario in horarios:
            # Obtener información adicional de otras tablas mediante ID
            asignatura = TBL_ASIGNATURAS.query.get(horario.id_asignatura).nombre_asignatura if horario.id_asignatura else None
            docente = TBL_DOCENTES.query.get(horario.id_docente)
            docente_nombre_completo = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}" if docente else None
            grado = TBL_GRADOS.query.get(horario.id_grado).nombre_grado if horario.id_grado else None
            grupo = TBL_GRUPOS.query.get(horario.id_grupo).nombre_grupos if horario.id_grupo else None
            carrera_tecnica = TBL_CARRERAS_TECNICAS.query.get(horario.id_carrera_tecnica).nombre_carrera_tecnica if horario.id_carrera_tecnica else None
            # Convertir los días y horarios de JSON a un formato legible si existe
            dias_horarios = json.loads(horario.dias_horarios) if horario.dias_horarios else []
            
            result.append({
                'id_horario': horario.id_horario,
                'asignatura': asignatura,
                'docente': docente_nombre_completo,
                'grado': grado,
                'grupo': grupo,
                'carrera_tecnica': carrera_tecnica,
                'ciclo_escolar': horario.ciclo_escolar,
                'dias_horarios': dias_horarios
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500