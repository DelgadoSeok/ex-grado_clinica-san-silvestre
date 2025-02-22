USE mutualista;

-- CONTRATOS
-- Traer lista de tipos de contrato
/* consultas utiles para el formulario, donde hay que seleccionar el tipo de contrato al crear uno nuevo.
se puede obtener los datos, cargarlos al dropdown y que cuando se seleccionen una opcion, se recupere el id, 
dicho id es el que se tiene que colocar en el sp crear_contrato para registrar un nuevo contra*/
DELIMITER $$
CREATE PROCEDURE ver_tipos_contrato()
BEGIN
    -- Ejemplo de uso: CALL ver_tipos_contrato();
    SELECT id, descripcion FROM contrato_tipo;
END;$$
DELIMITER ;


-- traer lista de puestos
-- esto ya esta en puestos 
/*DELIMITER $$
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
*/

-- traer estado de contrato:
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_contrato_estado`()
BEGIN
    -- Ejemplo de como llamarlo: CALL ver_contrato_estado();
    SELECT 
        id,
        descripcion
    FROM 
        contrato_estado;
END$$
DELIMITER ;


-- traer lista de todas las personas
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_personas`()
BEGIN
    -- Ejemplo de cómo llamar al procedimiento:
    -- CALL ver_personas();
    SELECT 
        p.id,
        p.nombres,
        p.apellidos,
        p.ci,
        p.telf,
        p.direccion,
        pe.descripcion AS estado_persona,
        pt.descripcion AS tipo_persona
    FROM 
        persona p
    INNER JOIN 
        persona_estado_id pe ON p.persona_estado_id = pe.id
    INNER JOIN 
        persona_tipo_id pt ON p.persona_tipo_id = pt.id
    WHERE 
        p.descartado = 0; -- traer solo los no descartados
END$$
DELIMITER;


-- consultas para regsitrar o editar datos de contato
-- Crear contrato
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_contrato`(
    IN p_contrato_tipo_id INT,
    IN p_puesto_id INT,
    IN p_fecha_ini DATE,
    IN p_fecha_fin DATE,
    IN p_monto DOUBLE,
    IN p_contrato_estado_id INT,
    IN p_persona1_id INT,
    IN p_persona2_id INT,
    IN p_descartado TINYINT
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL crear_contrato(1, 101, '2025-01-01', '2025-12-31', 500.00, 1, 1, 2, 0);
    INSERT INTO contrato (
        contrato_tipo_id,
        puesto_id,
        fecha_ini,
        fecha_fin,
        monto,
        contrato_estado_id,
        persona1_id,
        persona2_id,
        descartado
    ) 
    VALUES (
        p_contrato_tipo_id,
        p_puesto_id,
        p_fecha_ini,
        p_fecha_fin,
        p_monto,
        p_contrato_estado_id,
        p_persona1_id,
        p_persona2_id,
        p_descartado
    );
END$$
DELIMITER ;


-- Editar contrato
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `editar_contrato`(
    IN p_contrato_id INT,
    IN p_contrato_tipo_id INT,
    IN p_puesto_id INT,
    IN p_fecha_ini DATE,
    IN p_fecha_fin DATE,
    IN p_monto DOUBLE,
    IN p_contrato_estado_id INT,
    IN p_persona1_id INT,
    IN p_persona2_id INT,
    IN p_descartado TINYINT
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL editar_contrato(1, NULL, 101, '2025-02-01', NULL, 600.00, 1, NULL, NULL, 0);
    UPDATE contrato
    SET 
        contrato_tipo_id = IFNULL(p_contrato_tipo_id, contrato.contrato_tipo_id),
        puesto_id = IFNULL(p_puesto_id, contrato.puesto_id),
        fecha_ini = IFNULL(p_fecha_ini, contrato.fecha_ini),
        fecha_fin = IFNULL(p_fecha_fin, contrato.fecha_fin),
        monto = IFNULL(p_monto, contrato.monto),
        contrato_estado_id = IFNULL(p_contrato_estado_id, contrato.contrato_estado_id),
        persona1_id = IFNULL(p_persona1_id, contrato.persona1_id),
        persona2_id = IFNULL(p_persona2_id, contrato.persona2_id),
        descartado = IFNULL(p_descartado, contrato.descartado)
    WHERE id = p_contrato_id;
END$$
DELIMITER ;


-- Anular contrato
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `anular_contrato`(
    IN p_contrato_id INT
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL anular_contrato(1);

    UPDATE contrato
    SET 
        contrato_estado_id = 2
    WHERE id = p_contrato_id;
END$$
DELIMITER;


-- Descartar contrato
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `descartar_contrato`(
    IN p_contrato_id INT
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL descartar_contrato(1);
    UPDATE contrato
    SET 
        descartado = 1
    WHERE id = p_contrato_id;
END$$
DELIMITER ;

-- ver contratos
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_contratos`()
BEGIN
    -- Ejemplo de cómo llamarlo: CALL ver_contratos();
    SELECT 
        contrato.id AS contrato_id,
        contrato_tipo.descripcion AS tipo_contrato,
        puesto.numero AS puesto_numero,
        contrato.fecha_ini,
        contrato.fecha_fin,
        contrato.monto,
        contrato_estado.descripcion AS estado_contrato,
        persona1.nombres AS persona1_nombres,
        persona1.apellidos AS persona1_apellidos,
        persona2.nombres AS persona2_nombres,
        persona2.apellidos AS persona2_apellidos
    FROM 
        contrato
    JOIN 
        contrato_tipo ON contrato.contrato_tipo_id = contrato_tipo.id
    LEFT JOIN 
        puesto ON contrato.puesto_id = puesto.id
    LEFT JOIN 
        contrato_estado ON contrato.contrato_estado_id = contrato_estado.id
    LEFT JOIN 
        persona AS persona1 ON contrato.persona1_id = persona1.id
    LEFT JOIN 
        persona AS persona2 ON contrato.persona2_id = persona2.id
    WHERE 
        contrato.descartado = 0;
END$$
DELIMITER ;