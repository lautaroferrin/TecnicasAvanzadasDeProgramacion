from configuracion import conexion

class Usuario(conexion.Model):
    __tablename__='usuario'
    id = conexion.Column(conexion.Integer, primary_key=True)
    nombre = conexion.Column(conexion.String(50), nullable=False)
    mail = conexion.Column(conexion.String(50), unique=True, nullable=False)
    contraseña = conexion.Column(conexion.String(50), nullable=False)

class Personal(conexion.Model):
    __tablename__='personal'
    id = conexion.Column(conexion.Integer, primary_key=True)
    nombre = conexion.Column(conexion.String(50), nullable=False)
    mail = conexion.Column(conexion.String(50), unique=True, nullable=False)
    calificacion_promedio = conexion.Column(conexion.Float, nullable=True)
    contraseña = conexion.Column(conexion.String(50), nullable=False)

class Turno(conexion.Model):
    __tablename__='turno'
    id = conexion.Column(conexion.Integer, primary_key=True)
    usuario_id = conexion.Column(conexion.Integer, nullable=False)
    personal_id = conexion.Column(conexion.Integer, nullable=False)
    tipo = conexion.Column(conexion.String(30), nullable=False)
    fecha = conexion.Column(conexion.DateTime, unique=True, nullable=False)
    duracion = conexion.Column(conexion.Integer, nullable=False)

    def __init__(self, usuario_id, personal_id, tipo, fecha, duracion):
        print("Personal id modelo: ",personal_id)
        self.usuario_id = usuario_id
        self.personal_id = personal_id
        self.tipo = tipo
        self.fecha = fecha
        self.duracion = duracion