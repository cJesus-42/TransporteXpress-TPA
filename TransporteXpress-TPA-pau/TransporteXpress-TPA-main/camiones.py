import json
import os
from tkinter import StringVar

class Camiones:
    def __init__(self):
        # Variables de formulario, ingresar aquí variables de camiones
        pass

    def cargarcamiones(self):
        if not os.path.exists('camiones.json'):
            return []
        with open('camiones.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def guardarcamiones(self, camiones):
        with open('camiones.json', 'w', encoding='utf-8') as file:
            json.dump(camiones, file, indent=4, ensure_ascii=False)