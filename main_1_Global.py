# Nueva versión 1.2.3 – admin/admin123 funcional con reglas de duplicado
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import pandas as pd
from datetime import datetime
import os

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
    ''', ('admin', 'admin123', 1))
    conn.commit()
except sqlite3.IntegrityError:
    pass

# Crear tabla de pacientes
cursor.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT,
    telefono1 TEXT,
    telefono2 TEXT,
    especialidad TEXT,
    hospital1 TEXT,
    consultorio1 TEXT,
    hospital2 TEXT,
    consultorio2 TEXT,
    hospital3 TEXT,
    consultorio3 TEXT,
    correo TEXT
)
''')
conn.commit()

# --- Función para guardar en CSV ---
def guardar_en_csv(paciente_data):
    """Guarda un nuevo paciente en el archivo datos1.csv"""
    try:
        # Verificar si el archivo existe
        archivo_existe = os.path.isfile('datos1.csv')
        
        with open('datos1.csv', 'a', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            
            # Si el archivo no existe, escribir encabezados
            if not archivo_existe:
                encabezados = ['nombre', 'apellido', 'telefono1', 'telefono2', 'especialidad',
                              'hospital1', 'consultorio1', 'hospital2', 'consultorio2', 
                              'hospital3', 'consultorio3', 'correo']
                writer.writerow(encabezados)
            
            # Asegurarse de que tenemos exactamente 12 campos
            if len(paciente_data) < 12:
                # Rellenar con campos vacíos si faltan
                paciente_data.extend([''] * (12 - len(paciente_data)))
            elif len(paciente_data) > 12:
                # Truncar si hay más de 12 campos
                paciente_data = paciente_data[:12]
            
            # Escribir los datos del paciente (exactamente 12 campos)
            writer.writerow(paciente_data)
            
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")

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
            root.deiconify()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
    
    Button(login_window, text="Ingresar", command=verificar_credenciales).pack(pady=10)
    
    root.withdraw()

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

# --- Función para exportar a CSV ---
def exportar_a_csv():
    try:
        # Obtener todos los datos de la base de datos ordenados por ID
        cursor.execute('''
        SELECT id, nombre, apellido, telefono1, telefono2, especialidad,
               hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3, correo
        FROM pacientes ORDER BY id
        ''')
        datos = cursor.fetchall()
        
        if not datos:
            messagebox.showwarning("Exportar", "No hay datos para exportar")
            return
        
        # Crear nombre de archivo con fecha y hora
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_archivo = f"pacientes_exportados_{fecha_actual}.csv"
        
        # Exportar a CSV
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            
            # Escribir encabezados
            encabezados = ['ID', 'Nombre', 'Apellido', 'Teléfono 1', 'Teléfono 2', 'Especialidad',
                          'Hospital 1', 'Consultorio 1', 'Hospital 2', 'Consultorio 2', 
                          'Hospital 3', 'Consultorio 3', 'Correo']
            writer.writerow(encabezados)
            
            # Escribir datos
            for fila in datos:
                # Convertir None a cadenas vacías
                fila_limpia = ['' if valor is None else valor for valor in fila]
                writer.writerow(fila_limpia)
        
        # Abrir la carpeta donde se guardó el archivo
        os.startfile(os.path.dirname(os.path.abspath(nombre_archivo)))
        
        messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{nombre_archivo}")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a CSV: {str(e)}")

