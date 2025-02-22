USE mutualista;

-- PAGOS
-- Registrar nuevo pago.
-- Esto se ejecuta cuando se presione el boton “pagar” en la tabla de deudas pendientes por pagar.
DELIMITER $$
CREATE PROCEDURE registrar_pago(
    IN p_puesto_id INT,
    IN p_monto DOUBLE,
    IN p_monto_interes DOUBLE,
    IN p_fecha DATE,
    IN p_deuda_id INT
)
BEGIN
		-- Ejemplo de uso:
		-- CALL RegistrarPago('2025-02-18', 500.00, 50.00, 3);
    -- Insertar el pago en la tabla pago
    INSERT INTO pago (fecha, monto, monto_interes, deuda_id)
    VALUES (p_fecha, p_monto, p_monto_interes, p_deuda_id);
    -- Actualizar el estado de la deuda a "Pagado"
    UPDATE deuda 
	    SET deuda_estado_id = 1
    WHERE id = p_deuda_id;
END;$$
DELIMITER ;


-- Crear deuda
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_deuda`(
    IN p_fecha DATE,
    IN p_monto FLOAT
)
BEGIN
    -- inserta datos en la tabla deuda, 1 fila por cada puesto existente que no este descartado
    -- Crear una variable para almacenar el id del puesto
    DECLARE done INT DEFAULT 0;
    DECLARE v_puesto_id INT;
    DECLARE puesto_cursor CURSOR FOR
        SELECT id
        FROM puesto
        WHERE descartado = 0;
    -- Manejar el fin del cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    -- Abrir el cursor para recorrer los puestos
    OPEN puesto_cursor;
    -- Recorrer cada puesto y hacer el insert
    REPEAT
        FETCH puesto_cursor INTO v_puesto_id;
        IF NOT done THEN
            INSERT INTO deuda (puesto_id, fecha, monto, deuda_estado_id, descartado)
            VALUES (v_puesto_id, p_fecha, p_monto, 2, 0);
        END IF;
    UNTIL done END REPEAT;
    -- Cerrar el cursor después de terminar
    CLOSE puesto_cursor;
END$$
DELIMITER ;


-- ver deudas
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_deudas`()
BEGIN
    SELECT 
        d.id,
        d.fecha,
        d.monto,
        p.numero AS puesto_nro,
        CONCAT_WS(' ',pe.nombres,pe.apellidos) AS puesto_dueno, 
        de.descripcion AS deuda_estado,
        -- Cálculo del interés basado en la diferencia de días
        FLOOR(DATEDIFF(NOW(), d.fecha) / 30) * (d.monto * 0.25) AS interes,
        d.descartado
    FROM deuda d
    -- join con tabla de detalld e tipo de deuda
    LEFT JOIN deuda_estado de ON d.deuda_estado_id = de.id
    -- Realizamos el JOIN con la tabla 'puesto' para obtener nro de puesto
    LEFT JOIN puesto p ON d.puesto_id = p.id
    -- join con tabla de persona para obtener el nombre del dueno de puesto
    LEFT JOIN persona pe ON p.dueno_id = pe.id

    WHERE d.deuda_estado_id = 2
    
    ORDER BY d.fecha desc;
END$$
DELIMITER ;



-- reporte de pagos pdf
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `reporte_pago`(IN p_deuda_id INT)
BEGIN
    DECLARE v_puesto_id INT;

    -- Obtener el puesto_id de la deuda dada
    SELECT puesto_id INTO v_puesto_id
    FROM deuda
    WHERE id = p_deuda_id;

    -- Seleccionar los pagos de la deuda específica y unirlos con las deudas del mismo puesto
    (SELECT p.fecha, p.monto, p.monto_interes, 'Pagada' AS estado
     FROM pago p
     WHERE p.deuda_id = p_deuda_id)
     
    UNION ALL
    
    (SELECT
    d.fecha,
    d.monto,
    -- Cálculo del interés basado en la diferencia de días
    FLOOR(DATEDIFF(NOW(), d.fecha) / 30) * (d.monto * 0.25) AS monto_interes,
    de.descripcion AS estado
     FROM deuda d
     JOIN deuda_estado de ON d.deuda_estado_id = de.id
     WHERE d.puesto_id = v_puesto_id
      -- solo no pagados
     AND d.deuda_estado_id = 2
     );
     
END$$
DELIMITER ;