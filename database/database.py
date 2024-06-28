from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class TBL_TIPO_ROL(db.Model):
    id_tipo_rol = db.Column(db.Integer, primary_key=True)
    nombre_tipo_rol = db.Column(db.String(30), nullable=False,unique=True)
class TBL_SEXOS(db.Model):
    id_sexos = db.Column(db.Integer, primary_key=True)
    nombre_sexo = db.Column(db.String(30),unique=True)
class TBL_ACTIVOS_CUENTA(db.Model):
    id_activos_cuenta = db.Column(db.Integer, primary_key=True)
    nombre_activos_cuenta = db.Column(db.String(30),unique=True)
    
class TBL_TRASLADO(db.Model):
    id_traslado = db.Column(db.Integer, primary_key=True)
    nombre_traslado = db.Column(db.String(20),nullable=False ,unique=True)

class TBL_TRASLADO_TRANSPORTE(db.Model):
    id_traslado_transporte = db.Column(db.Integer, primary_key=True)
    nombre_traslado_transporte = db.Column(db.String(20),nullable=False, unique=True)

class TBL_ASIGNATURAS(db.Model):
    id_asignatura = db.Column(db.Integer, primary_key=True)
    nombre_asignatura = db.Column(db.String(40),nullable=False, unique=True)
    
class TBL_GRADOS(db.Model):
    id_grado= db.Column(db.Integer, primary_key=True)
    nombre_grado = db.Column(db.Integer,nullable=False,unique=True) 
    
class TBL_GRUPOS(db.Model):
    id_grupos = db.Column(db.Integer,primary_key=True)
    nombre_grupos = db.Column(db.String(3),nullable=False,unique=True)

class TBL_PREGUNTAS(db.Model):
    id_preguntas = db.Column(db.Integer, primary_key=True)
    nombre_preguntas = db.Column(db.String(100), nullable=False,unique=True)
    
class TBL_CARRERAS_TECNICAS(db.Model):
    id_carrera_tecnica = db.Column(db.Integer, primary_key=True)
    nombre_carrera_tecnica = db.Column(db.String(200), nullable=False, unique=True)
    descripcion_carrera_tecnica = db.Column(db.Text, nullable=False)
    foto_carrera_tecnica = db.Column(db.LargeBinary)

class TBL_CLINICAS(db.Model):
    id_clinicas = db.Column(db.Integer, primary_key=True)
    nombre_clinicas = db.Column(db.String(100), nullable=False, unique=True)

class TBL_PAISES(db.Model):
    id_pais = db.Column(db.Integer, primary_key=True)
    nombre_pais = db.Column(db.String(250), nullable=False,unique=True)
    foto_pais = db.Column(db.LargeBinary)

class TBL_ESTADOS(db.Model):
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(250), nullable=False, unique=True)
    foto_estado = db.Column(db.LargeBinary)
    
class TBL_CUENTA_CREDENCIAL(db.Model):
    id_cuenta_credencial = db.Column(db.Integer, primary_key=True)
    nombre_cuenta_credencial = db.Column(db.String(5),nullable=False)
    
class TBL_RELACION_FAMILIAR(db.Model):
    id_relacion_familiar = db.Column(db.Integer, primary_key=True)
    nombre_relacion_familiar = db.Column(db.String(50),nullable=False,unique=True)
    
class TBL_MOTIVO_CREDENCIAL(db.Model):
    id_motivo_credencial = db.Column(db.Integer,primary_key=True)
    nombre_motivo_credencial = db.Column(db.String(50),nullable=False,unique=True)
    
class TBL_ACTIVIDADES_ESCOLARES(db.Model):
    id_actividad_escolar= db.Column(db.Integer,primary_key=True)
    titulo_actividad= db.Column(db.String(250),nullable=False)
    descripcion_actividad= db.Column(db.Text,nullable=False)
    imagen_actividad= db.Column(db.LargeBinary)
    
