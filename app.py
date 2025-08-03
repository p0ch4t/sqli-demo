from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import mysql.connector
import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
import logging
import pyodbc
import oracledb

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configurations
DB_CONFIGS = {
    'mysql': {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', 'password'),
        'database': os.getenv('MYSQL_DATABASE', 'vulnerable_db'),
        'port': int(os.getenv('MYSQL_PORT', 3306))
    },
    'postgresql': {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password'),
        'database': os.getenv('POSTGRES_DATABASE', 'vulnerable_db'),
        'port': int(os.getenv('POSTGRES_PORT', 5432))
    },
    'sqlserver': {
        'server': os.getenv('SQLSERVER_HOST', 'localhost'),
        'database': os.getenv('SQLSERVER_DATABASE', 'vulnerable_db'),
        'username': os.getenv('SQLSERVER_USER', 'sa'),
        'password': os.getenv('SQLSERVER_PASSWORD', 'password'),
        'port': int(os.getenv('SQLSERVER_PORT', 1433))
    },
    'oracle': {
        'host': os.getenv('ORACLE_HOST', 'localhost'),
        'port': int(os.getenv('ORACLE_PORT', 1521)),
        'service_name': os.getenv('ORACLE_SERVICE', 'freepdb1'),
        'user': os.getenv('ORACLE_USER', 'system'),
        'password': os.getenv('ORACLE_PASSWORD', 'password')
    }
}

def initialize_sqlserver_db():
    try:
        logger.info("Conectando a la base master para inicializar vulnerable_db...")
        # Conexión a master para crear la base si no existe
        conn_master = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={DB_CONFIGS['sqlserver']['server']},{DB_CONFIGS['sqlserver']['port']};"
            f"DATABASE=master;"
            f"UID={DB_CONFIGS['sqlserver']['username']};"
            f"PWD={DB_CONFIGS['sqlserver']['password']};"
            "TrustServerCertificate=yes;"
        )
        conn_master.autocommit = True
        cursor_master = conn_master.cursor()

        # Crear DB si no existe
        cursor_master.execute("""
            IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'vulnerable_db')
            BEGIN
                CREATE DATABASE vulnerable_db;
                PRINT 'Base vulnerable_db creada';
            END
        """)
        logger.info("Base vulnerable_db creada o ya existente.")
        cursor_master.close()
        conn_master.close()

        logger.info("Conectando a vulnerable_db para crear tablas y datos iniciales...")
        # Conectar a vulnerable_db para crear tablas y datos
        conn_db = get_sqlserver_connection()
        cursor_db = conn_db.cursor()

        # Crear tabla users si no existe
        cursor_db.execute("""
            IF OBJECT_ID('users', 'U') IS NULL
            BEGIN
                CREATE TABLE users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    created_at DATETIME DEFAULT GETDATE()
                );
                PRINT 'Tabla users creada';
            END
        """)
        logger.info("Tabla users creada o ya existente.")

        # Insertar datos si tabla users vacía
        cursor_db.execute("SELECT COUNT(*) FROM users")
        count_users = cursor_db.fetchone()[0]
        if count_users == 0:
            cursor_db.execute("""
                INSERT INTO users (username, password, email) VALUES
                ('admin', 'admin123', 'admin@example.com'),
                ('user1', 'password123', 'user1@example.com'),
                ('user2', 'secret456', 'user2@example.com'),
                ('test', 'test123', 'test@example.com');
            """)
            logger.info("Datos iniciales insertados en tabla users.")
        else:
            logger.info("Tabla users ya contiene datos, no se insertó nada.")

        # Similar para tabla products...
        cursor_db.execute("""
            IF OBJECT_ID('products', 'U') IS NULL
            BEGIN
                CREATE TABLE products (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    description TEXT,
                    category VARCHAR(50)
                );
                PRINT 'Tabla products creada';
            END
        """)
        logger.info("Tabla products creada o ya existente.")

        cursor_db.execute("SELECT COUNT(*) FROM products")
        count_products = cursor_db.fetchone()[0]
        if count_products == 0:
            cursor_db.execute("""
                INSERT INTO products (name, price, description, category) VALUES
                ('Laptop', 999.99, 'High performance laptop', 'Electronics'),
                ('Mouse', 29.99, 'Wireless mouse', 'Electronics'),
                ('Keyboard', 59.99, 'Mechanical keyboard', 'Electronics'),
                ('Monitor', 299.99, '27 inch monitor', 'Electronics');
            """)
            logger.info("Datos iniciales insertados en tabla products.")
        else:
            logger.info("Tabla products ya contiene datos, no se insertó nada.")

        conn_db.commit()
        cursor_db.close()
        conn_db.close()

        logger.info("Inicialización SQL Server finalizada correctamente.")
    except Exception as e:
        logger.error(f"Error inicializando SQL Server DB: {e}")

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIGS['mysql'])
        return conn
    except Exception as e:
        logger.error(f"MySQL connection error: {e}")
        return None

def get_postgresql_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIGS['postgresql'])
        return conn
    except Exception as e:
        logger.error(f"PostgreSQL connection error: {e}")
        return None

def get_sqlserver_connection():
    try:
        conn_str_db = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={DB_CONFIGS['sqlserver']['server']},{DB_CONFIGS['sqlserver']['port']};"
            f"DATABASE={DB_CONFIGS['sqlserver']['database']};"
            f"UID={DB_CONFIGS['sqlserver']['username']};"
            f"PWD={DB_CONFIGS['sqlserver']['password']};"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str_db, autocommit=True)
        return conn
    except Exception as e:
        logger.error(f"SQL Server connection error: {e}")
        return None

def get_oracle_connection():
    try:
        dsn = oracledb.makedsn(
            DB_CONFIGS['oracle']['host'],
            DB_CONFIGS['oracle']['port'],
            service_name=DB_CONFIGS['oracle']['service_name']
        )
        conn = oracledb.connect(
            user=DB_CONFIGS['oracle']['user'],
            password=DB_CONFIGS['oracle']['password'],
            dsn=dsn
        )
        return conn
    except Exception as e:
        logger.error(f"Oracle connection error: {e}")
        return None

def execute_query_vulnerable(db_type, query):
    conn = None
    try:
        if db_type == 'mysql':
            conn = get_mysql_connection()
        elif db_type == 'postgresql':
            conn = get_postgresql_connection()
        elif db_type == 'sqlserver':
            conn = get_sqlserver_connection()
        elif db_type == 'oracle':
            conn = get_oracle_connection()

        if not conn:
            return {"error": f"Could not connect to {db_type}"}

        cursor = conn.cursor()
        cursor.execute(query)

        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            return {"results": results, "columns": columns}
        else:
            conn.commit()
            return {"message": "Query executed successfully", "affected_rows": cursor.rowcount}

    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def execute_query():
    db_type = request.form.get('database')
    user = request.form.get('user')
    query = f"SELECT * FROM users WHERE username = '{user}'"
    if not user:
        flash('Please enter a user', 'error')
        return redirect(url_for('index'))

    result = execute_query_vulnerable(db_type, query)
    return render_template('index.html', result=result, last_query=query, last_db=db_type)

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    db_type = data.get('db_type')
    user = request.form.get('user')
    query = f"SELECT * FROM users WHERE username = '{user}'"

    if not user:
        return jsonify({"error": "User is required"}), 400

    result = execute_query_vulnerable(db_type, query)
    return jsonify(result)

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    logger.info("Iniciando aplicación y base de datos...")
    initialize_sqlserver_db()
    logger.info("Inicio finalizado. Corriendo Flask.")
    app.run(debug=True, host='0.0.0.0', port=5000)
