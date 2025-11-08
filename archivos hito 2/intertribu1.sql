-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 01-11-2025 a las 21:55:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `intertribu1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad`
--

CREATE TABLE `actividad` (
  `idactividad` int(11) NOT NULL,
  `nombreActividad` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividad`
--

INSERT INTO `actividad` (`idactividad`, `nombreActividad`) VALUES
(1001, 'Futbol'),
(1002, 'Handball'),
(1003, 'Quemado'),
(1004, 'Futbol Tenis'),
(1005, 'Volley'),
(1006, 'Tejo'),
(1007, 'Atletismo'),
(1008, 'Foto Creativa'),
(1009, 'Coreografia'),
(1010, 'Truco'),
(1011, 'Ajedrez'),
(1012, 'Circuito de Habilidades'),
(1013, 'Ping Pong de Preguntas/Respuestas'),
(1014, 'Tutti Frutti'),
(1015, 'Talento'),
(1016, 'Gimnasia Artistica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `idestudiantes` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `carrera` varchar(45) NOT NULL,
  `genero` enum('F','M') NOT NULL,
  `tribu` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`idestudiantes`, `nombre`, `apellido`, `carrera`, `genero`, `tribu`) VALUES
(1, 'Camila', 'Pérez', 'Ed. Física', 'M', 'Azul'),
(2, 'Emilia', 'Pérez', 'Historia', 'F', 'Azul'),
(3, 'Valentina', 'Molina', 'Geografía', 'F', 'Azul'),
(4, 'Julieta', 'Molina', 'Biología', 'M', 'Azul'),
(5, 'Isabella', 'Fernández', 'Lengua', 'M', 'Azul'),
(6, 'Mateo', 'Torres', 'Matemática', 'F', 'Azul'),
(7, 'Camila', 'Herrera', 'Ed. Física', 'F', 'Azul'),
(8, 'Agustín', 'Ruiz', 'Programación', 'M', 'Azul'),
(9, 'Emilia', 'Castro', 'Ed. Física', 'M', 'Azul'),
(10, 'Lucía', 'Sosa', 'Biología', 'F', 'Azul'),
(11, 'Juan', 'Álvarez', 'Biología', 'M', 'Azul'),
(12, 'Facundo', 'Vega', 'Matemática', 'M', 'Azul'),
(13, 'Julieta', 'Medina', 'Matemática', 'M', 'Verde'),
(14, 'Valentina', 'Rojas', 'Ed. Física', 'M', 'Verde'),
(15, 'Lucas', 'López', 'Ed. Física', 'M', 'Verde'),
(16, 'Nicolás', 'Suárez', 'Geografía', 'M', 'Verde'),
(17, 'Mateo', 'Gómez', 'Ed. Física', 'M', 'Verde'),
(18, 'Martina', 'Sosa', 'Geografía', 'M', 'Verde'),
(19, 'Gonzalo', 'Suárez', 'Historia', 'F', 'Verde'),
(20, 'Emilia', 'Molina', 'Lengua', 'M', 'Verde'),
(21, 'Emilia', 'Acosta', 'Lengua', 'M', 'Verde'),
(22, 'Mateo', 'Sosa', 'Historia', 'F', 'Verde'),
(23, 'Martina', 'Torres', 'Geografía', 'M', 'Verde'),
(24, 'Lucía', 'Suárez', 'Geografía', 'M', 'Verde'),
(25, 'Franco', 'Álvarez', 'Geografía', 'F', 'Verde'),
(26, 'Agustín', 'Rojas', 'Biología', 'F', 'Verde'),
(27, 'Lucía', 'Pérez', 'Matemática', 'F', 'Azul'),
(28, 'Agustín', 'Medina', 'Matemática', 'M', 'Azul'),
(29, 'Julieta', 'Medina', 'Geografía', 'F', 'Azul'),
(30, 'Nicolás', 'Díaz', 'Matemática', 'F', 'Verde'),
(31, 'Valentina', 'Castro', 'Biología', 'M', 'Verde'),
(32, 'Julieta', 'López', 'Biología', 'M', 'Verde'),
(33, 'Facundo', 'Medina', 'Historia', 'M', 'Verde'),
(34, 'Renata', 'Sosa', 'Historia', 'F', 'Azul'),
(35, 'Valentina', 'Vega', 'Matemática', 'M', 'Azul'),
(36, 'Camila', 'Gómez', 'Geografía', 'M', 'Verde'),
(37, 'Isabella', 'Vega', 'Historia', 'F', 'Azul'),
(38, 'Martina', 'Medina', 'Matemática', 'F', 'Azul'),
(39, 'Gonzalo', 'Gómez', 'Geografía', 'M', 'Azul'),
(40, 'Gonzalo', 'Herrera', 'Programación', 'F', 'Azul'),
(41, 'Renata', 'Álvarez', 'Biología', 'M', 'Azul'),
(42, 'Valentina', 'Pérez', 'Ed. Física', 'F', 'Verde'),
(43, 'Camila', 'Castro', 'Matemática', 'F', 'Verde'),
(44, 'Gonzalo', 'Gómez', 'Ed. Física', 'F', 'Verde'),
(45, 'Nicolás', 'Vega', 'Lengua', 'F', 'Azul'),
(46, 'Lucía', 'Acosta', 'Lengua', 'F', 'Verde'),
(47, 'Camila', 'Sosa', 'Biología', 'M', 'Azul'),
(48, 'Mía', 'Silva', 'Biología', 'M', 'Verde'),
(49, 'Renata', 'Torres', 'Lengua', 'M', 'Verde'),
(50, 'Isabella', 'Ruiz', 'Matemática', 'M', 'Verde'),
(51, 'Sofía', 'Vega', 'Historia', 'F', 'Azul'),
(52, 'Valentina', 'Suárez', 'Historia', 'M', 'Verde'),
(53, 'Facundo', 'Medina', 'Historia', 'F', 'Verde'),
(54, 'Benjamín', 'Sosa', 'Programación', 'F', 'Verde'),
(55, 'Agustín', 'Suárez', 'Geografía', 'M', 'Azul'),
(56, 'Mía', 'Álvarez', 'Geografía', 'F', 'Azul'),
(57, 'Julieta', 'Suárez', 'Biología', 'M', 'Azul'),
(58, 'Sofía', 'Torres', 'Matemática', 'M', 'Azul'),
(59, 'Julieta', 'Gómez', 'Matemática', 'M', 'Verde'),
(60, 'Camila', 'Vega', 'Programación', 'M', 'Verde'),
(61, 'Agustín', 'García', 'Historia', 'M', 'Azul'),
(62, 'Valentina', 'Medina', 'Ed. Física', 'F', 'Verde'),
(63, 'Julieta', 'Álvarez', 'Biología', 'M', 'Azul'),
(64, 'Emilia', 'Fernández', 'Programación', 'F', 'Verde'),
(65, 'Juan', 'García', 'Lengua', 'M', 'Azul'),
(66, 'Tomás', 'Torres', 'Biología', 'M', 'Azul'),
(67, 'Camila', 'Ruiz', 'Ed. Física', 'F', 'Azul'),
(68, 'Julieta', 'Castro', 'Lengua', 'M', 'Verde'),
(69, 'Mateo', 'Díaz', 'Geografía', 'F', 'Azul'),
(70, 'Renata', 'Fernández', 'Geografía', 'F', 'Azul'),
(71, 'Emilia', 'Gómez', 'Lengua', 'F', 'Azul'),
(72, 'Lucas', 'Fernández', 'Programación', 'M', 'Azul'),
(73, 'Renata', 'Pérez', 'Geografía', 'F', 'Azul'),
(74, 'Renata', 'Ruiz', 'Lengua', 'F', 'Verde'),
(75, 'Emilia', 'Molina', 'Ed. Física', 'F', 'Verde'),
(76, 'Juan', 'Gómez', 'Historia', 'F', 'Verde'),
(77, 'Julieta', 'Rojas', 'Historia', 'M', 'Verde'),
(78, 'Sofía', 'Molina', 'Ed. Física', 'M', 'Azul'),
(79, 'Valentina', 'Molina', 'Matemática', 'F', 'Azul'),
(80, 'Valentina', 'Castro', 'Matemática', 'F', 'Azul'),
(81, 'Camila', 'Acosta', 'Ed. Física', 'F', 'Verde'),
(82, 'Mía', 'Pérez', 'Historia', 'F', 'Azul'),
(83, 'Mateo', 'Sosa', 'Biología', 'F', 'Azul'),
(84, 'Julieta', 'Silva', 'Programación', 'F', 'Verde'),
(85, 'Renata', 'Silva', 'Biología', 'M', 'Azul'),
(86, 'Julieta', 'Pérez', 'Historia', 'M', 'Verde'),
(87, 'Renata', 'Silva', 'Lengua', 'M', 'Azul'),
(88, 'Franco', 'Herrera', 'Programación', 'M', 'Azul'),
(89, 'Valentina', 'Pérez', 'Programación', 'M', 'Azul'),
(90, 'Sofía', 'López', 'Biología', 'M', 'Verde'),
(91, 'Lucía', 'Álvarez', 'Matemática', 'M', 'Azul'),
(92, 'Lucas', 'Vega', 'Lengua', 'M', 'Verde'),
(93, 'Juan', 'Romero', 'Programación', 'F', 'Azul'),
(94, 'Camila', 'Díaz', 'Historia', 'M', 'Azul'),
(95, 'Mía', 'Sosa', 'Geografía', 'M', 'Azul'),
(96, 'Mía', 'Álvarez', 'Ed. Física', 'F', 'Verde'),
(97, 'Agustín', 'Rojas', 'Historia', 'M', 'Azul'),
(98, 'Julieta', 'Romero', 'Lengua', 'M', 'Verde'),
(99, 'Nicolás', 'García', 'Biología', 'F', 'Azul'),
(100, 'Valentina', 'Rojas', 'Geografía', 'F', 'Azul'),
(101, 'Lucía', 'Rojas', 'Lengua', 'M', 'Verde'),
(102, 'Benjamín', 'Herrera', 'Biología', 'F', 'Azul'),
(103, 'Sofía', 'Suárez', 'Geografía', 'M', 'Azul'),
(104, 'Nicolás', 'Romero', 'Ed. Física', 'F', 'Azul'),
(105, 'Juan', 'Rojas', 'Matemática', 'F', 'Verde'),
(106, 'Mía', 'Rojas', 'Ed. Física', 'M', 'Azul'),
(107, 'Facundo', 'Silva', 'Lengua', 'F', 'Azul'),
(108, 'Emilia', 'Romero', 'Programación', 'M', 'Verde'),
(109, 'Juan', 'Álvarez', 'Historia', 'F', 'Verde'),
(110, 'Sofía', 'Medina', 'Matemática', 'F', 'Verde'),
(111, 'Lucía', 'Vega', 'Matemática', 'F', 'Azul'),
(112, 'Mía', 'Ruiz', 'Biología', 'M', 'Azul'),
(113, 'Gonzalo', 'López', 'Ed. Física', 'M', 'Azul'),
(114, 'Valentina', 'Sosa', 'Matemática', 'F', 'Azul'),
(115, 'Gonzalo', 'López', 'Geografía', 'F', 'Azul'),
(116, 'Nicolás', 'Molina', 'Geografía', 'M', 'Verde'),
(117, 'Tomás', 'Herrera', 'Geografía', 'M', 'Verde'),
(118, 'Juan', 'Vega', 'Lengua', 'M', 'Verde'),
(119, 'Gonzalo', 'Vega', 'Lengua', 'F', 'Verde'),
(120, 'Emilia', 'Díaz', 'Ed. Física', 'F', 'Azul'),
(121, 'Lucas', 'López', 'Geografía', 'F', 'Azul'),
(122, 'Valentina', 'Romero', 'Biología', 'F', 'Azul'),
(123, 'Benjamín', 'Sosa', 'Matemática', 'F', 'Verde'),
(124, 'Valentina', 'López', 'Geografía', 'F', 'Verde'),
(125, 'Gonzalo', 'Sosa', 'Matemática', 'M', 'Verde'),
(126, 'Nicolás', 'Molina', 'Programación', 'M', 'Verde'),
(127, 'Gonzalo', 'Rojas', 'Geografía', 'M', 'Verde'),
(128, 'Valentina', 'Romero', 'Matemática', 'F', 'Verde'),
(129, 'Benjamín', 'Sosa', 'Biología', 'M', 'Verde'),
(130, 'Agustín', 'Gómez', 'Lengua', 'M', 'Verde'),
(131, 'Benjamín', 'Fernández', 'Matemática', 'M', 'Verde'),
(132, 'Julieta', 'Herrera', 'Geografía', 'M', 'Verde'),
(133, 'Facundo', 'Díaz', 'Historia', 'F', 'Azul'),
(134, 'Renata', 'Pérez', 'Biología', 'F', 'Azul'),
(135, 'Lucas', 'Rojas', 'Biología', 'F', 'Azul'),
(136, 'Tomás', 'Suárez', 'Programación', 'F', 'Verde'),
(137, 'Franco', 'Rojas', 'Historia', 'F', 'Verde'),
(138, 'Gonzalo', 'García', 'Biología', 'M', 'Azul'),
(139, 'Mateo', 'Díaz', 'Biología', 'M', 'Verde'),
(140, 'Isabella', 'Silva', 'Ed. Física', 'F', 'Verde'),
(141, 'Mateo', 'Medina', 'Programación', 'F', 'Azul'),
(142, 'Mía', 'Gómez', 'Lengua', 'M', 'Verde'),
(143, 'Benjamín', 'Romero', 'Programación', 'M', 'Azul'),
(144, 'Camila', 'Díaz', 'Programación', 'F', 'Azul'),
(145, 'Isabella', 'Ruiz', 'Lengua', 'M', 'Verde'),
(146, 'Camila', 'Vega', 'Historia', 'F', 'Verde'),
(147, 'Julieta', 'Molina', 'Programación', 'F', 'Azul'),
(148, 'Isabella', 'Pérez', 'Matemática', 'M', 'Verde'),
(149, 'Juan', 'Acosta', 'Matemática', 'F', 'Verde'),
(150, 'Mía', 'Silva', 'Ed. Física', 'F', 'Verde'),
(151, 'Julieta', 'Medina', 'Lengua', 'M', 'Verde'),
(152, 'Benjamín', 'López', 'Lengua', 'F', 'Azul'),
(153, 'Valentina', 'López', 'Biología', 'M', 'Azul'),
(154, 'Juan', 'Vega', 'Matemática', 'F', 'Verde'),
(155, 'Camila', 'Fernández', 'Matemática', 'F', 'Verde'),
(156, 'Renata', 'Fernández', 'Programación', 'M', 'Azul'),
(157, 'Isabella', 'Torres', 'Matemática', 'M', 'Verde'),
(158, 'Mateo', 'Silva', 'Biología', 'M', 'Verde'),
(159, 'Mía', 'Rojas', 'Geografía', 'F', 'Azul'),
(160, 'Juan', 'Álvarez', 'Programación', 'M', 'Verde'),
(161, 'Emilia', 'Gómez', 'Geografía', 'F', 'Verde'),
(162, 'Lucía', 'López', 'Historia', 'M', 'Azul'),
(163, 'Benjamín', 'Vega', 'Geografía', 'M', 'Azul'),
(164, 'Mateo', 'Pérez', 'Geografía', 'F', 'Azul'),
(165, 'Lucía', 'Molina', 'Geografía', 'F', 'Verde'),
(166, 'Martina', 'Ruiz', 'Lengua', 'F', 'Verde'),
(167, 'Emilia', 'Molina', 'Biología', 'M', 'Verde'),
(168, 'Sofía', 'Fernández', 'Programación', 'M', 'Azul'),
(169, 'Lucía', 'Ruiz', 'Matemática', 'M', 'Azul'),
(170, 'Juan', 'Ruiz', 'Biología', 'M', 'Azul'),
(171, 'Julieta', 'Vega', 'Programación', 'M', 'Azul'),
(172, 'Gonzalo', 'Ruiz', 'Matemática', 'F', 'Azul'),
(173, 'Lucas', 'Torres', 'Lengua', 'M', 'Azul'),
(174, 'Emilia', 'Álvarez', 'Biología', 'F', 'Verde'),
(175, 'Lucas', 'Molina', 'Geografía', 'M', 'Verde'),
(176, 'Gonzalo', 'Sosa', 'Ed. Física', 'F', 'Verde'),
(177, 'Sofía', 'García', 'Lengua', 'M', 'Verde'),
(178, 'Martina', 'García', 'Historia', 'F', 'Azul'),
(179, 'Facundo', 'Gómez', 'Biología', 'M', 'Azul'),
(180, 'Sofía', 'Castro', 'Lengua', 'M', 'Azul'),
(181, 'Agustín', 'Rojas', 'Historia', 'F', 'Azul'),
(182, 'Martina', 'Herrera', 'Matemática', 'F', 'Azul'),
(183, 'Tomás', 'Romero', 'Programación', 'F', 'Azul'),
(184, 'Mía', 'Romero', 'Matemática', 'F', 'Azul'),
(185, 'Agustín', 'Vega', 'Lengua', 'M', 'Azul'),
(186, 'Facundo', 'Silva', 'Geografía', 'F', 'Verde'),
(187, 'Mía', 'Rojas', 'Programación', 'M', 'Verde'),
(188, 'Facundo', 'Vega', 'Ed. Física', 'F', 'Azul'),
(189, 'Benjamín', 'Herrera', 'Matemática', 'M', 'Verde'),
(190, 'Lucas', 'Ruiz', 'Lengua', 'F', 'Verde'),
(191, 'Nicolás', 'García', 'Ed. Física', 'M', 'Verde'),
(192, 'Lucía', 'Herrera', 'Lengua', 'M', 'Verde'),
(193, 'Tomás', 'Fernández', 'Historia', 'F', 'Verde'),
(194, 'Lucas', 'Pérez', 'Biología', 'F', 'Verde'),
(195, 'Franco', 'Pérez', 'Biología', 'M', 'Azul'),
(196, 'Camila', 'Medina', 'Biología', 'M', 'Verde'),
(197, 'Valentina', 'Molina', 'Biología', 'M', 'Verde'),
(198, 'Mateo', 'Medina', 'Matemática', 'F', 'Verde'),
(199, 'Mateo', 'Castro', 'Ed. Física', 'F', 'Verde'),
(200, 'Martina', 'Álvarez', 'Matemática', 'M', 'Azul');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones`
--

CREATE TABLE `inscripciones` (
  `idinscripciones` int(11) NOT NULL,
  `idEstudiante` int(11) NOT NULL,
  `idActividad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad`
--
ALTER TABLE `actividad`
  ADD PRIMARY KEY (`idactividad`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`idestudiantes`);

--
-- Indices de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`idinscripciones`),
  ADD KEY `idx_estudiante` (`idEstudiante`),
  ADD KEY `idx_actividad` (`idActividad`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad`
--
ALTER TABLE `actividad`
  MODIFY `idactividad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1017;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `idestudiantes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=201;

--
-- AUTO_INCREMENT de la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `idinscripciones` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `fk_inscripcion_actividad` FOREIGN KEY (`idActividad`) REFERENCES `actividad` (`idactividad`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_inscripcion_estudiante` FOREIGN KEY (`idEstudiante`) REFERENCES `estudiantes` (`idestudiantes`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
