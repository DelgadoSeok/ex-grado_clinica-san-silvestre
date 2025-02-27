-- TRIGGER
-- El trigger verificará si ya existe una consulta registrada en el mismo día, consultorio y doctor, 
-- y si el nuevo horario se solapa con alguna consulta existente.
DELIMITER $$
CREATE TRIGGER validar_horario_unico
BEFORE INSERT ON consulta
FOR EACH ROW
BEGIN
    DECLARE existe_solapamiento INT;
    -- Verificar si hay solapamiento de horarios para el mismo día, consultorio y doctor
    SELECT COUNT(*)
    INTO existe_solapamiento
    FROM consulta
    WHERE fecha = NEW.fecha
      AND consultorio_id = NEW.consultorio_id
      AND doctor_id = NEW.doctor_id
      AND (
          (NEW.hora_ini < hora_fin AND NEW.hora_fin > hora_ini) -- Solapamiento de horarios
      );

    -- Si existe solapamiento, lanzar un error
    IF existe_solapamiento > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El horario de la consulta se solapa con otra consulta existente.';
    END IF;
END$$
DELIMITER ;

-- consultar datos
SELECT * FROM consulta WHERE fecha = '2025-02-26' AND consultorio_id = 1 AND doctor_id = 1;
-- insertar consulta que no solapa
INSERT INTO consulta (paciente_id, doctor_id, consultorio_id, importe, fecha, hora_ini, hora_fin, tipo, estado)
VALUES (6, 1, 1, 60, '2025-02-26', '10:00:00', '10:20:00', 'C', 'A');
-- verificar la ultima ingresada
SELECT * FROM consulta WHERE id = LAST_INSERT_ID();
-- insertar consulta  con doctor, consultorio y hora ya ocupada
INSERT INTO consulta (paciente_id, doctor_id, consultorio_id, importe, fecha, hora_ini, hora_fin, tipo, estado)
VALUES (4, 1, 1, 50, '2025-02-26', '08:15:00', '08:35:00', 'R', 'A');