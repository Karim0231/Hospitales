import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import random

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect('hospitales.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    puede_modificar BOOLEAN DEFAULT 1
)
''')

try:
    cursor.execute('''
    INSERT INTO usuarios (username, password, puede_modificar) 
    VALUES (?, ?, ?)
    ''', ('admin', 'admin123', 1))
    conn.commit()
except sqlite3.IntegrityError:
    pass  # El usuario ya existe

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono1 TEXT,
    telefono2 TEXT,
    especialidad TEXT,
    hospital1 TEXT,
    consultorio1 TEXT,
    hospital2 TEXT,
    consultorio2 TEXT,
    hospital3 TEXT,
    consultorio3 TEXT
)
''')
conn.commit()

def mostrar_login():
    login_window = Toplevel(root)
    login_window.title("Iniciar sesión")
    login_window.geometry("300x170")
    
    Label(login_window, text="Usuario:").pack(pady=5)
    entry_usuario = Entry(login_window)
    entry_usuario.pack(pady=5)
    
    Label(login_window, text="Contraseña:").pack(pady=5)
    entry_password = Entry(login_window, show="*")
    entry_password.pack(pady=5)
    
    def verificar_credenciales():
        usuario = entry_usuario.get()
        password = entry_password.get()
        
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                      (usuario, password))
        if cursor.fetchone():
            login_window.destroy()
            root.deiconify()  # Mostrar la ventana principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    Button(login_window, text="Ingresar", command=verificar_credenciales).pack(pady=10)
    
    # Ocultar la ventana principal hasta que se loguee
    root.withdraw()

#cambiar usuario/contraseña
def cambiar_credenciales():
    config_window = Toplevel(root)
    config_window.title("Configurar credenciales")
    config_window.geometry("350x350")
    
    # Variable para controlar si es el usuario admin
    es_admin = False
    
    # Verificar si el usuario actual es admin
    cursor.execute('SELECT username FROM usuarios WHERE username = "admin"')
    if cursor.fetchone():
        es_admin = True
    
    if es_admin:
        Label(config_window, text="ADVERTENCIA: Está modificando la cuenta admin", 
              fg="red").pack(pady=5)
    
    Label(config_window, text="Usuario actual:").pack(pady=5)
    entry_usuario_actual = Entry(config_window)
    entry_usuario_actual.pack(pady=5)
    
    Label(config_window, text="Contraseña actual:").pack(pady=5)
    entry_password_actual = Entry(config_window, show="*")
    entry_password_actual.pack(pady=5)
    
    Label(config_window, text="Nuevo usuario:").pack(pady=5)
    entry_nuevo_usuario = Entry(config_window)
    entry_nuevo_usuario.pack(pady=5)
    
    Label(config_window, text="Nueva contraseña:").pack(pady=5)
    entry_nueva_password = Entry(config_window, show="*")
    entry_nueva_password.pack(pady=5)
    
    def actualizar_credenciales():
        usuario_actual = entry_usuario_actual.get()
        password_actual = entry_password_actual.get()
        nuevo_usuario = entry_nuevo_usuario.get()
        nueva_password = entry_nueva_password.get()
        
        if not usuario_actual or not password_actual:
            messagebox.showerror("Error", "Debe ingresar usuario y contraseña actual")
            return
            
        if not nuevo_usuario or not nueva_password:
            messagebox.showerror("Error", "Debe ingresar nuevo usuario y contraseña")
            return
            
        # Verificar credenciales actuales
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                      (usuario_actual, password_actual))
        usuario = cursor.fetchone()
        
        if usuario:
            try:
                # Eliminar el usuario antiguo
                cursor.execute('DELETE FROM usuarios WHERE username = ?', (usuario_actual,))
                
                # Insertar el nuevo usuario con las nuevas credenciales
                cursor.execute('''
                INSERT INTO usuarios (username, password, puede_modificar) 
                VALUES (?, ?, ?)
                ''', (nuevo_usuario, nueva_password, 1))
                
                conn.commit()
                messagebox.showinfo("Éxito", "Credenciales actualizadas correctamente.\n\n" +
                                  f"Usuario anterior: {usuario_actual}\n" +
                                  f"Nuevo usuario: {nuevo_usuario}")
                config_window.destroy()
                
                # Si era el admin, actualizar la variable
                if usuario_actual == "admin":
                    es_admin = False
                    
            except sqlite3.IntegrityError:
                conn.rollback()
                messagebox.showerror("Error", "El nombre de usuario ya existe")
        else:
            messagebox.showerror("Error", "Credenciales actuales incorrectas")
    
    Button(config_window, text="Actualizar", command=actualizar_credenciales).pack(pady=10)

