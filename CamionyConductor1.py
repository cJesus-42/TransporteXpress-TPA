from tkinter import *
from tkinter import ttk
from usuarios import Usuario 

class InicioSesionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TransporteXpress/Inicio de Sesión")

        # Centrar ventana
        self.anchoVentana = 1200
        self.altoVentana = 600
        self.anchoPantalla = self.root.winfo_screenwidth()
        self.altoPantalla = self.root.winfo_screenheight()
        self.x = (self.anchoPantalla - self.anchoVentana) // 2
        self.y = (self.altoPantalla - self.altoVentana) // 2
        self.root.geometry(f"{self.anchoVentana}x{self.altoVentana}+{self.x}+{self.y-70}")

        self.usuario1 = Usuario("admin", "1234")

        self.nombreUsuario = StringVar()
        self.contraseniaUsuario = StringVar()

        self.crearInterfaz()

    def crearInterfaz(self):
        self.clearWidgets() #elimina botones ayuda a despejar la ventana
         #Fondo
        #self.imagen = PhotoImage(file="C:/Users/Millaray/Desktop/SEMESTRE 3/Proyecto TPA/Imagenes/camionbg.png")
        #imagenLabel = Label(self.root, image=self.imagen)
        #imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)
        
        contenedor = Frame(self.root, bg="orange")
        contenedor.place(relx=0.5, rely=0.5, anchor=S)

        Label(contenedor, text="TransporteXpress", font=("Montserrat SemiBold", 20), bg="orange").grid(column=0, row=0, ipadx=20, padx=10, pady=10, columnspan=2)
        Label(contenedor, text="Nombre: ", font=("Montserrat", 14), bg="orange").grid(column=0, row=1)
        Label(contenedor, text="Contraseña: ", font=("Montserrat", 14), bg="orange").grid(column=0, row=2)

        Entry(contenedor, textvariable=self.nombreUsuario, bg="#faedcd").grid(column=1, row=1)
        Entry(contenedor, textvariable=self.contraseniaUsuario, bg="#faedcd", show="*").grid(column=1, row=2)

        ttk.Button(contenedor, text="Iniciar Sesión", command=self.iniciarSesion).grid(column=1, row=3, ipadx=5, ipady=5, padx=10, pady=10)
        ttk.Button(contenedor, text="Registrar", command=self.registrarUsuario).grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    def iniciarSesion(self):
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()
        print(f"Intentando iniciar sesión con usuario: {nombre}")
        # no verifica, simplemente muestra los botones
        self.mostrarBotonesCamionesYChoferes()

    def registrarUsuario(self):
        print("Función de registro aún no implementada.")

    def mostrarBotonesCamionesYChoferes(self):
        self.clearWidgets()
        self.contenedor_botones = Frame(self.root, bg="orange")
        self.contenedor_botones.place(relx=0.5, rely=0.5, anchor=S)

        Button(self.contenedor_botones, text="Camiones", command=self.mostrarMenuHorizontal,
               font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=0, column=0, padx=20, pady=10)

        Button(self.contenedor_botones, text="Conductores", command=self.mostrarMenuHorizontal,
               font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=1, column=0, padx=20, pady=10)
    

    def mostrarMenuHorizontal(self):
        self.clearWidgets()

        self.barra_horizontal = Frame(self.root, bg="orange", height=50)
        self.barra_horizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.accion_agregar),
            ("Editar", self.accion_editar),
            ("Eliminar", self.accion_eliminar),
            ("Ver", self.accion_ver),
            ("Volver", self.volver_a_botones)
        ]

        for texto, comando in botones:
            Button(self.barra_horizontal, text=texto, command=comando, bg="white", fg="black",
                   font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedor_menu = Frame(self.root)
        self.contenedor_menu.pack(expand=True)


    def volver_a_botones(self):
        self.clearWidgets()
        self.mostrarBotonesCamionesYChoferes()

    def accion_agregar(self):
        print("Acción Agregar ejecutada.")

    def accion_editar(self):
        print("Acción Editar ejecutada.")

    def accion_eliminar(self):
        print("Acción Eliminar ejecutada.")

    def accion_ver(self):
        print("Acción Ver ejecutada.")

    def clearWidgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()
