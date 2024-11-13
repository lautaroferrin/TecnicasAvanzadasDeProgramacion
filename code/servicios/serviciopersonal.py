from dao.personaldao import PersonalDAO

class ServicioPersonal:
    @staticmethod
    def agregar_personal(nombre,mail,contraseña):
        if not nombre or not mail or not contraseña:
            return "Todos los campos son obligatorios"
        
        if len(contraseña) < 5:
            return "La contraseña debe tener al menos 5 caracteres"
        
        if PersonalDAO.obtener_personal_por_mail(mail):
            return "Este correo ya esta registrado"
        
        PersonalDAO.agregar_personal(nombre,mail,contraseña)
        return "Personal agregado exitosamente"
    
    @staticmethod
    def obtener_personal_por_mail(mail):
        try:
            personal=PersonalDAO.obtener_personal_por_mail(mail)
            if not personal:
                return 0
            return personal
        except Exception as e:
            raise Exception("Error al obtener el personal",str(e))
        
    @staticmethod
    def eliminar_personal(id_personal):
        personal = PersonalDAO.obtener_personal_por_id(id_personal)
        print(f"Eliminando personal con id: {id_personal} - archivo servicio")
        if not personal:
            return "Personal no encontrado."
        else:
            PersonalDAO.eliminar_personal(id_personal)
            return "Personal eliminado exitosamente."
    
    @staticmethod
    def modificar_personal(id_personal,nombre=None,mail=None,contraseña=None):
        try:
            personal= PersonalDAO.obtener_personal_por_id(id_personal)
            print(f"Modificando personal con id: {id_personal} - archivo servicio")
            if not personal:
                return {"error":"Personal no encontrado"},400
            if not contraseña or len(contraseña)<5:
                contraseña=personal.contraseña
            if not mail or '@' not in mail:
                mail=personal.mail
            print("Personal modificado exitosamente")
            return PersonalDAO.modificar_personal(id_personal,nombre,mail,contraseña)
        except Exception as e:
            return{"error": str(e)},500
        
    @staticmethod
    def listar_personal():
        try:
            todopersonal = PersonalDAO.listar_personal()
            if not todopersonal:
                return 'No existe personal'
            else:
                return todopersonal
        except Exception as e:
            return {'error':f'ServicioPersonal {str(e)}'},500
        
    @staticmethod    
    def obtener_calificacion_personal(id_personal):
        try:
            personal = PersonalDAO.obtener_calificacion_personal(id_personal)
            if not personal:
                return 0
            return personal.calificacion_promedio
        except Exception as e:
            return {'error':f'ServicioPersonal {str(e)}'},500