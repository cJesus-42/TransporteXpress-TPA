for camiones import camiones #clase de cristian
class Conductores:
    numConductores = 0

    def __init__(self, idConductor, nombre, camion, disponible, telefono, correo, nacimiento, direccion, ingreso, vacaciones):
        self.idConductor = idConductor #rut
        self.nombre = nombre
        self.camion = [] #de qué camiones está "a cargo"
        self.disponible = True #saber si está disponible para un viaje para asignarlo a un camión automáticamente
        self.telefono = telefono #puede ser visible una vez que el cliente compre el servicio
        self.correo = correo #desde aquí es información para la empresa
        self.nacimiento = nacimiento #fecha de nacimiento
        self.direccion = direccion
        self.ingreso = ingreso #qué día ingresó a la empresa
        self.vacaciones = False #solo indicar si está de vacaciones
        
    def registrar(self, idConductor, nombre, telefono, correo, nacimiento, direccion, ingreso):
        contador = 0
        if self.idConductor == None:
            self.idConductor = int(input("Ingrese RUT sin guión: "))
            for contador in self.idConductor:
                if 9> contador >10:
                    print("Registrado.")
                    contador = 0
                else:
                    print("Error. Ingresa el RUT.")
                    contador = 0    
        
        if self.nombre == None:
            self.nombre = str(input("Ingrese nombre completo: "))
            for caracter in self.nombre:
                if caracter == "":
                    contador += 1
            if 5 > contador > 2:
                print("Registrado.")
                contador = 0
            else:
                print("Error. Ingresa el nombre completo.")
                contador = 0
                self.nombre = None

        if self.telefono == None:
            self.telefono = int(input("Ingrese el número de télefono: "))

            for contador in self.telefono:
                if 10 > contador > 8:
                    print("Registrado.")
                    contador = 0
                else:
                    print("Error. Vuelve a ingresar el número de teléfono.")
                    contador = 0
                    self.telefono = None
        
        if self.correo == None:
            self.correo = str(input("Ingrese el correo: "))

            for contador in self.correo:
                if contador == "@":
                    print("Registrado.")
                    contador = 0
                else:
                    print("Error. Vuelve a ingresar el correo.")
                    contador = 0
                    self.correo = None
            
        

    def conductorDispobible(self, vacaciones, disponible, camion): #ver con el cristian..... camion debería ser idCamion
        if vacaciones == True:
            self.disponible = False

        if disponible == True:
            a = 0
            for a in camiones:
                self.camion = [a]