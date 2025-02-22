USE mutualista;

CREATE TABLE `persona` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`nombres` VARCHAR(255) NOT NULL,
	`apellidos` VARCHAR(255) NOT NULL,
	`ci` VARCHAR(20) NOT NULL,
	`telf` VARCHAR(255),
	`direccion` VARCHAR(255),
	`persona_estado_id` INTEGER NOT NULL,
	`persona_tipo_id` INTEGER NOT NULL,
	`descartado` TINYINT,
	PRIMARY KEY(`id`)
);


CREATE TABLE `contrato` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`contrato_tipo_id` INTEGER NOT NULL,
	`puesto_id` INTEGER,
	`fecha_ini` DATE,
	`fecha_fin` DATE,
	`monto` DOUBLE,
	`contrato_estado_id` INTEGER,
	`persona1_id` INTEGER,
	`persona2_id` INTEGER,
	`descartado` TINYINT,
	PRIMARY KEY(`id`)
);


CREATE TABLE `contrato_tipo` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `puesto` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`numero` INTEGER NOT NULL,
	`asociacion_id` INTEGER,
	`gremio_id` INTEGER,
	`sector_id` INTEGER,
	`puesto_estado_id` INTEGER,
	`dueno_id` INTEGER NOT NULL,
	`inquilino_id` INTEGER,
	`descartado` TINYINT,
	PRIMARY KEY(`id`)
);


CREATE TABLE `usuario` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`usuario` VARCHAR(50) NOT NULL,
	`contrasena` VARCHAR(50) NOT NULL,
	`usuario_tipo_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `persona_estado_id` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `deuda` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`fecha` DATE NOT NULL,
	`monto` DOUBLE NOT NULL,
	`puesto_id` INTEGER NOT NULL,
	`deuda_estado_id` INTEGER NOT NULL,
	`descartado` TINYINT,
	PRIMARY KEY(`id`)
);


CREATE TABLE `pago` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`fecha` DATE NOT NULL,
	`monto` DOUBLE NOT NULL,
	`monto_interes` DOUBLE,
	`deuda_id` INTEGER NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `egreso` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`observacion` VARCHAR(255),
	`monto` DOUBLE NOT NULL,
	`fecha` DATE NOT NULL,
	`egreso_tipo_id` INTEGER NOT NULL,
	`descartado` TINYINT,
	PRIMARY KEY(`id`)
);


CREATE TABLE `tipo_egreso` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `usuario_tipo` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `persona_tipo_id` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(255),
	PRIMARY KEY(`id`)
);


CREATE TABLE `contrato_estado` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `asociacion` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `sector` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `gremio` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50),
	PRIMARY KEY(`id`)
);


CREATE TABLE `deuda_estado` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(50) NOT NULL,
	PRIMARY KEY(`id`)
);


CREATE TABLE `puesto_estado` (
	`id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`descripcion` VARCHAR(255) NOT NULL,
	PRIMARY KEY(`id`)
);


ALTER TABLE `contrato`
ADD FOREIGN KEY(`contrato_tipo_id`) REFERENCES `contrato_tipo`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `contrato`
ADD FOREIGN KEY(`persona1_id`) REFERENCES `persona`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `contrato`
ADD FOREIGN KEY(`persona2_id`) REFERENCES `persona`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `deuda`
ADD FOREIGN KEY(`puesto_id`) REFERENCES `puesto`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `pago`
ADD FOREIGN KEY(`monto_interes`) REFERENCES `deuda`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `contrato`
ADD FOREIGN KEY(`puesto_id`) REFERENCES `puesto`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `usuario`
ADD FOREIGN KEY(`usuario_tipo_id`) REFERENCES `usuario_tipo`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `persona`
ADD FOREIGN KEY(`persona_tipo_id`) REFERENCES `persona_tipo_id`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `persona`
ADD FOREIGN KEY(`persona_estado_id`) REFERENCES `persona_estado_id`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `contrato`
ADD FOREIGN KEY(`contrato_estado_id`) REFERENCES `contrato_estado`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`asociacion_id`) REFERENCES `asociacion`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`gremio_id`) REFERENCES `gremio`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`sector_id`) REFERENCES `sector`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `deuda`
ADD FOREIGN KEY(`deuda_estado_id`) REFERENCES `deuda_estado`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`puesto_estado_id`) REFERENCES `puesto_estado`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`dueno_id`) REFERENCES `persona`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `puesto`
ADD FOREIGN KEY(`inquilino_id`) REFERENCES `persona`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `egreso`
ADD FOREIGN KEY(`egreso_tipo_id`) REFERENCES `tipo_egreso`(`id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;