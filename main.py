#Importación de librerías y archivos
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os

class InicioSesionApp:
    def __init__(self, root):
        self.root = root #Ventana principal
        self.root.title("TransporteXpress/Inicio de Sesión") #Título de ventana
        
        #Centrar Ventana
        self.anchoVentana=1200
        self.altoVentana=600
        self.anchoPantalla = self.root.winfo_screenwidth()
        self.altoPantalla = self.root.winfo_screenheight()
        self.x = (self.anchoPantalla-self.anchoVentana) // 2
        self.y = (self.altoPantalla-self.altoVentana) // 2
        self.root.geometry(f"{self.anchoVentana}x{self.altoVentana}+{self.x}+{self.y-70}")
        
        #Variables de entrada
        self.nombreUsuario = StringVar()
        self.contraseniaUsuario = StringVar()
        self.intentos = 4 #Contador inicial
        self.crearInterfaz()
    
    def crearInterfaz(self):
        #Fondo
        self.imagen = PhotoImage(file="C:/Users/Millaray/Desktop/3° Semestre/Proyecto TPA/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)
        
        #Contenedor
        contenedor = Frame(self.root, bg="orange", )
        contenedor.place(relx=0.5, rely=0.5, anchor=S)
        
        #textos y títulos
        titulo = Label(contenedor, text="TransporteXpress",font=("Montserrat SemiBold", 20), bg="orange")
        titulo.grid(column=0, row=0, ipadx=20, padx=10, pady=10, columnspan=2)
        
        nombreLabel = Label(contenedor, text="Nombre: ", font=("Montserrat", 14), bg="orange")
        nombreLabel.grid(column=0, row=1)
        
        contraseniaLabel = Label(contenedor, text="Contraseña: ", font=("Montserrat", 14), bg="orange")
        contraseniaLabel.grid(column=0, row=2)
        
        #Entradas de textos
        nombreEntry = Entry(contenedor, textvariable=self.nombreUsuario, bg="#faedcd")
        nombreEntry.grid(column=1, row=1)
        
        contraseniaEntry = Entry(contenedor, textvariable=self.contraseniaUsuario, bg="#faedcd", show="*")
        contraseniaEntry.grid(column=1, row=2)
        
        #botones
        iniciarSesionButton = ttk.Button(contenedor, text="Iniciar Sesión", command=self.iniciarSesion)
        iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5,padx=10, pady=10)
        
        registrarButton = ttk.Button(contenedor, text="Registrar", command=self.registrarUsuario)
        registrarButton.grid(column=0, row=3, ipadx=5, ipady=5,padx=10, pady=10)  
        
    def cargarUsuarios(self):
        if not os.path.exists('usuarios.json'): #Verifica si el archivo 'ususarios.json' existe en el directorio actual
            return [] #si no existe returna una lista vacía para evitar errores
        with open('usuarios.json', 'r') as file: #manejo seguro de archivos, r(read) significa que es solo para lectura.
            return json.load(file) #convierte el contenido del archivo JSON en un diccionario de python, si quisieramos hacer el caso opuesto deberíamos usar json.dumps
    
    def guardarUsuarios(self, usuarios):
        with open('usuarios.json', 'w') as file: #w de write sobreescribe el archivo completo y si el archivo no exite lo crea automáticamente.
            json.dump(usuarios, file, indent=4) #y aquí usamos el dump para convertir un diccionario de python a formato json.
    
    def iniciarSesion(self):
        #Bloqueo preventivo
        if self.intentos<=0:
            messagebox.showerror('Bloqueado', 'Haz superado la cantidad de intentos permitidos')
            self.root.destroy()
            return
        
        #Datos de entrada
        usuarios = self.cargarUsuarios()
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()
        
        #Validación de inicio de sesión
        for usuario in usuarios:
            if usuario['nombre'] == nombre and usuario['contrasenia'] == contrasenia:
                messagebox.showinfo('Éxito', 'Inicio de sesión exitoso')
                
                # Limpiar widgets actuales
                for widget in self.root.winfo_children(): #winfo_children devuelve la lista con todos los widgets de un contenedor.
                    widget.destroy()

                # llamar a otra función que construya nueva interfaz
                self.crearInterfazPrincipal()
                return True
        
        #Intentos fallidos, son 4 oportunidades en total    
        self.intentos-=1
        
        if self.intentos>0:
            mensaje = (f'Contraseña incorrecta. Intentos restantes = {self.intentos}')
            messagebox.showerror('Error', mensaje)
        else:
            messagebox.showerror('Bloqueado', 'Haz alcanzado el máximo de intentos, la aplicación se cerrará.')
            self.root.destroy()
            
    def registrarUsuario(self):
        usuarios = self.cargarUsuarios()
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()
        
        #Para evitar que se ingresen datos vacíos:
        if not nombre or not contrasenia:
            messagebox.showerror('Error', 'Ingrese un nombre y una contraseña para poder registrar')
            return False
        
        for usuario in usuarios:
            if usuario['nombre'] == nombre:
                messagebox.showerror('Error', 'El usuario ya existe')
                return False
            
        usuarios.append({'nombre': nombre, 'contrasenia': contrasenia})
        self.guardarUsuarios(usuarios)
        messagebox.showinfo('Registro', 'Usuario registrado exitosamente')
        return True      
        
    def crearInterfazAdmin(self):
        pass
            
if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()

####### HASTA AQUÍ LA MILLY Y COMIENZA LA SOFI ########