# Función para agregar un registro
def agregar():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    telefono1 = entry_telefono1.get() or None
    telefono2 = entry_telefono2.get() or None
    especialidad = entry_especialidad.get() or None
    hospital1 = entry_hospital1.get() or None
    consultorio1 = entry_consultorio1.get() or None
    hospital2 = entry_hospital2.get() or None
    consultorio2 = entry_consultorio2.get() or None
    hospital3 = entry_hospital3.get() or None
    consultorio3 = entry_consultorio3.get() or None

    if nombre and apellido:  # Solo nombre y apellido son obligatorios
        cursor.execute('''
        INSERT INTO pacientes (nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3))
        conn.commit()
        messagebox.showinfo("Éxito", "Registro agregado correctamente")
        limpiar_campos()
        actualizar_lista()
    else:
        messagebox.showwarning("Error", "Nombre y Apellido son campos obligatorios")

# Función para actualizar un registro
def actualizar():
    seleccionado = treeview.selection()  # Obtener la fila seleccionada en el Treeview
    if seleccionado:
        # Obtener el ID del paciente desde la fila seleccionada
        id_paciente = treeview.item(seleccionado)['values'][0]  # El ID está en la primera columna
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        telefono1 = entry_telefono1.get() or None
        telefono2 = entry_telefono2.get() or None
        especialidad = entry_especialidad.get() or None
        hospital1 = entry_hospital1.get() or None
        consultorio1 = entry_consultorio1.get() or None
        hospital2 = entry_hospital2.get() or None
        consultorio2 = entry_consultorio2.get() or None
        hospital3 = entry_hospital3.get() or None
        consultorio3 = entry_consultorio3.get() or None

        if nombre and apellido:  # Solo nombre y apellido son obligatorios
            cursor.execute('''
            UPDATE pacientes
            SET nombre = ?, apellido = ?, telefono1 = ?, telefono2 = ?, especialidad = ?, hospital1 = ?, consultorio1 = ?, hospital2 = ?, consultorio2 = ?, hospital3 = ?, consultorio3 = ?
            WHERE id = ?
            ''', (nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3, id_paciente))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            limpiar_campos()
            actualizar_lista()
        else:
            messagebox.showwarning("Error", "Nombre y Apellido son campos obligatorios")
    else:
        messagebox.showwarning("Error", "Selecciona un registro para actualizar")

# Función para borrar un registro
def borrar():
    seleccionado = treeview.selection()  # Obtener la fila seleccionada en el Treeview
    if seleccionado:
        # Obtener el ID del paciente desde la fila seleccionada
        id_paciente = treeview.item(seleccionado)['values'][0]  # El ID está en la primera columna
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de borrar este registro?")
        if confirmar:
            cursor.execute('DELETE FROM pacientes WHERE id = ?', (id_paciente,))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro borrado correctamente")
            actualizar_lista()
    else:
        messagebox.showwarning("Error", "Selecciona un registro para borrar")

# Función para limpiar los campos de entrada
def limpiar_campos():
    entry_nombre.delete(0, END)
    entry_apellido.delete(0, END)
    entry_telefono1.delete(0, END)
    entry_telefono2.delete(0, END)
    entry_especialidad.delete(0, END)
    entry_hospital1.delete(0, END)
    entry_consultorio1.delete(0, END)
    entry_hospital2.delete(0, END)
    entry_consultorio2.delete(0, END)
    entry_hospital3.delete(0, END)
    entry_consultorio3.delete(0, END)

# Función para actualizar la lista de pacientes
def actualizar_lista():
    # Limpiar el Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Mostrar los datos de los pacientes
    cursor.execute('SELECT * FROM pacientes')
    for row in cursor.fetchall():
        # Extraer los datos de la fila
        datos = (
            row[0],  # ID
            row[1],  # Nombre
            row[2],  # Apellido
            row[3] if row[3] else "",  # Teléfono 1
            row[4] if row[4] else "",  # Teléfono 2
            row[5] if row[5] else "",  # Especialidad
            row[6] if row[6] else "",  # Hospital 1
            row[7] if row[7] else "",  # Consultorio 1
            row[8] if row[8] else "",  # Hospital 2
            row[9] if row[9] else "",  # Consultorio 2
            row[10] if row[10] else "",  # Hospital 3
            row[11] if row[11] else ""  # Consultorio 3
        )
        # Insertar los datos en el Treeview
        treeview.insert("", "end", values=datos)

# Función para cargar los datos seleccionados en los campos de entrada
def cargar_datos(event):
    seleccionado = treeview.selection()
    if seleccionado:
        # Obtener el ID del paciente desde la fila seleccionada
        id_paciente = treeview.item(seleccionado)['values'][0]  # El ID está en la primera columna
        cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id_paciente,))
        row = cursor.fetchone()

        if row:  # Verificar si se encontró un registro
            limpiar_campos()
            entry_nombre.insert(0, row[1])
            entry_apellido.insert(0, row[2])
            entry_telefono1.insert(0, row[3] if row[3] else "")
            entry_telefono2.insert(0, row[4] if row[4] else "")
            entry_especialidad.insert(0, row[5] if row[5] else "")
            entry_hospital1.insert(0, row[6] if row[6] else "")
            entry_consultorio1.insert(0, row[7] if row[7] else "")
            entry_hospital2.insert(0, row[8] if row[8] else "")
            entry_consultorio2.insert(0, row[9] if row[9] else "")
            entry_hospital3.insert(0, row[10] if row[10] else "")
            entry_consultorio3.insert(0, row[11] if row[11] else "")

# Función para cargar datos desde un archivo CSV
def cargar_desde_csv():
    try:
        with open('datos1.csv', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            next(lector)  # Saltar la primera fila (encabezados)
            for fila in lector:
                # Verificar que la fila tenga exactamente 11 columnas
                if len(fila) == 11:
                    nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3 = fila
                    cursor.execute('''
                    INSERT INTO pacientes (nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (nombre, apellido, telefono1 or None, telefono2 or None, especialidad or None, hospital1 or None, consultorio1 or None, hospital2 or None, consultorio2 or None, hospital3 or None, consultorio3 or None))
                else:
                    print(f"Advertencia: Fila ignorada porque no tiene 11 columnas: {fila}")
            conn.commit()
            messagebox.showinfo("Éxito", "Datos cargados desde CSV correctamente")
            actualizar_lista()
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo 'datos.csv' no existe")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo CSV: {e}")

