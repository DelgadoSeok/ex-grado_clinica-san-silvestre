USE mutualista;

-- DUEÑOS
-- crear nuevo dueño
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `crear_dueno`(
    IN p_nombres VARCHAR(255),
    IN p_apellidos VARCHAR(255),
    IN p_ci VARCHAR(20),
    IN p_telf VARCHAR(255),
    IN p_direccion VARCHAR(255)
)
BEGIN
    /*
    Ejemplo de uso:
    CALL crear_dueno('Juan', 'Pérez', '12345678', '555-1234', 'Av. Principal 123');
    */
    INSERT INTO persona (nombres, apellidos, ci, telf, direccion, persona_estado_id, persona_tipo_id, descartado)
    VALUES (p_nombres, p_apellidos, p_ci, p_telf, p_direccion, 1, 1, 0);
END$$
DELIMITER ;


-- Editar Dueño
DELIMITER $$
create procedure editar_dueno(
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
  -- Ejemplo de llamada: call editar_dueno(1, 'nuevo nombre', null, 'nueva ci', null, 'nueva dirección', 2, 1, 0);
  update persona
    set nombres = ifnull(p_nombres, nombres),
        apellidos = ifnull(p_apellidos, apellidos),
        ci = ifnull(p_ci, ci),
        telf = ifnull(p_telf, telf),
        direccion = ifnull(p_direccion, direccion),
        persona_estado_id = ifnull(p_estado, persona_estado_id),
        persona_tipo_id = ifnull(p_tipo, persona_tipo_id),
        descartado = ifnull(p_descartado, descartado)
  where id = p_id and persona_tipo_id = 1;
end
$$
DELIMITER ;


-- Actualizar datos de un dueño en base a su ID.
DELIMITER $$
CREATE PROCEDURE actualizar_dueno (
    IN p_id INT,
    IN p_nombres VARCHAR(255),
    IN p_apellidos VARCHAR(255),
    IN p_ci VARCHAR(20),
    IN p_telf VARCHAR(255),
    IN p_direccion VARCHAR(255),
    IN p_persona_tipo_id INT
)
BEGIN
    -- Ejemplo de llamada:
    -- CALL actualizar_dueno(1, 'Carlos', 'Gómez', '87654321', '555-5678', 'Av. Principal 456', 3);

    UPDATE persona
    SET
        nombres = p_nombres,
        apellidos = p_apellidos,
        ci = p_ci,
        telf = p_telf,
        direccion = p_direccion,
        persona_tipo_id = p_persona_tipo_id
    WHERE id = p_id
      AND persona_estado_id = 1
      AND (descartado IS NULL OR descartado = 0);
END$$
DELIMITER ;


-- Ver dueno
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `ver_dueno`()
BEGIN
    -- Ejemplo de cómo llamar al procedimiento:
    -- CALL ver_dueno();
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
        p.persona_tipo_id = 1  -- Filtra por tipo de persona "Dueño"
    AND
        p.descartado = 0; -- traer solo duenos no descartados
END$$
DELIMITER ;


-- **Seleccionar dueño en base a su ID.**
-- **Dueño** es un registro de la tabla **Persona**, pero con el atributo **persona_estado_id**  igual a 1.
DELIMITER $$
CREATE PROCEDURE seleccionar_dueno_por_id (
    IN p_id INT
)
BEGIN
    -- Ejemplo de llamada: CALL seleccionar_dueno_por_id(1);
    SELECT *
    FROM persona
    WHERE id = p_id
      AND persona_estado_id = 1
      AND (descartado IS NULL OR descartado = 0);
END $$
DELIMITER ;


-- Descartar persona (dueno)
-- Descartar a un dueño en base a su ID. El procedimiento es el mismo tanto para duenos como para inquilinos, ya que solo pide el id y ambos están en la misma tabla
DELIMITER $$
create procedure descartar_persona(
    in p_id int
)
begin
  -- Ejemplo de llamada: call descartar_persona(1);
  update persona
    set descartado = 1
  where id = p_id;
end$$
DELIMITER ;