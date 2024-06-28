from database.database import db, TBL_USUARIOS,BITACORA_SESION,BITACORA_USUARIOS, TBL_TIPO_ROL, TBL_SEXOS, TBL_ACTIVOS_CUENTA, TBL_PREGUNTAS
from flask import Blueprint, jsonify, request
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import random

# Crear un blueprint para las ruta
user_routes = Blueprint('user_routes', __name__)

# Variable para almacenar el código generado
current_code = None

# Ruta para generar el código
@user_routes.route('/generate-code', methods=['GET'])
def generate_code():
    global current_code
    current_code = str(random.randint(100000, 999999))
    return jsonify({'code': current_code})

# Ruta para verificar el código
@user_routes.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    code = data.get('code')

    if code == current_code:
         # Obtener la información del usuario desde la base de datos
        tbl_user = TBL_USUARIOS.query.filter_by().first()
        # Crear el diccionario con la información del usuario
        user = {
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
                'respuestaPregunta': tbl_user.respuestaPregunta,
            }
        return jsonify({'message': 'Código correcto', 'user': user})
    else:
        return jsonify({'message': 'Código incorrecto'}), 400
    
    
#fin de rutas de wear os

# Ruta para obtener todos los usuarios
@user_routes.route('/users/view', methods=['GET'])
def get_all_users():
    users = TBL_USUARIOS.query.all()
    result = []
    for tbl_users in users:
        result.append({
            'id_usuario': tbl_users.id_usuario,
            'nombre_usuario': tbl_users.nombre_usuario,
            'app_usuario': tbl_users.app_usuario,
            'apm_usuario': tbl_users.apm_usuario,
            'fecha_nacimiento_usuario': tbl_users.fecha_nacimiento_usuario,
            'token_usuario': tbl_users.token_usuario,
            'correo_usuario': tbl_users.correo_usuario,
            'pwd_usuario': tbl_users.pwd_usuario,
            'phone_usuario': tbl_users.phone_usuario,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
            'idPregunta':tbl_users.idPregunta,
            'respuestaPregunta':tbl_users.respuestaPregunta,
        })
    return jsonify({'users': result})

# Ruta para obtener todos los usuarios
@user_routes.route('/users2/view', methods=['GET'])
def get_all_users2():
    users = TBL_USUARIOS.query.all()
    result = []
    for tbl_users in users:
        # Obtener nombres asociados a los IDs
        rol = TBL_TIPO_ROL.query.get(tbl_users.idRol).nombre_tipo_rol
        sexo = TBL_SEXOS.query.get(tbl_users.idSexo).nombre_sexo
        cuenta_activo = TBL_ACTIVOS_CUENTA.query.get(tbl_users.idCuentaActivo).nombre_activos_cuenta
        pregunta = TBL_PREGUNTAS.query.get(tbl_users.idPregunta).nombre_preguntas
        
        result.append({
            'id_usuario': tbl_users.id_usuario,
            'nombre_usuario': tbl_users.nombre_usuario,
            'app_usuario': tbl_users.app_usuario,
            'apm_usuario': tbl_users.apm_usuario,
            'fecha_nacimiento_usuario': tbl_users.fecha_nacimiento_usuario,
            'token_usuario': tbl_users.token_usuario,
            'correo_usuario': tbl_users.correo_usuario,
            'pwd_usuario': tbl_users.pwd_usuario,
            'phone_usuario': tbl_users.phone_usuario,
            'rol_usuario': rol,  # Nombre asociado al ID de rol
            'sexo_usuario': sexo,  # Nombre asociado al ID de sexo
            'cuenta_activo': cuenta_activo,  # Nombre asociado al ID de cuenta activa
            'pregunta': pregunta,  # Nombre asociado al ID de pregunta
            'respuestaPregunta': tbl_users.respuestaPregunta,
        })
    return jsonify({'users': result})


 # Ruta para obtener un usuario por ID
@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    tbl_users = TBL_USUARIOS.query.get(user_id)
    if tbl_users:
        result = {
            'id_usuario': tbl_users.id_usuario,
            'nombre_usuario': tbl_users.nombre_usuario,
            'app_usuario': tbl_users.app_usuario,
            'apm_usuario': tbl_users.apm_usuario,
            'fecha_nacimiento_usuario': tbl_users.fecha_nacimiento_usuario,
            'token_usuario': tbl_users.token_usuario,
            'correo_usuario': tbl_users.correo_usuario,
            'pwd_usuario': tbl_users.pwd_usuario,
            'phone_usuario': tbl_users.phone_usuario,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
            'idPregunta':tbl_users.idPregunta,
            'respuestaPregunta':tbl_users.respuestaPregunta,
        }
        return jsonify({'tbl_users': result})
    return jsonify({'message': 'Usuario no encontrado'}), 404

