-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2025 at 08:53 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurante`
--

-- --------------------------------------------------------

--
-- Table structure for table `categorias`
--

CREATE TABLE `categorias` (
  `id` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `ruta_imagen` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `ruta_imagen`) VALUES
(1, 'Entradas', 'entradas.jpg'),
(2, 'Platos Fuertes', 'platos_fuertes.jpg'),
(3, 'Postres', 'postres.jpg'),
(4, 'Bebidas', 'bebidas.jpg'),
(5, 'Ensaladas', 'ensaladas.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `platos`
--

CREATE TABLE `platos` (
  `id` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(12,2) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `ruta_imagen` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `platos`
--

INSERT INTO `platos` (`id`, `nombre`, `descripcion`, `precio`, `id_categoria`, `ruta_imagen`) VALUES
(1, 'Empanadas de Queso', 'Crujientes empanadas rellenas de queso', 2.50, 1, 'empanadas.jpg'),
(2, 'Sopa de Pollo', 'Caldo tradicional con verduras y pollo desmenuzado', 3.75, 1, 'sopa_pollo.jpg'),
(3, 'Filete de Res', 'Filete a la plancha con papas fritas y ensalada', 8.90, 2, 'filete_res.jpg'),
(4, 'Pasta Alfredo', 'Pasta con salsa cremosa de queso parmesano', 7.20, 2, 'pasta_alfredo.jpg'),
(5, 'Dulce de Chocolate', 'Delicioso postre de chocolate con textura suave y sabor intenso', 4.50, 3, 'dulce_chocolate.jpg'),
(6, 'Helado de Vainilla', 'Helado artesanal con sirope de chocolate', 2.00, 3, 'helado_vainilla.jpg'),
(7, 'Limonada Natural', 'Refrescante bebida con limón recién exprimido', 1.50, 4, 'limonada.jpg'),
(8, 'Coca-Cola', 'Bebida gaseosa clásica', 1.25, 4, 'cocacola.jpg'),
(9, 'Ensalada César', 'Lechuga romana, pollo y aderezo césar', 5.80, 5, 'ensalada_cesar.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `platos`
--
ALTER TABLE `platos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `platos`
--
ALTER TABLE `platos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `platos`
--
ALTER TABLE `platos`
  ADD CONSTRAINT `platos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
