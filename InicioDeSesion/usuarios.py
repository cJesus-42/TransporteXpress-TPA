class Usuario():
    numUsuarios = 0
    
    def __init__(self, nombre, contrasenia): 
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.conectado = False
        self.intentos = 3
        
        Usuario.numUsuarios+=1
    
    def iniciarSesion(self, contrasenia=None):
        if contrasenia==None:
            miContrasenia=input("Ingrese su contraseña: ")
        else:
            miContrasenia=contrasenia
            
        if miContrasenia==self.contrasenia:
            print ("Ha iniciado sesión con exito")
            self.conectado = True
        else:
            self.intentos-=1
            if self.intentos>0:
                print ("Contraseña incorrecta, intente de nuevo")
                print (f"Intentos restantes: {self.intentos}")
                self.iniciarSesion()
            else:
                print ("Error, no se pudo iniciar sesión")
                
    def cerrarSesion(self):
        if self.conectado:
            print ("Se cerró sesión con éxito")
            self.conectado = False
        else:
            print ("Error, no inició sesión")
    
    def __str__(self):
        if self.conectado:
            conexion = "Conectado"
        else:
            conexion = "Desconectado"
            
        return (f"Mi nombre de usuario es {self.nombre} y estoy {conexion}")
    
#usuario1 = Usuario(input("Ingrese su nombre: "), input("Ingrese una contraseña: "))
#print(usuario1)

#usuario1.iniciarSesion()
#print(usuario1)

#usuario1.cerrarSesion()
#print(usuario1)