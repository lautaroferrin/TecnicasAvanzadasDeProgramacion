from modelos.modelos import Usuario
from configuracion import conexion

class UsuarioDAO:
    @staticmethod
    def agregar_usuario(nombre,mail,contraseña):
        nuevo_usuario=Usuario(nombre=nombre,mail=mail,contraseña=contraseña)
        conexion.session.add(nuevo_usuario)
        conexion.session.commit()
        return nuevo_usuario
    
    @staticmethod
    def obtener_usuario_por_mail(mail):
        return conexion.session.query(Usuario).filter_by(mail=mail).first()
    
    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        return conexion.session.query(Usuario).filter_by(id=id_usuario).first()
    
    @staticmethod
    def obtener_todos_usuarios():
        return Usuario.query.all()
    
    @staticmethod
    def eliminar_usuario(id_usuario):
        usuario=Usuario.query.get(id_usuario)
        if usuario:
            print(f"Eliminando el usuario con id: {id_usuario}")
            conexion.session.delete(usuario)
            conexion.session.commit()
            return True
        return False
    
    @staticmethod
    def modificar_usuario(id_usuario,nombre=None,mail=None,contraseña=None):
        usuario=Usuario.query.get(id_usuario)
        if usuario:
            print(f"Modificando el usuario con id: {id_usuario} - dao")
            if nombre:
                usuario.nombre=nombre
            else:
                usuario.nombre=usuario.nombre
            if mail:
                usuario.mail=mail
            else:
                usuario.mail=usuario.mail
            if contraseña:
                usuario.contraseña=contraseña
            else:
                usuario.contraseña=usuario.contraseña
            conexion.session.commit()
            print(f"Usuario con id {id_usuario} modificado correctamente - dao")
            return {"mensaje":"Usuario modificado correctamente"},200

    @staticmethod
    def calificarpersonal(id_personal,calificacion):
        try:
            personal = UsuarioDAO.obtener_usuario_por_id(id_personal)
            if not personal:
                return {"mensaje": "Personal no encontrado"}, 404
            
            if personal.calificacion_promedio is None:
                personal.calificacion_promedio = calificacion
                print(f"Calificando personal con id: {id_personal} C: {calificacion}- archivo dao")
            else:
                personal.calificacion_promedio = (personal.calificacion_promedio + calificacion) / 2
                print(f"Calificando personal con id: {id_personal} C: {calificacion}- archivo dao")
            
            conexion.session.commit()
            return {"mensaje": "Calificación actualizada correctamente"}, 200
        except Exception as e:
            return {"error": str(e)}, 500