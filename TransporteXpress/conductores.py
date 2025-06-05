import json
from tkinter import StringVar

class Conductores:
    def __init__(self):
        # Variables de formulario
        self.idConductor = StringVar() #RUT
        self.nombreConductor = StringVar()
        self.telefono = StringVar()
        self.correo = StringVar()
        self.direccion = StringVar()
        self.nacimiento = StringVar()
        self.ingreso = StringVar()
        self.vacaciones = False
        self.disponibilidad = True

    def cargarCamiones(self):
        with open('camiones.json', 'r', encoding='utf-8') as file:
            return json.load(file) # json a python

    def guardarCamiones(self, conductores):
        with open('camiones.json', 'w', encoding='utf-8') as file:
            json.dump(conductores, file, indent=4, ensure_ascii=False) #python a json
