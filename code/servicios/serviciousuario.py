from dao.usuariodao import UsuarioDAO
from dao.personaldao import PersonalDAO

class ServicioUsuario:
    @staticmethod
    def agregar_usuario(nombre,mail,contraseña):
        if not nombre or not mail or not contraseña:
            return "Todos los campos son obligatorios"
        
        if len(contraseña) < 5:
            return "La contraseña debe tener al menos 5 caracteres"
        
        if UsuarioDAO.obtener_usuario_por_mail(mail):
            return "Este correo ya esta registrado"
        
        UsuarioDAO.agregar_usuario(nombre,mail,contraseña)
        return "Usuario agregado exitosamente"
    
    @staticmethod
    def obtener_usuario_por_mail(mail):
        try:
            usuario=UsuarioDAO.obtener_usuario_por_mail(mail)
            if not usuario:
                return 0
            return usuario
        except Exception as e:
            raise Exception("Error al obtener el usuario",str(e))

    @staticmethod
    def eliminar_usuario(id_usuario):
        usuario = UsuarioDAO.obtener_usuario_por_id(id_usuario)
        print(f"Eliminando usuario con id: {id_usuario} - archivo servicio")
        if not usuario:
            return "Usuario no encontrado."
        else:
            UsuarioDAO.eliminar_usuario(id_usuario)
            return "Usuario eliminado exitosamente."
        
    @staticmethod
    def modificar_usuario(id_usuario,nombre=None,mail=None,contraseña=None):
        try:
            usuario= UsuarioDAO.obtener_usuario_por_id(id_usuario)
            print(f"Modificando usuario con id: {id_usuario} - archivo servicio")
            if not usuario:
                return {"error":"Usuario no encontrado"},400
            if not contraseña or len(contraseña)<5:
                contraseña=usuario.contraseña
            if not mail or '@' not in mail:
                mail=usuario.mail
            print("Usuario modificado exitosamente")
            return UsuarioDAO.modificar_usuario(id_usuario,nombre,mail,contraseña)
        except Exception as e:
            return{"error": str(e)},500
    
    @staticmethod
    def calificarpersonal(id_personal,calificacion):
        try:
            personal=PersonalDAO.obtener_personal_por_id(id_personal)
            if not personal:
                return 0
            print(f"Calificando personal con id: {id_personal} C: {calificacion} - archivo servicio")
            UsuarioDAO.calificarpersonal(id_personal,calificacion)
            return "Personal calificado exitosamente"
        except Exception as e:
            return{"error": str(e)},500
