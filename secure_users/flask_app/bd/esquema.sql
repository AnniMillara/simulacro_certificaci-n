DROP DATABASE IF EXISTS esquema;
CREATE DATABASE esquema CHARACTER SET utf8mb4;
USE esquema;

-- ============================================================
-- TABLA 1: USUARIOS (idéntica en TODOS los escenarios)
-- ============================================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA 2: CATEGORÍAS (idéntica en TODOS los escenarios)
-- ============================================================
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA 3: ENTIDAD PRINCIPAL (cambia según escenario)
-- ============================================================
CREATE TABLE entidades (
    id_entidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    -- ↓↓↓ CAMPOS ESPECÍFICOS SEGÚN ESCENARIO ↓↓↓
    fecha DATE,
    precio DECIMAL(10,2),
    stock INT,
    -- ↑↑↑ ↑↑↑
    categoria_id INT NOT NULL,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id_categoria),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Datos de prueba
INSERT INTO categorias (nombre, descripcion) VALUES
('General', 'Categoría por defecto'),
('Personal', 'Cosas personales'),
('Trabajo', 'Cosas del trabajo');