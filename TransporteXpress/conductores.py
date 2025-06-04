import json
import os
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

    def cargarConductores(self):
        if not os.path.exists('conductores.json'): #si no existe el archivo te retorna una lista vacía
            return []
        with open('conductores.json', 'r', encoding='utf-8') as file: 
            return json.load(file) #json a python

    def guardarConductores(self, conductores):
        with open('conductores.json', 'w', encoding='utf-8') as file:
            json.dump(conductores, file, indent=4, ensure_ascii=False) #python a json
