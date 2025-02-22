USE mutualista;

-- USUARIO
-- obtener rol de usuario en base a id y password
DELIMITER $$
CREATE PROCEDURE obtener_rol_usuario(IN p_usuario VARCHAR(50), IN p_contrasena VARCHAR(50))
BEGIN
    -- Ejemplo de cómo llamar al procedimiento:
    -- CALL obtener_rol_usuario('nombre_usuario', 'contraseña');
    SELECT u.usuario, ut.descripcion AS rol 
    FROM usuario u
    JOIN usuario_tipo ut ON u.usuario_tipo_id = ut.id
    WHERE u.usuario = p_usuario AND u.contrasena = p_contrasena;
END;$$
DELIMITER ;