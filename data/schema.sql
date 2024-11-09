-- Tabla de Usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    tipo_usuario VARCHAR(50) CHECK (tipo_usuario IN ('dueño', 'guardería'))
);

-- Tabla de Mascotas
CREATE TABLE mascotas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    raza VARCHAR(50),
    edad INT,
    peso DECIMAL(5, 2),
    alergias TEXT,
    vacunas TEXT,
    dueño_id INT REFERENCES usuarios(id)
);

-- Tabla de Guarderías
CREATE TABLE guarderias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(255),
    horarios VARCHAR(100),
    servicios TEXT
);

-- Tabla de Servicios
CREATE TABLE servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- Tabla de Reservas
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    estado VARCHAR(50),
    mascota_id INT REFERENCES mascotas(id),
    guarderia_id INT REFERENCES guarderias(id)
);

-- Tabla intermedia para Reservas y Servicios
CREATE TABLE reserva_servicio (
    reserva_id INT REFERENCES reservas(id),
    servicio_id INT REFERENCES servicios(id),
    PRIMARY KEY (reserva_id, servicio_id)
);

-- Tabla de Pagos
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    monto DECIMAL(10, 2),
    fecha DATE,
    metodo_pago VARCHAR(50),
    reserva_id INT REFERENCES reservas(id)
);