# Función para buscar por nombre
def buscar_por_nombre():
    nombre_busqueda = entry_buscar.get()
    if nombre_busqueda:
        # Limpiar el Treeview antes de mostrar los resultados
        for row in treeview.get_children():
            treeview.delete(row)

        # Buscar pacientes cuyo nombre coincida con la búsqueda (incluyendo el ID)
        cursor.execute('SELECT * FROM pacientes WHERE nombre LIKE ?', (f"%{nombre_busqueda}%",))
        resultados = cursor.fetchall()

        # Mostrar los resultados en el Treeview (incluyendo el ID oculto)
        for row in resultados:
            datos = (
                row[0],  # ID (ahora incluido)
                row[1],  # Nombre
                row[2],  # Apellido
                row[3] if row[3] else "",  # Teléfono 1
                row[4] if row[4] else "",  # Teléfono 2
                row[5] if row[5] else "",  # Especialidad
                row[6] if row[6] else "",  # Hospital 1
                row[7] if row[7] else "",  # Consultorio 1
                row[8] if row[8] else "",  # Hospital 2
                row[9] if row[9] else "",  # Consultorio 2
                row[10] if row[10] else "",  # Hospital 3
                row[11] if row[11] else ""  # Consultorio 3
            )
            treeview.insert("", "end", values=datos)
    else:
        messagebox.showwarning("Error", "Ingresa un nombre para buscar")
        actualizar_lista()  # Mostrar todos los registros si la búsqueda está vacía
        
# Interfaz gráfica
root = Tk()
root.title("Gestión de Pacientes")

# Configurar el grid principal para que los elementos se alineen a la izquierda
root.grid_columnconfigure(0, weight=1)

# Frame principal para organizar los campos (sin padding adicional)
frame_principal = Frame(root)
frame_principal.grid(row=0, column=0, sticky="w", padx=10, pady=10)

# Primera fila: Nombre, Apellido, Especialidad
frame_fila1 = Frame(frame_principal)
frame_fila1.grid(row=0, column=0, sticky="w", pady=5)

Label(frame_fila1, text="Nombre:").pack(side=LEFT)
entry_nombre = Entry(frame_fila1, width=45)
entry_nombre.pack(side=LEFT, padx=5)

Label(frame_fila1, text="Apellido:").pack(side=LEFT)
entry_apellido = Entry(frame_fila1, width=45)
entry_apellido.pack(side=LEFT, padx=5)

Label(frame_fila1, text="Especialidad:").pack(side=LEFT)
entry_especialidad = Entry(frame_fila1, width=45)
entry_especialidad.pack(side=LEFT, padx=5)

