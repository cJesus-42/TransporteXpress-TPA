# Importación de librerías y archivos
from tkinter import ttk, messagebox, StringVar
from datetime import datetime, timedelta
from conductores import Conductores
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
from clientes import Clientes
from camiones import Camiones
from datetime import datetime
from tkinter import *
import json
import re
import os

class InicioSesionApp:
    def __init__(self, root):
        self.root = root # Ventana principal
        self.root.title("TransporteXpress") # Título de ventana

        # Centrar ventana
        self.anchoVentana=1200
        self.altoVentana=600
        self.anchoPantalla = self.root.winfo_screenwidth()
        self.altoPantalla = self.root.winfo_screenheight()
        self.x = (self.anchoPantalla-self.anchoVentana) // 2
        self.y = (self.altoPantalla-self.altoVentana) // 2
        self.root.geometry(f"{self.anchoVentana}x{self.altoVentana}+{self.x}+{self.y-70}")

        # Variables de entrada
        self.nombreUsuario = StringVar()
        self.contraseniaUsuario = StringVar()
        self.intentos = 4 # Contador inicial
        self.crearInterfaz()

    def crearInterfaz(self):
        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
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
        iniciarSesionButton = ttk.Button(contenedor, text="Iniciar sesión", command=self.iniciarSesion)
        iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5,padx=10, pady=10)

        registrarButton = ttk.Button(contenedor, text="Registrar", command=self.registrarUsuario)
        registrarButton.grid(column=0, row=3, ipadx=5, ipady=5,padx=10, pady=10)  

    def cargarUsuarios(self):
        if not os.path.exists('usuarios.json'): # Verifica si el archivo 'usuarios.json' existe en el directorio actual
            return [] # Si no existe returna una lista vacía para evitar errores.

        with open('usuarios.json', 'r') as file: # Manejo seguro de archivos, r(read) significa que es solo para lectura.
            return json.load(file) # Convierte el contenido del archivo JSON en un diccionario de python, si quisieramos hacer el caso opuesto deberíamos usar json.dumps

    def guardarUsuarios(self, usuarios):
        with open('usuarios.json', 'w') as file: # w de write sobreescribe el archivo completo y si el archivo no exite lo crea automáticamente.
            json.dump(usuarios, file, indent=4) # Y aquí usamos el dump para convertir un diccionario de python a formato json.
        # Actualiza la variable en memoria 

    def iniciarSesion(self):
        # Bloqueo preventivo
        if self.intentos<=0:
            messagebox.showerror('Bloqueado', 'Haz superado la cantidad de intentos permitidos')
            self.root.destroy()
            return

        # Datos de entrada
        usuarios = self.cargarUsuarios()
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()

        # Validación de inicio de sesión
        for usuario in usuarios:
            if usuario['nombre'] == nombre and usuario['contrasenia'] == contrasenia:
                messagebox.showinfo('Éxito', 'Ha iniciado sesión con éxito')
                self.nombreUsuarioSesionActual = nombre # Guardar el nombre de usuario actual para usarlo en otras funciones.
                # Limpiar widgets actuales
                for widget in self.root.winfo_children(): # winfo_children devuelve la lista con todos los widgets de un contenedor.
                    widget.destroy()

                if nombre == 'admin':
                    # Llamar a otra función que construya nueva interfaz
                    self.root.after(50, lambda: MenuAdmin(self.root)) # Permite a acceder al menu sin errores
                    return True
                else:
                    # Llamar a otra función que construya nueva interfaz
                    self.root.after(50, lambda: MenuUsuarios(self.root, nombre)) # Permite a acceder al menu sin errores y pasa el nombre de usuario actual.
                    return True 

        # Intentos fallidos, son 4 oportunidades en total    
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

    def salir(self):
        self.limpiarWidgets()
        InicioSesionApp(self.root)

    def mostrarBotonesCamionesYConductores(self):
        self.limpiarWidgets()

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

        self.contenedorBotones = Frame(self.root, bg="orange")

        self.contenedorBotones.place(relx=0.5, rely=0.5, anchor=S)
        Button(self.contenedorBotones, text="Camiones", command=self.pasar,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=0, column=0, padx=20, pady=10)

        Button(self.contenedorBotones, text="Conductores", command=self.mostrarMenuHorizontalConductores,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=1, column=0, padx=20, pady=10)

        Button(self.contenedorBotones, text="Volver", command=self.salir,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=2, column=0, padx=20, pady=10)

    def mostrarMenuHorizontalConductores(self):
        self.limpiarWidgets() # Limpia la ventana para mostrar el menu horizontal

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
        columnas = ("RUT", "Nombre completo", "Teléfono", "Correo", "Dirección", "Fecha de nacimiento", "Fecha de ingreso")
        self.treeConductores = ttk.Treeview(self.contenedorLista, columns=columnas, show='headings')

        # Definir encabezados
        for col in columnas:
            self.treeConductores.heading(col, text=col)
            self.treeConductores.column(col, width=120, anchor='center')

        self.treeConductores.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        self.listaConductores()

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioAgregarConductor(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Etiquetas y entradas
        Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.idConductor).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreConductor).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        Label(contenedorFormulario, text="Fecha de nacimiento:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        DateEntry(
            contenedorFormulario,
            textvariable=self.nacimiento,
            date_pattern='yyyy-mm-dd',
            locale='es_CL',
            maxdate=datetime.now() - timedelta(days=18*365),
            mindate=datetime(1900, 1, 1)
        ).grid(row=5, column=1, pady=5)

        Label(contenedorFormulario, text="Fecha de ingreso:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        DateEntry(
            contenedorFormulario,
            textvariable=self.ingreso,
            date_pattern='yyyy-mm-dd',
            locale='es_CL',
            maxdate=datetime.now()
        ).grid(row=6, column=1, pady=5)

        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.formularioGuardarConductor).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=7, column=1, columnspan=2, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioGuardarConductor(self):
        # Obtiene los valores
        idConductor = self.idConductor.get().strip()
        nombreConductor = self.nombreConductor.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()
        nacimiento = self.nacimiento.get().strip()
        ingreso = self.ingreso.get().strip()

        conductores = self.cargarConductores()

        # Validaciones básicas
        for c in conductores:
            if c.get("idConductor") == idConductor and (len(c.get("idConductor")) != 9 or len(c.get("idConductor")) != 8):
                if not idConductor or not nombreConductor:
                    messagebox.showerror("Error", "Debe ingresar al menos RUT y nombre completo.")
                    return

                # Validar que el RUT tenga 9 dígitos
                elif len(idConductor.replace('-', '').replace('.', '')) != 9 or len(idConductor.replace('-', '').replace('.', '')) != 8:
                    messagebox.showerror("Error", "El RUT debe tener entre 8 o 9 dígitos.")
                    return
            break
            

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

    def listaConductores(self):
        # Verifica que el treeview existe antes de usarlo
        if not hasattr(self, 'treeConductores') or not self.treeConductores.winfo_exists():
            return  # O vuelve a crear el treeview aquí

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
        self.limpiarWidgets() # Limpia la ventana
        self.mostrarBotonesCamionesYConductores()

    def accionEditar(self):
        seleccion = self.treeConductores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un conductor para editar.")
            return
        item = seleccion[0]
        valores = self.treeConductores.item(item, "values")
        idConductor = valores[0]
        nombreConductor = valores[1]
        telefono = valores[2]
        correo = valores[3]
        direccion = valores[4]
        nacimiento = valores[5]
        ingreso = valores[6]

        self.formularioEditarConductor(idConductor, nombreConductor, telefono, correo, direccion, nacimiento, ingreso)

    def formularioEditarConductor(self, idConductor, nombreConductor, telefono, correo, direccion, nacimiento, ingreso):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Muestra el RUT solo como texto, no editable
        Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Label(contenedorFormulario, text=idConductor, bg="orange").grid(row=0, column=1, pady=5)

        # Rellena el formulario con los datos del usuario actual
        self.idConductor.set(idConductor)
        self.nombreConductor.set(nombreConductor)
        self.telefono.set(telefono)
        self.correo.set(correo)
        self.direccion.set(direccion)
        self.nacimiento.set(nacimiento)
        self.ingreso.set(ingreso)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreConductor).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Télefono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        Label(contenedorFormulario, text="Fecha de nacimiento:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        DateEntry(
            contenedorFormulario,
            textvariable=self.nacimiento,
            date_pattern='yyyy-mm-dd',
            locale='es_CL',
            maxdate=datetime.now() - timedelta(days=18*365),
            mindate=datetime(1950, 1, 1)
        ).grid(row=5, column=1, pady=5)

        Label(contenedorFormulario, text="Fecha de ingreso:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        DateEntry(
            contenedorFormulario,
            textvariable=self.ingreso,
            date_pattern='yyyy-mm-dd',
            locale='es_CL',
            maxdate=datetime.now()
        ).grid(row=6, column=1, pady=5)

        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.formularioGuardarEdicionConductor).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=7, column=1, columnspan=5, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioGuardarEdicionConductor(self):
        idConductor = self.idConductor.get().strip()
        nombreConductor = self.nombreConductor.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()
        nacimiento = self.nacimiento.get().strip()
        ingreso = self.ingreso.get().strip()

        conductores = self.cargarConductores()
        actualizado = False
        for c in conductores:
            if c.get("RUT") == idConductor:
                c["Nombre"] = nombreConductor
                c["Teléfono"] = telefono
                c["Correo Electrónico"] = correo
                c["Dirección"] = direccion
                c["Fecha Nacimiento"] = nacimiento
                c["Fecha Ingreso"] = ingreso
                actualizado = True
                break

        if actualizado:
            self.guardarConductores(conductores)
            messagebox.showinfo("Éxito", "Conductor editado correctamente.")
            self.mostrarMenuHorizontalConductores()
        else:
            messagebox.showerror("Error", "No se encontró el conductor para editar.")

    def accionEliminar(self):
        # Revisa si estas seleccionando algun elemento del árbol
        seleccion = self.treeConductores.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un conductor para eliminar.")
            return

        # Obtiene el RUT del conductor seleccionado (columna 0)
        item = seleccion[0]
        valores = self.treeConductores.item(item, "values")
        rut_a_eliminar = valores[0]

        #Confirmar con el usuario
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el conductor con RUT {rut_a_eliminar}?")
        if not confirmar:
            return

        # Cargar la lista de conductores
        conductores = self.cargarConductores()

        # Filtra la lista para eliminar el conductor seleccionado
        nuevos_conductores = [c for c in conductores if c.get("RUT") != rut_a_eliminar]
        # Incluye en la lista todos los conductores diferentes al rut a eliminar
        # "para cada elemento c en la lista conductores, incluye c en la nueva lista solo si cumple la condición después del if"

        # Guarda la lista actualizada
        self.guardarConductores(nuevos_conductores)

        # Refresca la tabla
        self.listaConductores()
        messagebox.showinfo("Éxito", f"Conductor con RUT {rut_a_eliminar} eliminado correctamente.")

    def pasar(self):
        self.limpiarWidgets()
        InfoCamiones(self.root)

