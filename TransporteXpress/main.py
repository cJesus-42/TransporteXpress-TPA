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

        nombreLabel = Label(contenedor, text="Usuario: ", font=("Montserrat", 14), bg="orange")
        nombreLabel.grid(column=0, row=1)

        contraseniaLabel = Label(contenedor, text="Contraseña: ", font=("Montserrat", 14), bg="orange")
        contraseniaLabel.grid(column=0, row=2)

        # Validación para nombre: solo letras, espacios y números, máximo 10 caracteres, sin dobles espacios
        def validar_nombre(valor):
            if len(valor) > 10:
                return False
            if not all(c.isalpha() or c.isdigit() or c == " " for c in valor):
                return False
            if valor and (valor[0] == " " or valor[-1] == " " or "  " in valor):
                return False
            return True

        # Validación para contraseña: solo letras y números, máximo 6 caracteres
        def validar_contrasenia(valor):
            if valor == "":  # Permite borrar el último dígito
                return True
            if len(valor) > 10:  # Ajusta la validación de longitud
                return False
            if not valor.isalnum():  # Solo permite letras y números
                return False
            return True

        vcmd_nombre = (self.root.register(validar_nombre), '%P')
        vcmd_contrasenia = (self.root.register(validar_contrasenia), '%P')

        #Entradas de textos con validación
        nombreEntry = Entry(contenedor, textvariable=self.nombreUsuario, bg="#faedcd", validate='key', validatecommand=vcmd_nombre)
        nombreEntry.grid(column=1, row=1)

        contraseniaEntry = Entry(contenedor, textvariable=self.contraseniaUsuario, bg="#faedcd", show="*", validate='key', validatecommand=vcmd_contrasenia)
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
        self.intentos -= 1

        if self.intentos > 0:
            mensaje = (f'Contraseña incorrecta. Intentos restantes = {self.intentos}')
            messagebox.showerror('Error', mensaje)
        else:
            messagebox.showerror('Bloqueado', 'Haz alcanzado el máximo de intentos, la aplicación se cerrará.')
            self.root.destroy()

    def registrarUsuario(self):
        usuarios = self.cargarUsuarios()
        nombre = self.nombreUsuario.get()
        contrasenia = self.contraseniaUsuario.get()

        # Validaciones para nombre de usuario
        def solo_letras(valor):
            if len(valor) > 10:  # máximo 10 caracteres
                return False
            if valor == "":
                return True
            if not all(c.isalpha() or c == " " or c.isdigit() for c in valor):  # Solo letras, espacios y números
                return False
            if valor[0] == " " or valor[-1] == " ":
                return False
            if "  " in valor:
                return False
            return True

        if not nombre or not contrasenia:
            messagebox.showerror('Error', 'Ingrese un nombre y una contraseña para poder registrar')
            return False

        if not solo_letras(nombre):
            messagebox.showerror('Error', 'El nombre de usuario solo puede contener letras, números y espacios, sin espacios al inicio/final ni dobles espacios. Máximo 10 caracteres.')
            return False

        letras = [c for c in nombre if c.isalpha()]
        if len(letras) < 3:
            messagebox.showerror('Error', 'El nombre de usuario debe tener al menos 3 letras.')
            return False

        # Contraseña: solo letras y números, sin espacios, mínimo 4 caracteres
        if not contrasenia.isalnum():
            messagebox.showerror('Error', 'La contraseña solo puede contener letras y números, sin espacios.')
            return False
        if " " in contrasenia:
            messagebox.showerror('Error', 'La contraseña no puede contener espacios.')
            return False
        if len(contrasenia) < 4:
            messagebox.showerror('Error', 'La contraseña debe tener mínimo 4 caracteres.')
            return False
        # No permitir contraseñas con todos los dígitos iguales (ej: "1111", "aaaa", "2222")
        if len(set(contrasenia)) < 3:
            messagebox.showerror('Error', 'La contraseña debe tener al menos 3 caracteres diferentes.')
            return False

        for usuario in usuarios:
            if usuario['nombre'] == nombre:
                messagebox.showerror('Error', 'El usuario ya existe')
                return False

        usuarios.append({'nombre': nombre, 'contrasenia': contrasenia, 'Nombre Completo': ''})  # Agregar a librería que después se convierte en JSON.
        self.guardarUsuarios(usuarios)
        messagebox.showinfo('Registro', 'Usuario registrado exitosamente')
        return True