# --- Función para abrir ventana de agregar paciente ---
def abrir_agregar_paciente():
    agregar_window = Toplevel(root)
    agregar_window.title("Agregar Nuevo Paciente")
    agregar_window.geometry("400x600")
    
    # Campos para agregar paciente
    campos_agregar = [
        ("Nombre", Entry(agregar_window, width=30)),
        ("Apellido", Entry(agregar_window, width=30)),
        ("Teléfono 1", Entry(agregar_window, width=20)),
        ("Teléfono 2", Entry(agregar_window, width=20)),
        ("Especialidad", Entry(agregar_window, width=20)),
        ("Hospital 1", Entry(agregar_window, width=20)),
        ("Consultorio 1", Entry(agregar_window, width=20)),
        ("Hospital 2", Entry(agregar_window, width=20)),
        ("Consultorio 2", Entry(agregar_window, width=20)),
        ("Hospital 3", Entry(agregar_window, width=20)),
        ("Consultorio 3", Entry(agregar_window, width=20)),
        ("Correo", Entry(agregar_window, width=30))
    ]
    
    # Posicionar campos en la ventana
    for i, (label_text, entry) in enumerate(campos_agregar):
        Label(agregar_window, text=label_text + ":").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        entry.grid(row=i, column=1, padx=10, pady=5)
    
    def guardar_nuevo_paciente():
        # Obtener valores de los campos
        valores = [entry.get().strip() or None for _, entry in campos_agregar]
        
        if not valores[0] or not valores[1]:
            messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
            return
        
        # Verificar duplicado
        if existe_paciente_completo(valores):
            messagebox.showwarning("Duplicado", "Este paciente ya existe")
            return
        
        # Insertar nuevo paciente
        cursor.execute('''
        INSERT INTO pacientes (nombre, apellido, telefono1, telefono2, especialidad,
        hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3, correo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(valores))
        conn.commit()
        
        # Guardar también en el archivo CSV
        # Convertir None a cadenas vacías para el CSV y asegurar 12 campos
        valores_csv = ['' if v is None else v for v in valores]
        
        # Asegurar que tenemos exactamente 12 campos
        if len(valores_csv) != 12:
            valores_csv = valores_csv[:12]  # Tomar solo los primeros 12 si hay más
            if len(valores_csv) < 12:
                valores_csv.extend([''] * (12 - len(valores_csv)))  # Rellenar si faltan
        
        guardar_en_csv(valores_csv)
        
        messagebox.showinfo("Éxito", "Paciente agregado correctamente")
        agregar_window.destroy()
        actualizar_lista()
    
    Button(agregar_window, text="Guardar", command=guardar_nuevo_paciente).grid(row=len(campos_agregar), column=0, columnspan=2, pady=10)
    Button(agregar_window, text="Cancelar", command=agregar_window.destroy).grid(row=len(campos_agregar)+1, column=0, columnspan=2, pady=5)

    
#Mostrar informacion de pacientes
def mostrar_detalles_paciente(event):
    seleccionado = treeview.selection()
    if not seleccionado:
        return
    
    id_paciente = treeview.item(seleccionado)['values'][0]
    
    detalles_window = Toplevel(root)
    detalles_window.title("Detalles del Paciente")
    detalles_window.geometry("500x600")
    
    # Obtener datos completos del paciente
    cursor.execute('SELECT * FROM pacientes WHERE id=?', (id_paciente,))
    paciente = cursor.fetchone()
    
    if not paciente:
        return
    
    # Crear campos editables
    campos_edicion = []
    labels = ["Nombre", "Apellido", "Teléfono 1", "Teléfono 2", "Especialidad", 
              "Hospital 1", "Consultorio 1", "Hospital 2", "Consultorio 2", 
              "Hospital 3", "Consultorio 3", "Correo"]
    
    for i in range(1, 13):  # Desde nombre (1) hasta correo (12)
        Label(detalles_window, text=labels[i-1] + ":", font=("Arial", 10, "bold")).grid(row=i-1, column=0, sticky="w", padx=10, pady=2)
        entry = Entry(detalles_window, width=40)
        entry.grid(row=i-1, column=1, sticky="w", padx=10, pady=2)
        entry.insert(0, paciente[i] if paciente[i] else "")
        campos_edicion.append(entry)
    
    # Botones
    frame_botones = Frame(detalles_window)
    frame_botones.grid(row=12, column=0, columnspan=2, pady=10)
    
    def actualizar_desde_detalles():
        nuevos_valores = [entry.get().strip() or None for entry in campos_edicion]
        
        if not nuevos_valores[0] or not nuevos_valores[1]:
            messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
            return
        
        # Verificar duplicado (excluyendo el actual)
        cursor.execute('''
        SELECT COUNT(*) FROM pacientes WHERE
        nombre=? AND apellido=? AND telefono1=? AND telefono2=? AND especialidad=? AND
        hospital1=? AND consultorio1=? AND hospital2=? AND consultorio2=? AND hospital3=? AND consultorio3=? AND correo=? AND id != ?
        ''', tuple(nuevos_valores + [id_paciente]))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Duplicado", "Otro paciente con los mismos datos ya existe")
            return
        
        # Actualizar paciente
        cursor.execute('''
        UPDATE pacientes SET nombre=?, apellido=?, telefono1=?, telefono2=?, especialidad=?,
        hospital1=?, consultorio1=?, hospital2=?, consultorio2=?, hospital3=?, consultorio3=?, correo=?
        WHERE id=?
        ''', tuple(nuevos_valores + [id_paciente]))
        conn.commit()
        messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
        detalles_window.destroy()
        actualizar_lista()
    
    def borrar_desde_detalles():
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar este paciente?"):
            cursor.execute('DELETE FROM pacientes WHERE id=?', (id_paciente,))
            conn.commit()
            messagebox.showinfo("Éxito", "Paciente borrado correctamente")
            detalles_window.destroy()
            actualizar_lista()
    
    Button(frame_botones, text="Actualizar", command=actualizar_desde_detalles, bg="lightblue").pack(side=LEFT, padx=5)
    Button(frame_botones, text="Borrar", command=borrar_desde_detalles, bg="salmon").pack(side=LEFT, padx=5)
    Button(frame_botones, text="Cerrar", command=detalles_window.destroy).pack(side=LEFT, padx=5)


# --- Funciones de pacientes ---
def limpiar_campos():
    for e in [entry_nombre, entry_apellido, entry_telefono1, entry_telefono2,
              entry_especialidad, entry_hospital1, entry_consultorio1,
              entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3, entry_correo]:
        e.delete(0, END)

def actualizar_lista():
    for row in treeview.get_children():
        treeview.delete(row)
    cursor.execute('SELECT id,nombre,apellido,telefono1,especialidad,hospital1,correo FROM pacientes')
    for row in cursor.fetchall():
        datos = (
            row[0],  # ID
            row[1],  # Nombre
            row[2],  # Apellido
            "" if row[3] is None else row[3],  # Teléfono1
            "" if row[4] is None else row[4],  # Especialidad
            "" if row[5] is None else row[5],  # Hospital
            "" if row[6] is None else row[6]   # Correo
        )
        treeview.insert("", "end", values=datos)

# Verifica duplicado completo
def existe_paciente_completo(campos_valores):
    # Campos de la tabla
    campos = ["nombre", "apellido", "telefono1", "telefono2", "especialidad",
              "hospital1", "consultorio1", "hospital2", "consultorio2", "hospital3", "consultorio3", "correo"]
    
    condiciones = []
    parametros = []
    
    for i, val in enumerate(campos_valores):
        if val is None:
            condiciones.append(f"{campos[i]} IS NULL")
        else:
            condiciones.append(f"{campos[i]}=?")
            parametros.append(val)
    
    consulta = "SELECT COUNT(*) FROM pacientes WHERE " + " AND ".join(condiciones)
    cursor.execute(consulta, tuple(parametros))
    return cursor.fetchone()[0] > 0

def agregar():
    campos_valores = [
        entry_nombre.get().strip(), 
        entry_apellido.get().strip(), 
        entry_telefono1.get().strip() or None,
        entry_telefono2.get().strip() or None, 
        entry_especialidad.get().strip() or None,
        entry_hospital1.get().strip() or None, 
        entry_consultorio1.get().strip() or None,
        entry_hospital2.get().strip() or None, 
        entry_consultorio2.get().strip() or None,
        entry_hospital3.get().strip() or None, 
        entry_consultorio3.get().strip() or None,
        entry_correo.get().strip() or None
    ]
    
    if not campos_valores[0] or not campos_valores[1]:
        messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
        return
    
    if existe_paciente_completo(campos_valores):
        messagebox.showwarning("Duplicado", "Este paciente ya existe")
        return

    cursor.execute('''
    INSERT INTO pacientes (nombre, apellido, telefono1, telefono2, especialidad,
    hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3, correo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(campos_valores))
    conn.commit()
    
    # Guardar también en el archivo CSV
    # Convertir None a cadenas vacías para el CSV y asegurar 12 campos
    valores_csv = ['' if v is None else v for v in campos_valores]
    
    # Asegurar que tenemos exactamente 12 campos
    if len(valores_csv) != 12:
        valores_csv = valores_csv[:12]  # Tomar solo los primeros 12 si hay más
        if len(valores_csv) < 12:
            valores_csv.extend([''] * (12 - len(valores_csv)))  # Rellenar si faltan
    
    guardar_en_csv(valores_csv)
    
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
                                   entry_hospital2, entry_consultorio2, entry_hospital3, entry_consultorio3, entry_correo]):
                e.insert(0, "" if row[i+1] is None else row[i+1])