# Segunda fila: Teléfono 1, Teléfono 2
frame_fila2 = Frame(frame_principal)
frame_fila2.grid(row=1, column=0, sticky="w", pady=5)

Label(frame_fila2, text="Teléfono 1:").pack(side=LEFT)
entry_telefono1 = Entry(frame_fila2, width=43)
entry_telefono1.pack(side=LEFT, padx=5)

Label(frame_fila2, text="Teléfono 2:").pack(side=LEFT)
entry_telefono2 = Entry(frame_fila2, width=43)
entry_telefono2.pack(side=LEFT, padx=5)

# Tercera fila: Hospital 1, Consultorio 1
frame_fila3 = Frame(frame_principal)
frame_fila3.grid(row=2, column=0, sticky="w", pady=5)

Label(frame_fila3, text="Hospital 1:").pack(side=LEFT)
entry_hospital1 = Entry(frame_fila3, width=43)
entry_hospital1.pack(side=LEFT, padx=5)

Label(frame_fila3, text="Consultorio 1:").pack(side=LEFT)
entry_consultorio1 = Entry(frame_fila3, width=40)
entry_consultorio1.pack(side=LEFT, padx=5)

# Cuarta fila: Hospital 2, Consultorio 2
frame_fila4 = Frame(frame_principal)
frame_fila4.grid(row=3, column=0, sticky="w", pady=5)

Label(frame_fila4, text="Hospital 2:").pack(side=LEFT)
entry_hospital2 = Entry(frame_fila4, width=43)
entry_hospital2.pack(side=LEFT, padx=5)

Label(frame_fila4, text="Consultorio 2:").pack(side=LEFT)
entry_consultorio2 = Entry(frame_fila4, width=40)
entry_consultorio2.pack(side=LEFT, padx=5)

# Quinta fila: Hospital 3, Consultorio 3
frame_fila5 = Frame(frame_principal)
frame_fila5.grid(row=4, column=0, sticky="w", pady=5)

Label(frame_fila5, text="Hospital 3:").pack(side=LEFT)
entry_hospital3 = Entry(frame_fila5, width=43)
entry_hospital3.pack(side=LEFT, padx=5)

Label(frame_fila5, text="Consultorio 3:").pack(side=LEFT)
entry_consultorio3 = Entry(frame_fila5, width=40)
entry_consultorio3.pack(side=LEFT, padx=5)

# Frame para los botones principales
frame_botones = Frame(frame_principal)
frame_botones.grid(row=5, column=0, sticky="w", pady=10)

Button(frame_botones, text="Agregar", command=agregar).pack(side=LEFT, padx=5)
Button(frame_botones, text="Actualizar", command=actualizar).pack(side=LEFT, padx=5)
Button(frame_botones, text="Borrar", command=borrar).pack(side=LEFT, padx=5)

# Crear el Treeview para mostrar los datos en columnas
columnas = (
    "ID", "Nombre", "Apellido", "Teléfono", "Teléfono 2", "Especialidad",
    "Hospital", "Consultorio", "Hospital 2", "Consultorio 2",
    "Hospital 3", "Consultorio 3"
)

treeview = ttk.Treeview(root, columns=columnas, show="headings")
treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configurar los encabezados de las columnas
for col in columnas:
    treeview.heading(col, text=col)

# Ajustar el ancho de las columnas
for col in columnas:
    treeview.column(col, width=100, anchor="w")

# Asociar la función cargar_datos a la selección de una fila
treeview.bind('<<TreeviewSelect>>', cargar_datos)

# Frame para la búsqueda
frame_busqueda = Frame(root)
frame_busqueda.grid(row=2, column=0, padx=10, pady=10)

Label(frame_busqueda, text="Buscar por nombre:").pack(side=LEFT, padx=5)
entry_buscar = Entry(frame_busqueda)
entry_buscar.pack(side=LEFT, padx=5)
Button(frame_busqueda, text="Buscar", command=buscar_por_nombre).pack(side=LEFT, padx=5)

# Frame para botones adicionales
frame_botones_adicionales = Frame(root)
frame_botones_adicionales.grid(row=3, column=0, padx=10, pady=10)

Button(frame_botones_adicionales, text="Cargar desde CSV", command=cargar_desde_csv).pack(side=LEFT, padx=5)
Button(frame_botones_adicionales, text="Cambiar credenciales", command=cambiar_credenciales).pack(side=LEFT, padx=5)

# Configurar el redimensionamiento de la ventana
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Actualizar lista al iniciar
actualizar_lista()

# Ejecutar la aplicación
mostrar_login()
root.mainloop()

# Cerrar la conexión a la base de datos al salir
conn.close()