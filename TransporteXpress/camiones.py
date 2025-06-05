from tkinter import StringVar
from datetime import datetime
import json

class Camiones:
    def __init__(self):
        # Variables de formulario
        self.idcamion = StringVar() # ID del camión
        self.patente = StringVar() # Patente del camión
        self.marca = StringVar()
        self.modelo = StringVar()
        self.disponible = True
        self.ingreso = StringVar() # Fecha de ingreso del camión
        self.ingreso.set(datetime.now().strftime("%Y-%m-%d"))

    def actualizarLlavesUsuarios(self):
        with open('camiones.json', 'r', encoding='utf-8') as file:
            camiones = json.load(file) #carga el archivo json

        for c in camiones: #se recorre el archivo json verificando que estén las llaves "idPatente", "Marca", etc. sino las crea y las deja en blanco, sin una clave.
            if 'idCamion' not in c:
                c['idCamion'] = ""
            if 'Patente' not in c:
                c['Patente'] = ""
            if 'Marca' not in c:
                c['Marca'] = ""
            if 'Modelo' not in c:
                c['Modelo'] = ""
            if 'Disponible' not in c:
                c['Disponible'] = ""
            if 'Ingreso' not in c:
                c['Ingreso'] = ""

        with open('camiones.json', 'w', encoding='utf-8') as file:
            json.dump(camiones, file, indent=4, ensure_ascii=False)  # Guarda el cambio realizado

    def cargarCamiones(self):
        with open('camiones.json', 'r', encoding='utf-8') as file:
            return json.load(file) # json a python

    def guardarCamiones(self, camiones):
        with open('camiones.json', 'w', encoding='utf-8') as file:
            json.dump(camiones, file, indent=4, ensure_ascii=False) # python a json
