from flask import render_template, request, jsonify, flash, Blueprint, session, url_for, redirect
from servicios.serviciousuario import ServicioUsuario
from servicios.servicioturno import ServicioTurno
from servicios.serviciopersonal import ServicioPersonal

appusuario = Blueprint('appusuario',__name__)

@appusuario.route('/login')
def login():
    data={
        'titulo':'Login:',
        'nombre':'Nombre: ',
        'mail':'Mail: ',
        'contraseña':'Contraseña: '
    }
    return render_template('login.html',data=data)

@appusuario.route('/modificar',methods=['POST'])
def modificar():
    data={
        'titulo':'Modificar datos:',
        'nombre':'Nuevo nombre: ',
        'mail':'Nuevo mail: ',
        'contraseña':'Nueva contraseña: '
    }
    return render_template('nuevosdatos_usuario.html',data=data)

@appusuario.route('/menuusuario', methods=['GET'])
def menuusuario():
    id_usuario = session.get('id_usuario')
    turnos = ServicioTurno.obtener_turno_por_usuario(id_usuario)
    todopersonal=ServicioPersonal.listar_personal()
    data={
        'titulo':'Bienvenido/a',
        'verTurnos':'Mis turnos: ',
        'sacarTurno':'Sacar nuevo turno: ',
        'cancelarTurno':'Cancelar un turno: ',
        'modificarCuenta':'Modificar Cuenta: ',
        'eliminarCuenta':'Eliminar cuenta: ',
        'calificarPersonal': 'Calificar personal: ',
        'turnos':turnos,
        'todopersonal':todopersonal
    }

    try:
        return render_template('menuusuario.html',data=data)
    except Exception as e:
        print(f"Error al renderizar el template2: {e}")
        return "Error al cargar el menu de usuario", 500
    
@appusuario.route('/sacarturno',methods=['POST'])
def sacarturno():
    id_usuario = session.get('id_usuario')
    data={
        'titulo':'Sacar nuevo turno',
        'tipo':'Seleccioná el tipo de turno: '
    }
    return render_template('sacarturno.html',data=data, id_usuario=id_usuario)

@appusuario.route('/registrarusuario',methods=['POST'])
def registrarusuario():
    nombre = request.form['nombre']
    mail = request.form['mail']
    contraseña = request.form['contraseña']
    
    mensaje = ServicioUsuario.agregar_usuario(nombre,mail,contraseña)
    flash(mensaje)
    usuario= ServicioUsuario.obtener_usuario_por_mail(mail)
    if usuario==0:
        error='Error al registrar'
        return render_template('login.html',error=error)
    else:
        if usuario.contraseña==contraseña:
            session['id_usuario']=usuario.id
            return redirect(url_for('appusuario.menuusuario', id_usuario=usuario.id))
        else:
            return 'Error al registrar'

@appusuario.route('/ingresarusuario',methods=['POST'])
def ingresarusuario():
    try:
        mail = request.form['mail2']
        contraseña = request.form['contraseña2']

        if not mail or not contraseña:
            print("Falta el correo o la contraseña")
            return jsonify({'error':'El correo y la contraseña son obligatorios'}),400
        else:
            usuario= ServicioUsuario.obtener_usuario_por_mail(mail)
            if usuario==0:
                error='Mail o contraseña incorrectos'
                flash(error)
                return redirect(url_for('appusuario.login'))
            else:
                if usuario.contraseña==contraseña:
                    session['id_usuario']=usuario.id
                    return redirect(url_for('appusuario.menuusuario', id_usuario=usuario.id))
                else:
                    error='Contraseña incorrecta'
                    flash(error)
                    return 'Contraseña incorrecta'
    except Exception as e:
        print(f"Error al ingresar usuario: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

@appusuario.route('/eliminarusuario', methods=['POST'])
def eliminarusuario():
    try:
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({'error':'No se encontro el ID del usuario'}), 400
        print(f"id: {id_usuario}")
        resultado= ServicioUsuario.eliminar_usuario(id_usuario)
        if resultado:
            session.pop('id_usuario',None)
            mensaje='Usuario eliminado correctamente'
            flash(mensaje)
            return redirect(url_for('appusuario.login'))
        else:
            return jsonify({'error':'No se pudo eliminar el usuario'}), 500
    except Exception as e:
        print(f"Error al eliminar el usuario {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500
    
@appusuario.route('/modificarusuario',methods=['POST'])
def modificarusuario():
    nombre = request.form['nombre']
    mail = request.form['mail']
    contraseña = request.form['contraseña']
    try:
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            return jsonify({'error':'No se encontro el ID del usuario'}), 400
        print(f"id: {id_usuario}")
        resultado= ServicioUsuario.modificar_usuario(id_usuario,nombre,mail,contraseña)
        if resultado:
            mensaje="Datos modificados correctamente"
            flash(mensaje)
            return redirect(url_for('appusuario.menuusuario',id_usuario=id_usuario))
        else:
            return jsonify({'error':'No se pudo modificar el usuario'}), 500
    except Exception as e:
        print(f"Error al modificar el usuario {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500 
    
@appusuario.route('/cancelarturno', methods=['POST'])
def cancelarturno():
    id_turno = request.form['id_turno']
    try:
        resultado = ServicioTurno.cancelarturno(id_turno)
        if resultado:
            mensaje='Turno cancelado correctamente'
            flash(mensaje)
            return redirect(url_for('appusuario.menuusuario'))
        else:
            return jsonify({'error':'No se pudo cancelar el turno'}), 500
    except Exception as e:
        print(f"Error al cancelar el turno {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500

@appusuario.route('/calificarpersonal', methods=['POST'])
def calificarpersonal():
    id_personal = request.form.get('id_personal')
    print(f"ID Personal: {id_personal}")
    data = {
        'titulo': 'Calificar personal',
        'id_personal': id_personal
    }
    try:
        return render_template('calificarpersonal.html', data=data)
    except Exception as e:
        print(f"Error al renderizar el template: {e}")
        return "Error al cargar la página de calificación", 500
    
@appusuario.route('/personalcalificado', methods=['POST'])
def personalcalificado():
    id_personal = request.form.get('id_personal')
    calificacion = int(request.form.get('calificacion'))
    print(f"ID Personal: {id_personal}, Calificación: {calificacion}")  # Debugging: Verifica que el ID personal y la calificación se obtienen correctamente
    resultado = ServicioUsuario.calificarpersonal(id_personal, calificacion)
    if resultado == "Personal calificado exitosamente":
        flash(resultado)
        return redirect(url_for('appusuario.menuusuario'))
    else:
        return jsonify({'error': resultado}), 500
    