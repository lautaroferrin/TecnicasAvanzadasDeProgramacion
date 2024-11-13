from modelos.modelos import Personal
from configuracion import conexion

class PersonalDAO:
    @staticmethod
    def agregar_personal(nombre,mail,contraseña):
        nuevo_personal=Personal(nombre=nombre,mail=mail,contraseña=contraseña)
        conexion.session.add(nuevo_personal)
        conexion.session.commit()
        return nuevo_personal
    
    @staticmethod
    def obtener_personal_por_mail(mail):
        return conexion.session.query(Personal).filter_by(mail=mail).first()
    
    @staticmethod
    def obtener_personal_por_id(id_personal):
        return conexion.session.query(Personal).filter_by(id=id_personal).first()
    
    @staticmethod
    def obtener_todos_personal():
        return Personal.query.all()
    
    @staticmethod
    def eliminar_personal(id_personal):
        personal=Personal.query.get(id_personal)
        if personal:
            print(f"Eliminando el personal con id: {id_personal}")
            conexion.session.delete(personal)
            conexion.session.commit()
            return True
        return False
    
    @staticmethod
    def modificar_personal(id_personal,nombre=None,mail=None,contraseña=None):
        personal=Personal.query.get(id_personal)
        if personal:
            print(f"Modificando el personal con id: {id_personal} - dao")
            if nombre:
                personal.nombre=nombre
            else:
                personal.nombre=personal.nombre
            if mail:
                personal.mail=mail
            else:
                personal.mail=personal.mail
            if contraseña:
                personal.contraseña=contraseña
            else:
                personal.contraseña=personal.contraseña
            conexion.session.commit()
            print(f"Personal con id {id_personal} modificado correctamente - dao")
            return {"mensaje":"Personal modificado correctamente"},200
        
    @staticmethod
    def listar_personal():
        todopersonal=Personal.query.all()
        return todopersonal
    
    @staticmethod
    def obtener_calificacion_personal(id_personal):
        personal=Personal.query.get(id_personal)
        if personal:
            return personal.calificacion_promedio
        return False