class TBL_USUARIOS(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    app_usuario = db.Column(db.String(100), nullable=False)
    apm_usuario = db.Column(db.String(100))
    fecha_nacimiento_usuario = db.Column(db.DateTime, nullable=True)
    token_usuario = db.Column(db.String(8))
    correo_usuario = db.Column(db.String(50), unique=True, nullable=False)
    pwd_usuario = db.Column(db.String(20), nullable=False)
    phone_usuario = db.Column(db.BigInteger)
    ip_usuario = db.Column(db.BigInteger)
    idRol = db.Column(db.Integer)
    idSexo = db.Column(db.Integer)
    idCuentaActivo = db.Column(db.Integer)
    idPregunta = db.Column(db.Integer)
    respuestaPregunta = db.Column(db.String(255))

class TBL_DOCENTES(db.Model):
    id_docentes = db.Column(db.Integer, primary_key=True)
    nombre_docentes = db.Column(db.String(50), nullable=False)
    app_docentes = db.Column(db.String(50), nullable=False)
    apm_docentes = db.Column(db.String(50), nullable=False)
    fecha_nacimiento_docentes = db.Column(db.DateTime, nullable=False)
    noconttrol_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    telefono_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    foto_docentes = db.Column(db.LargeBinary)
    seguro_social_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    idsexo = db.Column(db.Integer)
    idusuario = db.Column(db.Integer)
    idclinica = db.Column(db.Integer)

class TBL_ALUMNOS(db.Model):
    id_alumnos = db.Column(db.Integer, primary_key=True)
    nombre_alumnos = db.Column(db.String(100),nullable=False)
    app_alumnos = db.Column(db.String(100),nullable=False)
    apm_alumnos = db.Column(db.String(100),nullable=False)
    foto_alumnos = db.Column(db.LargeBinary)
    fecha_nacimiento_alumnos = db.Column(db.DateTime,nullable=False)
    curp_alumnos = db.Column(db.String(50),nullable=False,unique=True)
    nocontrol_alumnos = db.Column(db.BigInteger,nullable=False,unique=True)
    telefono_alumnos = db.Column(db.BigInteger,nullable=False,unique=True)
    seguro_social_alumnos = db.Column(db.BigInteger,nullable=False,unique=True)
    cuentacredencial_alumnos =  db.Column(db.String(2),nullable=False)
    idsexo = db.Column(db.Integer)
    idusuario = db.Column(db.Integer)
    idclinica = db.Column(db.Integer)
    idgrado = db.Column(db.Integer)
    idgrupo = db.Column(db.Integer)
    idtraslado = db.Column(db.Integer)
    idtrasladotransporte = db.Column(db.Integer)
    idcarreratecnica = db.Column(db.Integer)
    idpais=db.Column(db.Integer)
    idestado=db.Column(db.Integer)
    municipio_alumnos = db.Column(db.String(100),nullable=False)
    comunidad_alumnos = db.Column(db.String(100),nullable=False)
    calle_alumnos = db.Column(db.String(100),nullable=False)
    proc_sec_alumno = db.Column(db.String(100),nullable=False)
    nombre_familiar_alumno = db.Column(db.String(100),nullable=False)
    app_familiar_alumno = db.Column(db.String(100),nullable=False)
    apm_familiar_alumno = db.Column(db.String(100),nullable=False)
    idrelacionfamiliar=db.Column(db.Integer)
    numero_telefono_familiar_alumno = db.Column(db.BigInteger,nullable=False)
    foto_familiar_alumno = db.Column(db.LargeBinary)


    
class TBL_MENSAJES_MOTIVO_CREDENCIAL(db.Model):
    id_mensajes_motivo_credencial = db.Column(db.Integer, primary_key=True)
    idalumno = db.Column(db.Integer)
    idmotivo = db.Column(db.Integer)
    fecha_motivo_credencial = db.Column(db.DateTime)
    
class TBL_CREDENCIALES_ESCOLARES(db.Model):
    id_credencial_escolar = db.Column(db.Integer, primary_key=True)
    nombre_credencial_escolar = db.Column(db.String(100))
    app_credencial_escolar = db.Column(db.String(100))
    apm_credencial_escolar = db.Column(db.String(100))
    carrera_credencial_escolar = db.Column(db.String(100))
    grupo_credencial_escolar = db.Column(db.String(2))
    curp_credencial_escolar = db.Column(db.String(22))
    nocontrol_credencial_escolar = db.Column(db.String(22))
    segsocial_credencial_escolar = db.Column(db.String(22))
    idalumnocrede = db.Column(db.Integer)
    
class TBL_WELCOME(db.Model):
    id_welcome = db.Column(db.Integer, primary_key=True)
    welcome_text = db.Column(db.Text)
    
class TBL_MISION(db.Model):
    id_mision = db.Column(db.Integer, primary_key=True)
    mision_text = db.Column(db.Text)
    
class TBL_VISION(db.Model):
    id_vision = db.Column(db.Integer, primary_key=True)
    vision_text = db.Column(db.Text)
    
class BITACORA_SESION(db.Model):
    id_sesion = db.Column(db.Integer,primary_key=True)
    ID_USUARIO = db.Column(db.Integer)
    NOMBRE_USUARIO = db.Column(db.String(255),nullable=False)
    CORREO_USUARIO = db.Column(db.String(255), nullable=False)
    FECHA_INICIO = db.Column(db.DateTime, nullable=True)
    IP_USUARIO = db.Column(db.BigInteger)
    URL_SOLICITADA = db.Column(db.String(255), nullable=False)
class BITACORA_USUARIOS(db.Model):
    ID_BITACORA = db.Column(db.Integer,primary_key=True)
    ID_USUARIO = db.Column(db.Integer)
    NOMBRE_USUARIO = db.Column(db.String(255),nullable=False)
    ACCION_REALIZADA = db.Column(db.String(255), nullable=False)
    DETALLES_ACCION = db.Column(db.String(255), nullable=False)
    FECHA_ACCESO =db.Column(db.DateTime, nullable=True)
    IP_ACCESO = db.Column(db.BigInteger)
    
class TBL_HORARIOS_ESCOLARES(db.Model):
    id_horario = db.Column(db.Integer, primary_key=True)
    id_asignatura = db.Column(db.Integer,nullable=False)
    id_docente = db.Column(db.Integer,nullable=False)
    id_grado = db.Column(db.Integer,nullable=False)
    id_grupo = db.Column(db.Integer,nullable=False)
    id_carrera_tecnica = db.Column(db.Integer,nullable=False)
    ciclo_escolar = db.Column(db.String(10),nullable=False)
    dias_horarios = db.Column(db.Text)
    
class TBL_HORARIO_ALUMNOS(db.Model):
    id_horario_alumno = db.Column(db.Integer,primary_key=True)
    id_horario = db.Column(db.Integer,nullable=False)
    id_alumno = db.Column(db.Integer,nullable=False)
    fecha_inscripcion = db.Column(db.DateTime,nullable=False)

class TBL_ASISTENCIAS(db.Model):
    id_asistencia = db.Column(db.Integer,primary_key=True)
    id_alumno = db.Column(db.Integer,nullable=False)
    id_horario = db.Column(db.Integer,nullable=False)
    fecha = db.Column(db.DateTime,nullable=False)
    estado_asistencia = db.Column(db.String(50),nullable=False)
    comentarios = db.Column(db.Text,nullable=False)