from modelos.modelos import Turno
from configuracion import conexion

class TurnoDAO:
    @staticmethod
    def agregar_turno(usuario_id,personal_id,tipo,fecha,duracion):
        nuevo_turno=Turno(usuario_id,personal_id,tipo,fecha,duracion)
        conexion.session.add(nuevo_turno)
        conexion.session.commit()
        return nuevo_turno
    
    @staticmethod
    def obtener_turno_por_fecha(fecha):
        return conexion.session.query(Turno).filter_by(fecha=fecha).first()
    
    @staticmethod
    def obtener_turno_por_usuario(usuario_id):
        turnos=conexion.session.query(Turno).filter_by(usuario_id=usuario_id).all()
        return turnos
    
    @staticmethod
    def obtener_turno_por_personal(personal_id):
        turnos=conexion.session.query(Turno).filter_by(personal_id=personal_id).all()
        return turnos

    @staticmethod
    def obtener_turno_por_id(turno_id):
        return conexion.session.query(Turno).filter_by(id=turno_id).first()
    
    @staticmethod
    def cancelarturno(id_turno):
        turno=Turno.query.get(id_turno)
        if turno:
            conexion.session.delete(turno)
            conexion.session.commit()
            return True
        return False