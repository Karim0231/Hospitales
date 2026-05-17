# 🏥 Hospitales — Sistema de Gestión de Clientes Médicos

Aplicación de escritorio desarrollada en **Python** para la administración de información de clientes del sector salud. Permite gestionar datos de pacientes, hospitales, especialidades médicas y contactos de forma segura y eficiente.

---

## 📋 Descripción

**Hospitales** es una solución de escritorio diseñada para consultorios y clínicas que necesitan centralizar la información de sus clientes médicos. Cuenta con autenticación de usuario, operaciones completas de base de datos y respaldo de datos en formato CSV.

---

## ✨ Funcionalidades

- 🔐 **Autenticación** — Acceso protegido con usuario y contraseña
- 👤 **Gestión de clientes** — Alta, consulta, edición y eliminación de pacientes
- 🏨 **Hospitales y especialidades** — Registro de centros médicos y áreas de atención
- 📞 **Contactos múltiples** — Varios contactos por cliente
- 📤 **Exportación CSV** — Respaldo y exportación de datos
- 📥 **Importación CSV** — Carga masiva de información
- 💾 **Base de datos local** — Almacenamiento con SQLite, sin necesidad de internet

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| Python | Lenguaje principal |
| SQLite | Base de datos local |
| Tkinter | Interfaz gráfica de usuario |
| CSV | Exportación e importación de datos |
| Git | Control de versiones |

---

## 🚀 Instalación y uso

### Opción 1 — Ejecutable (recomendado)
1. Descarga el archivo `Hospitales.exe` desde la sección [Releases](../../releases)
2. Ejecuta el archivo directamente, no requiere instalación
3. Ingresa con tus credenciales de acceso

### Opción 2 — Desde el código fuente
```bash
# Clonar el repositorio
git clone https://github.com/karim-osvaldo/hospitales.git

# Entrar al directorio
cd hospitales

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

---

## 📸 Capturas de pantalla

> *Próximamente*

---

## 📁 Estructura del proyecto

```
hospitales/
│
├── main.py              # Punto de entrada de la aplicación
├── database.py          # Conexión y operaciones con SQLite
├── auth.py              # Módulo de autenticación
├── ui/                  # Interfaces gráficas
├── exports/             # Archivos CSV generados
└── requirements.txt     # Dependencias del proyecto
```

---

## 👨‍💻 Autor

**Karim Osvaldo Sánchez Robledo**  
Ingeniero en Sistemas Computacionales  
🔗 [LinkedIn](https://mx.linkedin.com/in/karim-osvaldo-s%C3%A1nchez-robledo-543b21265)

---

## 📄 Licencia

Este proyecto fue desarrollado como proyecto freelance. Todos los derechos reservados.
