#Importación de librerías y archivos
from tkinter import *
from tkinter import ttk, messagebox
from conductores import Conductores
from camiones import Camiones
import os
import json

class InicioSesionApp:
    def __init__(self, root):
        self.root = root #Ventana principal
        self.root.title("TransporteXpress") #Título de ventana
        
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
        
        #Textos y títulos
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
        
        #Botones
        iniciarSesionButton = ttk.Button(contenedor, text="Iniciar Sesión", command=self.iniciarSesion)
        iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5,padx=10, pady=10)
        
        registrarButton = ttk.Button(contenedor, text="Registrar", command=self.registrarUsuario)
        registrarButton.grid(column=0, row=3, ipadx=5, ipady=5,padx=10, pady=10)  

    def cargarUsuarios(self):
        if not os.path.exists('usuarios.json'): #Verifica si el archivo 'usuarios.json' existe en el directorio actual
            return [] #si no existe returna una lista vacía para evitar errores.
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
                if nombre == 'admin':
                    messagebox.showinfo('Éxito', 'Ha iniciado sesión con éxito')
                    # Limpiar widgets actuales
                    for widget in self.root.winfo_children(): #winfo_children devuelve la lista con todos los widgets de un contenedor.
                        widget.destroy()
                    #Llamar a otra función que construya nueva interfaz
                    self.root.after(50, lambda: MenuAdmin(self.root)) #permite a acceder al menu sin errores
                    return True
                else:
                    pass
                    #aquí debería llamar a la función de que se abra la ventana de usuario.
        
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
            
        usuarios.append({'nombre': nombre, 'contrasenia': contrasenia}) #Agregar a librería que después se convierte en JSON.
        self.guardarUsuarios(usuarios)
        messagebox.showinfo('Registro', 'Usuario registrado exitosamente')
        return True     

