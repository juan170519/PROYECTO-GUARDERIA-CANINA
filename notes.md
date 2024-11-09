# Notas para Correr el Proyecto de Inventario

Este proyecto utiliza Flask para la creación de un CRUD que maneja clientes, productos, órdenes y préstamos, utilizando MySQL como base de datos.

## Requisitos

- Python 3.x
- MySQL (puede estar instalado localmente o en un contenedor Docker)
- Pip (gestor de paquetes de Python)
- Docker (opcional, si deseas ejecutar MySQL en un contenedor)

### Dependencias del Proyecto

Antes de comenzar, asegúrate de instalar las dependencias del proyecto listadas en `requirements.txt`.
```plaintext
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
PyMySQL==1.0.2
```
Puedes instalar todas las dependencias ejecutando:
pip install -r requirements.txt


Configuración de la Base de Datos MySQL

Opción 1: MySQL en un Contenedor Docker

Puedes ejecutar una instancia de MySQL en un contenedor Docker usando el siguiente comando:

docker run \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=090211428 \
  -e MYSQL_DATABASE=tiendazapatos \
  -e MYSQL_USER=tiendazapatos \
  -e MYSQL_PASSWORD=090211428 \
  -d mysql:latest

Opción 2: MySQL instalado localmente

Si prefieres usar MySQL instalado localmente, asegúrate de crear una base de datos con el siguiente comando SQL:

CREATE DATABASE tiendazapatos;
CREATE USER 'tiendazapatos'@'localhost' IDENTIFIED BY '090211428';
GRANT ALL PRIVILEGES ON tiendazapatos.* TO 'tiendazapatos'@'localhost';


Estructura de la Base de Datos

A continuación, se incluyen las instrucciones SQL para crear las tablas necesarias en la base de datos tiendazapatos.

-- Tabla de clientes
CREATE TABLE t_customers (
    id VARCHAR(255) PRIMARY KEY,
    tipo_id VARCHAR(255) NOT NULL,
    primer_nombre VARCHAR(255) NOT NULL,
    primer_apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    celular VARCHAR(50),
    direccion VARCHAR(255),
    ciudad VARCHAR(255)
);

-- Tabla de productos
CREATE TABLE t_products (
    product_key VARCHAR(255) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla de órdenes
CREATE TABLE t_orders (
    id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    product_id VARCHAR(255),
    cantidad DECIMAL(10,2) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES t_customers(id),
    FOREIGN KEY (product_id) REFERENCES t_products(product_key)
);

-- Tabla de préstamos
CREATE TABLE t_loans (
    credit_id VARCHAR(255) PRIMARY KEY,
    pedido_id VARCHAR(255),
    saldo DECIMAL(10,2) NOT NULL,
    fecha_corte DATE,
    ultimo_pago DATE,
    mora_dias DECIMAL(5,2),
    cuotas_acumuladas DECIMAL(5,2),
    status VARCHAR(255),
    start_date DATE,
    due_date DATE,
    FOREIGN KEY (pedido_id) REFERENCES t_orders(id)
);

Correr el Proyecto

Para iniciar el proyecto, ejecuta el siguiente comando:

python3 app.py
