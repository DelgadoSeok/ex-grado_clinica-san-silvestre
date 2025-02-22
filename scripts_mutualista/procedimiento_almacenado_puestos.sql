USE mutualista;

-- PUESTOS
-- registrar nuevo puesto
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `registrar_puesto`(
    IN p_numero INTEGER,
    IN p_asociacion_id INTEGER,
    IN p_gremio_id INTEGER,
    IN p_sector_id INTEGER,
    IN p_puesto_estado_id INTEGER,
    IN p_dueno_id INTEGER,
    IN p_inquilino_id INTEGER
)
BEGIN
    /*
    Ejemplo de ejecución:
    CALL registrar_puesto(101, 1, 2, 3, 1, 5, NULL);
    */
    INSERT INTO puesto (numero, asociacion_id, gremio_id, sector_id, puesto_estado_id, dueno_id, inquilino_id, descartado)
    VALUES (p_numero, p_asociacion_id, p_gremio_id, p_sector_id, p_puesto_estado_id, p_dueno_id, p_inquilino_id, 0);
END$$
DELIMITER ;


-- editar puesto existente
DELIMITER $$
CREATE PROCEDURE editar_puesto(
    IN p_id INTEGER,
    IN p_numero INTEGER,
    IN p_asociacion_id INTEGER,
    IN p_gremio_id INTEGER,
    IN p_sector_id INTEGER,
    IN p_puesto_estado_id INTEGER,
    IN p_dueno_id INTEGER,
    IN p_inquilino_id INTEGER
)
BEGIN
    /*
    Ejemplo de ejecución:
    -- Actualizar solo el número, sin cambiar los demás campos:
    CALL editar_puesto(1, 102, NULL, NULL, NULL, NULL, NULL, NULL);
    */
    UPDATE puesto
    SET numero = COALESCE(p_numero, numero),
        asociacion_id = COALESCE(p_asociacion_id, asociacion_id),
        gremio_id = COALESCE(p_gremio_id, gremio_id),
        sector_id = COALESCE(p_sector_id, sector_id),
        puesto_estado_id = COALESCE(p_puesto_estado_id, puesto_estado_id),
        dueno_id = COALESCE(p_dueno_id, dueno_id),
        inquilino_id = COALESCE(p_inquilino_id, inquilino_id)
    WHERE id = p_id;
END$$
DELIMITER;

-- ver puestos
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_puestos`()
BEGIN
    -- Ejemplo de como llamarlo: CALL ver_puestos();
    SELECT 
        p.id AS puesto_id,
        p.numero,
        a.descripcion AS asociacion,
        g.descripcion AS gremio,
        s.descripcion AS sector,
        pe.descripcion AS puesto_estado,
        per1.nombres AS dueno_nombres,
        per2.nombres AS inquilino_nombres
    FROM 
        puesto p
    LEFT JOIN asociacion a ON p.asociacion_id = a.id
    LEFT JOIN gremio g ON p.gremio_id = g.id
    LEFT JOIN sector s ON p.sector_id = s.id
    LEFT JOIN puesto_estado pe ON p.puesto_estado_id = pe.id
    LEFT JOIN persona per1 ON p.dueno_id = per1.id
    LEFT JOIN persona per2 ON p.inquilino_id = per2.id
    -- solo traer filas no descartadas
    WHERE p.descartado = 0;
END$$
DELIMITER ;

-- obtener_puesto_por_id
DELIMITER $$

CREATE PROCEDURE obtener_puesto_por_id(IN p_id INT)
BEGIN
    SELECT * FROM puesto WHERE id = p_id;
END $$

DELIMITER ;

-- Eliminar puesto existente (nos e puede eliminar porque otras dependen de ella
/*DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `eliminar_puesto`(
    IN p_id INTEGER
)
BEGIN

    -- Verificar si el puesto existe
    IF EXISTS (SELECT 1 FROM puesto WHERE id = p_id) THEN
        DELETE FROM puesto WHERE id = p_id;
        SELECT 'success' AS status; 
    ELSE
        SELECT 'error' AS status, 'Puesto no encontrado' AS message;  
    END IF;
END$$
DELIMITER ;*/
    /*
    Ejemplo de ejecución:
    CALL eliminar_puesto(1);
    */
DROP PROCEDURE IF EXISTS editar_puesto;

CALL editar_puesto(109, 9, NULL, NULL, NULL, NULL, NULL, NULL);

SELECT * FROM puesto;
DESCRIBE puesto;
SELECT * FROM puesto WHERE id = 101;