class MenuAdmin(Conductores, Camiones):
    def __init__(self, root):
        super().__init__()  # Inicializa las variables de Conductores
        self.root = root
        self.mostrarBotonesCamionesYConductores()

    def cargarModelos(self):
        import os
        if not os.path.exists('modelos.json'):
            return {}
        with open('modelos.json', 'r') as file:
            return json.load(file)

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

        Button(self.contenedorBotones, text="Cerrar sesión", command=self.salir,
            font=("Montserrat", 12), bg="white", fg="black", width=15).grid(row=2, column=0, padx=20, pady=10)

    def mostrarMenuHorizontalConductores(self):
        self.limpiarWidgets()  # Limpia la ventana para mostrar el menú horizontal

        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Agregar", self.formularioAgregarConductor),
            ("Editar", self.accionEditar),
            ("Eliminar", self.accionEliminar),
            ("Asociar camión", self.formularioAsociarCamionConductor),
            ("Desasociar camión", self.formularioDesasociarCamionConductor)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        Button(self.barraHorizontal, text="Volver", command=self.volverBotones, font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedor_menu = Frame(self.root)
        self.contenedor_menu.pack(expand=True)

        # Contenedor para la lista de conductores debajo de la barra
        self.contenedorLista = Frame(self.root)
        self.contenedorLista.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Crear el Treeview con columnas para cada dato
        columnas = ("RUT", "Nombre completo", "Teléfono", "Correo", "Dirección", "Fecha de nacimiento", "Fecha de ingreso", "Camión asociado")
        self.treeConductores = ttk.Treeview(self.contenedorLista, columns=columnas, show='headings')

        # Definir encabezados
        for col in columnas:
            self.treeConductores.heading(col, text=col)
            self.treeConductores.column(col, width=120, anchor='center')

        self.treeConductores.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        conductores = self.cargarConductores()
        camiones = self.cargarCamiones()
        rut_a_patente = {c.get("ConductorRUT"): c.get("Patente") for c in camiones if c.get("ConductorRUT")}

        for conductor in conductores:
            rut = conductor.get("RUT", "")
            camión_asociado = rut_a_patente.get(rut, "N/A")  # Obtiene la patente del camión asociado, si existe
            self.treeConductores.insert('', 'end', values=(
                rut,
                conductor.get("Nombre", ""),
                conductor.get("Teléfono", ""),
                conductor.get("Correo Electrónico", ""),
                conductor.get("Dirección", ""),
                conductor.get("Fecha Nacimiento", ""),
                conductor.get("Fecha Ingreso", ""),
                camión_asociado
            ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioAgregarConductor(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Inicializa las variables nacimiento e ingreso
        nacimiento = ""
        ingreso = ""

        # Etiquetas y entradas
        Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        def validar_rut(valor):
            # Permite escribir mientras se ingresa el RUT
            if not valor:
                return True
            # Solo dígitos y K, máximo 10 caracteres
            if not re.match(r'^[0-9kK\-\.]*$', valor):
                return False
            if len(valor.replace("-", "").replace(".", "")) > 9:
                return False
            return True

        vcmd_rut = (self.root.register(validar_rut), '%P')
        Entry(contenedorFormulario, textvariable=self.idConductor, validate='key', validatecommand=vcmd_rut).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        def ValidarNombreConductor(valor):
            if not valor:
                return True
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            # Permite espacio al final mientras se escribe
            palabras = valor.strip().split()
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)

        vcmd_nombre_conductor = (self.root.register(ValidarNombreConductor), '%P')
        Entry(contenedorFormulario, textvariable=self.nombreConductor, validate='key', validatecommand=vcmd_nombre_conductor).grid(column=1, row=1, pady=5)

        Label(contenedorFormulario, text="Teléfono +56:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        # Teléfono solo números, sin espacios ni doble espacios
        def validar_telefono(valor):
            if not valor:
                return True
            if " " in valor or not valor.isdigit():
                return False
            return True

        vcmd_telefono = (self.root.register(validar_telefono), '%P')
        Entry(contenedorFormulario, textvariable=self.telefono, validate='key', validatecommand=vcmd_telefono).grid(row=2, column=1, pady=5)

        Label(contenedorFormulario, text="Correo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        # Correo solo formato Gmail
        def validar_gmail(valor):
            if not valor:
                return True  # Permitimos vacío mientras se escribe

            # Permite letras, números, punto, guion y arroba
            patron = r'^[a-zA-Z0-9._@-]*$'
            if not re.match(patron, valor):
                return False

            # Si termina en @gmail.com, verificamos la longitud total
            if valor.lower().endswith('@gmail.com'):
                return True  # Si es válido, permitimos seguir escribiendo

            return True  # Si aún no terminó en @gmail.com, permitimos seguir escribiendo

        vcmd_correo = (self.root.register(validar_gmail), '%P')
        Entry(contenedorFormulario, textvariable=self.correo, validate='key', validatecommand=vcmd_correo).grid(row=3, column=1, pady=5)

        Label(contenedorFormulario, text="Dirección:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=self.direccion).grid(row=4, column=1, pady=5)

        # Calendario para fecha de nacimiento
        Label(contenedorFormulario, text="Fecha de nacimiento:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        nacimiento_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            maxdate=datetime.now() - timedelta(days=18*365),
            mindate=datetime(1900, 1, 1)
        )

        # Inicializa el calendario con la fecha guardada
        try:
            nacimiento_entry.set_date(datetime.strptime(nacimiento, "%d-%m-%Y"))
        except Exception:
            nacimiento_entry.set_date(datetime.now())
        nacimiento_entry.grid(row=5, column=1, pady=5)

        # Calendario para fecha de ingreso
        Label(contenedorFormulario, text="Fecha de ingreso:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        ingreso_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            maxdate=datetime.now()
        )

        # Inicializa el calendario con la fecha guardada
        try:
            ingreso_entry.set_date(datetime.strptime(ingreso, "%d-%m-%Y"))
        except Exception:
            ingreso_entry.set_date(datetime.now())
        ingreso_entry.grid(row=6, column=1, pady=5)

        # Botón para guardar
        def validar_modulo_11(rut):
            rut = rut.replace(".", "").replace("-", "").upper()
            if len(rut) < 2:
                return False
            cuerpo = rut[:-1]
            dv = rut[-1]
            suma = 0
            multiplo = 2
            for c in reversed(cuerpo):
                suma += int(c) * multiplo
                multiplo += 1
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
            return dv == dv_calculado

        def guardar_conductor():
            rut = self.idConductor.get().strip().replace("-", "").replace(".", "").upper()
            # Validación módulo 11
            if not validar_modulo_11(rut):
                messagebox.showerror("Error", "El RUT ingresado no es válido.")
                return
            self.nacimiento.set(nacimiento_entry.get_date().strftime("%d-%m-%Y"))
            self.ingreso.set(ingreso_entry.get_date().strftime("%d-%m-%Y"))
            self.formularioGuardarConductor()

        Button(contenedorFormulario, text="Guardar", command=guardar_conductor).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=7, column=1, columnspan=2, pady=15)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioGuardarConductor(self):
        # Obtiene los valores
        idConductor = self.idConductor.get().strip().replace("-", "").replace(".", "").upper()
        nombreConductor = self.nombreConductor.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()
        nacimiento = self.nacimiento.get().strip()
        ingreso = self.ingreso.get().strip()

        # Validación: todos los campos obligatorios
        if not all([idConductor, nombreConductor, telefono, correo, direccion, nacimiento, ingreso]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validación nombre: mínimo 3 palabras, solo letras y espacios
        palabras = nombreConductor.strip().split()
        if len(palabras) < 3 or not all(p.isalpha() for p in palabras):
            messagebox.showerror("Error", "Debe ingresar nombre y dos apellidos.")
            return
        if any(c.isdigit() for c in nombreConductor) or "  " in nombreConductor or nombreConductor[0] == " " or nombreConductor[-1] == " ":
            return

        # Teléfono: solo números, 9 dígitos, formato chileno, sin patrones repetidos
        if not telefono.isdigit() or len(telefono) != 9:
            messagebox.showerror("Error", "El teléfono debe tener 9 dígitos.")
            return
        if len(set(telefono)) == 1:
            messagebox.showerror("Error", "El teléfono no puede tener todos los dígitos iguales.")
            return
        if telefono in ["123456789", "987654321"]:
            messagebox.showerror("Error", "El teléfono no puede ser una secuencia simple.")
            return
        if not telefono.startswith("9"):
            messagebox.showerror("Error", "El teléfono debe comenzar con 9.")
            return
        if telefono[1:] == "00000000":
            messagebox.showerror("Error", "El teléfono no puede ser 9 seguido de puros ceros.")
            return

        # Validación para correo
        if len(correo) < 14 or len(correo) > 31:
            messagebox.showerror("Error", "El correo debe tener entre 14 y 30 caracteres, incluyendo '@gmail.com'.")
            return

        patron = r'^[\w\.-]+@gmail\.com$'
        if not re.match(patron, correo):
            messagebox.showerror("Error", "El correo debe tener formato Gmail.")
            return

        # Dirección: mínimo 5 caracteres
        if len(direccion) < 5:
            messagebox.showerror("Error", "Ingrese la dirección completa (mínimo 5 caracteres).")
            return

        # Verifica que el conductor no tenga camión asociado
        camiones = self.cargarCamiones()
        for c in camiones:
            if c.get("ConductorRUT") == idConductor:
                messagebox.showerror("Error", "Este conductor ya tiene un camión asociado.")
                return

        # Formatear fechas al formato chileno dd-mm-yyyy
        try:
            if nacimiento:
                nacimiento = datetime.strptime(nacimiento, "%Y-%m-%d").strftime("%d-%m-%Y")
            if ingreso:
                ingreso = datetime.strptime(ingreso, "%Y-%m-%Y").strftime("%d-%m-%Y")
        except Exception:
            pass

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
        conductores = self.cargarConductores()  # Método que carga conductores desde JSON

        conductores.append(nuevoConductor)  # <-- Agrega el nuevo conductor

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

    def formularioAsociarCamionConductor(self):
        self.limpiarWidgets()
        contenedor = Frame(self.root, bg="orange")
        contenedor.pack(padx=20, pady=20)

        # Cargar conductores SIN camión asociado
        conductores = self.cargarConductores()
        camiones = self.cargarCamiones()
        conductores_sin_camion = [c for c in conductores if not any(cam.get("ConductorRUT") == c["RUT"] for cam in camiones)]
        if not conductores_sin_camion:
            messagebox.showinfo("Info", "Todos los conductores ya tienen camión asociado.")
            self.mostrarMenuHorizontalConductores()
            return

        ruts = [c["RUT"] for c in conductores_sin_camion]
        nombres = [f'{c["Nombre"]} ({c["RUT"]})' for c in conductores_sin_camion]
        Label(contenedor, text="Conductor:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        conductor_var = StringVar()
        conductor_combo = Combobox(contenedor, textvariable=conductor_var, values=nombres, state="readonly")
        conductor_combo.grid(row=0, column=1, pady=5)
        if nombres:
            conductor_combo.current(0)

        # Cargar camiones disponibles (sin conductor asociado)
        camiones_disponibles = [c for c in camiones if not c.get("ConductorRUT")]
        patentes = [c["Patente"] for c in camiones_disponibles]

        Label(contenedor, text="Patente de camión:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        patente_var = StringVar()
        patente_combo = Combobox(contenedor, textvariable=patente_var, values=patentes, state="readonly")
        patente_combo.grid(row=1, column=1, pady=5)
        if patentes:
            patente_combo.current(0)

        # Marca, modelo y valor fijo (solo texto)
        marca_var = StringVar()
        modelo_var = StringVar()
        valor_fijo_var = StringVar()  # Define valor_fijo_var aquí
        Label(contenedor, text="Marca:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=marca_var, bg="orange").grid(row=2, column=1, pady=5)
        Label(contenedor, text="Modelo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=modelo_var, bg="orange").grid(row=3, column=1, pady=5)
        Label(contenedor, text="Valor diario:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=valor_fijo_var, bg="orange").grid(row=4, column=1, pady=5)

        def actualizar_marca_modelo(*args):
            modelos_dict = self.cargarModelos()  # Cargar modelos dentro del método
            patente = patente_var.get()
            for c in camiones_disponibles:
                if c["Patente"] == patente:
                    marca = c.get("Marca", "")
                    modelo = c.get("Modelo", "")
                    marca_var.set(marca)
                    modelo_var.set(modelo)
                    # Obtener valor fijo desde modelos.json
                    valor_fijo = c.get("valor_fijo")
                    if valor_fijo is None or valor_fijo == "":
                        modelos = modelos_dict.get(marca, [])
                        for m in modelos:
                            nombre = m["nombre"] if isinstance(m, dict) else m
                            if nombre == modelo and isinstance(m, dict):
                                valor_fijo = m.get('valor_fijo', 0)
                                break
                    valor_fijo_str = f"${valor_fijo:,}" if valor_fijo else ""
                    valor_fijo_var.set(valor_fijo_str)
                    break
            else:
                marca_var.set("")
                modelo_var.set("")
                valor_fijo_var.set("")

        patente_var.trace('w', actualizar_marca_modelo)
        if patentes:
            actualizar_marca_modelo()

        def guardar():
            conductor_idx = conductor_combo.current()
            patente = patente_var.get()
            if conductor_idx == -1 or not patente:
                messagebox.showerror("Error", "Debe seleccionar camión y conductor.")
                return
            rut_conductor = ruts[conductor_idx]
            # Verifica que el conductor no tenga camión asociado
            camiones = self.cargarCamiones()
            for c in camiones:
                if c.get("ConductorRUT") == rut_conductor:
                    messagebox.showerror("Error", "Este conductor ya tiene un camión asociado.")
                    return
            for c in camiones:
                if c["Patente"] == patente:
                    c["ConductorRUT"] = rut_conductor
                    break
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", f"Camión {patente} asociado a conductor {rut_conductor}.")
            self.mostrarMenuHorizontalConductores()

        Button(contenedor, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=15)
        Button(contenedor, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=6, column=0, columnspan=2, pady=5)

    def formularioDesasociarCamionConductor(self):
        self.limpiarWidgets()
        contenedor = Frame(self.root, bg="orange")
        contenedor.pack(padx=20, pady=20)

        # Cargar conductores CON camión asociado
        camiones = self.cargarCamiones()
        conductores = self.cargarConductores()
        ruts_con_camion = set(c.get("ConductorRUT") for c in camiones if c.get("ConductorRUT"))
        conductores_con_camion = [c for c in conductores if c["RUT"] in ruts_con_camion]
        if not conductores_con_camion:
            messagebox.showinfo("Info", "Ningún conductor tiene camión asociado.")
            self.mostrarMenuHorizontalConductores()
            return

        ruts = [c["RUT"] for c in conductores_con_camion]
        nombres = [f'{c["Nombre"]} ({c["RUT"]})' for c in conductores_con_camion]
        Label(contenedor, text="Conductor:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        conductor_var = StringVar()
        conductor_combo = Combobox(contenedor, textvariable=conductor_var, values=nombres, state="readonly")
        conductor_combo.grid(row=0, column=1, pady=5)
        if nombres:
            conductor_combo.current(0)

        # Mostrar patente, marca y modelo del camión asociado
        patente_var = StringVar()
        marca_var = StringVar()
        modelo_var = StringVar()
        Label(contenedor, text="Patente de camión:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=patente_var, bg="orange").grid(row=1, column=1, pady=5)
        Label(contenedor, text="Marca:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=marca_var, bg="orange").grid(row=2, column=1, pady=5)
        Label(contenedor, text="Modelo:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Label(contenedor, textvariable=modelo_var, bg="orange").grid(row=3, column=1, pady=5)

        def actualizar_camion(*args):
            idx = conductor_combo.current()
            if idx == -1:
                patente_var.set("")
                marca_var.set("")
                modelo_var.set("")
                return
            rut = ruts[idx]
            for c in camiones:
                if c.get("ConductorRUT") == rut:
                    patente_var.set(c.get("Patente", ""))
                    marca_var.set(c.get("Marca", ""))
                    modelo_var.set(c.get("Modelo", ""))
                    break
            else:
                patente_var.set("")
                marca_var.set("")
                modelo_var.set("")

        conductor_var.trace('w', actualizar_camion)
        conductor_combo.bind("<<ComboboxSelected>>", lambda e: actualizar_camion())
        if nombres:
            actualizar_camion()

        def desasociar():
            idx = conductor_combo.current()
            if idx == -1:
                messagebox.showerror("Error", "Debe seleccionar un conductor.")
                return
            rut = ruts[idx]
            encontrado = False
            for c in camiones:
                if c.get("ConductorRUT") == rut:
                    c["ConductorRUT"] = ""
                    encontrado = True
                    break
            if encontrado:
                self.guardarCamiones(camiones)
                messagebox.showinfo("Éxito", "Camión desasociado correctamente.")
                self.mostrarMenuHorizontalConductores()
            else:
                messagebox.showinfo("Info", "El conductor no tiene camión asociado.")

        Button(contenedor, text="Desasociar", command=desasociar).grid(row=4, column=0, columnspan=2, pady=15)
        Button(contenedor, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=5, column=0, columnspan=2, pady=5)

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

        # Calendario para fecha de nacimiento
        Label(contenedorFormulario, text="Fecha de nacimiento:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        nacimiento_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            maxdate=datetime.now() - timedelta(days=18*365),
            mindate=datetime(1900, 1, 1)
        )
        # Inicializa el calendario con la fecha guardada
        try:
            nacimiento_entry.set_date(datetime.strptime(nacimiento, "%d-%m-%Y"))
        except Exception:
            nacimiento_entry.set_date(datetime.now())
        nacimiento_entry.grid(row=5, column=1, pady=5)

        # Calendario para fecha de ingreso
        Label(contenedorFormulario, text="Fecha de ingreso:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        ingreso_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            maxdate=datetime.now()
        )
        # Inicializa el calendario con la fecha guardada
        try:
            ingreso_entry.set_date(datetime.strptime(ingreso, "%d-%m-%Y"))
        except Exception:
            ingreso_entry.set_date(datetime.now())
        ingreso_entry.grid(row=6, column=1, pady=5)

        def guardar_edicion():
            nombreConductor = self.nombreConductor.get().strip()
            telefono = self.telefono.get().strip()
            correo = self.correo.get().strip()
            direccion = self.direccion.get().strip()
            nacimiento = nacimiento_entry.get_date().strftime("%d-%m-%Y")
            ingreso = ingreso_entry.get_date().strftime("%d-%m-%Y")

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

        Button(contenedorFormulario, text="Guardar", command=guardar_edicion).grid(row=7, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalConductores).grid(row=7, column=1, columnspan=5, pady=15)

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
        nuevos_conductores = [c for c in conductores if c.get("RUT") != rut_a_eliminar]
        self.guardarConductores(nuevos_conductores)

        # Solo elimina el rut del conductor en los camiones asociados, no el camión
        camiones = self.cargarCamiones()
        for c in camiones:
            if c.get("ConductorRUT") == rut_a_eliminar:
                c["ConductorRUT"] = ""
        self.guardarCamiones(camiones)

        # Refresca la tabla
        self.listaConductores()
        messagebox.showinfo("Éxito", f"Conductor con RUT {rut_a_eliminar} eliminado correctamente y desasociado de su camión.")

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

    def cargarModelos(self):
        if not os.path.exists('modelos.json'):
            return {}
        with open('modelos.json', 'r') as file:
            return json.load(file)

    def guardarModelos(self, modelos):
        with open('modelos.json', 'w') as file:
            json.dump(modelos, file, indent=4)        

    def guardarTiposArriendo(self, tipos):
        with open('tipos_arriendo.json', 'w') as file:
            json.dump(tipos, file, indent=4)

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
            ("Contrato de arriendo", self.mostrarContratoArriendo),
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        Button(self.barraHorizontal, text="Volver", command=self.volverBotones, font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedor_menu = Frame(self.root)
        self.contenedor_menu.pack(expand=True)

        # Contenedor para la lista de camiones debajo de la barra
        self.contenedorListaCamiones = Frame(self.root)
        self.contenedorListaCamiones.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Crear el Treeview con columnas para cada dato
        columnas = ("ID", "Patente", "Marca", "Modelo", "Valor diario", "Fecha de ingreso", "Disponible", "Tipo de arriendo", "Conductor")
        self.treeCamiones = ttk.Treeview(self.contenedorListaCamiones, columns=columnas, show='headings')

        for col in columnas:
            self.treeCamiones.heading(col, text=col)
            self.treeCamiones.column(col, width=120, anchor='center')
        self.treeCamiones.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos
        camiones = self.cargarCamiones()
        conductores = self.cargarConductores()
        rut_a_nombre = {c["RUT"]: c["Nombre"] for c in conductores}

        modelos_dict = self.cargarModelos()
        tipos_arriendo = self.cargarTiposArriendo()
        for c in camiones:
            marca = c.get("Marca", "")  # Definir marca
            modelo = c.get("Modelo", "")  # Definir modelo
            rut = c.get("ConductorRUT", "")
            nombre_conductor = rut_a_nombre.get(rut, "") if rut else ""
            # Obtener valor fijo desde modelos.json
            valor_fijo = c.get("valor_fijo")
            if valor_fijo is None or valor_fijo == "":
                # Buscar en modelos.json si no está en el camión
                modelos = modelos_dict.get(marca, [])
                for m in modelos:
                    nombre = m["nombre"] if isinstance(m, dict) else m
                    if nombre == modelo and isinstance(m, dict):
                        valor_fijo = m.get('valor_fijo', 0)
                        break
            valor_fijo_str = f"${valor_fijo:,}" if valor_fijo else ""

            # Obtener tipo de arriendo y valor diario
            tipo_arriendo = c.get("TipoArriendo", "")
            tipo_arriendo_valor = tipo_arriendo
            for t in tipos_arriendo:
                if isinstance(t, dict) and t.get("tipo", "") == tipo_arriendo:
                    tipo_arriendo_valor = f"{tipo_arriendo}, ${t.get('valor_diario', 0):,}"
                    break

            self.treeCamiones.insert('', 'end', values=(
                c.get("idCamion", ""),
                c.get("Patente", ""),
                marca,
                modelo,
                valor_fijo_str,
                c.get("Ingreso", ""),
                c.get("Disponible", ""),
                tipo_arriendo_valor,
                nombre_conductor
            ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def mostrarContratoArriendo(self):
        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Nuevo contrato", self.nuevoContrato),
            ("Consultar contratos", self.consultarContratos),
            ("Eliminar contrato", self.eliminarContrato)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedorListaContratos = Frame(self.root)
        self.contenedorListaContratos.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("ID", "Usuario", "Patente", "Marca", "Modelo", "Valor fijo", "Tipo de arriendo", "Fecha de arriendo", "Fecha de término", "Estado")
        self.treeContratos = ttk.Treeview(self.contenedorListaContratos, columns=columnas, show='headings')

        for col in columnas:
            self.treeContratos.heading(col, text=col)
            self.treeContratos.column(col, width=120, anchor='center')

        self.treeContratos.pack(fill=BOTH, expand=True)

        # Cargar y mostrar los datos de cotizaciones
        if os.path.exists("camiones.json"):
            with open("camiones.json", "r") as file:
                camiones = json.load(file)
        else:
            camiones = []

        if os.path.exists("cotizaciones.json"):
            with open("cotizaciones.json", "r") as file:
                cotizaciones = json.load(file)
        else:
            cotizaciones = []            

        for camion, cotizaciones in camiones, cotizaciones:
            if camion.get("Disponible", "").lower() == "en arriendo":  # Filtrar camiones con estado "En arriendo"
                self.treeContratos.insert('', 'end', values=(
                    camion.get("ID", ""),
                    cotizaciones.get("Usuario", ""),
                    camion.get("Patente", ""),
                    camion.get("Marca", ""),
                    camion.get("Modelo", ""),
                    camion.get("Valor fijo", ""),
                    camion.get("Tipo de arriendo", ""),
                    camion.get("Fecha de arriendo", ""),
                    camion.get("Fecha de término", ""),
                    camion.get("Estado", "")
                ))

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)   
        
    def nuevoContrato(self):
        messagebox.showinfo("Nuevo contrato", "Funcionalidad para crear un nuevo contrato.")
        
    def consultarContratos(self):
        seleccion = self.treeContratos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un contrato para consultar.")
            return
        item = seleccion[0]
        valores = self.treeContratos.item(item, "values")
        contrato_id = valores[0]
        messagebox.showinfo("Consultar contrato", f"Detalles del contrato ID: {contrato_id}")
        
    def eliminarContrato(self):
        seleccion = self.treeContratos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un contrato para eliminar.")
            return
        item = seleccion[0]
        valores = self.treeContratos.item(item, "values")
        contrato_id = valores[0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el contrato ID: {contrato_id}?")
        if not confirmar:
            return

        if os.path.exists("cotizaciones.json"):
            with open("cotizaciones.json", "r") as file:
                cotizaciones = json.load(file)
            cotizaciones = [c for c in cotizaciones if c.get("ID") != contrato_id]
            with open("cotizaciones.json", "w") as file:
                json.dump(cotizaciones, file, indent=4)
            messagebox.showinfo("Éxito", f"Contrato ID: {contrato_id} eliminado correctamente.")
            self.mostrarContratoArriendo()    

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
        modelos_inicial = [m["nombre"] if isinstance(m, dict) else m for m in modelos_dict.get(self.marca_var.get(), [])]
        modelo_combo = Combobox(contenedorFormularioCamion, textvariable=self.modelo_var, values=modelos_inicial, state="readonly")
        modelo_combo.grid(row=2, column=1, pady=5)
        if modelos_inicial:
            modelo_combo.current(0)

        # Mostrar el valor fijo debajo del modelo (solo texto, no editable)
        valor_fijo_var = StringVar()
        Label(contenedorFormularioCamion, text="Valor diario:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        valor_fijo_label = Label(contenedorFormularioCamion, textvariable=valor_fijo_var, bg="orange")
        valor_fijo_label.grid(row=3, column=1, pady=5)

        def actualizar_valor_fijo(*args):
            marca = self.marca_var.get()
            modelo = self.modelo_var.get()
            modelos = self.cargarModelos().get(marca, [])
            for m in modelos:
                nombre = m["nombre"] if isinstance(m, dict) else m
                if nombre == modelo and isinstance(m, dict):
                    valor_fijo_var.set(f"${m.get('valor_fijo', ''):,}")
                    break
            else:
                valor_fijo_var.set("")

        self.marca_var.trace('w', actualizar_valor_fijo)
        self.modelo_var.trace('w', actualizar_valor_fijo)
        if modelos_inicial:
            actualizar_valor_fijo()

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
        Patente = Patente.replace("-", "").replace(".", "").upper()

        if not all([Patente, marca, modelo]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False

        # Letras válidas: A-H, J-N, P, R-T, V-Z (excluye I, O, Q, U, Ñ)
        letras_validas = "A-HJ-NPR-TV-Z"
        formato_1 = rf'^[{letras_validas}]{{2}}[0-9]{{4}}$'    # Ej: BB1234
        formato_2 = rf'^[{letras_validas}]{{4}}[0-9]{{2}}$'    # Ej: BBBB12

        if not (re.match(formato_1, Patente) or re.match(formato_2, Patente)):
            messagebox.showerror(
                "Error",
                "La patente debe tener el formato LLNNNN o LLLLNN, usando solo letras válidas (sin I, O, Q, U, Ñ)."
            )
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
        patente = self.patente.get().strip().upper()
        marca = self.marca_var.get().strip().upper()
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
                    c.get("Disponible", "")
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
                c.get("TipoArriendo", "") or c.get("Tipo de arriendo", ""),
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
        valor_fijo_var = StringVar()

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
        modelos_inicial = [m["nombre"] if isinstance(m, dict) else m for m in modelos_dict.get(marca, [])]
        modelo_combo = Combobox(contenedorFormulario, textvariable=modelo_var, values=modelos_inicial, state="readonly")
        modelo_combo.grid(row=2, column=1, pady=5)
        if modelo in modelos_inicial:
            modelo_combo.set(modelo)
        elif modelos_inicial:
            modelo_combo.current(0)

        # Campo editable para valor fijo debajo de modelo
        Label(contenedorFormulario, text="Valor diario:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Entry(contenedorFormulario, textvariable=valor_fijo_var).grid(row=3, column=1, pady=5)

        # Actualiza el valor fijo al cambiar marca/modelo
        def actualizar_valor_fijo(*args):
            marca_sel = marca_var.get()
            modelo_sel = modelo_var.get()
            modelos = self.cargarModelos().get(marca_sel, [])
            for m in modelos:
                nombre = m["nombre"] if isinstance(m, dict) else m
                if nombre == modelo_sel and isinstance(m, dict):
                    valor_fijo_var.set(str(m.get('valor_fijo', '')))
                    break
            else:
                valor_fijo_var.set("")

        marca_var.trace('w', actualizar_valor_fijo)
        modelo_var.trace('w', actualizar_valor_fijo)
        if modelos_inicial:
            actualizar_valor_fijo()

        def guardarCamion():
            nueva_patente = patente_var.get().strip().upper()
            nueva_marca = marca_var.get().strip().upper()
            nuevo_modelo = modelo_var.get().strip().upper()
            nuevo_valor_fijo = valor_fijo_var.get().strip()

            # Validaciones de patente usando validarCamion
            if not self.validarCamion(nueva_patente, nueva_marca, nuevo_modelo):
                return
            if not nuevo_valor_fijo.isdigit() or int(nuevo_valor_fijo) < 10000:
                messagebox.showerror("Error", "El valor diario debe ser un número mayor o igual a $10000.")
                return

            camiones = self.cargarCamiones()
            actualizado = False
            for c in camiones:
                if c.get("Patente", "") == patente:
                    c["Patente"] = nueva_patente
                    c["Marca"] = nueva_marca
                    c["Modelo"] = nuevo_modelo
                    actualizado = True
                    break
            if actualizado:
                # Actualiza el valor fijo en modelos.json
                modelos = self.cargarModelos()
                lista_modelos = modelos.get(nueva_marca, [])
                for m in lista_modelos:
                    nombre = m["nombre"] if isinstance(m, dict) else m
                    if nombre == nuevo_modelo and isinstance(m, dict):
                        m["valor_fijo"] = int(nuevo_valor_fijo)
                        break
                self.guardarModelos(modelos)
                self.guardarCamiones(camiones)
                messagebox.showinfo("Éxito", "Camión editado correctamente.")
                self.mostrarMenuHorizontalCamiones()
            else:
                messagebox.showerror("Error", "No se encontró el camión para editar.")

        Button(contenedorFormulario, text="Guardar", command=guardarCamion).grid(row=4, column=0, columnspan=2, pady=15)
        Button(contenedorFormulario, text="Volver", command=self.mostrarMenuHorizontalCamiones).grid(row=5, column=0, columnspan=2, pady=15)

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
                        if not any(c.get("idCamion") == nuevoId for c in camiones):
                            c["idCamion"] = nuevoId
                            c["Patente"] = Patente
                            c["Marca"] = marca
                            c["Modelo"] = modelo
                            c["Ingreso"] = datetime.now().strftime("%Y-%m-%d")
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
                    if not any(c.get("idCamion") == posibleId for c in camiones):
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
                    # Fecha en formato chileno dd-mm-yyyy
                    "Ingreso": datetime.now().strftime("%d-%m-%Y"),
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
               font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

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
               font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

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
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Eliminar marca", command=self.eliminarMarca, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Volver", command=self.mostrarMenuHorizontalCamiones, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

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

        # Solo letras y espacios, máximo 20 caracteres, sin dobles espacios, permite espacio al final para seguir escribiendo
        def solo_letras(valor):
            if not valor:
                return True
            if len(valor) > 20:
                return False
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            # Permite espacio al final mientras se escribe
            palabras = valor.strip().split()
            # Permite escribir mínimo 3 palabras, pero no menos al guardar
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=marca_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            marca = marca_var.get().strip().upper()
            letras = marca.replace(" ", "")
            if not marca or len(letras) < 3 or not letras.isalpha():
                messagebox.showerror("Error", "La marca debe tener al menos 3 letras, solo letras y espacios.")
                return

            marcas = [m.upper() for m in self.cargarMarcas()]
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

        # Verifica si hay camiones con esa marca
        camiones = self.cargarCamiones()
        if any(c.get("Marca", "").upper() == marca.upper() for c in camiones):
            messagebox.showwarning("Advertencia", f"No se puede eliminar la marca '{marca}' porque existen camiones asociados a ella.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar la marca '{marca}'?\nEsto también eliminará todos los modelos de esa marca.")
        if not confirmar:
            return
        # Elimina la marca del listado de marcas
        marcas = self.cargarMarcas()
        marcas = [m for m in marcas if m != marca]
        self.guardarMarcas(marcas)
        # Elimina los modelos asociados a esa marca
        modelos = self.cargarModelos()
        if marca in modelos:
            del modelos[marca]
            self.guardarModelos(modelos)
        messagebox.showinfo("Éxito", "Marca y modelos asociados eliminados correctamente.")
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

        # Validación: Solo letras y espacios, máximo 20 caracteres, sin dobles espacios
        def solo_letras(valor):
            if not valor:
                return True
            if len(valor) > 20:
                return False
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            palabras = valor.strip().split()
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)

        vcmd = (top.register(solo_letras), '%P')
        Entry(top, textvariable=marca_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)

        def guardar():
            nueva_marca = marca_var.get().strip().upper()
            if not nueva_marca or len(nueva_marca.replace(" ", "")) < 3:
                messagebox.showerror("Error", "La marca debe tener al menos 3 letras.")
                return

            marcas = self.cargarMarcas()
            if nueva_marca in marcas:
                messagebox.showerror("Error", "La marca ya existe.")
                return

            # Actualiza la marca en los modelos
            modelos = self.cargarModelos()
            if marca_actual in modelos:
                modelos[nueva_marca] = modelos.pop(marca_actual)
                self.guardarModelos(modelos)

            # Actualiza la marca en los camiones asociados
            camiones = self.cargarCamiones()
            for camion in camiones:
                if camion.get("Marca", "").upper() == marca_actual.upper():
                    camion["Marca"] = nueva_marca
            self.guardarCamiones(camiones)

            # Actualiza la lista de marcas
            marcas = [m if m != marca_actual else nueva_marca for m in marcas]
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
            font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedorListaModelos = Frame(self.root)
        self.contenedorListaModelos.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Marca", "Modelo", "Valor diario")
        self.treeModelos = ttk.Treeview(self.contenedorListaModelos, columns=columnas, show='headings')
        for col in columnas:
            self.treeModelos.heading(col, text=col)
            self.treeModelos.column(col, width=150, anchor='center')
        self.treeModelos.pack(fill=BOTH, expand=True)

        # Cargar y mostrar modelos
        modelos = self.cargarModelos()
        for marca, lista_modelos in modelos.items():
            for modelo in lista_modelos:
                if isinstance(modelo, dict):
                    self.treeModelos.insert('', 'end', values=(marca, modelo.get("nombre", ""), modelo.get("valor_fijo", "")))
                else:
                    self.treeModelos.insert('', 'end', values=(marca, modelo, ""))

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

        # Solo muestra el botón "Agregar marca" si NO hay marcas existentes
        if not marcas:
            def agregar_marca():
                def solo_letras(valor):
                    if len(valor) > 20:
                        return False
                    if valor == "":
                        return True
                    if not all(c.isalpha() or c == " " for c in valor):  # Solo letras y espacios
                        return False
                    if valor[0] == " " or valor[-1] == " ":
                        return False
                    if "  " in valor:
                        return False
                    return True

                def guardar_marca():
                    nueva_marca = nueva_marca_var.get().strip().upper()
                    letras = nueva_marca.replace(" ", "")
                    if not nueva_marca or len(letras) < 3 or not letras.isalpha():
                        messagebox.showerror("Error", "La marca debe tener al menos 3 letras, solo letras y espacios.")
                        return
                    marcas_actuales = [m.upper() for m in self.cargarMarcas()]
                    if nueva_marca in marcas_actuales:
                        messagebox.showerror("Error", "La marca ya existe.")
                        return
                    marcas_actuales.append(nueva_marca)
                    self.guardarMarcas(marcas_actuales)
                    marca_combo['values'] = marcas_actuales
                    marca_var.set(nueva_marca)
                    top_marca.destroy()
                    messagebox.showinfo("Éxito", "Marca agregada correctamente.")

                top_marca = Toplevel(top)
                top_marca.title("Agregar Marca")
                Label(top_marca, text="Nueva marca:").pack(padx=10, pady=10)
                nueva_marca_var = StringVar()
                vcmd = (top_marca.register(solo_letras), '%P')
                Entry(top_marca, textvariable=nueva_marca_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=10)
                Button(top_marca, text="Guardar", command=guardar_marca).pack(pady=10)
            Button(top, text="Agregar marca", command=agregar_marca).pack(padx=10, pady=5)

        Label(top, text="Modelo:").pack(padx=10, pady=5)
        modelo_var = StringVar()

        def solo_modelo(valor):
            if len(valor) > 20:
                return False
            if valor == "":
                return True
            if not all(c.isalnum() or c == " " for c in valor):
                return False
            if valor[0] == " " or valor[-1] == " ":
                return False
            if "  " in valor:
                return False
            return True

        vcmd = (top.register(solo_modelo), '%P')
        Entry(top, textvariable=modelo_var, validate='key', validatecommand=vcmd).pack(padx=10, pady=5)

        # Valor fijo: solo números, sin espacios ni caracteres especiales, mínimo 10000
        Label(top, text="Valor diario:").pack(padx=10, pady=5)
        valor_fijo_var = StringVar()
        def solo_numeros(valor):
            if not valor:
                return True
            if not valor.isdigit() or " " in valor:
                return False
            return True
        vcmd_valor_fijo = (top.register(solo_numeros), '%P')
        Entry(top, textvariable=valor_fijo_var, validate='key', validatecommand=vcmd_valor_fijo).pack(padx=10, pady=5)

        def guardar():
            marca = marca_var.get().strip()
            modelo = modelo_var.get().strip().upper()
            valor_fijo = valor_fijo_var.get().strip()
            if not marca or not modelo or not valor_fijo:
                messagebox.showerror("Error", "Debe completar todos los campos.")
                return
            if "  " in modelo:
                messagebox.showerror("Error", "El modelo no puede contener doble espacios.")
                return
            if not valor_fijo.isdigit() or int(valor_fijo) < 10000:
                messagebox.showerror("Error", "El valor diario debe ser un número mayor o igual a $10000.")
                return
            modelos = self.cargarModelos()
            if marca not in modelos:
                modelos[marca] = []
            # Verifica que no exista el modelo con ese nombre para esa marca
            if any(isinstance(m, dict) and m.get("nombre", "").upper() == modelo for m in modelos[marca]):
                messagebox.showerror("Error", "Ese modelo ya existe para la marca seleccionada.")
                return
            # Guarda modelo y valor fijo juntos (como dict)
            modelos[marca].append({"nombre": modelo, "valor_fijo": int(valor_fijo)})
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
        marca, modelo, valor_fijo = self.treeModelos.item(item, "values")  ################################################

        # Verifica si hay camiones con esa marca y modelo
        camiones = self.cargarCamiones()
        if any(
            c.get("Marca", "").upper() == marca.upper() and c.get("Modelo", "").upper() == modelo.upper()
            for c in camiones
        ):
            messagebox.showwarning("Advertencia", f"No se puede eliminar el modelo '{modelo}' de la marca '{marca}' porque existen camiones asociados.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro que desea eliminar el modelo '{modelo}' de la marca '{marca}'?"
        )
        if not confirmar:
            return

        modelos = self.cargarModelos()
        # Elimina el modelo dict por nombre (y valor fijo si lo deseas)
        if marca in modelos:
            modelos[marca] = [
                m for m in modelos[marca]
                if not (isinstance(m, dict) and m.get("nombre", "") == modelo)
            ]
            # Si no quedan modelos, elimina la marca
            if not modelos[marca]:
                del modelos[marca]
            self.guardarModelos(modelos)
            messagebox.showinfo("Éxito", "Modelo eliminado correctamente.")
            self.mostrarCrudModelos()

    def formularioEditarModelo(self):
        seleccion = self.treeModelos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un modelo para editar.")
            return
        item = seleccion[0]
        marca_actual, modelo_actual, valor_fijo_actual = self.treeModelos.item(item, "values")

        top = Toplevel(self.root)
        top.title("Editar Modelo")
        Label(top, text="Marca:").pack(padx=10, pady=5)
        Label(top, text=marca_actual).pack(padx=10, pady=5)
        Label(top, text="Nuevo modelo:").pack(padx=10, pady=5)

        modelo_var = StringVar(value=modelo_actual)
        valor_fijo_var = StringVar(value=valor_fijo_actual)

        def solo_modelo(valor):
            if len(valor) > 20:
                return False
            if valor == "":
                return True
            if not all(c.isalnum() or c == " " for c in valor):
                return False
            if valor[0] == " " or valor[-1] == " ":
                return False
            if "  " in valor:
                return False
            return True

        def solo_numeros(valor):
            if not valor:
                return True
            if not valor.isdigit() or " " in valor:
                return False
            return True

        vcmd_modelo = (top.register(solo_modelo), '%P')
        Entry(top, textvariable=modelo_var, validate='key', validatecommand=vcmd_modelo).pack(padx=10, pady=5)

        Label(top, text="Valor diario:").pack(padx=10, pady=5)
        vcmd_valor_fijo = (top.register(solo_numeros), '%P')
        Entry(top, textvariable=valor_fijo_var, validate='key', validatecommand=vcmd_valor_fijo).pack(padx=10, pady=5)

        def guardar():
            nuevo_modelo = modelo_var.get().strip().upper()
            nuevo_valor_fijo = valor_fijo_var.get().strip()
            if not nuevo_modelo or not nuevo_valor_fijo:
                messagebox.showerror("Error", "Debe completar todos los campos.")
                return
            if "  " in nuevo_modelo:
                messagebox.showerror("Error", "El modelo no puede contener doble espacios.")
                return
            if not nuevo_valor_fijo.isdigit() or int(nuevo_valor_fijo) < 10000:
                messagebox.showerror("Error", "El valor diario debe ser un número mayor o igual a $10000.")
                return

            modelos = self.cargarModelos()
            # Verifica que no exista el modelo con ese nombre para esa marca (excepto el actual)
            if any(isinstance(m, dict) and m.get("nombre", "").upper() == nuevo_modelo and m.get("nombre", "") != modelo_actual for m in modelos.get(marca_actual, [])):
                messagebox.showerror("Error", "Ese modelo ya existe para la marca seleccionada.")
                return

            # Actualiza el modelo y valor fijo
            for idx, m in enumerate(modelos.get(marca_actual, [])):
                if isinstance(m, dict) and m.get("nombre", "") == modelo_actual:
                    modelos[marca_actual][idx] = {"nombre": nuevo_modelo, "valor_fijo": int(nuevo_valor_fijo)}
                    break
                elif m == modelo_actual:
                    modelos[marca_actual][idx] = {"nombre": nuevo_modelo, "valor_fijo": int(nuevo_valor_fijo)}
                    break

            self.guardarModelos(modelos)

            # Actualiza el modelo en los camiones asociados
            camiones = self.cargarCamiones()
            for camion in camiones:
                if camion.get("Marca", "").upper() == marca_actual.upper() and camion.get("Modelo", "").upper() == modelo_actual.upper():
                    camion["Modelo"] = nuevo_modelo
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
            font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedorListaTipos = Frame(self.root)
        self.contenedorListaTipos.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Tipo de arriendo", "Valor diario")
        self.treeTipos = ttk.Treeview(self.contenedorListaTipos, columns=columnas, show='headings')
        self.treeTipos.heading("Tipo de arriendo", text="Tipo de arriendo")
        self.treeTipos.heading("Valor diario", text="Valor diario")
        self.treeTipos.column("Tipo de arriendo", width=200, anchor='center')
        self.treeTipos.column("Valor diario", width=120, anchor='center')
        self.treeTipos.pack(fill=BOTH, expand=True)

        # Cargar y mostrar tipos
        tipos = self.cargarTiposArriendo()
        for tipo in tipos:
            # Si tipo es dict, muestra ambos valores
            if isinstance(tipo, dict):
                self.treeTipos.insert('', 'end', values=(tipo.get("tipo", ""), tipo.get("valor_diario", "")))

    def formularioAgregarTipoArriendo(self):
        top = Toplevel(self.root)
        top.title("Agregar Tipo de Arriendo")
        Label(top, text="Tipo de arriendo:").pack(padx=10, pady=10)
        tipo_var = StringVar()

        # Solo letras y espacios, máximo 20 caracteres, sin dobles espacios, permite espacio al final para seguir escribiendo
        def solo_letras(valor):
            if not valor:
                return True
            if len(valor) > 20:
                return False
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            # Permite espacio al final mientras se escribe
            palabras = valor.strip().split()
            # Permite escribir hasta 3 palabras, pero no menos al guardar
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)

        vcmd_tipo = (top.register(solo_letras), '%P')
        Entry(top, textvariable=tipo_var, validate='key', validatecommand=vcmd_tipo).pack(padx=10, pady=10)

        # Valor diario: solo números, sin espacios ni caracteres especiales
        Label(top, text="Valor diario:").pack(padx=10, pady=5)
        valor_var = StringVar()
        def solo_numeros(valor):
            if not valor:
                return True
            if not valor.isdigit() or " " in valor:
                return False
            return True
        vcmd_valor = (top.register(solo_numeros), '%P')
        Entry(top, textvariable=valor_var, validate='key', validatecommand=vcmd_valor).pack(padx=10, pady=5)

        def guardar():
            tipo = tipo_var.get().strip().capitalize()
            valor = valor_var.get().strip()
            # Validaciones
            if not tipo:
                messagebox.showerror("Error", "Ingrese un tipo de arriendo.")
                return
            if not tipo.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Solo se permiten letras y espacios.")
                return
            if len(tipo) > 20:
                messagebox.showerror("Error", "Máximo 20 caracteres.")
                return
            if not valor:
                messagebox.showerror("Error", "Ingrese el valor diario.")
                return
            if not valor.isdigit() or int(valor) < 10000:
                messagebox.showerror("Error", "El valor diario debe ser un número mayor o igual a $10000.")
                return

            tipos = self.cargarTiposArriendo()
            # Filtro para no guardar con el mismo nombre, independiente del valor
            if any(isinstance(t, dict) and t.get("tipo", "").strip().lower() == tipo.lower() for t in tipos):
                messagebox.showerror("Error", "Ya existe un tipo de arriendo con ese nombre.")
                return

            tipos.append({"tipo": tipo, "valor_diario": int(valor)})
            self.guardarTiposArriendo(tipos)
            messagebox.showinfo("Éxito", "Tipo de arriendo agregado correctamente.")
            top.destroy()
            self.mostrarCrudTipoArriendo()
        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def formularioEditarTipoArriendo(self):
        seleccion = self.treeTipos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un tipo de arriendo para editar.")
            return
        item = seleccion[0]
        tipo_actual = self.treeTipos.item(item, "values")[0]
        valor_actual = self.treeTipos.item(item, "values")[1]

        top = Toplevel(self.root)
        top.title("Editar Tipo de Arriendo")
        Label(top, text="Nuevo tipo:").pack(padx=10, pady=10)
        tipo_var = StringVar(value=tipo_actual)

        # Validación: Solo letras y espacios, máximo 20 caracteres, sin dobles espacios
        def solo_letras(valor):
            if not valor:
                return True
            if len(valor) > 20:
                return False
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            palabras = valor.strip().split()
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)

        vcmd_tipo = (top.register(solo_letras), '%P')
        Entry(top, textvariable=tipo_var, validate='key', validatecommand=vcmd_tipo).pack(padx=10, pady=10)

        # Valor diario: solo números, sin espacios ni caracteres especiales
        Label(top, text="Valor diario:").pack(padx=10, pady=5)
        valor_var = StringVar(value=valor_actual)

        def solo_numeros(valor):
            if not valor:
                return True
            if not valor.isdigit() or " " in valor:
                return False
            return True

        vcmd_valor = (top.register(solo_numeros), '%P')
        Entry(top, textvariable=valor_var, validate='key', validatecommand=vcmd_valor).pack(padx=10, pady=5)

        def guardar():
            nuevo_tipo = tipo_var.get().strip()
            nuevo_valor = valor_var.get().strip()

            if not nuevo_tipo:
                messagebox.showerror("Error", "Ingrese un tipo de arriendo.")
                return
            if not nuevo_tipo.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Solo se permiten letras y espacios.")
                return
            if len(nuevo_tipo) > 20:
                messagebox.showerror("Error", "Máximo 20 caracteres.")
                return
            if not nuevo_valor:
                messagebox.showerror("Error", "Ingrese el valor diario.")
                return
            if not nuevo_valor.isdigit() or int(nuevo_valor) < 10000:
                messagebox.showerror("Error", "El valor diario debe ser mayor o igual a $10000.")
                return

            tipos = self.cargarTiposArriendo()
            # Verifica que no exista el tipo con ese nombre (excepto el actual)
            if any(isinstance(t, dict) and t.get("tipo", "").strip().lower() == nuevo_tipo.lower() and t.get("tipo", "") != tipo_actual for t in tipos):
                messagebox.showerror("Error", "Ya existe un tipo de arriendo con ese nombre.")
                return

            # Actualiza el tipo y valor
            for t in tipos:
                if isinstance(t, dict) and t.get("tipo", "") == tipo_actual:
                    t["tipo"] = nuevo_tipo
                    t["valor_diario"] = int(nuevo_valor)
                    break

            self.guardarTiposArriendo(tipos)

            # Actualiza el tipo de arriendo en los camiones disponibles
            camiones = self.cargarCamiones()
            for camion in camiones:
                if camion.get("TipoArriendo", "").lower() == tipo_actual.lower() and camion.get("Disponible", "").lower() == "si":
                    camion["TipoArriendo"] = nuevo_tipo
                    camion["ValorDiario"] = int(nuevo_valor)

            # Programa la actualización para camiones no disponibles
            for camion in camiones:
                if camion.get("TipoArriendo", "").lower() == tipo_actual.lower() and camion.get("Disponible", "").lower() != "si":
                    camion["TipoArriendoPendiente"] = nuevo_tipo
                    camion["ValorDiarioPendiente"] = int(nuevo_valor)

            self.guardarCamiones(camiones)

            messagebox.showinfo("Éxito", "Tipo de arriendo editado correctamente. Los cambios se aplicarán automáticamente a los camiones no disponibles cuando estén disponibles.")
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
        # Filtra correctamente si tipo es dict
        tipos = [t for t in tipos if not (isinstance(t, dict) and t.get("tipo", "") == tipo)]
        self.guardarTiposArriendo(tipos)
        messagebox.showinfo("Éxito", "Tipo de arriendo eliminado correctamente.")
        self.mostrarCrudTipoArriendo()

    def cargarTiposArriendo(self):
        import os
        if not os.path.exists('tipos_arriendo.json'):
            return []
        with open('tipos_arriendo.json', 'r') as file:
            return json.load(file)

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

        # Obtiene el RUT del cliente seleccionado (columna 0)
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

    def cargarTiposArriendo(self):
        if not os.path.exists('tipos_arriendo.json'):
            return []
        with open('tipos_arriendo.json', 'r') as file:
            return json.load(file)

    def cargarModelos(self):
        if not os.path.exists('modelos.json'):
            return {}
        with open('modelos.json', 'r') as file:
            return json.load(file)

    def enviarCotizacion(self):
        camiones_seleccionados = []
        for item in self.treeCarrito.get_children():
            valores = self.treeCarrito.item(item, "values")
            camiones_seleccionados.append({
                "Patente": valores[0],
                "Marca": valores[1],
                "Modelo": valores[2],
                "Valor fijo": valores[3],
                "Tipo de arriendo": valores[6],
                "Fecha de arriendo": valores[4],
                "Fecha de término": valores[5]
            })

        if not camiones_seleccionados:
            messagebox.showwarning("Advertencia", "No hay camiones en el carrito.")
            return

        # Generar un ID único para la cotización
        letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        if not os.path.exists("cotizaciones.json"):
            cotizaciones = []
        else:
            with open("cotizaciones.json", "r") as file:
                cotizaciones = json.load(file)

        ids_existentes = [cotizacion.get("ID") for cotizacion in cotizaciones]
        nuevo_id = None
        for letra in letras:
            for i in range(1, 4):  # Limita a 3 cotizaciones por letra
                posible_id = f"{i}{letra}"
                if posible_id not in ids_existentes:
                    nuevo_id = posible_id
                    break
            if nuevo_id:
                break

        if not nuevo_id:
            messagebox.showerror("Error", "No se pudo generar un ID único para la cotización.")
            return

        # Crear la cotización
        cotizacion = {
            "ID": nuevo_id,
            "Usuario": self.nombreUsuarioSesionActual,
            "Camiones": camiones_seleccionados,
            "Estado": "Pendiente",
            "Fecha de creación": datetime.now().strftime("%d-%m-%Y")  # Formato chileno
        }

        # Guardar cotización en cotizaciones.json
        cotizaciones.append(cotizacion)

        with open("cotizaciones.json", "w") as file:
            json.dump(cotizaciones, file, indent=4)

        messagebox.showinfo("Éxito", f"Cotización enviada correctamente con ID: {nuevo_id}.")

    def menuInicial(self):
        self.limpiarWidgets()

        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        botones = [
            ("Editar perfil", self.editarPerfil),
            ("Carrito", self.mostrarCarrito)
        ]

        for texto, comando in botones:
            Button(self.barraHorizontal, text=texto, command=comando, bg="white", fg="black",
                font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        self.contenedorMenu = Frame(self.root)
        self.contenedorMenu.pack(expand=True)

        Button(self.barraHorizontal, text="Cerrar sesión", command=self.salir, font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)
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
        cuerpo = rut[:-1]
        dv = rut[-1]

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
            messagebox.showerror("Error", f"El RUT ingresado no es válido.")
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
        nombre = nombreCompleto.strip()  # Elimina espacios al inicio y al final
        telefono = telefono.replace(" ", "") 

        def esNumeroSimple(numero):
            # Asegura que el número tenga exactamente 9 dígitos y empiece con 9
            if len(numero) != 9 or not numero.startswith("9") or not numero.isdigit():
                return True  # Lo dejamos pasar a otras validaciones

            cuerpo = numero[1:]

            # Secuencia repetida
            if len(set(cuerpo)) == 1:
                return True

            # Secuencia ascendente
            if cuerpo == ''.join(str(i) for i in range(int(cuerpo[0]), int(cuerpo[0]) + len(cuerpo)) if int(cuerpo[0]) + len(cuerpo) <= 10):
                return True

            # Secuencia descendente
            if cuerpo == ''.join(str(i) for i in range(int(cuerpo[0]), int(cuerpo[0]) - len(cuerpo), -1) if int(cuerpo[0]) - len(cuerpo) >= -1):
                return True

            return False

        # Teléfono: 9 dígitos, solo números
        if not telefono.isdigit() or len(telefono) != 9:
            messagebox.showerror("Error", "El teléfono debe tener 9 dígitos.")
            return
        if len(set(telefono)) == 1:
            messagebox.showerror("Error", "El teléfono no puede tener todos los dígitos iguales.")
            return
        if telefono in ["123456789", "987654321"]:
            messagebox.showerror("Error", "El teléfono no puede ser una secuencia simple.")
            return
        if not telefono.startswith("9"):
            messagebox.showerror("Error", "El teléfono debe comenzar con 9.")
            return
        if telefono[1:] == "00000000":
            messagebox.showerror("Error", "El teléfono no puede ser 9 seguido de puros ceros.")
            return
        #############################
        if esNumeroSimple(telefono):
            messagebox.showerror("Error", "El teléfono no puede contener una secuencia simple después del 9.")
            return

        # Validación para correo
        if len(correo) < 14 or len(correo) > 31:
            messagebox.showerror("Error", "El correo debe tener entre 14 y 30 caracteres, incluyendo '@gmail.com'.")
            return

        patron = r'^[\w\.-]+@gmail\.com$'
        if not re.match(patron, correo):
            messagebox.showerror("Error", "El correo debe tener formato Gmail.")
            return

        # Dirección: mínimo 5 caracteres
        if len(direccion) < 5:
            messagebox.showerror("Error", "Ingrese la dirección completa (mínimo 5 caracteres).")
            return

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
            Label(contenedorFormulario, text="RUT:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
            Entry(contenedorFormulario, textvariable=self.rut, validate='key', validatecommand=vcmd).grid(row=0, column=1, pady=5)

        Label(contenedorFormulario, text="Nombre completo:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        def ValidarNombreUsuario(valor):
            if not valor:
                return True
            if any(c.isdigit() for c in valor):
                return False
            if "  " in valor:
                return False
            # Permite espacio al final mientras se escribe
            palabras = valor.strip().split()
            if len(palabras) > 3:
                return False
            return all(p.isalpha() for p in palabras)
        vcmd_nombre_usuario = (self.root.register(ValidarNombreUsuario), '%P')

        Entry(contenedorFormulario, textvariable=self.nombreCompleto, validate='key', validatecommand=vcmd_nombre_usuario).grid(column=1, row=1, pady=5)

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
        usuarios = self.cargarUsuarios()
        
        for usuario in usuarios:
            if usuario.get("nombre") == self.nombreUsuarioSesionActual:
                if usuario.get("Nombre Completo") == "":
                    messagebox.showerror("Error", "Debe completar su perfil antes de acceder al carrito.")
                    self.menuInicial()
                    return False

        self.limpiarWidgets()
        self.barraHorizontal = Frame(self.root, bg="orange", height=50)
        self.barraHorizontal.pack(side=TOP, fill=X)

        Button(self.barraHorizontal, text="Agregar", command=self.formularioAgregarCamionCarrito, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Editar", command=self.editarCamionCarrito, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)
        Button(self.barraHorizontal, text="Eliminar", command=self.eliminarCamionCarrito, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        Button(self.barraHorizontal, text="Enviar cotización", command=self.enviarCotizacion, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=LEFT, padx=10, pady=10)

        Button(self.barraHorizontal, text="Volver", command=self.menuInicial, bg="white", fg="black",
            font=("Montserrat", 12)).pack(side=RIGHT, padx=10, pady=10)

        self.contenedorCarrito = Frame(self.root)
        self.contenedorCarrito.pack(fill=BOTH, expand=True, padx=20, pady=20)

        columnas = ("Patente", "Marca", "Modelo", "Valor fijo", "Fecha de ingreso", "Disponible", "Tipo de arriendo", "Valor diario arriendo", "Total")
        self.treeCarrito = ttk.Treeview(self.contenedorCarrito, columns=columnas, show='headings')

        for col in columnas:
            self.treeCarrito.heading(col, text=col)
            self.treeCarrito.column(col, width=120, anchor='center')

        self.treeCarrito.pack(fill=BOTH, expand=True)

        camiones = self.cargarCamiones()
        tipos_arriendo = self.cargarTiposArriendo()
        for c in camiones:
            # Filtrar camiones arrendados por el usuario actual
            if c.get("ArrendadoPor", "") == self.nombreUsuarioSesionActual:
                tipo_arriendo = c.get("TipoArriendo", "")
                valor_diario = next((t.get("valor_diario", 0) for t in tipos_arriendo if t.get("tipo", "") == tipo_arriendo), 0)

                # Obtener el valor fijo del modelo
                marca = c.get("Marca", "")
                modelo = c.get("Modelo", "")
                modelos_dict = self.cargarModelos()
                modelos = modelos_dict.get(marca, [])  # Obtener los modelos de la marca correspondiente

                # Buscar el valor fijo del modelo
                valor_fijo = next((m.get("valor_fijo", 0) for m in modelos if m.get("nombre", "") == modelo), 0)

                # Formatear el valor fijo
                try:
                    valor_fijo_num = int(valor_fijo)
                    valor_fijo_str = f"${valor_fijo_num:,}"
                except (ValueError, TypeError):
                    valor_fijo_str = "$0"

                # Calcular el total
                try:
                    fecha_arriendo = datetime.strptime(c.get("FechaArriendo", ""), "%d-%m-%Y")
                    fecha_termino = datetime.strptime(c.get("FechaTermino", ""), "%d-%m-%Y")
                    dias_arriendo = (fecha_termino - fecha_arriendo).days
                    total = (valor_fijo_num + valor_diario) * dias_arriendo
                    total_str = f"${total:,}"
                except Exception:
                    total_str = "$0"

                self.treeCarrito.insert('', 'end', values=(
                    c.get("Patente", ""),
                    c.get("Marca", ""),
                    c.get("Modelo", ""),
                    valor_fijo_str,
                    c.get("Ingreso", ""),
                    c.get("Disponible", ""),
                    tipo_arriendo,
                    f"${valor_diario:,}",
                    total_str
                ))

        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def formularioAgregarCamionCarrito(self):
        self.limpiarWidgets()
        contenedorFormulario = Frame(self.root, bg="orange")
        contenedorFormulario.pack(padx=20, pady=20)

        # Cargar camiones disponibles
        camiones = self.cargarCamiones()
        camiones_disponibles = [c for c in camiones if c.get("Disponible", "") == "Si"]
        patentes = [c["Patente"] for c in camiones_disponibles]

        Label(contenedorFormulario, text="Patente de camión:", bg="orange").grid(row=0, column=0, sticky=E, pady=5)
        patente_var = StringVar()
        patente_combo = Combobox(contenedorFormulario, textvariable=patente_var, values=patentes, state="readonly")
        patente_combo.grid(row=0, column=1, pady=5)
        if patentes:
            patente_combo.current(0)

        # Mostrar marca, modelo y valor fijo del camión
        marca_var = StringVar()
        modelo_var = StringVar()
        valor_fijo_var = StringVar()
        Label(contenedorFormulario, text="Marca:", bg="orange").grid(row=1, column=0, sticky=E, pady=5)
        Label(contenedorFormulario, textvariable=marca_var, bg="orange").grid(row=1, column=1, pady=5)
        Label(contenedorFormulario, text="Modelo:", bg="orange").grid(row=2, column=0, sticky=E, pady=5)
        Label(contenedorFormulario, textvariable=modelo_var, bg="orange").grid(row=2, column=1, pady=5)
        Label(contenedorFormulario, text="Valor diario:", bg="orange").grid(row=3, column=0, sticky=E, pady=5)
        Label(contenedorFormulario, textvariable=valor_fijo_var, bg="orange").grid(row=3, column=1, pady=5)

        def actualizar_marca_modelo(*args):
            modelos_dict = self.cargarModelos()
            patente = patente_var.get()
            for c in camiones_disponibles:
                if c["Patente"] == patente:
                    marca = c.get("Marca", "")
                    modelo = c.get("Modelo", "")
                    marca_var.set(marca)
                    modelo_var.set(modelo)
                    valor_fijo = c.get("valor_fijo")
                    if valor_fijo is None or valor_fijo == "":
                        modelos = modelos_dict.get(marca, [])
                        for m in modelos:
                            nombre = m["nombre"] if isinstance(m, dict) else m
                            if nombre == modelo and isinstance(m, dict):
                                valor_fijo = m.get('valor_fijo', 0)
                                break
                    valor_fijo_str = f"${valor_fijo:,}" if valor_fijo else ""
                    valor_fijo_var.set(valor_fijo_str)
                    break
            else:
                marca_var.set("")
                modelo_var.set("")
                valor_fijo_var.set("")

        patente_var.trace('w', actualizar_marca_modelo)
        if patentes:
            actualizar_marca_modelo()

        # Selección de tipo de arriendo
        tipos = self.cargarTiposArriendo()
        tipos_opciones = [
            f'{t["tipo"]}, ${t["valor_diario"]:,}' for t in tipos if isinstance(t, dict)
        ]
        Label(contenedorFormulario, text="Tipo de arriendo:", bg="orange").grid(row=4, column=0, sticky=E, pady=5)
        tipo_var = StringVar()
        tipo_combo = Combobox(contenedorFormulario, textvariable=tipo_var, values=tipos_opciones, state="readonly")
        tipo_combo.grid(row=4, column=1, pady=5)
        if tipos_opciones:
            tipo_combo.current(0)

        # Fecha de arriendo
        Label(contenedorFormulario, text="Fecha de arriendo:", bg="orange").grid(row=5, column=0, sticky=E, pady=5)
        fecha_arriendo_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            mindate=datetime.now() + timedelta(days=2),  # Desde el día siguiente
            maxdate=datetime.now() + timedelta(days=330)  # Hasta el próximo año
        )
        fecha_arriendo_entry.grid(row=5, column=1, pady=5)

        # Fecha de término
        Label(contenedorFormulario, text="Fecha de término:", bg="orange").grid(row=6, column=0, sticky=E, pady=5)
        fecha_termino_entry = DateEntry(
            contenedorFormulario,
            date_pattern='dd/MM/yyyy',
            locale='es_CL',
            mindate=datetime.now() + timedelta(days=3),  # Mínimo un día después de la fecha de arriendo
            maxdate=datetime.now() + timedelta(days=365)  # Hasta el próximo año
        )
        fecha_termino_entry.grid(row=6, column=1, pady=5)

        def calcular_total(*args):
            try:
                # Obtener el valor del modelo del camión
                valor_fijo = int(valor_fijo_var.get().replace("$", "").replace(",", ""))
                
                # Obtener el valor diario del tipo de arriendo
                tipo_arriendo_str = tipo_var.get()
                valor_diario_arriendo = int(tipo_arriendo_str.split(", $")[1].replace(",", ""))
                
                # Calcular la cantidad de días de arriendo
                fecha_arriendo = fecha_arriendo_entry.get_date()
                fecha_termino = fecha_termino_entry.get_date()
                dias_arriendo = (fecha_termino - fecha_arriendo).days
                
                # Calcular el total
                total = (valor_fijo + valor_diario_arriendo) * dias_arriendo
                total_var.set(f"${total:,}")
            except Exception:
                total_var.set("$0")
        
        # Total calculado
        total_var = StringVar()
        Label(contenedorFormulario, text="Total:", bg="orange").grid(row=7, column=0, sticky=E, pady=5)
        Label(contenedorFormulario, textvariable=total_var, bg="orange").grid(row=7, column=1, pady=5)

        tipo_var.trace('w', calcular_total)
        fecha_arriendo_entry.bind("<<DateEntrySelected>>", calcular_total)
        fecha_termino_entry.bind("<<DateEntrySelected>>", calcular_total)

        def guardar():
            patente = patente_var.get()
            tipo_arriendo_str = tipo_var.get()
            fecha_arriendo = fecha_arriendo_entry.get_date()
            fecha_termino = fecha_termino_entry.get_date()

            if not patente or not tipo_arriendo_str:
                messagebox.showerror("Error", "Debe seleccionar camión y tipo de arriendo.")
                return

            tipo_arriendo = tipo_arriendo_str.split(",")[0].strip()

            # Verificar conflictos de fechas
            camiones = self.cargarCamiones()
            for c in camiones:
                if c.get("Patente") == patente:
                    fecha_arriendo_existente = datetime.strptime(c.get("FechaArriendo", ""), "%d-%m-%Y").date() if c.get("FechaArriendo") else None
                    fecha_termino_existente = datetime.strptime(c.get("FechaTermino", ""), "%d-%m-%Y").date() if c.get("FechaTermino") else None

                    if fecha_arriendo_existente and fecha_termino_existente:
                        if not (fecha_termino < fecha_arriendo_existente or fecha_arriendo > fecha_termino_existente):
                            messagebox.showerror("Error", f"El camión con patente {patente} ya está arrendado en el periodo seleccionado.")
                            return

                    # Mantener disponible hasta dos días antes de la fecha de arriendo
                    if fecha_arriendo - timedelta(days=2) > datetime.now().date():
                        c["Disponible"] = "Si"
                    else:
                        c["Disponible"] = "En arriendo"

                    c["TipoArriendo"] = tipo_arriendo
                    c["ArrendadoPor"] = self.nombreUsuarioSesionActual
                    c["FechaArriendo"] = fecha_arriendo.strftime("%d-%m-%Y")
                    c["FechaTermino"] = fecha_termino.strftime("%d-%m-%Y")
                    self.guardarCamiones(camiones)
                    messagebox.showinfo("Éxito", f"Camión {patente} agregado al carrito.")
                    self.mostrarCarrito()
                    return

            messagebox.showerror("Error", "No se pudo agregar el camión al carrito.")

        Button(contenedorFormulario, text="Guardar", command=guardar).grid(row=8, column=0, columnspan=2, pady=5)
        Button(contenedorFormulario, text="Volver", command=self.mostrarCarrito).grid(row=8, column=1, columnspan=2, pady=5)

        # Fondo de la ventana
        self.imagen = PhotoImage(file="C:/Users/Crist/Documents/TransporteXpress/TransporteXpress/Imagenes/camionbg.png")
        imagenLabel = Label(self.root, image=self.imagen)
        imagenLabel.pack(side=LEFT, fill="both", expand=TRUE)

    def editarCamionCarrito(self):
        seleccion = self.treeCarrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para editar.")
            return
        item = seleccion[0]
        valores = self.treeCarrito.item(item, "values")
        patente = valores[0]

        camiones = self.cargarCamiones()
        camion = next((c for c in camiones if c.get("Patente") == patente and c.get("ArrendadoPor") == self.nombreUsuarioSesionActual), None)
        if not camion:
            messagebox.showerror("Error", "No se encontró el camión seleccionado.")
            return

        # Mostrar formulario para editar tipo de arriendo
        top = Toplevel(self.root)
        top.title("Editar tipo de arriendo")
        Label(top, text=f"Patente: {patente}").pack(padx=10, pady=10)

        tipos = self.cargarTiposArriendo()
        tipos_opciones = [
            f'{t["tipo"]}, ${t["valor_diario"]:,}' for t in tipos if isinstance(t, dict)
        ]

        tipo_actual = camion.get("TipoArriendo", "")
        tipo_actual_valor = next(
            (f'{t["tipo"]}, ${t["valor_diario"]:,}' for t in tipos if t.get("tipo") == tipo_actual),
            tipo_actual
        )

        tipo_var = StringVar(value=tipo_actual_valor)
        tipo_combo = Combobox(top, textvariable=tipo_var, values=tipos_opciones, state="readonly")
        tipo_combo.pack(padx=10, pady=10)

        if tipos_opciones and tipo_actual_valor in tipos_opciones:
            tipo_combo.set(tipo_actual_valor)
        elif tipos_opciones:
            tipo_combo.current(0)

        def guardar():
            nuevo_tipo_valor = tipo_var.get()
            if not nuevo_tipo_valor:
                messagebox.showerror("Error", "Debe seleccionar un tipo de arriendo.")
                return
            nuevo_tipo = nuevo_tipo_valor.split(",")[0].strip()
            camion["TipoArriendo"] = nuevo_tipo
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", "Tipo de arriendo actualizado.")
            top.destroy()
            self.mostrarCarrito()

        Button(top, text="Guardar", command=guardar).pack(pady=10)

    def eliminarCamionCarrito(self):
        seleccion = self.treeCarrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un camión para eliminar del carrito.")
            return
        item = seleccion[0]
        valores = self.treeCarrito.item(item, "values")
        patente = valores[0]

        # Confirmación antes de eliminar
        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el camión con patente {patente} del carrito?")
        if not confirmar:
            return

        camiones = self.cargarCamiones()
        encontrado = False
        for c in camiones:
            if c.get("Patente") == patente and c.get("ArrendadoPor") == self.nombreUsuarioSesionActual:
                c["Disponible"] = "Si"
                c["TipoArriendo"] = ""
                c["ArrendadoPor"] = ""
                encontrado = True
                break
        if encontrado:
            self.guardarCamiones(camiones)
            messagebox.showinfo("Éxito", f"Camión {patente} eliminado del carrito.")
            self.mostrarCarrito()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el camión del carrito.")

# Clase principal para ejecutar la aplicación
if __name__=="__main__":
    root = Tk()
    app = InicioSesionApp(root)
    root.mainloop()
