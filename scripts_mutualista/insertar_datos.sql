USE mutualista;

-- Insertar tipos de usuario
INSERT INTO usuario_tipo (id, descripcion) VALUES 
(1, 'admin'), 
(2, 'secretario');

-- Insertar usuarios
INSERT INTO usuario (id, usuario, contrasena, usuario_tipo_id) 
VALUES 
(1, 'admin', 'gato78', 1), 
(2, 'secre', 'gato78', 2);



-- Insertar estados de persona
INSERT INTO persona_estado_id (id, descripcion) VALUES 
(1, 'Activo'), 
(2, 'Inactivo');

-- Insertar tipos de persona
INSERT INTO persona_tipo_id (id, descripcion) VALUES 
(1, 'Dueño'), 
(2, 'Inquilino');

-- Insertar personas ficticias
INSERT INTO persona (id, nombres, apellidos, ci, telf, direccion, persona_estado_id, persona_tipo_id, descartado) 
VALUES 
(1, 'Carlos', 'Fernández', '12345678', '789456123', 'Av. Central 101', 1, 1, 0),
(2, 'Luisa', 'Martínez', '87654321', '321654987', 'Calle Norte 202', 1, 2, 0),
(3, 'Pedro', 'López', '56781234', '741258369', 'Pasaje Sur 303', 2, 1, 1),
(4, 'Ana', 'González', '34567812', '852369741', 'Bulevar Este 404', 2, 2, 1),
(5, 'Javier', 'Ramírez', '91234567', '963852741', 'Calle Oeste 505', 1, 1, 0),
(6, 'Mariana', 'Torres', '67891234', '159753468', 'Avenida Central 606', 1, 2, 0),
(7, 'Ricardo', 'Sánchez', '23456789', '753159486', 'Camino del Sol 707', 2, 1, 1),
(8, 'Sofía', 'Ortega', '87651234', '951753852', 'Calle del Río 808', 2, 2, 1),
(9, 'Fernando', 'Vargas', '12348765', '357159852', 'Paseo del Parque 909', 1, 1, 0),
(10, 'Gabriela', 'Hernández', '98761234', '654852159', 'Avenida del Lago 1010', 1, 2, 0),
(11, 'Diego', 'Castro', '74125896', '369258147', 'Plaza Mayor 1111', 2, 1, 1),
(12, 'Paola', 'Mendoza', '36987412', '258147369', 'Calle de la Luna 1212', 2, 2, 1),
(13, 'Manuel', 'Díaz', '45678912', '789654123', 'Bulevar del Sol 1313', 1, 1, 0),
(14, 'Valentina', 'Paredes', '96321478', '147852369', 'Avenida Primavera 1414', 1, 2, 0),
(15, 'Hugo', 'Morales', '85214796', '369741258', 'Pasaje del Bosque 1515', 2, 1, 1);



-- Insertar tipos de contrato
INSERT INTO contrato_tipo (id, descripcion) VALUES 
(1, 'Alquiler'), 
(2, 'Venta');

-- Insertar estados de contrato
INSERT INTO contrato_estado (id, descripcion) VALUES 
(1, 'Vigente'), 
(2, 'Anulado');

-- Insertar contratos (solo entre personas con estado "Activo")
INSERT INTO contrato (id, contrato_tipo_id, puesto_id, fecha_ini, fecha_fin, monto, contrato_estado_id, persona1_id, persona2_id, descartado) 
VALUES 
-- Alquiler (Dueño -> Inquilino)
(1, 1, 101, '2025-01-01', '2024-12-31', 500.00, 1, 1, 2, 0),
(2, 1, 102, '2025-02-01', '2024-12-31', 600.00, 1, 5, 6, 0),

-- Venta (Dueño -> Dueño)
(3, 2, 103, '2025-03-01', NULL, 15000.00, 1, 9, 13, 0),
(4, 2, 104, '2025-04-15', NULL, 18000.00, 1, 1, 5, 0),
(5, 2, 105, '2025-05-01', NULL, 700.00, 1, 13, 10, 0);



