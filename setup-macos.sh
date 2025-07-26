#!/bin/bash

# SQL Injection Demo - macOS Setup Script
# ⚠️ ADVERTENCIA: Solo para fines educativos

echo "
╔══════════════════════════════════════════════════════════════╗
║                    SQL Injection Demo                        ║
║                Aplicación Web Vulnerable                    ║
║                                                              ║
║  ⚠️  ADVERTENCIA: Solo para fines educativos  ⚠️           ║
╚══════════════════════════════════════════════════════════════╝
"

echo "🔍 Verificando requisitos..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Instala Python 3 desde https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version detectado"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew no está instalado"
    echo "Para instalar drivers adicionales, instala Homebrew:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

echo ""
echo "📦 Instalando dependencias básicas..."

# Install basic dependencies
python3 -m pip install -r requirements-basic.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias básicas instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo ""
echo "⚙️  Configurando archivos..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Archivo .env creado desde env.example"
    else
        echo "❌ Error: No se encontró env.example"
        exit 1
    fi
else
    echo "ℹ️  Archivo .env ya existe"
fi

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configura tus bases de datos (opcional):"
echo "   - MySQL: brew install mysql"
echo "   - PostgreSQL: brew install postgresql"
echo ""
echo "2. Para SQL Server y Oracle (opcional):"
echo "   - SQL Server: brew install microsoft/mssql-release/msodbcsql17"
echo "   - Oracle: brew install oracle-instantclient"
echo ""
echo "3. Ejecuta la aplicación:"
echo "   python3 app.py"
echo ""
echo "4. Abre tu navegador en:"
echo "   http://localhost:5000"
echo ""
echo "📚 Para más información, consulta el README.md"
echo ""
echo "⚠️  RECUERDA: Esta aplicación es vulnerable por diseño"
echo "    para fines educativos únicamente."
echo ""
echo "🔧 Bases de datos disponibles:"
echo "   - MySQL: ✅"
echo "   - PostgreSQL: ✅"
if command -v brew &> /dev/null; then
    echo "   - SQL Server: ⚠️  (requiere driver ODBC)"
    echo "   - Oracle: ⚠️  (requiere Oracle Instant Client)"
else
    echo "   - SQL Server: ❌ (requiere Homebrew)"
    echo "   - Oracle: ❌ (requiere Homebrew)"
fi 