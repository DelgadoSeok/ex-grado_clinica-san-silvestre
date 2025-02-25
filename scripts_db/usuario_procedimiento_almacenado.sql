DELIMITER $$
CREATE PROCEDURE obtener_rol_usuario(IN nombre_usuario VARCHAR(100), IN contrasena VARCHAR(100))
BEGIN
	-- Ejemplo de cómo llamar al procedimiento:
    -- CALL obtener_rol_usuario('nombre_usuario', 'contraseña');
    SELECT id, nombre_usuario, contrasena, nombre_usuario AS rol  
    FROM usuario
    WHERE nombre_usuario = nombre_usuario AND contrasena = contrasena;
END $$
DELIMITER ;