class MenuAdmin(Conductores, Camiones):
    def __init__(self, root):
        super().__init__()  # Inicializa las variables de Conductores
        self.root = root
        self.mostrarBotonesCamionesYConductores()

    def limpiarWidgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrarBotonesCamionesYConductores(self):
        self.limpiarWidgets()
        
        self.imagen = PhotoImage(file="C:/Users/Millaray/Desktop/3° Semestre/Proyecto TPA/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)
        
        self.contenedorBotones = Frame(self.root, bg="orange")
        self.contenedorBotones.place(relx=0.5, rely=0.5, anchor=S)
        Button(self.contenedorBotones, text="Camiones", command=self.mostrarMenuHorizontalCamiones,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=0, column=0, padx=20, pady=10)
        Button(self.contenedorBotones, text="Conductores", command=self.mostrarMenuHorizontalConductores,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=1, column=0, padx=20, pady=10)

    def mostrarMenuHorizontalConductores(self):
        self.limpiarWidgets() #limpia la ventana para mostrar el menu horizontal
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.formularioAgregarConductor),
            ("Editar", self.accionEditar),
            ("Eliminar", self.accionEliminar),
            ("Volver", self.volverBotones)
        ]
            
        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
            self.contenedor_menu = Frame(self.root)
            self.contenedor_menu.pack(expand=True)

        # Contenedor para la lista de conductores debajo de la barra
        self.contenedorLista = Frame(self.root)
        self.contenedorLista.pack(fill=BOTH, expand=True, padx=20, pady=20)

        
        # Crear el Treeview con columnas para cada dato
        columnas = ("RUT", "Nombre", "Teléfono", "Correo", "Dirección", "Fecha Nacimiento", "Fecha Ingreso")
        self.treeConductores = ttk.Treeview(self.contenedorLista, columns=columnas, show='headings')

        # Definir encabezados
        for col in columnas:
            self.treeConductores.heading(col, text=col)
            self.treeConductores.column(col, width=120, anchor='center')

        self.treeConductores.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        self.listaConductores()

    def formularioAgregarConductor(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)
        
        # Etiquetas y entradas
        Label(contenedorFormulario, text="RUT (sin guión):", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.idConductor).grid(row=0, column=1, pady=5)
        
        Label(contenedorFormulario, text="Nombre:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreConductor).grid(row=1, column=1, pady=5)
        
        Label(contenedorFormulario, text="Teléfono:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono).grid(row=2, column=1, pady=5)
        
        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)
        
        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)
        
        Label(contenedorFormulario, text="Fecha Nacimiento:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nacimiento).grid(row=5, column=1, pady=5)
        
        Label(contenedorFormulario, text="Fecha Ingreso:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.ingreso).grid(row=6, column=1, pady=5)
        
        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.formularioGuardarConductor).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.volverBotones).grid(row=7, column=1, columnspan=2, pady=15)

    def formularioGuardarConductor(self):
        # Obtiene los valores
        idConductor = self.idConductor.get().strip()
        nombreConductor = self.nombreConductor.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()
        nacimiento = self.nacimiento.get().strip()
        ingreso = self.ingreso.get().strip()
        
        # Validaciones básicas
        if not idConductor or not nombreConductor:
            messagebox.showerror("Error", "Debe ingresar al menos RUT y Nombre.")
            return
        
        # Validar que el RUT tenga 9 dígitos
        if len(idConductor.replace('-', '').replace('.', '')) != 9:
            messagebox.showerror("Error", "El RUT debe tener 9 dígitos.")
            return
            
        # Cargar conductores existentes
        conductores = self.cargarConductores()

        # Verificar si ya existe el conductor por RUT
        for c in conductores:
            if c['RUT'] == idConductor:
                messagebox.showerror("Error", "Ya existe un conductor con ese RUT.")
                return

        # Agregar nuevo conductor
        nuevoConductor = {
            "RUT": idConductor,
            "Nombre": nombreConductor,
            "Teléfono": telefono,
            "Correo Electrónico": correo,
            "Dirección": direccion,
            "Fecha Nacimiento": nacimiento,
            "Fecha Ingreso": ingreso
        }
        conductores.append(nuevoConductor)

        # Guardar en JSON
        self.guardarConductores(conductores)

        messagebox.showinfo("Éxito", "Conductor agregado correctamente.")

        # Limpiar variables para nuevo ingreso
        self.idConductor.set("")
        self.nombreConductor.set("")
        self.telefono.set("")
        self.correo.set("")
        self.direccion.set("")
        self.nacimiento.set("")
        self.ingreso.set("")

        # Volver al menú principal o refrescar formulario
        self.mostrarMenuHorizontalConductores()

    def listaConductores (self):
            # Limpia la tabla antes de cargar datos nuevos
            for item in self.treeConductores.get_children():
                self.treeConductores.delete(item)

            conductores = self.cargarConductores()  # Método que carga conductores desde JSON

            for conductor in conductores:
                self.treeConductores.insert('', 'end', values=(
                    conductor.get("RUT", ""),
                    conductor.get("Nombre", ""),
                    conductor.get("Teléfono", ""),
                    conductor.get("Correo Electrónico", ""),
                    conductor.get("Dirección", ""),
                    conductor.get("Fecha Nacimiento", ""),
                    conductor.get("Fecha Ingreso", ""),
                ))

    def volverBotones(self):
        self.limpiarWidgets() #limpia la ventana
        self.mostrarBotonesCamionesYConductores()     

    def accionEditar(self):
        print("Acción Editar ejecutada.")

    def accionEliminar(self):
        #Revisa si estas seleccionando algun elemento del árbol
        seleccion = self.treeConductores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un conductor para eliminar.")
            return
        #Obtiene el RUT del conductor seleccionado (columna 0)
        item = seleccion[0]
        valores = self.treeConductores.item(item, "values")
        rut_a_eliminar = valores[0]
        
        #Confirmar con el usuario
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el conductor con RUT {rut_a_eliminar}?")
        if not confirmar:
            return

        #Cargar la lista de conductores
        conductores = self.cargarConductores()

        #Filtra la lista para eliminar el conductor seleccionado
        nuevos_conductores = [c for c in conductores if c.get("RUT") != rut_a_eliminar]
        #incluye en la lista todos los conductores diferentes al rut a eliminar
        #"para cada elemento c en la lista conductores, incluye c en la nueva lista solo si cumple la condición después del if"

        #Guarda la lista actualizada
        self.guardarConductores(nuevos_conductores)

        #Refresca la tabla
        self.listaConductores()
        messagebox.showinfo("Éxito", f"Conductor con RUT {rut_a_eliminar} eliminado correctamente.")

    def mostrarMenuHorizontalCamiones(self):
        self.limpiarWidgets() #limpia la ventana para mostrar el menu horizontal
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.FormularioAgregarConductor),
            ("Editar", self.accionEditar),
            ("Eliminar", self.accionEliminar),
            ("Ver", self.accionVer),
            ("Volver", self.volverBotones)
        ]
            
        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        self.contenedor_menu = Frame(self.root)
        self.contenedor_menu.pack(expand=True)

if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()

