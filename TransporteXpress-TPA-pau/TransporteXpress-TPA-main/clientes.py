import json
import os
from tkinter import StringVar
class Clientes:
    def __init__(self):
        self.rut = int()
        self.nombre = StringVar()
        self.telefono = int()
        self.direccion = StringVar()
        self.correo = StringVar()
        
    def cargarClientes(self):
        with open('usuarios.json', 'r', encoding='utf-8') as file:
            return json.load(file) #json a python
    def guardarClientes(self, usuarios):
        with open('usuarios.json', 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False) #python a json