# Nueva versión 1.1.1 – admin/admin123 funcional
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

# Conectar a la base de datos
conn = sqlite3.connect('hospitales.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    puede_modificar BOOLEAN DEFAULT 1
)
''')

# Crear usuario admin si no existe
try:
    cursor.execute('''
    INSERT INTO usuarios (username, password, puede_modificar) 
    VALUES (?, ?, ?)
    ''', ('admin', 'admin123', 1))  # Contraseña en texto plano
    conn.commit()
except sqlite3.IntegrityError:
    pass  # Si ya existe, no hace nada

# Crear tabla de pacientes
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

# --- Funciones ---
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
    
    root.withdraw()  # Ocultar la ventana principal hasta el login

# --- Función para cambiar credenciales ---
def cambiar_credenciales():
    config_window = Toplevel(root)
    config_window.title("Configurar credenciales")
    config_window.geometry("350x350")
    
    cursor.execute('SELECT username FROM usuarios WHERE username = "admin"')
    es_admin = cursor.fetchone() is not None
    
    if es_admin:
        Label(config_window, text="ADVERTENCIA: Modificando la cuenta admin", fg="red").pack(pady=5)
    
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
            messagebox.showerror("Error", "Ingrese usuario y contraseña actual")
            return
        if not nuevo_usuario or not nueva_password:
            messagebox.showerror("Error", "Ingrese nuevo usuario y contraseña")
            return
        
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                      (usuario_actual, password_actual))
        usuario = cursor.fetchone()
        if usuario:
            try:
                cursor.execute('DELETE FROM usuarios WHERE username = ?', (usuario_actual,))
                cursor.execute('INSERT INTO usuarios (username, password, puede_modificar) VALUES (?, ?, ?)',
                               (nuevo_usuario, nueva_password, 1))
                conn.commit()
                messagebox.showinfo("Éxito", f"Usuario anterior: {usuario_actual}\nNuevo usuario: {nuevo_usuario}")
                config_window.destroy()
            except sqlite3.IntegrityError:
                conn.rollback()
                messagebox.showerror("Error", "El nombre de usuario ya existe")
        else:
            messagebox.showerror("Error", "Credenciales actuales incorrectas")
    
    Button(config_window, text="Actualizar", command=actualizar_credenciales).pack(pady=10)

# --- Funciones de pacientes ---
def limpiar_campos():
    for e in [entry_nombre, entry_apellido, entry_telefono1, entry_telefono2,
              entry_especialidad, entry_hospital1, entry_consultorio1,
              entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3]:
        e.delete(0, END)

def actualizar_lista():
    for row in treeview.get_children():
        treeview.delete(row)
    cursor.execute('SELECT * FROM pacientes')
    for row in cursor.fetchall():
        datos = tuple("" if v is None else v for v in row)
        treeview.insert("", "end", values=datos)

def existe_paciente(nombre, apellido, telefono1):
    cursor.execute('SELECT COUNT(*) FROM pacientes WHERE nombre=? AND apellido=? AND telefono1=?',
                   (nombre, apellido, telefono1))
    return cursor.fetchone()[0] > 0

def agregar():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    telefono1 = entry_telefono1.get().strip() or None
    if not nombre or not apellido:
        messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
        return
    if existe_paciente(nombre, apellido, telefono1):
        messagebox.showwarning("Duplicado", "Paciente ya existe")
        return
    
    campos = [entry_telefono2, entry_especialidad, entry_hospital1, entry_consultorio1,
              entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3]
    valores = [e.get().strip() or None for e in campos]
    cursor.execute('''INSERT INTO pacientes
    (nombre, apellido, telefono1, telefono2, especialidad, hospital1, consultorio1,
    hospital2, consultorio2, hospital3, consultorio3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (nombre, apellido, telefono1, *valores))
    conn.commit()
    messagebox.showinfo("Éxito", "Registro agregado correctamente")
    limpiar_campos()
    actualizar_lista()

def cargar_datos(event):
    seleccionado = treeview.selection()
    if seleccionado:
        id_paciente = treeview.item(seleccionado)['values'][0]
        cursor.execute('SELECT * FROM pacientes WHERE id=?', (id_paciente,))
        row = cursor.fetchone()
        if row:
            limpiar_campos()
            for i, e in enumerate([entry_nombre, entry_apellido, entry_telefono1, entry_telefono2,
                                   entry_especialidad, entry_hospital1, entry_consultorio1,
                                   entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3]):
                e.insert(0, "" if row[i+1] is None else row[i+1])

def actualizar():
    seleccionado = treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un registro para actualizar")
        return
    id_paciente = treeview.item(seleccionado)['values'][0]
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    if not nombre or not apellido:
        messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
        return
    campos = [entry_telefono1, entry_telefono2, entry_especialidad, entry_hospital1, entry_consultorio1,
              entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3]
    valores = [e.get().strip() or None for e in campos]
    cursor.execute('''UPDATE pacientes SET nombre=?, apellido=?, telefono1=?, telefono2=?,
    especialidad=?, hospital1=?, consultorio1=?, hospital2=?, consultorio2=?, hospital3=?, consultorio3=? 
    WHERE id=?''', (nombre, apellido, *valores, id_paciente))
    conn.commit()
    messagebox.showinfo("Éxito", "Registro actualizado")
    limpiar_campos()
    actualizar_lista()

