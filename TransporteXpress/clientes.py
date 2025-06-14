from tkinter import StringVar
import json

class Clientes:
    def __init__(self):
        # Variables de formulario
        self.rut = StringVar()
        self.nombreCompleto = StringVar()
        self.telefono = StringVar()
        self.direccion = StringVar()
        self.correo = StringVar()
        
    def actualizarLlavesUsuarios(self):
        with open('usuarios.json', 'r', encoding='utf-8') as file:
            usuarios = json.load(file) # Carga el archivo json

        for usuario in usuarios: # Se recorre el archivo json verificando que estén las llaves "RUT", "Nombre Completo", etc. sino las crea y las deja en blanco, sin una clave.
            if 'RUT' not in usuario:
                usuario['RUT'] = ""
            if 'Nombre Completo' not in usuario:
                usuario['Nombre Completo'] = ""
            if 'Telefono' not in usuario:
                usuario['Telefono'] = ""
            if 'Direccion' not in usuario:
                usuario['Direccion'] = ""
            if 'Correo' not in usuario:
                usuario['Correo'] = ""

        with open('usuarios.json', 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False)  # Guarda el cambio realizado
            
    def validarEnteros(self):
        try:
            int(self.rut.get())
            int(self.telefono.get())
        except ValueError:
            return False
        return True
        
    def cargarClientes(self):
        with open('usuarios.json', 'r', encoding='utf-8') as file:
            return json.load(file) # json a python

    def guardarClientes(self, usuarios):
        with open('usuarios.json', 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False) # python a json
