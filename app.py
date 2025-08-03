from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import mysql.connector
import psycopg2
import sqlite3
import os
from dotenv import load_dotenv
import logging

try:
    import pyodbc
    SQLSERVER_AVAILABLE = True
except ImportError:
    SQLSERVER_AVAILABLE = False
    print("⚠️  pyodbc no disponible. SQL Server no estará disponible.")
try:
    import oracledb
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    print("⚠️  cx_Oracle no disponible. Oracle no estará disponible.")

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

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

def get_mysql_connection():
    """Get MySQL connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIGS['mysql'])
        return conn
    except Exception as e:
        logger.error(f"MySQL connection error: {e}")
        return None

def get_postgresql_connection():
    """Get PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIGS['postgresql'])
        return conn
    except Exception as e:
        logger.error(f"PostgreSQL connection error: {e}")
        return None

def get_sqlserver_connection():
    """Get SQL Server connection"""
    if not SQLSERVER_AVAILABLE:
        return None
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={DB_CONFIGS['sqlserver']['server']},{DB_CONFIGS['sqlserver']['port']};"
            f"DATABASE={DB_CONFIGS['sqlserver']['database']};"
            f"UID={DB_CONFIGS['sqlserver']['username']};"
            f"PWD={DB_CONFIGS['sqlserver']['password']};"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logger.error(f"SQL Server connection error: {e}")
        return None

def get_oracle_connection():
    """Get Oracle connection with oracledb thin mode"""
    if not ORACLE_AVAILABLE:
        return None
    try:
        dsn = oracledb.makedsn(
            DB_CONFIGS['oracle']['host'],
            DB_CONFIGS['oracle']['port'],
            service_name=DB_CONFIGS['oracle']['service_name']
        )
        # Thin mode por defecto, no requiere cliente nativo
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
    """Execute query with SQL injection vulnerability"""
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
        
        # VULNERABLE: Direct string concatenation - SQL Injection vulnerability
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
    app.run(debug=True, host='0.0.0.0', port=5000) 
