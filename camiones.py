import json
import os
from tkinter import StringVar

class Camiones:
    def __init__(self):
        # Variables de formulario
        self.idConductor = StringVar() # RUT
        self.nombreConductor = StringVar()
        self.telefono = int()
        self.correo = StringVar()
        self.direccion = StringVar()
        self.nacimiento = StringVar()
        self.ingreso = StringVar()
        self.vacaciones = False
        self.disponibilidad = True

    def cargarCamiones(self):
        if not os.path.exists('camiones.json'):
            return []
        with open('camiones.json', 'r', encoding='utf-8') as file:
            return json.load(file) # json a python

    def guardarCamiones(self, camiones):
        with open('camiones.json', 'w', encoding='utf-8') as file:
            json.dump(camiones, file, indent=4, ensure_ascii=False) # python a json
