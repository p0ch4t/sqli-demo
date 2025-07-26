#!/usr/bin/env python3
"""
Setup script for SQL Injection Demo Application
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Print application banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    SQL Injection Demo                        ║
    ║                Aplicación Web Vulnerable                    ║
    ║                                                              ║
    ║  ⚠️  ADVERTENCIA: Solo para fines educativos  ⚠️           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 o superior es requerido")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✅ Archivo .env creado desde env.example")
        else:
            print("❌ Error: No se encontró env.example")
            return False
    else:
        print("ℹ️  Archivo .env ya existe")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directorios creados")

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/demo.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Todos los archivos requeridos están presentes")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print("""
    🎉 ¡Configuración completada!
    
    📋 Próximos pasos:
    
    1. Configura tus bases de datos (opcional):
       - MySQL, PostgreSQL, SQL Server, Oracle
       
    2. Edita el archivo .env con tus credenciales:
       - Copia env.example a .env
       - Actualiza las credenciales de las bases de datos
       
    3. Ejecuta la aplicación:
       python app.py
       
    4. Abre tu navegador en:
       http://localhost:5000
       
    📚 Para más información, consulta el README.md
    
    ⚠️  RECUERDA: Esta aplicación es vulnerable por diseño
        para fines educativos únicamente.
    """)

def main():
    """Main setup function"""
    print_banner()
    
    print("🔍 Verificando requisitos...")
    check_python_version()
    
    print("\n📁 Verificando archivos...")
    if not check_files():
        print("❌ Setup falló: Faltan archivos requeridos")
        sys.exit(1)
    
    print("\n📂 Creando directorios...")
    create_directories()
    
    print("\n⚙️  Configurando archivos...")
    if not create_env_file():
        print("❌ Setup falló: No se pudo crear .env")
        sys.exit(1)
    
    print("\n📦 Instalando dependencias...")
    if not install_dependencies():
        print("❌ Setup falló: No se pudieron instalar dependencias")
        sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main() 