def borrar():
    seleccionado = treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un registro para borrar")
        return
    id_paciente = treeview.item(seleccionado)['values'][0]
    if messagebox.askyesno("Confirmar", "¿Borrar este registro?"):
        cursor.execute('DELETE FROM pacientes WHERE id=?', (id_paciente,))
        conn.commit()
        actualizar_lista()

def cargar_desde_csv():
    try:
        with open('datos1.csv', newline='', encoding='utf-8') as archivo_csv:
            lector = csv.reader(archivo_csv)
            next(lector)
            for fila in lector:
                if len(fila)==11:
                    cursor.execute('''INSERT INTO pacientes
                    (nombre, apellido, telefono1, telefono2, especialidad,
                    hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   tuple(v if v != "" else None for v in fila))
            conn.commit()
        messagebox.showinfo("Éxito", "Datos cargados desde CSV")
        actualizar_lista()
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo 'datos1.csv' no encontrado")

def buscar_por_nombre():
    nombre_busqueda = entry_buscar.get()
    if not nombre_busqueda:
        actualizar_lista()
        return
    for row in treeview.get_children():
        treeview.delete(row)
    cursor.execute('SELECT * FROM pacientes WHERE nombre LIKE ?', (f"%{nombre_busqueda}%",))
    for row in cursor.fetchall():
        datos = tuple("" if v is None else v for v in row)
        treeview.insert("", "end", values=datos)

# --- Interfaz gráfica ---
root = Tk()
root.title("Gestión de Pacientes")

frame_principal = Frame(root)
frame_principal.grid(row=0, column=0, sticky="w", padx=10, pady=10)

# Campos de paciente
entry_nombre = Entry(frame_principal, width=30)
entry_apellido = Entry(frame_principal, width=30)
entry_telefono1 = Entry(frame_principal, width=20)
entry_telefono2 = Entry(frame_principal, width=20)
entry_especialidad = Entry(frame_principal, width=20)
entry_hospital1 = Entry(frame_principal, width=20)
entry_consultorio1 = Entry(frame_principal, width=20)
entry_hospital2 = Entry(frame_principal, width=20)
entry_consultorio2 = Entry(frame_principal, width=20)
entry_hospital3 = Entry(frame_principal, width=20)
entry_consultorio3 = Entry(frame_principal, width=20)

# Organizar los campos (simplificado)
campos = [("Nombre", entry_nombre), ("Apellido", entry_apellido),
          ("Teléfono 1", entry_telefono1), ("Teléfono 2", entry_telefono2),
          ("Especialidad", entry_especialidad), ("Hospital 1", entry_hospital1),
          ("Consultorio 1", entry_consultorio1), ("Hospital 2", entry_hospital2),
          ("Consultorio 2", entry_consultorio2), ("Hospital 3", entry_hospital3),
          ("Consultorio 3", entry_consultorio3)]

for i, (label_text, entry) in enumerate(campos):
    Label(frame_principal, text=label_text).grid(row=i, column=0, sticky="w")
    entry.grid(row=i, column=1, pady=2, padx=5)

# Botones principales
Button(frame_principal, text="Agregar", command=agregar).grid(row=0, column=2, padx=5)
Button(frame_principal, text="Actualizar", command=actualizar).grid(row=1, column=2, padx=5)
Button(frame_principal, text="Borrar", command=borrar).grid(row=2, column=2, padx=5)

# Treeview
columnas = ("ID", "Nombre", "Apellido", "Teléfono1", "Teléfono2", "Especialidad",
            "Hospital1", "Consultorio1", "Hospital2", "Consultorio2", "Hospital3", "Consultorio3")
treeview = ttk.Treeview(root, columns=columnas, show="headings")
for col in columnas:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)
treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
treeview.bind('<<TreeviewSelect>>', cargar_datos)

# Buscador
frame_busqueda = Frame(root)
frame_busqueda.grid(row=2, column=0, padx=10, pady=10)
entry_buscar = Entry(frame_busqueda)
entry_buscar.pack(side=LEFT, padx=5)
Button(frame_busqueda, text="Buscar", command=buscar_por_nombre).pack(side=LEFT, padx=5)

# Botones adicionales
frame_botones_adicionales = Frame(root)
frame_botones_adicionales.grid(row=3, column=0, padx=10, pady=10)
Button(frame_botones_adicionales, text="Cargar desde CSV", command=cargar_desde_csv).pack(side=LEFT, padx=5)
Button(frame_botones_adicionales, text="Cambiar credenciales", command=cambiar_credenciales).pack(side=LEFT, padx=5)

# Ajustes de redimensionamiento
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Actualizar lista y mostrar login
actualizar_lista()
mostrar_login()

# Ejecutar aplicación
root.mainloop()
conn.close()
