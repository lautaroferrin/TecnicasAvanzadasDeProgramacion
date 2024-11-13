from dao.turnodao import TurnoDAO

class ServicioTurno:
    @staticmethod
    def agregar_turno(usuario_id,personal_id,tipo,fecha,duracion):
        if not usuario_id or not personal_id or not tipo or not fecha or not duracion:
            return "Todos los campos son obligatorios"
        
        if TurnoDAO.obtener_turno_por_fecha(fecha):
            return "Este turno ya esta registrado"
        
        TurnoDAO.agregar_turno(usuario_id,personal_id,tipo,fecha,duracion)
        return "Turno agregado exitosamente"
    
    @staticmethod
    def obtener_turno_por_fecha(fecha):
        try:
            turno=TurnoDAO.obtener_turno_por_fecha(fecha)
            if not turno:
                return 0
            return turno
        except Exception as e:
            raise Exception("Error al obtener el turno",str(e))
        
    @staticmethod
    def obtener_turno_por_usuario(usuario_id):
        try:
            turno=TurnoDAO.obtener_turno_por_usuario(usuario_id)
            if not turno:
                return []
            return turno
        except Exception as e:
            print(f"Error al obtener el turno por usuario aca: {e}")
            raise Exception("Error al obtener el turno",str(e))
        
    @staticmethod
    def obtener_turno_por_personal(personal_id):
        try:
            turnos=TurnoDAO.obtener_turno_por_personal(personal_id)
            print("turnos servicioturno: ",turnos)
            if not turnos:
                return []
            return turnos
        except Exception as e:
            print(f"Error al obtener el turno por personal aca: {e}")
            raise Exception("Error al obtener el turno",str(e))
        
    @staticmethod
    def cancelarturno(id_turno):
        try:
            turno=TurnoDAO.obtener_turno_por_id(id_turno)
            if not turno:
                return 0
            TurnoDAO.cancelarturno(id_turno)
            return "Turno cancelado exitosamente"
        except Exception as e:
            return{"error": str(e)},500
        