-- Insertar sectores
INSERT INTO sector (id, descripcion) VALUES 
(1, 'Frutas y Verduras'),
(2, 'Carnes y Embutidos'),
(3, 'Pescadería'),
(4, 'Abarrotes y Granos'),
(5, 'Comida Preparada'),
(6, 'Ropa y Calzado');

-- Insertar asociaciones
INSERT INTO asociacion (id, descripcion) VALUES 
(1, 'Asociación de Vendedores de Frutas'),
(2, 'Comerciantes de Carnes Selectas'),
(3, 'Gremio de Pescaderos del Mercado Central'),
(4, 'Asociación de Abarroteros Unidos'),
(5, 'Emprendedores de Comida al Paso');

-- Insertar gremios
INSERT INTO gremio (id, descripcion) VALUES 
(1, 'Gremio de Verduleros y Fruteros'),
(2, 'Carniceros del Mercado Municipal'),
(3, 'Pescaderos Artesanales'),
(4, 'Abarroteros Independientes'),
(5, 'Cocineros y Reposteros Populares'),
(6, 'Vendedores de Ropa y Accesorios');



-- Insertar puesto_estado
INSERT INTO puesto_estado (id, descripcion) VALUES 
(1, 'Atendiendo'),
(2, 'Cerrado por deuda');



-- Insertar puestos
INSERT INTO puesto (id, numero, asociacion_id, gremio_id, sector_id, puesto_estado_id, dueno_id, inquilino_id, descartado) 
VALUES 
(101, 1, 1, 1, 1, 1, 1, 2, 0),  -- Puesto de frutas (Dueño: Persona 1, Inquilino: Persona 2)
(102, 2, 2, 2, 2, 1, 5, 6, 0),  -- Puesto de carnes (Dueño: Persona 5, Inquilino: Persona 6)
(103, 3, 3, 3, 3, 1, 9, NULL, 0),  -- Puesto de pescadería (Dueño: Persona 9, Sin inquilino - Venta)
(104, 4, 4, 4, 4, 1, 1, 5, 0),  -- Puesto de abarrotes (Dueño: Persona 1, Comprador: Persona 5 - Venta)
(105, 5, 5, 5, 5, 1, 13, 10, 0),  -- Puesto de comida (Dueño: Persona 13, Inquilino: Persona 10)
(106, 6, 1, 1, 1, 2, 3, NULL, 0),  -- Puesto de frutas cerrado por deuda (Dueño: Persona 3, sin inquilino)
(107, 7, 2, 2, 2, 1, 7, NULL, 0),  -- Puesto de carnes activo (Dueño: Persona 7)
(108, 8, 3, 3, 3, 1, 11, NULL, 0);  -- Puesto de pescadería activo (Dueño: Persona 11)



-- Insertar estados de deuda
INSERT INTO deuda_estado (id, descripcion) VALUES 
(1, 'Pagado'),
(2, 'No pagado');

-- Insertar tipos de egreso
INSERT INTO tipo_egreso (id, descripcion) VALUES 
(1, 'Mantenimiento de extinguidores'),
(2, 'Energía eléctrica común'),
(3, 'Servicio de agua en común'),
(4, 'Mantenimiento cámaras de seguridad'),
(5, 'Sueldos guardias de seguridad'),
(6, 'Limpieza del mercado');



-- Insertar deudas para el puesto 101
INSERT INTO deuda (fecha, monto, puesto_id, deuda_estado_id, descartado) 
VALUES 
('2025-02-18', 200.00, 101, 2, 0),  -- Primera deuda, misma fecha y monto
('2025-02-18', 250.00, 101, 2, 0);  -- Segunda deuda, diferente monto

-- Insertar deudas para el puesto 102
INSERT INTO deuda (fecha, monto, puesto_id, deuda_estado_id, descartado) 
VALUES 
('2025-02-18', 300.00, 102, 2, 0),  -- Primera deuda, misma fecha y monto
('2025-02-18', 350.00, 102, 2, 0);  -- Segunda deuda, diferente monto