class InfoCamiones(MenuAdmin, Camiones):
    def __init__(self, root):
        Camiones.__init__(self)  # Inicializa las variables de Camiones
        super().__init__(root)  # Inicializa las variables de Conductores
        self.root = root
        self.mostrarMenuHorizontalCamiones()

    def cargarCamiones(self):
        if not os.path.exists('camiones.json'): # Verifica si el archivo 'camiones.json' existe en el directorio actual
            return [] # Si no existe returna una lista vacía para evitar errores.

        with open('camiones.json', 'r') as file: # Manejo seguro de archivos, r(read) significa que es solo para lectura.
            return json.load(file) # Convierte el contenido del archivo JSON en un diccionario de python, si quisieramos hacer el caso opuesto deberíamos usar json.dumps
        

    def guardarCamiones(self, camiones):
        with open('camiones.json', 'w') as file:
            json.dump(camiones, file, indent=4)

    def mostrarMenuHorizontalCamiones(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.agregarCamion),
            ("Editar", self.editarCamion),
            ("Eliminar", self.accionEliminarCamiones),
            ("Mantención", self.mostrarCamionesNoDisponibles),
            ("Marcas", self.mostrarCrudMarcas),
            ("Modelos", self.mostrarCrudModelos),
            ("Tipo de arriendo", self.mostrarCrudTipoArriendo),
            ("Volver", self.volverBotones)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedor_menu = Frame(self.root)
        self.contenedor_menu.pack(expand=True)

        # Contenedor para la lista de camiones debajo de la barra
        self.contenedorListaCamiones = Frame(self.root)
        self.contenedorListaCamiones.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Incluye la columna "Tipo de arriendo"
        columnas = ("ID", "Patente", "Marca", "Modelo", "Fecha de ingreso", "Disponible", "Tipo de arriendo")
        self.treeCamiones = ttk.Treeview(self.contenedorListaCamiones, columns=columnas, show='headings')

        for col in columnas:
            self.treeCamiones.heading(col, text=col)
            self.treeCamiones.column(col, width=120, anchor='center')

        self.treeCamiones.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        camiones = self.cargarCamiones()
        for c in camiones:
            self.treeCamiones.insert('', 'end', values=(
                c.get("idCamion", ""),
                c.get("Patente", ""),
                c.get("Marca", ""),
                c.get("Modelo", ""),
                c.get("Ingreso", ""),
                c.get("Disponible", ""),
                c.get("TipoArriendo", "") or c.get("Tipo de arriendo", "")
            ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def agregarCamion(self): 
        self.limpiarWidgets()
        contenedorFormularioCamion = Frame(self.root, bg="orange")
        contenedorFormularioCamion.pack(padx=20, pady=20)

        # Cargar marcas
        marcas = self.cargarMarcas()
        self.marca_var = StringVar()
        self.modelo_var = StringVar()

        Label(contenedorFormularioCamion, text="Marca:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        marca_combo = Combobox(contenedorFormularioCamion, textvariable=self.marca_var, values=marcas, state="readonly")
        marca_combo.grid(row=1, column=1, pady=5)
        if marcas:
            marca_combo.current(0)

        Label(contenedorFormularioCamion, text="Patente:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormularioCamion, textvariable=self.patente).grid(row=0, column=1, pady=5)

        Label(contenedorFormularioCamion, text="Modelo:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        modelos_dict = self.cargarModelos()
        modelos_inicial = modelos_dict.get(self.marca_var.get(), [])
        modelo_combo = Combobox(contenedorFormularioCamion, textvariable=self.modelo_var, values=modelos_inicial, state="readonly")
        modelo_combo.grid(row=2, column=1, pady=5)
        if modelos_inicial:
            modelo_combo.current(0)

        def actualizar_modelos(*args):
            modelos_actualizados = self.cargarModelos().get(self.marca_var.get(), [])
            modelo_combo['values'] = modelos_actualizados
            if modelos_actualizados:
                modelo_combo.current(0)
                self.modelo_var.set(modelos_actualizados[0])
            else:
                self.modelo_var.set("")

        self.marca_var.trace('w', actualizar_modelos)

        # Botón para guardar
        Button(contenedorFormularioCamion, text="Guardar", command=self.guardarCamion).grid(row=7, column=0, columnspan=2, pady=15, ipadx=10, padx=20)
        Button(contenedorFormularioCamion, text="Volver", command=self.mostrarMenuHorizontalCamiones).grid(row=7, column=2, columnspan=2, pady=15, ipadx=30, padx=20)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def validarCamion(self, Patente, marca, modelo):
        Patente = Patente.replace("-", "").replace(".", "")
        modelo = modelo.replace("-", "").replace(".", "")

        if not all([Patente, marca, modelo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False

        elif len(Patente) != 6:
            messagebox.showerror("Error", "La patente debe tener 6 dígitos.")
            return False

        elif Patente == len(Patente) * Patente[0]:
            messagebox.showerror("Error", "La patente no puede ser una secuencia de dígitos repetidos.")
            return False

        elif Patente in "012345":
            messagebox.showerror("Error", "La patente no puede ser una secuencia ascendente.")
            return False

        elif Patente in "987654":
            messagebox.showerror("Error", "La patente no puede ser una secuencia descendente.")
            return False

        # Verificar si la patente ya existe
        a = self.cargarCamiones()
        for c in a:
            Patente_existente = c.get("Patente", "")
            if Patente_existente == Patente:
                messagebox.showerror("Error", "Ya existe un camión con esa patente.")
                return False
        return True

    def guardarCamion(self):
        patente = self.patente.get().strip()
        marca = self.marca_var.get().strip()
        modelo = self.modelo_var.get().strip().upper()

        if not self.validarCamion(patente, marca, modelo):
            return

        self.actualizarCamion(patente, marca, modelo)

    def listaCamiones(self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeCamiones.get_children():
            self.treeCamiones.delete(item)

        camiones = self.cargarCamiones()

        for c in camiones:
            if c.get("Disponible", "").lower() == "si":
                self.treeCamiones.insert('', 'end', values=(
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Ingreso", ""),
                    c.get("Disponible", ""),
                    c.get("Tipo de arriendo", "")
                ))

    def listaCamionesCompletos(self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeCamiones.get_children():
            self.treeCamiones.delete(item)

        camiones = self.cargarCamiones()

        for c in camiones:
            # Muestra TODOS los camiones, sin filtrar por "Disponible"
            self.treeCamiones.insert('', 'end', values=(
                c.get("idCamion", ""),
                c.get("Patente", ""),
                c.get("Marca", ""),
                c.get("Modelo", ""),
                c.get("Ingreso", ""),
                c.get("Disponible", ""),
                c.get("Tipo de arriendo", "")
            ))

    def accionEliminarCamiones(self):
        # Revisa si estas seleccionando algun elemento del árbol
        seleccion = self.treeCamiones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para eliminar.")
            return

        # Obtiene la patente del camión seleccionado (columna 0)
        item = seleccion[0]
        valores = self.treeCamiones.item(item, "values")
        patente_a_eliminar = valores[1]

        #Confirmar con el usuario
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el camión con patente {patente_a_eliminar}?")
        if not confirmar:
            return

        # Cargar la lista de conductores
        camiones = self.cargarCamiones()

        # Filtra la lista para eliminar el conductor seleccionado
        nuevos_camiones = [c for c in camiones if c.get("Patente") != patente_a_eliminar]
        # Incluye en la lista todos los conductores diferentes al rut a eliminar
        # "para cada elemento c en la lista conductores, incluye c en la nueva lista solo si cumple la condición después del if"

        # Guarda la lista actualizada
        self.guardarCamiones(nuevos_camiones)

        # Refresca la tabla
        self.listaCamionesCompletos()
        messagebox.showinfo("Éxito", f"Camión con patente {patente_a_eliminar} eliminado correctamente.")

    def editarCamion(self):
        seleccion = self.treeCamiones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para editar.")
            return
        item = seleccion[0]
        valores = self.treeCamiones.item(item, "values")
        patente = valores[1]
        marca = valores[2]
        modelo = valores[3]

        # Aquí puedes abrir un formulario de edición y pasar estos valores
        self.formularioEditarCamion(patente, marca, modelo)

    def formularioEditarCamion(self, patente, marca, modelo):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Variables temporales para edición
        patente_var = StringVar(value=patente)
        marca_var = StringVar(value=marca)
        modelo_var = StringVar(value=modelo)

        Label(contenedorFormulario, text="Patente:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=patente_var).grid(row=0, column=1, pady=5)

        # Menú desplegable de marcas
        Label(contenedorFormulario, text="Marca:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        marcas = self.cargarMarcas()
        marca_combo = Combobox(contenedorFormulario, textvariable=marca_var, values=marcas, state="readonly")
        marca_combo.grid(row=1, column=1, pady=5)
        if marca in marcas:
            marca_combo.set(marca)
        elif marcas:
            marca_combo.current(0)

        Label(contenedorFormulario, text="Modelo:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        modelos_dict = self.cargarModelos()
        modelos_inicial = modelos_dict.get(marca, [])
        modelo_combo = Combobox(contenedorFormulario, textvariable=modelo_var, values=modelos_inicial, state="readonly")
        modelo_combo.grid(row=2, column=1, pady=5)
        if modelo in modelos_inicial:
            modelo_combo.set(modelo)
        elif modelos_inicial:
            modelo_combo.current(0)

        def guardarCamion():
            # Actualiza el camión en tu JSON usando los nuevos valores
            self.actualizarCamion(patente_var.get(), marca_var.get(), modelo_var.get())

        Button(contenedorFormulario, text="Guardar", command=guardarCamion).grid(row=3, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalCamiones).grid(row=4, column=0, columnspan=2, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def actualizarCamion(self, Patente, marca, modelo):
        camiones = self.cargarCamiones()
        letra = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        asignado = False

        for c in camiones:
            if c.get("idCamion") == "":
                for l in letra:
                    for i in range(1, 4):
                        nuevoId = f"{l}{i}"
                        if not any(cam.get("idCamion") == nuevoId for cam in camiones):
                            c["idCamion"] = nuevoId
                            c["Patente"] = Patente
                            c["Marca"] = marca
                            c["Modelo"] = modelo
                            c["Ingreso"]= datetime.now().strftime("%Y-%m-%d")
                            c["Disponible"] = "Si"
                            asignado = True
                            break
                    if asignado:
                        break
            if asignado:
                break

        if asignado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "El camión se ha agregado exitosamente")
            self.mostrarMenuHorizontalCamiones()
        else:
            # Si no hay camión vacío, agrega uno nuevo
            nuevoId = None
            for l in letra:
                for i in range(1, 4):
                    posibleId = f"{l}{i}"
                    if not any(cam.get("idCamion") == posibleId for cam in camiones):
                        nuevoId = posibleId
                        break
                if nuevoId:
                    break
            if nuevoId:
                nuevoCamion = {
                    "idCamion": nuevoId,
                    "Patente": Patente,
                    "Marca": marca,
                    "Modelo": modelo,
                    "Ingreso": datetime.now().strftime("%Y-%m-%d"),
                    "Disponible": "Si"
                }
                camiones.append(nuevoCamion)
                self.guardarCamiones(camiones)
                messagebox.showinfo("Éxito", "El camión se ha agregado exitosamente")
                self.mostrarMenuHorizontalCamiones()
            else:
                messagebox.showerror("Error", "No se pudo asignar un ID.")

    def mostrarCamionesNoDisponibles(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Liberar camión", command=self.liberarCamion, bg="white", fg="black",
               font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Enviar a mantención", command=self.mostrarCamionesDisponibles, bg="white", fg="black",
               font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, bg="white", fg="black",
               font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorListaMantencion = Frame(self.root)
        self.contenedorListaMantencion.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Agrega la columna Asunto
        columnas = ("ID", "Patente", "Marca", "Modelo", "Fecha de ingreso", "Disponible")
        self.treeMantencion = ttk.Treeview(self.contenedorListaMantencion, columns=columnas, show='headings')

        for col in columnas:
            self.treeMantencion.heading(col, text=col)
            self.treeMantencion.column(col, width=120, anchor='center')

        self.treeMantencion.pack(fill=BOTH, expand=True)

        # Cargar solo camiones no disponibles
        camiones = self.cargarCamiones()
        for c in camiones:
            if c.get("Disponible", "").lower() == "no":
                self.treeMantencion.insert('', 'end', values=(
                    c.get("idCamion", ""),
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Ingreso", ""),
                    c.get("Disponible", "")
                ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def mostrarCamionesDisponibles(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Enviar a mantención", command=self.enviarAMantencion, bg="white", fg="black",
               font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarCamionesNoDisponibles, bg="white", fg="black",
               font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorListaDisponibles = Frame(self.root)
        self.contenedorListaDisponibles.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("ID", "Patente", "Marca", "Modelo", "Fecha de ingreso", "Disponible")
        self.treeDisponibles = ttk.Treeview(self.contenedorListaDisponibles, columns=columnas, show='headings')

        for col in columnas:
            self.treeDisponibles.heading(col, text=col)
            self.treeDisponibles.column(col, width=120, anchor='center')

        self.treeDisponibles.pack(fill=BOTH, expand=True)

        # Cargar solo camiones disponibles
        camiones = self.cargarCamiones()
        for c in camiones:
            if c.get("Disponible", "").lower() == "si":
                self.treeDisponibles.insert('', 'end', values=(
                    c.get("idCamion", ""),
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Ingreso", ""),
                    c.get("Disponible", "")
                ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def enviarAMantencion(self):
        seleccion = self.treeDisponibles.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para enviar a mantención.")
            return
        item = seleccion[0]
        valores = self.treeDisponibles.item(item, "values")
        id_camion = valores[0]

        camiones = self.cargarCamiones()
        encontrado = False
        for c in camiones:
            if c.get("idCamion") == id_camion:
                c["Disponible"] = "No"
                encontrado = True
                break
        if encontrado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "El camión ha sido liberado y ahora está disponible.")
            self.mostrarCamionesNoDisponibles()
        else:
            messagebox.showerror("Error", "No se encontró el camión seleccionado.")

    def liberarCamion(self):
        seleccion = self.treeMantencion.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para liberar.")
            return
        item = seleccion[0]
        valores = self.treeMantencion.item(item, "values")
        id_camion = valores[0]

        camiones = self.cargarCamiones()
        encontrado = False
        for c in camiones:
            if c.get("idCamion") == id_camion:
                c["Disponible"] = "Si"
                encontrado = True
                break
        if encontrado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "El camión ha sido liberado y ahora está disponible.")
            self.mostrarCamionesNoDisponibles()
        else:
            messagebox.showerror("Error", "No se encontró el camión seleccionado.")

    def mostrarCrudMarcas(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Agregar marca", command=self.formularioAgregarMarca, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Editar marca", command=self.formularioEditarMarca, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)  # Nuevo botón
        Button(self.barraHorizontal, text="Eliminar marca", command=self.eliminarMarca, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorListaMarcas = Frame(self.root)
        self.contenedorListaMarcas.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Marca",)
        self.treeMarcas = ttk.Treeview(self.contenedorListaMarcas, columns=columnas, show='headings')
        self.treeMarcas.heading("Marca", text="Marca")
        self.treeMarcas.column("Marca", width=200, anchor='center')
        self.treeMarcas.pack(fill=BOTH, expand=True)

        # Cargar y mostrar marcas
        marcas = self.cargarMarcas()
        for marca in marcas:
            self.treeMarcas.insert('', 'end', values=(marca,))

    def formularioAgregarMarca(self):
        top = Toplevel(self.root)
        top.title("Agregar Marca")
        Label(top, text="Marca:").pack(padx=10, pady=10)
        marca_var = StringVar()

        # Solo letras y espacios, máximo 20 caracteres
        def solo_letras(valor):
            return (valor.isalpha() or (valor.replace(" ", "").isalpha() and " " in valor)) and len(valor) <= 20 or valor == ""

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=marca_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            marca = marca_var.get().strip().upper()  # <-- Convierte a mayúsculas
            if not marca:
                messagebox.showerror("Error", "Ingrese una marca.")
                return
            marcas = [m.upper() for m in self.cargarMarcas()]  # <-- Compara en mayúsculas
            if marca in marcas:
                messagebox.showerror("Error", "La marca ya existe.")
                return
            marcas.append(marca)
            self.guardarMarcas(marcas)
            messagebox.showinfo("Éxito", "Marca agregada correctamente.")
            top.destroy()
            self.mostrarCrudMarcas()
        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def eliminarMarca(self):
        seleccion = self.treeMarcas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una marca para eliminar.")
            return
        item = seleccion[0]
        marca = self.treeMarcas.item(item, "values")[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar la marca '{marca}'?\nEsto también eliminará todos los camiones de esa marca.")
        if not confirmar:
            return
        # Elimina la marca del listado de marcas
        marcas = self.cargarMarcas()
        marcas = [m for m in marcas if m != marca]
        self.guardarMarcas(marcas)
        # Elimina los camiones de esa marca
        camiones = self.cargarCamiones()
        nuevos_camiones = [c for c in camiones if c.get("Marca") != marca]
        self.guardarCamiones(nuevos_camiones)
        messagebox.showinfo("Éxito", "Marca y camiones asociados eliminados correctamente.")
        self.mostrarCrudMarcas()

    def formularioEditarMarca(self):
        seleccion = self.treeMarcas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar una marca para editar.")
            return
        item = seleccion[0]
        marca_actual = self.treeMarcas.item(item, "values")[0]

        top = Toplevel(self.root)
        top.title("Editar Marca")
        Label(top, text="Nueva marca:").pack(padx=10, pady=10)
        marca_var = StringVar(value=marca_actual)

        # Solo letras y espacios, máximo 20 caracteres
        def solo_letras(valor):
            return (valor.isalpha() or (valor.replace(" ", "").isalpha() and " " in valor)) and len(valor) <= 20 or valor == ""

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=marca_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            nueva_marca = marca_var.get().strip().upper()
            if not nueva_marca:
                messagebox.showerror("Error", "Ingrese una marca.")
                return
            marcas = [m.upper() for m in self.cargarMarcas()]
            if nueva_marca in marcas and nueva_marca != marca_actual.upper():
                messagebox.showerror("Error", "La marca ya existe.")
                return
            # Actualiza la marca
            marcas = [nueva_marca if m.upper() == marca_actual.upper() else m.upper() for m in self.cargarMarcas()]
            self.guardarMarcas(marcas)
            messagebox.showinfo("Éxito", "Marca editada correctamente.")
            top.destroy()
            self.mostrarCrudMarcas()

        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def cargarMarcas(self):
        if not os.path.exists('marcas.json'):
            return []
        with open('marcas.json', 'r') as file:
            return json.load(file)

    def guardarMarcas(self, marcas):
        with open('marcas.json', 'w') as file:
            json.dump(marcas, file, indent=4)

    def mostrarCrudModelos(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Agregar modelo", command=self.formularioAgregarModelo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Editar modelo", command=self.formularioEditarModelo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Eliminar modelo", command=self.eliminarModelo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorListaModelos = Frame(self.root)
        self.contenedorListaModelos.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Marca", "Modelo")
        self.treeModelos = ttk.Treeview(self.contenedorListaModelos, columns=columnas, show='headings')
        for col in columnas:
            self.treeModelos.heading(col, text=col)
            self.treeModelos.column(col, width=150, anchor='center')
        self.treeModelos.pack(fill=BOTH, expand=True)

        # Cargar y mostrar modelos
        modelos = self.cargarModelos()
        for marca, lista_modelos in modelos.items():
            for modelo in lista_modelos:
                self.treeModelos.insert('', 'end', values=(marca, modelo))

    def formularioAgregarModelo(self):
        top = Toplevel(self.root)
        top.title("Agregar Modelo")
        Label(top, text="Marca:").pack(padx=10, pady=5)
        marcas = self.cargarMarcas()
        marca_var = StringVar()
        marca_combo = Combobox(top, textvariable=marca_var, values=marcas, state="readonly")
        marca_combo.pack(padx=10, pady=5)
        if marcas:
            marca_combo.current(0)
        Label(top, text="Modelo:").pack(padx=10, pady=5)
        modelo_var = StringVar()

        # Solo letras y números, sin espacios ni caracteres especiales, máximo 20 caracteres
        def solo_modelo(valor):
            # Permite letras y espacios, máximo 20 caracteres, no permite espacios al inicio/final ni dobles espacios
            if len(valor) > 20:
                return False
            if valor == "":
                return True
            # Solo letras y espacios
            if not all(c.isalpha() or c == " " for c in valor):
                return False
            # No espacios al inicio o final
            if valor[0] == " " or valor[-1] == " ":
                return False
            # No dobles espacios seguidos
            if "  " in valor:
                return False
            return True

        vcmd = (top.register(solo_modelo), '%P')
        Entry(top, textvariable=modelo_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=5)

        def guardar():
            marca = marca_var.get().strip()
            modelo = modelo_var.get().strip().upper()
            if not marca or not modelo:
                messagebox.showerror("Error", "Debe seleccionar una marca y escribir un modelo.")
                return
            if " " in modelo:
                messagebox.showerror("Error", "El modelo no puede contener espacios.")
                return
            if not modelo.isalnum():
                messagebox.showerror("Error", "El modelo solo puede contener letras y números, sin caracteres especiales.")
                return
            modelos = self.cargarModelos()
            if marca not in modelos:
                modelos[marca] = []
            if modelo in [m.upper() for m in modelos[marca]]:
                messagebox.showerror("Error", "Ese modelo ya existe para la marca seleccionada.")
                return
            modelos[marca].append(modelo)
            self.guardarModelos(modelos)
            messagebox.showinfo("Éxito", "Modelo agregado correctamente.")
            top.destroy()
            self.mostrarCrudModelos()

        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def eliminarModelo(self):
        seleccion = self.treeModelos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un modelo para eliminar.")
            return
        item = seleccion[0]
        marca, modelo = self.treeModelos.item(item, "values")
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar el modelo '{modelo}' de la marca '{marca}'?\nEsto también eliminará todos los camiones de ese modelo."
        )
        if not confirmar:
            return
        modelos = self.cargarModelos()
        if marca in modelos and modelo in modelos[marca]:
            modelos[marca].remove(modelo)
            if not modelos[marca]:
                del modelos[marca]
            self.guardarModelos(modelos)
            # Elimina los camiones de ese modelo
            camiones = self.cargarCamiones()
            nuevos_camiones = [c for c in camiones if not (c.get("Marca") == marca and c.get("Modelo") == modelo)]
            self.guardarCamiones(nuevos_camiones)
            messagebox.showinfo("Éxito", "Modelo y camiones asociados eliminados correctamente.")
            self.mostrarCrudModelos()

    def formularioEditarModelo(self):
        seleccion = self.treeModelos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un modelo para editar.")
            return
        item = seleccion[0]
        marca_actual, modelo_actual = self.treeModelos.item(item, "values")

        top = Toplevel(self.root)
        top.title("Editar Modelo")
        Label(top, text="Marca:").pack(padx=10, pady=5)
        Label(top, text=marca_actual).pack(padx=10, pady=5)
        Label(top, text="Nuevo modelo:").pack(padx=10, pady=5)
        modelo_var = StringVar(value=modelo_actual)

        # Solo letras y números, sin espacios ni caracteres especiales, máximo 20 caracteres
        def solo_modelo(valor):
            # Permite letras y espacios, máximo 20 caracteres, no permite espacios al inicio/final ni dobles espacios
            if len(valor) > 20:
                return False
            if valor == "":
                return True
            # Solo letras y espacios
            if not all(c.isalpha() or c == " " for c in valor):
                return False
            # No espacios al inicio o final
            if valor[0] == " " or valor[-1] == " ":
                return False
            # No dobles espacios seguidos
            if "  " in valor:
                return False
            return True

        vcmd = (top.register(solo_modelo), '%P')
        Entry(top, textvariable=modelo_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=5)

        def guardar():
            nuevo_modelo = modelo_var.get().strip().upper()
            if not nuevo_modelo:
                messagebox.showerror("Error", "Ingrese un modelo.")
                return
            if " " in nuevo_modelo:
                messagebox.showerror("Error", "El modelo no puede contener espacios.")
                return
            if not nuevo_modelo.isalnum():
                messagebox.showerror("Error", "El modelo solo puede contener letras y números, sin caracteres especiales.")
                return
            modelos = self.cargarModelos()
            if nuevo_modelo in [m.upper() for m in modelos.get(marca_actual, [])] and nuevo_modelo != modelo_actual.upper():
                messagebox.showerror("Error", "Ese modelo ya existe para la marca seleccionada.")
                return
            # Actualiza el modelo en la lista de modelos
            modelos[marca_actual] = [nuevo_modelo if m.upper() == modelo_actual.upper() else m.upper() for m in modelos[marca_actual]]
            self.guardarModelos(modelos)
            # Actualiza el modelo en los camiones existentes
            camiones = self.cargarCamiones()
            for c in camiones:
                if c.get("Marca") == marca_actual and c.get("Modelo") == modelo_actual:
                    c["Modelo"] = nuevo_modelo
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "Modelo editado correctamente.")
            top.destroy()
            self.mostrarCrudModelos()
        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def mostrarCrudTipoArriendo(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Agregar tipo", command=self.formularioAgregarTipoArriendo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Editar tipo", command=self.formularioEditarTipoArriendo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Eliminar tipo", command=self.eliminarTipoArriendo, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorListaTipos = Frame(self.root)
        self.contenedorListaTipos.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Tipo de arriendo",)
        self.treeTipos = ttk.Treeview(self.contenedorListaTipos, columns=columnas, show='headings')
        self.treeTipos.heading("Tipo de arriendo", text="Tipo de arriendo")
        self.treeTipos.column("Tipo de arriendo", width=200, anchor='center')
        self.treeTipos.pack(fill=BOTH, expand=True)

        # Cargar y mostrar tipos
        tipos = self.cargarTiposArriendo()
        for tipo in tipos:
            self.treeTipos.insert('', 'end', values=(tipo,))

    def formularioAgregarTipoArriendo(self):
        top = Toplevel(self.root)
        top.title("Agregar Tipo de Arriendo")
        Label(top, text="Tipo de arriendo:").pack(padx=10, pady=10)
        tipo_var = StringVar()

        # Solo letras y espacios, máximo 20 caracteres
        def solo_letras(valor):
            return (valor.replace(" ", "").isalpha() and len(valor) <= 20) or valor == ""

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=tipo_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            tipo = tipo_var.get().strip()
            if not tipo:
                messagebox.showerror("Error", "Ingrese un tipo de arriendo.")
                return
            if not tipo.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Solo se permiten letras y espacios.")
                return
            if len(tipo) > 20:
                messagebox.showerror("Error", "Máximo 20 caracteres.")
                return
            tipos = self.cargarTiposArriendo()
            if tipo in tipos:
                messagebox.showerror("Error", "Ese tipo ya existe.")
                return
            tipos.append(tipo)
            self.guardarTiposArriendo(tipos)
            messagebox.showinfo("Éxito", "Tipo de arriendo agregado correctamente.")
            top.destroy()
            self.mostrarCrudTipoArriendo()
        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def formularioEditarTipoArriendo(self):
        seleccion = self.treeTipos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un tipo para editar.")
            return
        item = seleccion[0]
        tipo_actual = self.treeTipos.item(item, "values")[0]

        top = Toplevel(self.root)
        top.title("Editar Tipo de Arriendo")
        Label(top, text="Nuevo tipo:").pack(padx=10, pady=10)
        tipo_var = StringVar(value=tipo_actual)

        # Solo letras y espacios, máximo 20 caracteres
        def solo_letras(valor):
            return (valor.replace(" ", "").isalpha() and len(valor) <= 20) or valor == ""

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=tipo_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            nuevo_tipo = tipo_var.get().strip()
            if not nuevo_tipo:
                messagebox.showerror("Error", "Ingrese un tipo de arriendo.")
                return
            if not nuevo_tipo.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Solo se permiten letras y espacios.")
                return
            if len(nuevo_tipo) > 20:
                messagebox.showerror("Error", "Máximo 20 caracteres.")
                return
            tipos = self.cargarTiposArriendo()
            if nuevo_tipo in tipos and nuevo_tipo != tipo_actual:
                messagebox.showerror("Error", "Ese tipo ya existe.")
                return
            tipos = [nuevo_tipo if t == tipo_actual else t for t in tipos]
            self.guardarTiposArriendo(tipos)
            messagebox.showinfo("Éxito", "Tipo de arriendo editado correctamente.")
            top.destroy()
            self.mostrarCrudTipoArriendo()
        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def eliminarTipoArriendo(self):
        seleccion = self.treeTipos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un tipo para eliminar.")
            return
        item = seleccion[0]
        tipo = self.treeTipos.item(item, "values")[0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el tipo '{tipo}'?")
        if not confirmar:
            return
        tipos = self.cargarTiposArriendo()
        tipos = [t for t in tipos if t != tipo]
        self.guardarTiposArriendo(tipos)
        messagebox.showinfo("Éxito", "Tipo de arriendo eliminado correctamente.")
        self.mostrarCrudTipoArriendo()

    def cargarTiposArriendo(self):
        if not os.path.exists('tipos_arriendo.json'):
            return []
        with open('tipos_arriendo.json', 'r') as file:
            return json.load(file)

    def guardarTiposArriendo(self, tipos):
        with open('tipos_arriendo.json', 'w') as file:
            json.dump(tipos, file, indent=4)

    def formularioAgregarCliente(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Etiquetas y entradas
        Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.rut).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreCompleto).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.formularioGuardarCliente).grid(row=5, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.menuInicial).grid(row=6, column=0, columnspan=2, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioGuardarCliente(self):
        rut = self.rut.get().strip()
        nombreCompleto = self.nombreCompleto.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()

        if not all([rut, nombreCompleto, telefono, correo, direccion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not self.validarRut(rut):
            return

        if not self.validarDatos(nombreCompleto, telefono, correo, direccion):
            return

        self.agregarCliente(rut, nombreCompleto, telefono, correo, direccion)

    def listaClientes(self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeClientes.get_children():
            self.treeClientes.delete(item)

        clientes = self.cargarUsuarios()  # Método que carga clientes desde JSON

        for c in clientes:
            self.treeClientes.insert('', 'end', values=(
                c.get("RUT", ""),
                c.get("Nombre completo", ""),
                c.get("Teléfono", ""),
                c.get("Correo Electrónico", ""),
                c.get("Dirección", ""),
                c.get("Fecha Nacimiento", ""),
                c.get("Fecha Ingreso", ""),
            ))

    def accionEditarCliente(self):
        seleccion = self.treeClientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para editar.")
            return
        item = seleccion[0]
        valores = self.treeClientes.item(item, "values")
        rut = valores[0]
        nombreCompleto = valores[1]
        telefono = valores[2]
        correo = valores[3]
        direccion = valores[4]

        self.formularioEditarCliente(rut, nombreCompleto, telefono, correo, direccion)

    def formularioEditarCliente(self, rut, nombreCompleto, telefono, correo, direccion):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Rellena el formulario con los datos del cliente seleccionado
        self.rut.set(rut)
        self.nombreCompleto.set(nombreCompleto)
        self.telefono.set(telefono)
        self.correo.set(correo)
        self.direccion.set(direccion)

        Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.rut, state='readonly').grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreCompleto).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        # Botón para guardar cambios
        Button(contenedorFormulario, text="Guardar cambios", command=self.guardarCambiosCliente).grid(row=5, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuClientes).grid(row=6, column=0, columnspan=2, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def guardarCambiosCliente(self):
        rut = self.rut.get().strip()
        nombreCompleto = self.nombreCompleto.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()

        if not all([rut, nombreCompleto, telefono, correo, direccion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not self.validarRut(rut):
            return

        if not self.validarDatos(nombreCompleto, telefono, correo, direccion):
            return

        clientes = self.cargarUsuarios()
        for c in clientes:
            if c.get("RUT") == rut:
                c["Nombre Completo"] = nombreCompleto
                c["Telefono"] = telefono
                c["Correo"] = correo
                c["Direccion"] = direccion
                break

        self.guardarUsuarios(clientes)
        messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        self.mostrarMenuClientes()

    def accionEliminarCliente(self):
        seleccion = self.treeClientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para eliminar.")
            return
        item = seleccion[0]
        valores = self.treeClientes.item(item, "values")
        rut_a_eliminar = valores[0]

        #Confirmar con el usuario
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el cliente con RUT {rut_a_eliminar}?")
        if not confirmar:
            return

        # Cargar la lista de clientes
        clientes = self.cargarUsuarios()

        # Filtra la lista para eliminar el cliente seleccionado
        nuevos_clientes = [c for c in clientes if c.get("RUT") != rut_a_eliminar]
        # Incluye en la lista todos los clientes diferentes al rut a eliminar
        # "para cada elemento c en la lista clientes, incluye c en la nueva lista solo si cumple la condición después del if"

        # Guarda la lista actualizada
        self.guardarUsuarios(nuevos_clientes)

        # Refresca la tabla
        self.listaClientes()
        messagebox.showinfo("Éxito", f"Cliente con RUT {rut_a_eliminar} eliminado correctamente.")

class MenuUsuarios(InicioSesionApp, MenuAdmin, Clientes):
    def __init__(self, root, nombreUsuarioSesionActual):
        Clientes.__init__(self)  # Inicializa las variables de Clientes
        super().__init__(root)  # Inicializa las variables de Conductores
        self.nombreUsuarioSesionActual = nombreUsuarioSesionActual
        self.actualizarLlavesUsuarios() # Asegura que las llaves de los usuarios estén actualizadas
        self.root = root
        self.menuInicial()

    def menuInicial(self):
        self.limpiarWidgets()

        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Editar perfil", self.editarPerfil),
            ("Carrito", self.mostrarCarrito),
            ("Arrendar camión", self.arrendarCamion), 
            ("Volver", self.salir)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        self.contenedorMenu = Frame(self.root)
        self.contenedorMenu.pack(expand=True)

        Button(self.barraHorizontal, text="Eliminar usuario", command=self.eliminarUsuario, font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        # Contenedor para la lista de camiones debajo de la barra
        self.contenedorListaCamiones = Frame(self.root)
        self.contenedorListaCamiones.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Crear el Treeview con columnas para cada dato
        columnas = ("Patente", "Marca", "Modelo", "Fecha de ingreso", "Disponible")
        self.treeCamiones = ttk.Treeview(self.contenedorListaCamiones, columns=columnas, show='headings')

        # Definir encabezados
        for col in columnas:
            self.treeCamiones.heading(col, text=col)
            self.treeCamiones.column(col, width=120, anchor='center')

        self.treeCamiones.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        self.listaCamiones()

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def listaCamiones(self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeCamiones.get_children():
            self.treeCamiones.delete(item)

        camiones = self.cargarCamiones()

        for c in camiones:
            if c.get("Disponible", "").lower() == "si":
                self.treeCamiones.insert('', 'end', values=(
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Ingreso", ""),
                    c.get("Disponible", "")
                ))

    def camionesDispobibles(self):
        pass

    def salir(self):
        self.limpiarWidgets()
        self.crearInterfaz()

    def validarRut(self, rut):
        # Elimina guiones y puntos
        rut = rut.replace("-", "").replace(".", "").upper()
        if not (8 <= len(rut) <= 9):
            messagebox.showerror("Error", "El RUT debe tener entre 8 y 9 caracteres.")
            return False

        cuerpo = rut[:-1]
        dv = rut[-1]

        if not cuerpo.isdigit():
            messagebox.showerror("Error", "El RUT debe tener solo números en la parte numérica.")
            return False

        # Calcular dígito verificador usando módulo 11
        suma = 0
        multiplo = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo = 9 if multiplo == 7 else multiplo + 1
            if multiplo > 7:
                multiplo = 2
        resto = suma % 11
        dv_calculado = 11 - resto
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(dv_calculado)

        if dv != dv_calculado:
            messagebox.showerror("Error", f"El dígito verificador es incorrecto. Debe ser {dv_calculado}.")
            return False

        # Verificar si el RUT ya existe (excepto para el usuario actual)
        usuarios = self.cargarUsuarios()
        for usuario in usuarios:
            rut_existente = usuario.get("RUT", "").replace("-", "").replace(".", "")
            if (usuario["nombre"] != self.nombreUsuarioSesionActual and 
                rut_existente == rut):
                messagebox.showerror("Error", "Ya existe un usuario con ese RUT.")
                return False
        return True

    def validarDatos(self, nombreCompleto, telefono, correo, direccion):
        nombre = nombreCompleto.strip() # Elimina espacios al inicio y al final
        telefono = telefono.replace(" ", "") 

        if len(nombre.split()) < 3:  # Al menos nombre y 2 apellidos
            messagebox.showerror("Error", "Debe ingresar nombre y 2 apellidos.")
            return False

        # Teléfono: 9 dígitos, solo números
        if not telefono.isdigit() or len(telefono) != 9:
            messagebox.showerror("Error", "El teléfono debe tener exactamente 9 dígitos y solo números.")
            return False

        elif telefono == "123456789" or telefono == "987654321" or telefono == len(telefono) * telefono[0]:
            messagebox.showerror("Error", "El teléfono no es válido.")
            return False

        # Validar correo con regex
        patron = r'^[\w\.-]+@[\w\.-]+\.(com|cl)$'
        if not re.match(patron, correo):
            messagebox.showerror("Error", "El correo debe tener formato válido y terminar en '.cl' o '.com'.")
            return False

        elif len(direccion) == 3:
            messagebox.showerror("Error", "Ingrese la dirección completa.")
            return False
        else:
            self.actualizarClientes(
            self.rut.get(),
            self.nombreCompleto.get(),
            self.telefono.get(),
            self.correo.get(),
            self.direccion.get()
            )
        # Si pasa todas las validaciones, pasa a actualizar los datos del usuario

    def formularioGuardarUsuario(self):
        rut = self.rut.get().strip()
        nombreCompleto = self.nombreCompleto.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()

        if not all([rut, nombreCompleto, telefono, correo, direccion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not self.validarRut(rut):
            return

        if not self.validarDatos(nombreCompleto, telefono, correo, direccion):
            return

        self.actualizarClientes(rut, nombreCompleto, telefono, correo, direccion)

    def editarPerfil(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Función de validación para solo números
        def soloNumeros(valor):
            return valor.isdigit() or valor == ""

        vcmd = (self.root.register(soloNumeros), '%P')
        clientes = self.cargarUsuarios()  # Método que carga clientes desde JSON

        # Rellena el formulario con los datos del usuario actual
        for c in clientes:
            if c.get("nombre") == self.nombreUsuarioSesionActual:
                self.rut.set(c.get("RUT", ""))
                self.nombreCompleto.set(c.get("Nombre Completo", ""))
                self.telefono.set(c.get("Telefono", ""))
                self.correo.set(c.get("Correo", ""))
                self.direccion.set(c.get("Direccion", ""))
                break

        # Variables para los campos del formulario
        if self.rut.get() == "":
            # Si el RUT está vacío, se habilita formulario para ingresar RUT
            Label(contenedorFormulario, text="RUT (sin guión y 0 si termina en K):", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
            Entry(contenedorFormulario, textvariable=self.rut, validate='key', validatecommand=vcmd).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreCompleto).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono, validate='key', validatecommand=vcmd).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.formularioGuardarUsuario).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.menuInicial).grid(row=7, column=1, columnspan=5, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def actualizarClientes(self, rut, nombreCompleto, telefono, correo, direccion):    
        clientes = self.cargarUsuarios()  # Método que carga clientes desde JSON
        usuarioEncontrado = False
        for c in clientes:
            if c.get("nombre") == self.nombreUsuarioSesionActual:
                c["RUT"] = rut
                c["Nombre Completo"] = nombreCompleto
                c["Telefono"] = telefono
                c["Correo"] = correo
                c["Direccion"] = direccion
                usuarioEncontrado = True
                break

        # Agregar nuevo usuario
        if usuarioEncontrado:
            self.guardarClientes(clientes)
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")

            self.menuInicial()  # Volver al menú principal
        else:
            messagebox.showerror("Error", "No se encontró un usuario con ese nombre.")

    def eliminarUsuario(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=40, pady=40)
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        usuarios = self.cargarUsuarios()  # Método que carga usuarios desde JSON

        # Busca y muestra los datos del usuario actual
        for c in usuarios:
            if c.get("nombre") == self.nombreUsuarioSesionActual:
                self.rut.set(c.get("RUT", ""))
                self.nombreCompleto.set(c.get("Nombre Completo", ""))
                self.telefono.set(c.get("Telefono", ""))
                self.correo.set(c.get("Correo", ""))
                self.direccion.set(c.get("Direccion", ""))

                # Mostrar los datos en el formulario, bien distribuidos
                Label(contenedorFormulario, text=f"RUT:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=0, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.rut.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=0, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Nombre completo:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.nombreCompleto.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=1, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Teléfono +56:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=2, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.telefono.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=2, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Correo:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=3, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.correo.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=3, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Dirección:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=4, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.direccion.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=4, column=1, sticky="w", pady=5, padx=5)
                break

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

        # Configura las columnas para que se expandan y centren los botones
        contenedorFormulario.grid_columnconfigure(0, weight=1)
        contenedorFormulario.grid_columnconfigure(1, weight=1)
            
        def confirmar():
            confirmar = messagebox.askyesno("Confirmar", f'¿Está seguro que desea eliminar el usuario "{self.nombreUsuarioSesionActual}"?')
            if confirmar:
                nuevos_usuarios = [u for u in usuarios if u.get("nombre") != self.nombreUsuarioSesionActual]
                self.guardarUsuarios(nuevos_usuarios)
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                self.salir()

        # Botones centrados en la fila
        Button(contenedorFormulario, text="Confirmar", command=confirmar, width=12).grid(row=6, column=0, pady=20, padx=10)
        Button(contenedorFormulario, text="Volver", command=self.menuInicial, width=12).grid(row=6, column=1, pady=20, padx=10)

    def listaUsuario (self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeDatos.get_children():
            self.treeDatos.delete(item)

        usuarios = self.cargarUsuarios()  # Método que carga usuarios desde JSON

        for usuario in usuarios:
            self.treeDatos.insert('', 'end', values=(
                usuario.get("RUT", ""),
                usuario.get("Nombre Completo", ""),
                usuario.get("Teléfono", ""),
                usuario.get("Correo Electrónico", ""),
                usuario.get("Dirección", "")
            ))

    def mostrarCarrito(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Editar", command=self.editarCamionCarrito, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Eliminar", command=self.eliminarCamionCarrito, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.menuInicial, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        self.contenedorCarrito = Frame(self.root)
        self.contenedorCarrito.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Patente", "Marca", "Modelo", "Fecha de ingreso", "Disponible", "Tipo de arriendo")
        self.treeCarrito = ttk.Treeview(self.contenedorCarrito, columns=columnas, show='headings')

        for col in columnas:
            self.treeCarrito.heading(col, text=col)
            self.treeCarrito.column(col, width=120, anchor='center')

        self.treeCarrito.pack(fill=BOTH, expand=True)

        # Cargar solo camiones arrendados por el usuario actual
        camiones = self.cargarCamiones()
        for c in camiones:
            if (
                c.get("Disponible", "").lower() == "en arriendo"
                and c.get("ArrendadoPor", "") == self.nombreUsuarioSesionActual
            ):
                self.treeCarrito.insert('', 'end', values=(
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Ingreso", ""),
                    c.get("Disponible", ""),
                    c.get("TipoArriendo", "")
                ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def arrendarCamion(self):
        seleccion = self.treeCamiones.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para arrendar.")
            return
        item = seleccion[0]
        valores = self.treeCamiones.item(item, "values")
        patente = valores[0]

        # Buscar el id_camion por patente
        camiones = self.cargarCamiones()
        id_camion = None
        for c in camiones:
            if c.get("Patente") == patente:
                id_camion = c.get("idCamion")
                break
        if not id_camion:
            messagebox.showerror("Error", "No se encontró el camión seleccionado.")
            return

        # Mostrar ventana para elegir tipo de arriendo
        top = Toplevel(self.root)
        top.title("Seleccionar tipo de arriendo")
        Label(top, text="Tipo de arriendo:").pack(padx=10, pady=10)
        tipos = self.cargarTiposArriendo()
        tipo_var = StringVar()
        tipo_combo = Combobox(top, textvariable=tipo_var, values=tipos, state="readonly")
        tipo_combo.pack(padx=10, pady=10)
        if tipos:
            tipo_combo.current(0)
        def confirmar():
            tipo_seleccionado = tipo_var.get()
            if not tipo_seleccionado:
                messagebox.showerror("Error", "Debe seleccionar un tipo de arriendo.")
                return
            camiones = self.cargarCamiones()
            encontrado = False
            for c in camiones:
                if c.get("idCamion") == id_camion and c.get("Disponible", "").lower() == "si":
                    c["Disponible"] = "En arriendo"
                    c["TipoArriendo"] = tipo_seleccionado
                    c["ArrendadoPor"] = self.nombreUsuarioSesionActual 
                    encontrado = True
                    break
            if encontrado:
                self.guardarCamiones(camiones)
                messagebox.showinfo("Éxito", f"Camión arrendado como '{tipo_seleccionado}'.")
                top.destroy()
                self.menuInicial()  # Refresca la lista de camiones
            else:
                messagebox.showerror("Error", "No se pudo arrendar el camión seleccionado.")
        Button(top, text="Confirmar", command=confirmar).pack(pady=10)
    def cargarTiposArriendo(self):
        if not os.path.exists('tipos_arriendo.json'):
            return []
        with open('tipos_arriendo.json', 'r') as file:
            return json.load(file)

    def guardarTiposArriendo(self, tipos):
        with open('tipos_arriendo.json', 'w') as file:
            json.dump(tipos, file, indent=4)

    def eliminarCamionCarrito(self):
        seleccion = self.treeCarrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para eliminar del carrito.")
            return
        item = seleccion[0]
        valores = self.treeCarrito.item(item, "values")
        patente = valores[0]

        camiones = self.cargarCamiones()
        encontrado = False
        for c in camiones:
            if c.get("Patente") == patente and c.get("ArrendadoPor", "") == self.nombreUsuarioSesionActual:
                c["Disponible"] = "Si"
                c["ArrendadoPor"] = ""
                c["TipoArriendo"] = ""
                encontrado = True
                break
        if encontrado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "Camión devuelto a disponibles.")
            self.mostrarCarrito()
        else:
            messagebox.showerror("Error", "No se pudo devolver el camión.")

    def editarCamionCarrito(self):
        seleccion = self.treeCarrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para editar.")
            return
        item = seleccion[0]
        valores = self.treeCarrito.item(item, "values")
        patente = valores[0]

        camiones = self.cargarCamiones()
        camion = None
        for c in camiones:
            if c.get("Patente") == patente and c.get("ArrendadoPor", "") == self.nombreUsuarioSesionActual:
                camion = c
                break
        if not camion:
            messagebox.showerror("Error", "No se encontró el camión seleccionado.")
            return

        top = Toplevel(self.root)
        top.title("Editar tipo de arriendo")
        Label(top, text="Tipo de arriendo:").pack(padx=10, pady=10)
        tipos = self.cargarTiposArriendo()
        tipo_var = StringVar(value=camion.get("TipoArriendo", ""))
        tipo_combo = Combobox(top, textvariable=tipo_var, values=tipos, state="readonly")
        tipo_combo.pack(padx=10, pady=10)
        if tipos and camion.get("TipoArriendo", "") in tipos:
            tipo_combo.set(camion.get("TipoArriendo", ""))
        elif tipos:
            tipo_combo.current(0)
        def guardar():
            tipo_seleccionado = tipo_var.get()
            if not tipo_seleccionado:
                messagebox.showerror("Error", "Debe seleccionar un tipo de arriendo.")
                return
            camion["TipoArriendo"] = tipo_seleccionado
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "Tipo de arriendo actualizado.")
            top.destroy()
            self.mostrarCarrito()
        Button(top, text="Guardar", command=guardar).pack(pady=10)
        
# Clase principal para ejecutar la aplicación
if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()
