# Importación de librerías y archivos
from tkinter import ttk, messagebox, StringVar
from conductores import Conductores
from clientes import Clientes
from camiones import Camiones
from datetime import datetime
from tkinter import *
import json
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
        #Fondo
        # self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TPA/TransporteXpress-TPA-main/Imagenes/camionbg.png")
        # imagenLabel = Label(self.root, image=self.imagen)
        # imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

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
    
    def mostrarBotonesCamionesYConductores(self):
        self.limpiarWidgets()
        
        # Fondo
        # self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TPA/TransporteXpress-TPA-main/Imagenes/camionbg.png")
        # imagenLabel = Label(self.root, image=self.imagen)
        # imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)
        
        self.contenedorBotones = Frame(self.root, bg="orange")
        self.contenedorBotones.place(relx=0.5, rely=0.5, anchor=S)
        Button(self.contenedorBotones, text="Camiones", command=self.pasar,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=0, column=0, padx=20, pady=10)
        Button(self.contenedorBotones, text="Conductores", command=self.mostrarMenuHorizontalConductores,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=1, column=0, padx=20, pady=10)

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
        self.limpiarWidgets() # Limpia la ventana
        self.mostrarBotonesCamionesYConductores()     

    def accionEditar(self):
        print("Acción Editar ejecutada.")

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
        
    def mostrarMenuHorizontalCamiones(self):
        self.limpiarWidgets() #limpia la ventana para mostrar el menu horizontal
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.agregarCamion),
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
        self.contenedorListaCamiones = Frame(self.root)
        self.contenedorListaCamiones.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Crear el Treeview con columnas para cada dato
        columnas = ("ID", "Patente", "Marca", "Modelo", "Fecha de Ingreso", "Disponible")
        self.treeCamiones = ttk.Treeview(self.contenedorListaCamiones, columns=columnas, show='headings')

        # Definir encabezados
        for col in columnas:
            self.treeCamiones.heading(col, text=col)
            self.treeCamiones.column(col, width=120, anchor='center')

        self.treeCamiones.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        self.listaCamiones()
        
    def agregarCamion(self): 
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)
          
        # Etiquetas y entradas
        Label(contenedorFormulario, text="Patente:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.patente).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Marca:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.marca).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Modelo:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.modelo).grid(row=2, column=1, pady=5)

        # Botón para guardar
        Button(contenedorFormulario, text="Guardar", command=self.guardarCamion).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalCamiones).grid(row=7, column=1, columnspan=2, pady=15)
        
    def validarCamion(self, Patente, marca, modelo):
        Patente = Patente.replace("-", "").replace(".", "")
        marca = marca.replace("-", "").replace(".", "")
        modelo = modelo.replace("-", "").replace(".", "")

        if not all([Patente, marca, modelo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        elif len(Patente) != 6:
            messagebox.showerror("Error", "La patente debe tener 6 dígitos.")
            return False

        elif Patente == len(Patente) * Patente[0]:
            messagebox.showerror("Error", "La patente no puede ser una secuencia de dígitos repetidos.")
            return

        # Secuencia ascendente
        elif Patente in "012345":
            messagebox.showerror("Error", "La patente no puede ser una secuencia ascendente.")
            return

        # Secuencia descendente
        elif Patente in "987654":
            messagebox.showerror("Error", "El RUT no puede ser una secuencia descendente.")
            return

        # Verificar si la patente ya existe
        a = self.cargarCamiones()
        for c in a:
            Patente_existente = c.get("idPatente", "")
            if Patente_existente == Patente:
                messagebox.showerror("Error", "Ya existe un camión con esa patente.")
                return False

        if len(marca) < 2 and len(modelo) < 2:
            messagebox.showerror("Error", "La marca y modelo debe tener como mínimo 2 dígitos.")
            return False

    def guardarCamion(self):
        patente = self.patente.get().strip()
        marca = self.marca.get().strip()
        modelo = self.modelo.get().strip()

        if not self.validarCamion(patente, marca, modelo):
            return

        self.actualizarCamion(patente, marca, modelo)

    def listaCamiones(self):
        # Limpia la tabla antes de cargar datos nuevos
        for item in self.treeCamiones.get_children():
            self.treeCamiones.delete(item)

        camiones = self.cargarCamiones()
        
        for c in camiones:
                self.treeConductores.insert('', 'end', values=(
                    c.get("idCamion", ""),
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    c.get("Disponible", ""),
                    c.get("Ingreso", "")
                ))

    def actualizarCamion(self, idPatente, marca, modelo):    
        camiones = self.cargarCamiones()  # Método que carga camiones desde JSON

        letra = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        asignado = False

        for c in camiones:
            if c.get("idCamion") == "":
                for l in letra:
                    for i in range(1, 4):
                        nuevoId = f"{l}{i}"
                        # Verifica que no esté ya asignado a otro camion
                        if not any(cam.get("idCamion") == nuevoId for cam in camiones):
                            c["idCamion"] = nuevoId
                            c["idPatente"] = idPatente
                            c["Marca"] = marca
                            c["Modelo"] = modelo
                            c["Ingreso"]= datetime.now().strftime("%Y-%m-%d")
                            asignado = True
                            break
                    if asignado:
                        break
            if asignado:
                break

        if asignado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "Camión asignado correctamente.")
            self.mostrarMenuHorizontalCamiones()
        else:
            messagebox.showerror("Error", "No se pudo asignar un idCamion.")
            self.guardarCamion()  # Volver al menú de camiones

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
            ("Disponibles", self.camionesDispobibles),
            ("Salir", self.salir),
            ("Editar Perfil", self.editarPerfil)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
            self.contenedorMenu = Frame(self.root)
            self.contenedorMenu.pack(expand=True)

        Button(self.barraHorizontal, text="Eliminar Usuario", command=self.eliminarUsuario,font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

    def camionesDispobibles(self):
        pass

    def salir(self):
        self.limpiarWidgets()
        self.crearInterfaz()

    def validarRut(self, rut):
        rut = rut.replace("-", "").replace(".", "")
        
        if len(rut) < 8 or len(rut) > 9:
            messagebox.showerror("Error", "El RUT debe tener entre 8 y 9 dígitos.")
            return False
 
        elif not rut.isdigit():
            messagebox.showerror("Error", "El RUT solo puede contener números.")
            return False

        elif rut == len(rut) * rut[0]:
            messagebox.showerror("Error", "El RUT no puede ser una secuencia de dígitos repetidos.")
            return

        # Secuencia ascendente
        elif rut in "0123456789":
            messagebox.showerror("Error", "El RUT no puede ser una secuencia ascendente.")
            return

        # Secuencia descendente
        elif rut in "9876543210":
            messagebox.showerror("Error", "El RUT no puede ser una secuencia descendente.")
            return

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
                   
        if len(telefono) != 9:
            messagebox.showerror("Error", "El teléfono debe tener 9 dígitos.")
            return False

        elif telefono == "123456789" or telefono == "987654321" or telefono == len(telefono) * telefono[0]:
            messagebox.showerror("Error", "El teléfono no es válido.")
            return False
            
        elif "@" not in correo or (not correo.endswith(".cl") or not correo.endswith(".com")) and len(correo) < 13:
            messagebox.showerror("Error", "El correo electrónico debe contener '@' y terminar en '.cl' o '.com' y tener al menos 13 caracteres.")
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
    
        #Rellena el formulario con los datos del usuario actual
        for c in clientes:
            if c.get("nombre") == self.nombreUsuarioSesionActual:
                self.rut.set(c.get("RUT", ""))
                self.nombreCompleto.set(c.get("Nombre Completo", ""))
                self.telefono.set(c.get("Telefono", ""))
                self.correo.set(c.get("Correo", ""))
                self.direccion.set(c.get("Direccion", ""))

        # Variables para los campos del formulario
        if self.rut.get() == "":
            # Si el RUT está vacío, se habilita formulario para ingresar RUT
            Label(contenedorFormulario, text="RUT (sin guión y 0 si termina en K):", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
            Entry(contenedorFormulario, textvariable=self.rut, validate='key', validatecommand=vcmd).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre Completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.nombreCompleto).grid(row=1, column=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.telefono, validate='key', validatecommand=vcmd).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        # Botón para guardar
        Button(
    contenedorFormulario,
    text="Guardar",
    command=self.formularioGuardarUsuario
    ).grid(row=7, column=0, columnspan=2, pady=15)
        
        Button(contenedorFormulario, text="Volver", command=self.menuInicial).grid(row=7, column=1, columnspan=5, pady=15)
        
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
                Label(contenedorFormulario, text=f"Nombre:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.nombreCompleto.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=1, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Teléfono:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=2, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.telefono.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=2, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Correo:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=3, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.correo.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=3, column=1, sticky="w", pady=5, padx=5)
                Label(contenedorFormulario, text=f"Dirección:", bg="orange", anchor="w", font=("Montserrat", 12, "bold")).grid(row=4, column=0, sticky="e", pady=5, padx=5)
                Label(contenedorFormulario, text=self.direccion.get(), bg="orange", anchor="w", font=("Montserrat", 12)).grid(row=4, column=1, sticky="w", pady=5, padx=5)
                break

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

        # Botones centrados en la fila 6
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

# Clase principal para ejecutar la aplicación
if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()
