# SQL Injection Demo - Aplicación Web Vulnerable

⚠️ **ADVERTENCIA**: Esta aplicación es vulnerable por diseño para fines educativos únicamente. No usar en producción o con datos sensibles.

## Descripción

Esta es una aplicación web vulnerable en Python que se conecta a 4 motores de base de datos distintos:

- **MySQL**
- **PostgreSQL** 
- **SQL Server**
- **Oracle**

La aplicación está diseñada específicamente para demostrar vulnerabilidades de SQL Injection y aprender técnicas de seguridad.

## Características

- 🔥 **Vulnerabilidades Intencionales**: SQL Injection por concatenación directa de strings
- 🗄️ **4 Motores de BD**: Soporte completo para MySQL, PostgreSQL, SQL Server y Oracle
- 🎨 **Interfaz Moderna**: UI responsive con Bootstrap 5 y animaciones
- 📚 **Ejemplos Educativos**: Página de demostración con ejemplos de SQL Injection
- 🔧 **API REST**: Endpoint para ejecutar queries programáticamente
- 📊 **Resultados Visuales**: Tablas formateadas para mostrar resultados de queries

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd sqli-demo
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

**Para macOS (recomendado):**
```bash
# Opción A: Script automático
./setup-macos.sh

# Opción B: Manual
python3 -m pip install -r requirements-basic.txt
```

**Para Linux/Windows:**
```bash
# Opción A: Dependencias básicas
pip install -r requirements-basic.txt

# Opción B: Todas las dependencias
pip install -r requirements.txt
```

**Nota para macOS:** Si tienes problemas con `pyodbc` o `cx_Oracle`, usa las dependencias básicas. Para usar SQL Server y Oracle en macOS, necesitarás instalar drivers adicionales.

### 4. Configurar bases de datos
```bash
cp env.example .env
# Editar .env con tus credenciales de base de datos
```

### 5. Configurar bases de datos (Opcional)

Si quieres usar las bases de datos, necesitarás configurarlas:

#### MySQL
```sql
CREATE DATABASE vulnerable_db;
USE vulnerable_db;
CREATE TABLE users (id INT, username VARCHAR(50), password VARCHAR(50), email VARCHAR(100));
INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com');
INSERT INTO users VALUES (2, 'user1', 'secret456', 'user1@example.com');
```

#### PostgreSQL
```sql
CREATE DATABASE vulnerable_db;
\c vulnerable_db;
CREATE TABLE users (id INT, username VARCHAR(50), password VARCHAR(50), email VARCHAR(100));
INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com');
INSERT INTO users VALUES (2, 'user1', 'secret456', 'user1@example.com');
```

#### SQL Server
```sql
CREATE DATABASE vulnerable_db;
USE vulnerable_db;
CREATE TABLE users (id INT, username VARCHAR(50), password VARCHAR(50), email VARCHAR(100));
INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com');
INSERT INTO users VALUES (2, 'user1', 'secret456', 'user1@example.com');
```

#### Oracle
```sql
CREATE TABLE users (id NUMBER, username VARCHAR2(50), password VARCHAR2(50), email VARCHAR2(100));
INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com');
INSERT INTO users VALUES (2, 'user1', 'secret456', 'user1@example.com');
```

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## Uso

### Interfaz Web
1. Abre http://localhost:5000 en tu navegador
2. Selecciona una base de datos del dropdown
3. Escribe tu query SQL en el textarea
4. Haz click en "Ejecutar Query"

### API REST
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"database": "mysql", "query": "SELECT * FROM users"}'
```

## Ejemplos de SQL Injection

### Bypass de Autenticación
```sql
admin' OR '1'='1' --
```

### Union Attack
```sql
' UNION SELECT 1,2,3,4,5 --
```

### Error Based Injection
```sql
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(0x7e,(SELECT version()),0x7e,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) --
```

### Time Based Injection
```sql
' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --
```

### Dump de Tablas
```sql
' UNION SELECT table_name,NULL,NULL,NULL,NULL FROM information_schema.tables --
```

### Dump de Datos
```sql
' UNION SELECT username,password,email,NULL,NULL FROM users --
```

## Estructura del Proyecto

```
sqli-demo/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── env.example           # Ejemplo de configuración
├── README.md            # Este archivo
├── templates/           # Templates HTML
│   ├── base.html       # Template base
│   ├── index.html      # Página principal
│   └── demo.html       # Página de ejemplos
└── static/             # Archivos estáticos
    ├── css/
    │   └── style.css   # Estilos CSS
    └── js/
        └── app.js      # JavaScript
```

## Vulnerabilidades Implementadas

### 1. SQL Injection por Concatenación Directa
```python
# VULNERABLE: Direct string concatenation
cursor.execute(query)
```

### 2. Falta de Sanitización
- No se valida ni sanitiza la entrada del usuario
- Se ejecutan queries directamente sin parámetros preparados

### 3. Información de Error Expuesta
- Los errores de base de datos se muestran al usuario
- Información de debugging visible

## Medidas de Seguridad (NO Implementadas)

❌ **Parámetros Preparados**: No se usan prepared statements
❌ **Validación de Entrada**: No se valida la entrada del usuario
❌ **Sanitización**: No se sanitiza la entrada
❌ **Principio de Mínimo Privilegio**: No se implementa
❌ **Logging de Seguridad**: No se registran intentos de ataque
❌ **Rate Limiting**: No hay límites de velocidad
❌ **WAF**: No hay Web Application Firewall

## Configuración de Bases de Datos

### MySQL
```bash
# Instalar MySQL
sudo apt-get install mysql-server  # Ubuntu/Debian
brew install mysql                 # macOS

# Crear base de datos
mysql -u root -p
CREATE DATABASE vulnerable_db;
```

### PostgreSQL
```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql                              # macOS

# Crear base de datos
sudo -u postgres psql
CREATE DATABASE vulnerable_db;
```

### SQL Server
```bash
# Instalar SQL Server (Docker)
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=password" \
  -p 1433:1433 --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2019-latest
```

### Oracle
```bash
# Instalar Oracle (Docker)
docker run -d --name oracle \
  -p 1521:1521 \
  -e ORACLE_PWD=password \
  oracleinanutshell/oracle-xe-11g
```

## Troubleshooting

### Error de Conexión a Base de Datos
1. Verifica que la base de datos esté ejecutándose
2. Confirma las credenciales en el archivo `.env`
3. Asegúrate de que el puerto esté abierto

### Error de Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Error de ODBC (SQL Server)
En macOS, instala el driver ODBC:
```bash
brew install microsoft/mssql-release/msodbcsql17
```

### Error de Oracle (cx_Oracle)
En macOS, instala Oracle Instant Client:
```bash
brew install oracle-instantclient
```

### Alternativa: Usar solo MySQL y PostgreSQL
Si tienes problemas con SQL Server u Oracle, puedes usar solo MySQL y PostgreSQL:
```bash
pip install -r requirements-basic.txt
```
La aplicación funcionará con las bases de datos disponibles.

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Disclaimer

⚠️ **ADVERTENCIA LEGAL**: Esta aplicación es únicamente para fines educativos. El uso de esta aplicación para atacar sistemas sin autorización es ilegal. Los desarrolladores no son responsables del uso indebido de esta aplicación.

## Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio. 