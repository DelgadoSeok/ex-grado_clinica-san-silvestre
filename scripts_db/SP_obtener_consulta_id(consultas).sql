USE clinica_san_silvestre;
DELIMITER $$
CREATE PROCEDURE ObtenerConsultaPorID(IN consulta_id INT)
BEGIN
    SELECT 
        c.*, 
        CONCAT(pp.nombres, ' ', pp.p_apellido, ' ', pp.s_apellido) AS paciente_nombre,
        CONCAT(pd.nombres, ' ', pd.p_apellido, ' ', pd.s_apellido) AS doctor_nombre,
        co.nro_consultorio
    FROM 
        consulta c
    JOIN 
        persona pp ON c.paciente_id = pp.id
    JOIN 
        doctor d ON c.doctor_id = d.id
    JOIN 
        persona pd ON d.id = pd.id
    JOIN 
        consultorio co ON c.consultorio_id = co.id
    WHERE 
        c.id = consulta_id;
END $$

DELIMITER ;

CALL ObtenerConsultaPorID(1);