def actualizar():
    seleccionado = treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un registro para actualizar")
        return
    id_paciente = treeview.item(seleccionado)['values'][0]

    campos_valores = [
        entry_nombre.get().strip(), entry_apellido.get().strip(), entry_telefono1.get().strip() or None,
        entry_telefono2.get().strip() or None, entry_especialidad.get().strip() or None,
        entry_hospital1.get().strip() or None, entry_consultorio1.get().strip() or None,
        entry_hospital2.get().strip() or None, entry_consultorio2.get().strip() or None,
        entry_hospital3.get().strip() or None, entry_consultorio3.get().strip() or None,
        entry_correo.get().strip() or None
    ]

    if not campos_valores[0] or not campos_valores[1]:
        messagebox.showwarning("Error", "Nombre y Apellido son obligatorios")
        return
    
    cursor.execute('''
    SELECT COUNT(*) FROM pacientes WHERE
    nombre=? AND apellido=? AND telefono1=? AND telefono2=? AND especialidad=? AND
    hospital1=? AND consultorio1=? AND hospital2=? AND consultorio2=? AND hospital3=? AND consultorio3=? AND correo=? AND id != ?
    ''', tuple(campos_valores + [id_paciente]))
    if cursor.fetchone()[0] > 0:
        messagebox.showwarning("Duplicado", "Otro paciente con los mismos datos ya existe")
        return

    cursor.execute('''
    UPDATE pacientes SET nombre=?, apellido=?, telefono1=?, telefono2=?, especialidad=?,
    hospital1=?, consultorio1=?, hospital2=?, consultorio2=?, hospital3=?, consultorio3=?, correo=?
    WHERE id=?
    ''', tuple(campos_valores + [id_paciente]))
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
            next(lector)  # Saltar encabezado
            agregados = 0
            duplicados = 0
            for fila in lector:
                if len(fila) == 12:
                    valores = tuple(v if v != "" else None for v in fila)
                    if existe_paciente_completo(valores):
                        duplicados += 1
                        continue  # Saltar duplicados
                    cursor.execute('''INSERT INTO pacientes
                        (nombre, apellido, telefono1, telefono2, especialidad,
                        hospital1, consultorio1, hospital2, consultorio2, hospital3, consultorio3, correo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', valores)
                    agregados += 1
            conn.commit()
        messagebox.showinfo("Éxito", f"Datos cargados desde CSV.\nAgregados: {agregados}\nDuplicados: {duplicados}")
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
entry_correo = Entry(frame_principal,width=30)

Button(frame_principal, text="Borrar", command=borrar).grid(row=2, column=4, padx=5)
Button(frame_principal, text="Nuevo Paciente", command=abrir_agregar_paciente).grid(row=2, column=2, padx=5, pady=5)

columnas = ("ID", "Nombre", "Apellido", "Teléfono1", "Especialidad", "Hospital", "Correo")
treeview = ttk.Treeview(root, columns=columnas, show="headings")
for col in columnas:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)
treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
treeview.bind('<<TreeviewSelect>>', cargar_datos)
treeview.bind('<Double-1>', mostrar_detalles_paciente)

frame_busqueda = Frame(root)
frame_busqueda.grid(row=2, column=0, padx=10, pady=10)
entry_buscar = Entry(frame_busqueda)
entry_buscar.pack(side=LEFT, padx=5)
Button(frame_busqueda, text="Buscar", command=buscar_por_nombre).pack(side=LEFT, padx=5)

frame_botones_adicionales = Frame(root)
frame_botones_adicionales.grid(row=3, column=0, padx=10, pady=10)
Button(frame_botones_adicionales, text="Cargar desde CSV", command=cargar_desde_csv).pack(side=LEFT, padx=5)
Button(frame_botones_adicionales, text="Exportar a CSV", command=exportar_a_csv).pack(side=LEFT, padx=5)
Button(frame_botones_adicionales, text="Cambiar credenciales", command=cambiar_credenciales).pack(side=LEFT, padx=5)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

actualizar_lista()
mostrar_login()

root.mainloop()
conn.close()