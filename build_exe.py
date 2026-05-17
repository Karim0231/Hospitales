# build_exe.py
import os
import subprocess
import sys

# Instalar versiones compatibles
subprocess.call([sys.executable, "-m", "pip", "install", "pandas==1.5.3", "numpy==1.24.4", "pyinstaller==5.13.0"])

# Comando de PyInstaller
cmd = [
    'pyinstaller',
    '--onefile',
    '--windowed',
    '--name=GestionPacientes',
    '--add-data=hospitales.db;.',
    '--add-data=datos1.csv;.',
    '--hidden-import=pandas',
    '--hidden-import=numpy', 
    '--hidden-import=pandas._libs.tslibs.timedeltas',
    '--hidden-import=pandas._libs.tslibs.nattype',
    '--hidden-import=pandas._libs.tslibs.base',
    '--hidden-import=numpy.core._methods',
    '--hidden-import=numpy.lib.format',
    '--clean',
    'main_1_Global.py'
]

# Ejecutar
subprocess.call(cmd)