# Ruta para crear un nuevo usuario2 
@user_routes.route('/users/insert', methods=['POST'])
def create_user2():
    data = request.json

    # Obtener la dirección IP del usuario
    user_ip = request.remote_addr

    new_user2 = TBL_USUARIOS(
        nombre_usuario=data.get('nombre_usuario'),
        app_usuario=data.get('app_usuario'),
        apm_usuario=data.get('apm_usuario'),
        fecha_nacimiento_usuario=data.get('fecha_nacimiento_usuario'),
        token_usuario=data.get('token_usuario'),
        correo_usuario=data.get('correo_usuario'),
        pwd_usuario=data.get('pwd_usuario'),  # Guardar la contraseña encriptada
        phone_usuario=data.get('phone_usuario'),
        ip_usuario=user_ip,
        idRol=data.get('idRol'),
        idSexo=data.get('idSexo'),
        idCuentaActivo=data.get('idCuentaActivo'),
        idPregunta=data.get('idPregunta'),
        respuestaPregunta=data.get('respuestaPregunta')
    )


    try:
        db.session.add(new_user2)
        db.session.commit()
        
        # Insertar un nuevo registro en BITACORA_USUARIOS
        new_bitacora = BITACORA_USUARIOS(
            ID_USUARIO=new_user2.id_usuario,
            NOMBRE_USUARIO=new_user2.nombre_usuario,
            ACCION_REALIZADA='Registro',
            DETALLES_ACCION='Usuario registrado exitosamente',
            FECHA_ACCESO=datetime.now(),
            IP_ACCESO=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()
        # Envío de correo electrónico después de agregar el usuario exitosamente
        send_email(data['correo_usuario'], 'Bienvenido a la aplicación', data['nombre_usuario'])

        
        print(f"Nuevo usuario: {request.json['nombre_usuario']}")
        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    except Exception as e:
        # Manejar errores al agregar el usuario2
        print(f"Error al agregar usuario: {str(e)}")
        return jsonify({'message': 'Error al crear el usuario2'}), 500

def send_email(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('templates/email.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()
    


# Ruta para verificar la disponibilidad del correo
@user_routes.route('/check-email', methods=['POST'])
def check_email_availability():
    try:
        data = request.json
        existing_user = TBL_USUARIOS.query.filter_by(correo_usuario=data['correo_usuario']).first()
        if existing_user:
            return jsonify({'exists': True}), 200
        return jsonify({'exists': False}), 200
    except SQLAlchemyError as e:
        print('Error en la verificación de correo:', str(e))
        return jsonify({'error': 'Error en la verificación de correo'}), 500
    
# Ruta para obtener el token a partir del correo
@user_routes.route('/get-token', methods=['POST'])
def get_token_by_email():
    data = request.json
    tbl_users = TBL_USUARIOS.query.filter_by(correo_usuario=data['correo_usuario']).first()
    
    if tbl_users:
        send_token_notification(tbl_users.correo_usuario, 'Notificación de inicio de sesión', tbl_users.token_usuario)
        return jsonify({'token_usuario': tbl_users.token_usuario, 'id_usuario': tbl_users.id_usuario}), 200
    
    return jsonify({'message': 'Correo no encontrado'}), 404

# Añade esta función en tu código
def send_token_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('templates/emailupdate.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()

    

@user_routes.route('/get-token-by-emai/<string:user_email>', methods=['GET'])
def get_token_by_emai(user_email):
    # Busca un usuario con el correo proporcionado
    tbl_user = TBL_USUARIOS.query.filter_by(correo_usuario=user_email).first()

    # Verifica si se encontró un usuario con el correo
    if tbl_user:
        return jsonify({'token_usuario': tbl_user.token_usuario}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    
# Ruta para actualizar la contraseña de un usuario por correo electrónico
@user_routes.route('/updates-password', methods=['POST'])
def updates_password():
    try:
        data = request.json
        correo = data.get('correo_usuario')
        new_password = data.get('new_password')

        # Buscar al usuario por correo electrónico
        tbl_users = TBL_USUARIOS.query.filter_by(correo_usuario=correo).first()

        if tbl_users:
            # Verificar si la nueva contraseña es diferente de la anterior
            if tbl_users.pwd_usuario != new_password:
                # Actualizar la contraseña
                tbl_users.pwd_usuario = new_password
                db.session.commit()
                
                 # Insertar un nuevo registro en BITACORA_USUARIOS
                new_bitacora = BITACORA_USUARIOS(
                    ID_USUARIO=tbl_users.id_usuario,
                    NOMBRE_USUARIO=tbl_users.nombre_usuario,
                    ACCION_REALIZADA='Actualizacion',
                    DETALLES_ACCION='Usuario Actualizo exitosamente su password',
                    FECHA_ACCESO=datetime.now(),
                    IP_ACCESO=request.remote_addr
                )
                db.session.add(new_bitacora)
                db.session.commit()
                
                send_update_notification(tbl_users.correo_usuario, 'Notificación de Actualizacion de Contraseña', tbl_users.nombre_usuario)
                return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
            else:
                return jsonify({'message': 'La nueva contraseña debe ser diferente de la anterior'}), 400
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except SQLAlchemyError as e:
        print('Error al actualizar la contraseña:', str(e))
        return jsonify({'error': 'Error al actualizar la contraseña'}), 500
    
 # Añade esta función en tu código
def send_update_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('templates/emailupdatepwd.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()   

# Ruta para el proceso de inicio de sesión
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.json

    tbl_users = TBL_USUARIOS.query.filter_by(correo_usuario=data['correo_usuario']).first()
    if tbl_users:
        result = {
            'id_usuario': tbl_users.id_usuario,
            'nombre_usuario': tbl_users.nombre_usuario,
            'app_usuario': tbl_users.app_usuario,
            'apm_usuario': tbl_users.apm_usuario,
            'fecha_nacimiento_usuario': tbl_users.fecha_nacimiento_usuario,
            'token_usuario': tbl_users.token_usuario,
            'correo_usuario': tbl_users.correo_usuario,
            'pwd_usuario': tbl_users.pwd_usuario,
            'phone_usuario': tbl_users.phone_usuario,
            'idRol': tbl_users.idRol,
            'idSexo': tbl_users.idSexo,
            'idCuentaActivo': tbl_users.idCuentaActivo,
            'idPregunta':tbl_users.idPregunta,
            'respuestaPregunta':tbl_users.respuestaPregunta,
           }

         # Enviar la notificación de inicio de sesión
        send_login_notification(tbl_users.correo_usuario, 'Notificación de inicio de sesión', tbl_users.nombre_usuario)
        
        # Insertar un nuevo registro en BITACORA_SESION
        new_sesion = BITACORA_SESION(
            ID_USUARIO=tbl_users.id_usuario,
            NOMBRE_USUARIO=tbl_users.nombre_usuario,
            CORREO_USUARIO=tbl_users.correo_usuario,
            FECHA_INICIO=datetime.now(),
            IP_USUARIO=request.remote_addr,
            URL_SOLICITADA=request.url
        )
        db.session.add(new_sesion)
        db.session.commit()
        
        return jsonify({'tbl_users': result})
    return jsonify({'message': 'Credenciales incorrectas'}), 401


@user_routes.route('/Login', methods=['POST'])
def Login():
    data = request.json

    tbl_users = TBL_USUARIOS.query.filter_by(correo_usuario=data['correo_usuario']).first()
    if tbl_users:
        if tbl_users.pwd_usuario == data['pwd_usuario']:  # Verificar la contraseña
            result = {
                'id_usuario': tbl_users.id_usuario,
                'nombre_usuario': tbl_users.nombre_usuario,
                'app_usuario': tbl_users.app_usuario,
                'apm_usuario': tbl_users.apm_usuario,
                'fecha_nacimiento_usuario': tbl_users.fecha_nacimiento_usuario,
                'token_usuario': tbl_users.token_usuario,
                'correo_usuario': tbl_users.correo_usuario,
                'pwd_usuario': tbl_users.pwd_usuario,
                'phone_usuario': tbl_users.phone_usuario,
                'idRol': tbl_users.idRol,
                'idSexo': tbl_users.idSexo,
                'idCuentaActivo': tbl_users.idCuentaActivo,
                'idPregunta': tbl_users.idPregunta,
                'respuestaPregunta': tbl_users.respuestaPregunta,
            }

            # Enviar la notificación de inicio de sesión
            send_login_notification(tbl_users.correo_usuario, 'Notificación de inicio de sesión', tbl_users.nombre_usuario)

            # Insertar un nuevo registro en BITACORA_SESION
            new_sesion = BITACORA_SESION(
                ID_USUARIO=tbl_users.id_usuario,
                NOMBRE_USUARIO=tbl_users.nombre_usuario,
                CORREO_USUARIO=tbl_users.correo_usuario,
                FECHA_INICIO=datetime.now(),
                IP_USUARIO=request.remote_addr,
                URL_SOLICITADA=request.url
            )
            db.session.add(new_sesion)
            db.session.commit()

            return jsonify({'tbl_users': result})
        else:
            return jsonify({'message': 'La contraseña no coincide'}), 401
    return jsonify({'message': 'Correo no encontrado'}), 404

# Añade esta función en tu código
def send_login_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('templates/loginemail.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()
    
@user_routes.route('/recover-password', methods=['POST'])
def recover_password():
    try:
        data = request.json
        correo_usuario = data.get('correo_usuario')
        idPregunta = data.get('idPregunta')
        respuestaPregunta = data.get('respuestaPregunta')

        # Buscar al usuario por correo electrónico
        tbl_user = TBL_USUARIOS.query.filter_by(correo_usuario=correo_usuario).first()

        # Verificar si se encontró un usuario con el correo proporcionado
        if tbl_user:
            # Verificar si el idPregunta y la respuestaPregunta coinciden
            if tbl_user.idPregunta == idPregunta and tbl_user.respuestaPregunta == respuestaPregunta:
                return jsonify({'message': 'Éxito'}), 200
            else:
                return jsonify({'message': 'Las credenciales proporcionadas no coinciden'}), 400
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except Exception as e:
        print('Error al recuperar contraseña:', str(e))
        return jsonify({'error': 'Error al recuperar contraseña'}), 500
    


@user_routes.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        new_password = data.get('new_password')
        # Buscar al usuario por su ID
        tbl_user = TBL_USUARIOS.query.get(user_id)

        # Verificar si el usuario existe
        if tbl_user:
          if tbl_user.pwd_usuario != new_password:
            # Actualizar los datos del usuario con los nuevos valores
            tbl_user.nombre_usuario = data.get('nombre_usuario')
            tbl_user.app_usuario = data.get('app_usuario')
            tbl_user.apm_usuario = data.get('apm_usuario')
            tbl_user.correo_usuario = data.get('correo_usuario')
            tbl_user.pwd_usuario = data.get('new_password')
            tbl_user.phone_usuario = data.get('phone_usuario')


            # Guardar los cambios en la base de datos
            db.session.commit()

            # Insertar un nuevo registro en la bitácora de usuarios
            new_bitacora = BITACORA_USUARIOS(
                ID_USUARIO=user_id,
                NOMBRE_USUARIO=tbl_user.nombre_usuario,
                ACCION_REALIZADA='Actualización',
                DETALLES_ACCION='Datos de usuario actualizados exitosamente',
                FECHA_ACCESO=datetime.now(),
                IP_ACCESO=request.remote_addr
            )
            db.session.add(new_bitacora)
            db.session.commit() 
            send_update_info_notification(tbl_user.correo_usuario, 'Notificación de Actualizacion de Informacion', tbl_user.nombre_usuario)
            return jsonify({'message': 'Datos de usuario actualizados exitosamente'}), 200
          else:
             return jsonify({'message': 'La nueva contraseña debe ser diferente de la anterior'}), 400 
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except Exception as e:
        print('Error al actualizar datos de usuario:', str(e))
        return jsonify({'error': 'Error al actualizar datos de usuario'}), 500

 # Añade esta función en tu código
def send_update_info_notification(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('templates/emaildates.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())

    server.quit()   
    
@user_routes.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        # Buscar al usuario por su ID
        tbl_user = TBL_USUARIOS.query.get(user_id)

        # Verificar si el usuario existe
        if tbl_user:
            # Eliminar al usuario de la base de datos
            db.session.delete(tbl_user)
            db.session.commit()
            
            # Insertar un nuevo registro en la bitácora de usuarios
            new_bitacora = BITACORA_USUARIOS(
                ID_USUARIO=user_id,
                NOMBRE_USUARIO=tbl_user.nombre_usuario,
                ACCION_REALIZADA='Eliminación',
                DETALLES_ACCION='Usuario eliminado exitosamente',
                FECHA_ACCESO=datetime.now(),
                IP_ACCESO=request.remote_addr
            )
            db.session.add(new_bitacora)
            db.session.commit()
            
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

    except Exception as e:
        print('Error al eliminar usuario:', str(e))
        return jsonify({'error': 'Error al eliminar usuario'}), 500
    

