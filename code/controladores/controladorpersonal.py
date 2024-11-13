from flask import render_template, request, jsonify, flash, Blueprint, session, redirect, url_for
from servicios.serviciopersonal import ServicioPersonal
from servicios.servicioturno import ServicioTurno

apppersonal = Blueprint('apppersonal',__name__)

@apppersonal.route('/login')
def login():
    data={
        'titulo':'Login:',
        'nombre':'Nombre: ',
        'mail':'Mail: ',
        'contraseña':'Contraseña: '
    }
    return render_template('loginpersonal.html',data=data)

@apppersonal.route('/modificar',methods=['POST'])
def modificar():
    data={
        'titulo':'Modificar datos:',
        'nombre':'Nuevo nombre: ',
        'mail':'Nuevo mail: ',
        'contraseña':'Nueva contraseña: '
    }
    return render_template('nuevosdatos_personal.html',data=data)

@apppersonal.route('/menupersonal')
def menupersonal():
    id_personal=session.get('id_personal')
    turnos= ServicioTurno.obtener_turno_por_personal(id_personal)
    print("Turnos: ",turnos)
    calificacion= ServicioPersonal.obtener_calificacion_personal(id_personal)
    data={
        'titulo':'Bienvenido/a',
        'verTurnos':'Ver mis turnos: ',
        'miCalificacion':'Mi calificacion: ',
        'cancelarTurno':'Cancelar un turno: ',
        'modificarCuenta':'Modificar Cuenta: ',
        'eliminarCuenta':'Eliminar cuenta: ',
        'turnos': turnos,
        'calificacion': calificacion
    }
    try:
        return render_template('menupersonal.html',data=data)
    except Exception as e:
        print(f"Error al renderizar el template2: {e}")
        return "Error al cargar el menu de personal", 500

@apppersonal.route('/registrarpersonal',methods=['POST'])
def registrarpersonal():
    nombre = request.form['nombre']
    mail = request.form['mail']
    contraseña = request.form['contraseña']
    
    mensaje = ServicioPersonal.agregar_personal(nombre,mail,contraseña)
    flash(mensaje)
    personal= ServicioPersonal.obtener_personal_por_mail(mail)
    if personal==0:
        error='Error al registrar'
        return render_template('login.html',error=error)
    else:
        if personal.contraseña==contraseña:
            session['id_personal']=personal.id
            return redirect(url_for('apppersonal.menupersonal',id_personal=personal.id))

@apppersonal.route('/ingresarpersonal',methods=['POST'])
def ingresarpersonal():
    try:
        mail = request.form['mail2']
        contraseña = request.form['contraseña2']

        if not mail or not contraseña:
            print("Falta el correo o la contraseña")
            return jsonify({'error':'El correo y la contraseña son obligatorios'}),400
        else:
            personal= ServicioPersonal.obtener_personal_por_mail(mail)
            if personal==0:
                error='Mail o contraseña incorrectos'
                flash(error)
                return redirect('apppersonal.login')
            else:
                if personal.contraseña==contraseña:
                    session['id_personal']=personal.id
                    return redirect(url_for('apppersonal.menupersonal',id_personal=personal.id))
                else:
                    error='Contraseña incorrecta'
                    flash(error)
                    return 'Contraseña incorrecta'
    except Exception as e:
        print(f"Error al ingresar personal: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500
    
@apppersonal.route('/eliminarpersonal', methods=['POST'])
def eliminarpersonal():
    try:
        id_personal = session.get('id_personal')
        if not id_personal:
            return jsonify({'error':'No se encontro el ID del personal'}), 400
        print(f"id: {id_personal}")
        resultado= ServicioPersonal.eliminar_personal(id_personal)
        if resultado:
            session.pop('id_personal',None)
            mensaje='Personal eliminado correctamente'
            flash(mensaje)
            return redirect(url_for('apppersonal.login'))
        else:
            return jsonify({'error':'No se pudo eliminar el personal'}), 500
    except Exception as e:
        print(f"Error al eliminar el personal {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500
    
@apppersonal.route('/modificarpersonal',methods=['POST'])
def modificarpersonal():
    nombre = request.form['nombre']
    mail = request.form['mail']
    contraseña = request.form['contraseña']
    try:
        id_personal = session.get('id_personal')
        if not id_personal:
            return jsonify({'error':'No se encontro el ID del personal'}), 400
        print(f"id: {id_personal}")
        resultado= ServicioPersonal.modificar_personal(id_personal,nombre,mail,contraseña)
        if resultado:
            mensaje="Datos modificados correctamente"
            flash(mensaje)
            return redirect(url_for('apppersonal.menupersonal',id_personal=id_personal))
        else:
            return jsonify({'error':'No se pudo modificar el personal'}), 500
    except Exception as e:
        print(f"Error al modificar el personal {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500 
    
@apppersonal.route('/cancelarturno', methods=['POST'])
def cancelarturno():
    id_turno = request.form['id_turno']
    print(f"ID turno: {id_turno}")
    try:
        resultado = ServicioTurno.cancelarturno(id_turno)
        if resultado:
            mensaje='Turno cancelado correctamente'
            flash(mensaje)
            return redirect(url_for('apppersonal.menupersonal'))
        else:
            return jsonify({'error':'No se pudo cancelar el turno'}), 500
    except Exception as e:
        print(f"Error al cancelar el turno {e}")
        return jsonify({'error':'Error al procesar la solicitud'}), 500
