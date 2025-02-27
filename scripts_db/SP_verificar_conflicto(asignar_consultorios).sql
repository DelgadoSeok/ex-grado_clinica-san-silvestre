DELIMITER //

CREATE PROCEDURE sp_verificar_conflicto (
    IN p_consultorio_id INT,
    IN p_dia_semana VARCHAR(10),
    IN p_hora_ini TIME,
    IN p_hora_fin TIME,
    OUT p_conflicto TINYINT
)
BEGIN
    DECLARE v_total INT DEFAULT 0;
    
    SELECT COUNT(*) INTO v_total
    FROM asignacion_consultorio
    WHERE consultorio_id = p_consultorio_id
      AND dia_semana = p_dia_semana
      AND estado = 'A'
      AND (hora_ini < p_hora_fin AND hora_fin > p_hora_ini);
    
    IF v_total > 0 THEN
        SET p_conflicto = 1;
    ELSE
        SET p_conflicto = 0;
    END IF;
END //

DELIMITER ;
