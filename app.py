from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os 
from database.database import db
from routes.usuario_route import user_routes
from routes.rol_user_route import rol_routes
from routes.sexs_routes import user_sex_routes
from routes.cuenta_activa import user_active_cuenta_routes
from routes.preguntas_route import user_preguntas
from routes.asignatura_route import user_asignatura_routes
from routes.grado_route import user_grado_routes
from routes.grupos_route import user_grupos_routes
from routes.carrera_tecnica_route import user_carrera_tecnica_routes
from routes.clinicas_route import user_clinicas_routes
from routes.docentes_route import user_docentes_routes
from routes.paises import user_paises_routes
from routes.estados import user_estados_routes
from routes.cuenta_credencial import user_cuenta_credencial_routes
from routes.alumnos import alumnos_routes
from routes.motivo_credencial import motivos_credencial_routes
from routes.mensajes_motivo_credencial import mensajes_motivo_credencial_routes
from routes.credencial_escolar import credencial_escolar_routes
from routes.welcome import welcome_routes
from routes.mision_route import mision_routes
from routes.vision_route import vision_routes
from routes.horarios_escolares import horarios_escolares_routes
from routes.horario_alumnos import horario_alumnos
from routes.asistencia_alumnos import asistencia_alumnos_routes
from routes.user_alumnos_routes import user_alumnos_routes
from routes.alumnos_search_routes import alumnos_search_routes
from routes.carrusel_routes import carrusel_routes

from waitress import serve
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

app = Flask(__name__)
CORS(app)

# SQL SERVER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Telcel4773@WasakaBegeinTv/EDUCBTAOFICIAL?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
db.init_app(app)

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, SQLAlchemyError):
        return jsonify({'error': 'Error de la base de datos'}), 500
    return jsonify({'error': str(e)}), 500



# Registrar las rutas
app.register_blueprint(user_routes)
app.register_blueprint(rol_routes)
app.register_blueprint(user_sex_routes)
app.register_blueprint(user_active_cuenta_routes)
app.register_blueprint(user_preguntas)
app.register_blueprint(user_asignatura_routes)
app.register_blueprint(user_grado_routes)
app.register_blueprint(user_grupos_routes)
app.register_blueprint(user_carrera_tecnica_routes)
app.register_blueprint(user_clinicas_routes)
app.register_blueprint(user_docentes_routes)
app.register_blueprint(user_paises_routes)
app.register_blueprint(user_estados_routes)
app.register_blueprint(user_cuenta_credencial_routes)
app.register_blueprint(alumnos_routes)
app.register_blueprint(motivos_credencial_routes)
app.register_blueprint(mensajes_motivo_credencial_routes)
app.register_blueprint(credencial_escolar_routes)
app.register_blueprint(welcome_routes)
app.register_blueprint(mision_routes)
app.register_blueprint(vision_routes)
app.register_blueprint(horarios_escolares_routes)
app.register_blueprint(horario_alumnos)
app.register_blueprint(asistencia_alumnos_routes)
app.register_blueprint(user_alumnos_routes)
app.register_blueprint(alumnos_search_routes)
app.register_blueprint(carrusel_routes)
@app.route('/')
def hello_world():
    return 'API CORRIENDO EDU CONTROL CBTA5 xxxx'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=50002)