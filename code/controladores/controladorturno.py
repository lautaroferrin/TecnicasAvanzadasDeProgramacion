from flask import render_template, request, jsonify, flash, Blueprint, session, redirect, url_for
from servicios.servicioturno import ServicioTurno
from servicios.serviciopersonal import ServicioPersonal
from datetime import datetime, timedelta

appturno = Blueprint('appturno',__name__)

@appturno.route('/sacarmasajes')
def sacarmasajes():
    id_usuario = session.get('id_usuario')
    data={
        'titulo':f'Nuevo turno del usuario con id: {id_usuario}',
        'duracion':'Los masajes tienen una duracion de 60 minutos.',
        'personal':'Seleccioná el personal con quien queres el turno: '
    }
    return render_template('sacarmasajes.html',data=data)

@appturno.route('/confirmarmasajes',methods=['POST'])
def confirmarmasajes():
    id_usuario = session.get('id_usuario')
    id_personal = request.form.get('id_personal')
    print(f"ID personal: {id_personal}")
    tipo='masajes'
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    duracion = 60

    fecha_hora_str = f"{fecha} {hora}"
    fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
    
    print("fecha final:",fecha_hora)

    busqueda = ServicioTurno.obtener_turno_por_fecha(fecha_hora)
    if busqueda:
        mensaje = "Este turno ya esta registrado"
        flash(mensaje)
        return redirect(url_for('appturno.sacarmasajes'))
    resultado = ServicioTurno.agregar_turno(id_usuario, id_personal, tipo, fecha_hora, duracion)
    print("Resultado: ", resultado)
    if resultado == "Turno agregado exitosamente":
        flash(resultado)
        return redirect(url_for('appusuario.menuusuario'))
    else:
        return jsonify({'error': resultado}), 500

@appturno.route('/listarpersonal', methods=['GET'])
def listar_personal():
    id_usuario = session.get('id_usuario')
    try:
        todopersonal = ServicioPersonal.listar_personal()
        data = {
            'titulo': f'Nuevo turno del usuario {id_usuario}',
            'duracion': 'Los masajes tienen una duracion de 60 minutos.',
            'personal': 'Seleccioná el personal con quien queres el turno: '
        }
        return render_template('sacarmasajes.html',todopersonal=todopersonal, data=data)
    except Exception as e:
        print(f"Error al listar personal aca: {e}")
        return "Error al listar personal", 500

@appturno.route('/calendario', methods=['GET'])
def calendario():
    id_personal = request.args.get('id_personal')
    fecha_hoy = datetime.now()
    fecha_manana = fecha_hoy + timedelta(days=1)
    fecha_formateada = fecha_manana.strftime('%Y-%m-%d')

    horas = [f"{hora}:00" for hora in range(10, 19)]

    data = {
        'titulo': 'Calendario',
        'fecha': fecha_formateada,
        'horas': horas
    }
    return render_template('calendario.html', data=data, id_personal=id_personal)

