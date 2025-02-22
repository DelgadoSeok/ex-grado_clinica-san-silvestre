USE mutualista;

-- INQUILINOS
-- crear nuevo inquilino
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_inquilino`(
    IN p_nombres VARCHAR(255),
    IN p_apellidos VARCHAR(255),
    IN p_ci VARCHAR(20),
    IN p_telf VARCHAR(255),
    IN p_direccion VARCHAR(255)
)
BEGIN
    /*
    Ejemplo de uso:
    CALL crear_inquilino('Juan', 'Pérez', '12345678', '555-1234', 'Av. Principal 123');
    */
    INSERT INTO persona (nombres, apellidos, ci, telf, direccion, persona_estado_id, persona_tipo_id, descartado)
    VALUES (p_nombres, p_apellidos, p_ci, p_telf, p_direccion, 1, 2, 0);
END$$
DELIMITER ;


-- Editar inquilino
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `editar_inquilino`(
    in p_id int,
    in p_nombres varchar(255),
    in p_apellidos varchar(255),
    in p_ci varchar(20),
    in p_telf varchar(255),
    in p_direccion varchar(255),
    in p_estado int,
    in p_tipo int,
    in p_descartado tinyint
)
begin
  -- Ejemplo de llamada: call editar_inquilino(1, 'nuevo nombre', null, 'nueva ci', null, 'nueva dirección', 2, 1, 0);
  update persona
    set nombres = ifnull(p_nombres, nombres),
        apellidos = ifnull(p_apellidos, apellidos),
        ci = ifnull(p_ci, ci),
        telf = ifnull(p_telf, telf),
        direccion = ifnull(p_direccion, direccion),
        persona_estado_id = ifnull(p_estado, persona_estado_id),
        persona_tipo_id = ifnull(p_tipo, persona_tipo_id),
        descartado = ifnull(p_descartado, descartado)
  where id = p_id and persona_tipo_id = 2;
end$$
DELIMITER ;


-- Ver inquilino
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_inquilino`()
BEGIN
    -- Ejemplo de cómo llamar al procedimiento:
    -- CALL ver_inquilino();
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
        p.persona_tipo_id = 2  -- Filtra por tipo de persona "Inquilino"
    AND
        p.descartado = 0; -- traer solo los no descartados
END$$
DELIMITER ;

