-- MySQL Setup - CONFIGURACIÓN VULNERABLE PARA RCE
-- ⚠️ SOLO PARA FINES EDUCATIVOS - NUNCA EN PRODUCCIÓN ⚠️

CREATE DATABASE IF NOT EXISTS vulnerable_db;
USE vulnerable_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, email) VALUES
('admin', 'admin123', 'admin@example.com'),
('user1', 'password123', 'user1@example.com'),
('user2', 'secret456', 'user2@example.com'),
('test', 'test123', 'test@example.com');

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    category VARCHAR(50)
);

INSERT INTO products (name, price, description, category) VALUES
('Laptop', 999.99, 'High performance laptop', 'Electronics'),
('Mouse', 29.99, 'Wireless mouse', 'Electronics'),
('Keyboard', 59.99, 'Mechanical keyboard', 'Electronics'),
('Monitor', 299.99, '27 inch monitor', 'Electronics');
