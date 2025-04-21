#Importación de librerías y archivos
from tkinter import *
from tkinter import ttk as ttk
from usuarios import Usuario

class InicioSesionApp:
    def __init__(self, root):
        self.root = root #ventana principal
        self.root.title("TransporteXpress/Inicio de Sesión")
        
        #Centrar Ventana
        self.anchoVentana=1200
        self.altoVentana=600
        self.anchoPantalla = self.root.winfo_screenwidth()
        self.altoPantalla = self.root.winfo_screenheight()
        self.x = (self.anchoPantalla-self.anchoVentana) // 2
        self.y = (self.altoPantalla-self.altoVentana) // 2
        self.root.geometry(f"{self.anchoVentana}x{self.altoVentana}+{self.x}+{self.y-70}")
        
        #Usuario de Prueba
        self.usuario1= Usuario ("admin", "1234")
        
        #Variables de entrada
        self.nombreUsuario = StringVar()
        self.contraseniaUsuario = StringVar()
        self.crearInterfaz()
        
    def crearInterfaz(self):
        #Fondo
        self.imagen = PhotoImage(file="C:/Users/Millaray/Desktop/SEMESTRE 3/Proyecto TPA/Imagenes/camionbg.png")
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
        
        
    def iniciarSesion(self):
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()
        print(f"Intentando iniciar sesión con usuario: {nombre}")
        self.usuario1.iniciarSesion(contrasenia)
        
    def registrarUsuario(self):
        print("Función de registro aún no implementada.")
        # Aquí podrías abrir una nueva ventana o formulario

if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()

####### HASTA AQUÍ LA MILLY Y COMIENZA LA SOFI ########
