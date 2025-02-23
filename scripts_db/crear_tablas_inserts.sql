-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 23-02-2025 a las 22:49:53
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `clinica`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_consultorio`
--

DROP TABLE IF EXISTS `asignacion_consultorio`;
CREATE TABLE IF NOT EXISTS `asignacion_consultorio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `dia_semana` tinyint NOT NULL,
  `hora_ini` time NOT NULL,
  `hora_fin` time NOT NULL,
  `consultorio_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `consultorio_id` (`consultorio_id`),
  KEY `doctor_id` (`doctor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `asignacion_consultorio`
--

INSERT INTO `asignacion_consultorio` (`id`, `doctor_id`, `dia_semana`, `hora_ini`, `hora_fin`, `consultorio_id`) VALUES
(1, 1, 1, '08:00:00', '12:00:00', 1),
(2, 1, 3, '08:00:00', '12:00:00', 1),
(3, 1, 5, '08:00:00', '12:00:00', 1),
(4, 2, 1, '08:00:00', '12:00:00', 2),
(5, 2, 2, '14:00:00', '18:00:00', 2),
(6, 2, 4, '08:00:00', '12:00:00', 2),
(7, 3, 2, '08:00:00', '12:00:00', 3),
(8, 3, 2, '14:00:00', '18:00:00', 1),
(9, 3, 4, '08:00:00', '18:00:00', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consulta`
--

DROP TABLE IF EXISTS `consulta`;
CREATE TABLE IF NOT EXISTS `consulta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `consultorio_id` int NOT NULL,
  `importe` double NOT NULL,
  `fecha` date NOT NULL,
  `hora_ini` time NOT NULL,
  `hora_fin` time NOT NULL,
  `tipo` enum('C','R') NOT NULL DEFAULT 'C',
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `consultorio_id` (`consultorio_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `consulta`
--

INSERT INTO `consulta` (`id`, `paciente_id`, `doctor_id`, `consultorio_id`, `importe`, `fecha`, `hora_ini`, `hora_fin`, `tipo`, `estado`) VALUES
(1, 4, 1, 1, 80, '2025-02-26', '08:00:00', '08:20:00', 'C', 'A'),
(2, 5, 1, 1, 40, '2025-02-26', '08:30:00', '08:50:00', 'R', 'A'),
(3, 6, 1, 1, 80, '2025-02-28', '08:00:00', '08:20:00', 'C', 'I'),
(4, 4, 2, 2, 40, '2025-02-25', '14:00:00', '14:20:00', 'R', 'A'),
(5, 5, 2, 2, 80, '2025-02-25', '14:30:00', '14:50:00', 'C', 'A'),
(6, 6, 2, 2, 40, '2025-02-27', '08:00:00', '08:20:00', 'R', 'A'),
(7, 4, 3, 3, 80, '2025-02-25', '08:00:00', '08:20:00', 'C', 'A'),
(8, 5, 3, 3, 40, '2025-02-25', '08:30:00', '08:50:00', 'R', 'A'),
(9, 6, 3, 3, 80, '2025-02-27', '08:00:00', '08:20:00', 'C', 'I'),
(10, 4, 3, 1, 40, '2025-02-25', '14:00:00', '14:20:00', 'R', 'A');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultorio`
--

DROP TABLE IF EXISTS `consultorio`;
CREATE TABLE IF NOT EXISTS `consultorio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nro_consultorio` varchar(20) NOT NULL,
  `fecha_registro` date NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `consultorio`
--

INSERT INTO `consultorio` (`id`, `nro_consultorio`, `fecha_registro`, `estado`) VALUES
(1, 'C-101', '2025-02-23', 'A'),
(2, 'C-102', '2025-02-23', 'A'),
(3, 'C-103', '2025-02-23', 'A'),
(4, 'C-104', '2025-02-23', 'I'),
(5, 'C-105', '2025-02-23', 'I'),
(6, 'C-106', '2025-02-23', 'I');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultorio_equipamiento`
--

DROP TABLE IF EXISTS `consultorio_equipamiento`;
CREATE TABLE IF NOT EXISTS `consultorio_equipamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultorio_id` int NOT NULL,
  `equipamiento_id` int NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `equipamiento_id` (`equipamiento_id`),
  KEY `consultorio_id` (`consultorio_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `consultorio_equipamiento`
--

INSERT INTO `consultorio_equipamiento` (`id`, `consultorio_id`, `equipamiento_id`, `estado`) VALUES
(1, 1, 1, 'A'),
(2, 1, 2, 'A'),
(3, 2, 3, 'A'),
(4, 3, 4, 'A'),
(5, 3, 5, 'A');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `doctor`
--

DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `id` int NOT NULL,
  `matricula_profesional` varchar(100) NOT NULL,
  `fecha_contratacion` date NOT NULL,
  `fecha_retiro` date DEFAULT NULL,
  `estado` enum('A','I') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `doctor`
--

INSERT INTO `doctor` (`id`, `matricula_profesional`, `fecha_contratacion`, `fecha_retiro`, `estado`) VALUES
(1, '12345678', '2025-02-01', NULL, 'A'),
(2, '98754651', '2025-01-01', NULL, 'A'),
(3, '845456465465', '2025-01-09', '2025-02-23', 'I');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `doctor_especialidad`
--

DROP TABLE IF EXISTS `doctor_especialidad`;
CREATE TABLE IF NOT EXISTS `doctor_especialidad` (
  `doctor_id` int NOT NULL,
  `especialidad_id` int NOT NULL,
  PRIMARY KEY (`doctor_id`,`especialidad_id`),
  KEY `especialidad_id` (`especialidad_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `doctor_especialidad`
--

INSERT INTO `doctor_especialidad` (`doctor_id`, `especialidad_id`) VALUES
(1, 1),
(2, 2),
(2, 3),
(3, 1),
(3, 4),
(3, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipamiento`
--

DROP TABLE IF EXISTS `equipamiento`;
CREATE TABLE IF NOT EXISTS `equipamiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `equipamiento`
--

INSERT INTO `equipamiento` (`id`, `descripcion`) VALUES
(1, 'Equipo de Rayos X'),
(2, 'Electrocardiógrafo'),
(3, 'Máquina de Ultrasonido'),
(4, 'Equipo de Rehabilitación'),
(5, 'Monitor de signos vitales');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `especialidad`
--

DROP TABLE IF EXISTS `especialidad`;
CREATE TABLE IF NOT EXISTS `especialidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `especialidad`
--

INSERT INTO `especialidad` (`id`, `descripcion`) VALUES
(1, 'Cardiología'),
(2, 'Neurología'),
(3, 'Pediatría'),
(4, 'Dermatología'),
(5, 'Oftalmología');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historia_clinica`
--

DROP TABLE IF EXISTS `historia_clinica`;
CREATE TABLE IF NOT EXISTS `historia_clinica` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nro_carpeta_fisica` int NOT NULL,
  `fecha_registro` date NOT NULL,
  `antecedentes` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `paciente_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `paciente_id` (`paciente_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `historia_clinica`
--

INSERT INTO `historia_clinica` (`id`, `nro_carpeta_fisica`, `fecha_registro`, `antecedentes`, `paciente_id`) VALUES
(1, 97, '2025-02-23', 'Antecedentes médicos del paciente con ID 4', 4),
(2, 43, '2025-02-23', 'Antecedentes médicos del paciente con ID 5', 5),
(3, 7, '2025-02-23', 'Antecedentes médicos del paciente con ID 6', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paciente`
--

DROP TABLE IF EXISTS `paciente`;
CREATE TABLE IF NOT EXISTS `paciente` (
  `id` int NOT NULL,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `paciente`
--

INSERT INTO `paciente` (`id`, `fecha_registro`) VALUES
(6, '2025-02-23'),
(5, '2025-02-23'),
(4, '2025-02-23');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

DROP TABLE IF EXISTS `persona`;
CREATE TABLE IF NOT EXISTS `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(255) NOT NULL,
  `p_apellido` varchar(255) NOT NULL,
  `s_apellido` varchar(255) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `sexo` enum('M','F') NOT NULL,
  `ci` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`id`, `nombres`, `p_apellido`, `s_apellido`, `fecha_nacimiento`, `sexo`, `ci`, `email`, `direccion`) VALUES
(1, 'Juan Moreno', 'Tapia', 'Martinez', '1990-02-02', 'M', '12345678', 'correo@correo.com', 'Calle ficticia'),
(2, 'Maria Magdalena', 'Saucedo', 'Vargas', '1995-01-01', 'F', '7854126', 'maria@gmail.com', 'Av. Mercedez'),
(3, 'Luis', 'Castañeda', 'Romero', '2000-05-12', 'M', '7894546', 'luis@gmail.com', 'Av. Pastel de cereza'),
(4, 'Juan', 'Pérez', 'Gómez', '1990-05-15', 'M', '12345678', 'juan.perez@email.com', 'Av. Siempre Viva 123'),
(5, 'María', 'López', 'Fernández', '1985-09-22', 'F', '87654321', 'maria.lopez@email.com', 'Calle Falsa 456'),
(6, 'Carlos', 'Rodríguez', 'Martínez', '2000-11-10', 'M', '11223344', 'carlos.rodriguez@email.com', 'Plaza Central 789');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `telefono`
--

DROP TABLE IF EXISTS `telefono`;
CREATE TABLE IF NOT EXISTS `telefono` (
  `id` int NOT NULL AUTO_INCREMENT,
  `persona_id` int NOT NULL,
  `nro_telefono` varchar(100) NOT NULL,
  `estado` enum('A','I') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `persona_id` (`persona_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `telefono`
--

INSERT INTO `telefono` (`id`, `persona_id`, `nro_telefono`, `estado`) VALUES
(1, 1, '555-1234', 'A'),
(2, 1, '555-5678', 'I'),
(3, 2, '555-2345', 'A'),
(4, 2, '555-6789', 'I'),
(5, 3, '555-3456', 'A'),
(6, 3, '555-7890', 'I'),
(7, 4, '555-4567', 'A'),
(8, 4, '555-8901', 'I'),
(9, 5, '555-5678', 'A'),
(10, 5, '555-9012', 'I'),
(11, 6, '555-6789', 'A'),
(12, 6, '555-0123', 'I');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

DROP TABLE IF EXISTS `usuario`;
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre_usuario`, `contrasena`) VALUES
(1, 'secretaria', '123456');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
