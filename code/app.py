from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from controladores.controladorusuario import appusuario
from controladores.controladorpersonal import apppersonal
from controladores.controladorturno import appturno
from configuracion import conexion

def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY'] = 'root'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root1234@localhost/appturn'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    conexion.init_app(app)
    return app

app=create_app()

app.register_blueprint(appusuario,url_prefix='/appusuario')
app.register_blueprint(apppersonal,url_prefix='/apppersonal')
app.register_blueprint(appturno,url_prefix='/appturno')

#PAGINA PRINCIPAL
@app.route('/')
def index():
    data={
        'titulo':'Gestión de turnos SpAto',
        'bienvenida':'¡Hola, seleccione su próximo turno!',
        'eleccion':'¿Que sos?:'
    }
    try:
        return render_template('index.html',data=data)
    except Exception as e:
        print("Error al renderizar la plantilla: ",e)
        return "Error al cargar la pagina",500

''' TIPO TURNO
@app.route('/turno/<tipo>')
def turno(tipo):
    data={
        'titulo':'Tipo de Turno',
        'tipo':tipo
    }
    return render_template('turno.html',data=data)

REQUEST CON PARAMETROS
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Error en la ruta."

GET A TURNOS (VA EN EL CONTROLADORTURNO)
@app.route('/turnos')
def listar_turnos():
    data={
        
    }
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM turno"
        cursor.execute(sql)
        turnos=cursor.fetchall()
        #print(turnos)
        data['turnos']= turnos
        data['mensaje']='Exito.'
    except Exception as ex:
        data['mensaje']='Error...'
    return jsonify(data)


GET A PERSONAL (VA EN EL CONTROLADORPERSONAL)
@app.route('/personal')
def listar_personal():
    data={
        
    }
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM personal"
        cursor.execute(sql)
        personal=cursor.fetchall()
        #print(turnos)
        data['personal']= personal
        data['mensaje']='Exito.'
    except Exception as ex:
        data['mensaje']='Error...'
    return jsonify(data)
'''

def pagina_no_encontrada(error):
    # para avisar que no existe la pagina: return render_template('404.html'),404
    return redirect(url_for('index'))

if __name__=='__main__':
    #app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,port=5000)
