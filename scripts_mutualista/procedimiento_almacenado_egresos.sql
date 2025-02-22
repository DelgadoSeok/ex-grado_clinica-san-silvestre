USE mutualista;

-- EGRESOS
-- crear nuevo egreso
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_egreso`(
    IN p_observacion VARCHAR(255),
    IN p_monto DOUBLE,
    IN p_fecha DATE,
    IN p_egreso_tipo_id INTEGER
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL crear_egreso('Mantenimiento de zona Este', 500.00, '2025-02-20', 1);

    INSERT INTO egreso (observacion, monto, fecha, egreso_tipo_id, descartado)
    VALUES (p_observacion, p_monto, p_fecha, p_egreso_tipo_id, 0);
END$$
DELIMITER ;


-- ver tipos egreso
/*es de utilidad para mostrar todos los tipos de egreso en el dropdown del formulario para obtener el id 
y luego usar ese id para pasarlo como parametro al momento de crear un nuevo egreso */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_tipos_egreso`()
BEGIN
    -- Ejemplo de uso: CALL ver_tipos_egreso();
    SELECT id, descripcion FROM tipo_egreso;
END$$
DELIMITER ;


-- ver egresos
/*si se pasan 2 fechas, filtrar entre ese intervalo. si no se pasa alguna fecha, traer todo hasta antes 
o despues de esa fecha (dependiendo si es la fecha inicio o fin), si no se pasa ninguna fecha, trae todo */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_egresos`(
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    -- ejemplo de uso:
    -- CALL ver_egresos('2024-01-01', '2025-12-31')
    -- Si ambas fechas se pasan, filtra entre ambas
    IF p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL THEN
        SELECT * 
        FROM egreso 
        WHERE fecha BETWEEN p_fecha_inicio AND p_fecha_fin;
    -- Si solo se pasa la fecha de inicio, filtra los registros mayores o iguales a la fecha de inicio
    ELSEIF p_fecha_inicio IS NOT NULL THEN
        SELECT * 
        FROM egreso 
        WHERE fecha >= p_fecha_inicio;
    -- Si solo se pasa la fecha de fin, filtra los registros menores o iguales a la fecha de fin
    ELSEIF p_fecha_fin IS NOT NULL THEN
        SELECT * 
        FROM egreso 
        WHERE fecha <= p_fecha_fin;
    -- Si no se pasa ninguna fecha, trae todos los registros
    ELSE
        SELECT * 
        FROM egreso;
    END IF;
END$$
DELIMITER ;


-- ver ingresos
/*misma logica con las fechas de inicio y final que con “ver egresos” */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_ingresos`(
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    -- ejemplo de uso:
    -- CALL ver_ingresos('2024-01-01', '2025-12-31')
    -- Si ambas fechas se pasan, filtra entre ambas
    IF p_fecha_inicio IS NOT NULL AND p_fecha_fin IS NOT NULL THEN
        SELECT * 
        FROM pago 
        WHERE fecha BETWEEN p_fecha_inicio AND p_fecha_fin;
    -- Si solo se pasa la fecha de inicio, filtra los registros mayores o iguales a la fecha de inicio
    ELSEIF p_fecha_inicio IS NOT NULL THEN
        SELECT * 
        FROM pago 
        WHERE fecha >= p_fecha_inicio;
    -- Si solo se pasa la fecha de fin, filtra los registros menores o iguales a la fecha de fin
    ELSEIF p_fecha_fin IS NOT NULL THEN
        SELECT * 
        FROM pago 
        WHERE fecha <= p_fecha_fin;
    -- Si no se pasa ninguna fecha, trae todos los registros
    ELSE
        SELECT * 
        FROM pago;
    END IF;
END$$
DELIMITER ;


-- editar egreso
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `editar_egreso`(
    IN p_id INTEGER,
    IN p_observacion VARCHAR(255),
    IN p_monto DOUBLE,
    IN p_fecha DATE,
    IN p_egreso_tipo_id INTEGER,
    IN p_descartado BOOLEAN
)
BEGIN
    -- Actualiza los campos del egreso según el ID
    UPDATE egreso 
    SET 
		observacion =IFNULL(p_observacion, observacion), 
        monto = IFNULL(p_monto, monto), 
        fecha = IFNULL(p_fecha, fecha),
        egreso_tipo_id = IFNULL(p_egreso_tipo_id, egreso_tipo_id),
        descartado = IFNULL(p_descartado, descartado)
    WHERE id = p_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS editar_egreso;
SELECT * FROM egreso;
DESCRIBE egreso;