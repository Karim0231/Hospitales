# 🏥 Hospitales — Sistema de Gestión de Pacientes Médicos

Aplicación de escritorio desarrollada en **Python** para la administración de información de pacientes del sector salud. Permite gestionar datos de pacientes, hospitales, especialidades médicas y contactos de forma segura y eficiente.

---

## 📋 Descripción

**Hospitales** es una solución de escritorio diseñada para consultorios y clínicas que necesitan centralizar la información de sus pacientes. Cuenta con autenticación de usuario, operaciones completas de base de datos y respaldo de datos en formato CSV.

La base de datos se crea automáticamente al ejecutar la aplicación por primera vez, no requiere configuración adicional.

---

## ✨ Funcionalidades

- 🔐 **Autenticación** — Acceso protegido con usuario y contraseña
- 👤 **Gestión de pacientes** — Alta, consulta, edición y eliminación de registros
- 🏨 **Hospitales y especialidades** — Registro de centros médicos y áreas de atención
- 📞 **Contactos múltiples** — Hasta 3 hospitales y consultorios por paciente
- 📤 **Exportación CSV** — Respaldo y exportación de datos
- 📥 **Importación CSV** — Carga masiva de información
- 💾 **Base de datos automática** — Se crea automáticamente al iniciar la app, sin configuración

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| Python | Lenguaje principal |
| SQLite | Base de datos local (generada automáticamente) |
| Tkinter | Interfaz gráfica de usuario |
| CSV | Exportación e importación de datos |
| PyInstaller | Compilación a ejecutable .exe |
| Git | Control de versiones |

---

## 🚀 Instalación y uso

### Opción 1 — Ejecutable (recomendado)
1. Descarga el archivo `Main_1_Global.exe` desde la sección [Releases](../../releases)
2. Coloca el archivo `datos1.csv` en la misma carpeta que el ejecutable
3. Ejecuta el archivo directamente, no requiere instalación
4. La base de datos se crea automáticamente al primer inicio
5. Ingresa con las credenciales de acceso

> ⚠️ El archivo `datos1.csv` debe estar en la misma carpeta que el `.exe` para que la aplicación funcione correctamente. Se incluye una plantilla vacía en el repositorio.

### Opción 2 — Desde el código fuente
```bash
# Clonar el repositorio
git clone https://github.com/Karim0231/Hospitales.git

# Entrar al directorio
cd Hospitales

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python Main_1_Global.py
```

### Opción 3 — Compilar el ejecutable
Si deseas generar el `.exe` desde el código fuente:
```bash
pip install pyinstaller
python build_exe.py
```

---

## 📁 Estructura del proyecto

```
Hospitales/
│
├── Main_1_Global.py     # Versión final de la aplicación
├── build_exe.py         # Script para compilar el ejecutable .exe
├── datos1.csv           # Plantilla CSV vacía (requerida por el .exe)
└── README.md            # Documentación del proyecto
```

---

## 👨‍💻 Autor

**Karim Osvaldo Sánchez Robledo**  
Ingeniero en Sistemas Computacionales  
🔗 [LinkedIn](https://mx.linkedin.com/in/karim-osvaldo-s%C3%A1nchez-robledo-543b21265)

---

## 📄 Licencia

Este proyecto fue desarrollado como proyecto freelance. Todos los derechos reservados.
