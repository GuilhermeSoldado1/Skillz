-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.4.3 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for libskilliana_guilhermesoldado_n24
CREATE DATABASE IF NOT EXISTS `libskilliana_guilhermesoldado_n24` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `libskilliana_guilhermesoldado_n24`;

-- Dumping structure for table libskilliana_guilhermesoldado_n24.autor
DROP TABLE IF EXISTS `autor`;
CREATE TABLE IF NOT EXISTS `autor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `dataNasc` date NOT NULL,
  `biografia` varchar(200) NOT NULL,
  `outrasInformacoes` varchar(200) NOT NULL,
  `facebook` varchar(200) DEFAULT NULL,
  `instagram` varchar(200) DEFAULT NULL,
  `x` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.autor: ~5 rows (approximately)
INSERT INTO `autor` (`id`, `nome`, `dataNasc`, `biografia`, `outrasInformacoes`, `facebook`, `instagram`, `x`) VALUES
	(1, 'João Silva', '1990-01-01', 'exemplo bio', 'exemplo info', 'fb.joao.com', 'ig.joao.com', 'x.joao.com'),
	(2, 'Pedro Silva', '1990-01-02', 'exemplo bio', 'exemplo info', 'fb.pedro.com', 'ig.pedro.com', 'x.pedro.com'),
	(3, 'Amélio', '1990-01-03', 'exemplo bio', 'exemplo info', 'fb.amelio.com', 'ig.amelio.com', 'x.amelio.com'),
	(4, 'Jacinta Silva', '1990-01-04', 'exemplo bio', 'exemplo info', 'fb.jacinta.com', 'ig.jacinta.com', 'x.jacinta.com'),
	(5, 'Jacinta Silva', '1990-01-05', 'exemplo bio', 'exemplo info', 'fb.pero.com', 'ig.pero.com', 'x.pero.com');

-- Dumping structure for table libskilliana_guilhermesoldado_n24.autoreslivros
DROP TABLE IF EXISTS `autoreslivros`;
CREATE TABLE IF NOT EXISTS `autoreslivros` (
  `id` int NOT NULL AUTO_INCREMENT,
  `autor_id` int DEFAULT NULL,
  `livro_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `autor_id` (`autor_id`),
  KEY `livro_id` (`livro_id`),
  CONSTRAINT `autoreslivros_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `autor` (`id`),
  CONSTRAINT `autoreslivros_ibfk_2` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.autoreslivros: ~5 rows (approximately)
INSERT INTO `autoreslivros` (`id`, `autor_id`, `livro_id`) VALUES
	(1, 1, 1),
	(2, 2, 1),
	(3, 3, 2),
	(4, 3, 3),
	(5, 5, 4);

-- Dumping structure for table libskilliana_guilhermesoldado_n24.estante
DROP TABLE IF EXISTS `estante`;
CREATE TABLE IF NOT EXISTS `estante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `seccao_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `seccao_id` (`seccao_id`),
  CONSTRAINT `estante_ibfk_1` FOREIGN KEY (`seccao_id`) REFERENCES `seccao` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.estante: ~5 rows (approximately)
INSERT INTO `estante` (`id`, `seccao_id`) VALUES
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
	(5, 5);

-- Dumping structure for table libskilliana_guilhermesoldado_n24.livro
DROP TABLE IF EXISTS `livro`;
CREATE TABLE IF NOT EXISTS `livro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) DEFAULT NULL,
  `dataLancamento` date NOT NULL,
  `sinopse` varchar(200) NOT NULL,
  `edicao` varchar(10) NOT NULL,
  `editora` varchar(50) NOT NULL,
  `genero` varchar(50) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `idioma` varchar(50) NOT NULL,
  `numPaginas` int NOT NULL,
  `isbn` varchar(50) NOT NULL DEFAULT '',
  `estado` tinyint NOT NULL DEFAULT (1),
  `qtd` int NOT NULL DEFAULT (1),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.livro: ~5 rows (approximately)
INSERT INTO `livro` (`id`, `titulo`, `dataLancamento`, `sinopse`, `edicao`, `editora`, `genero`, `categoria`, `idioma`, `numPaginas`, `isbn`, `estado`, `qtd`) VALUES
	(1, 'Aventura de Romance', '2000-01-01', 'um livro de aventura', '1ª', 'Porto Editora', 'Romance', 'Romance Clássico', 'Português', 254, '1234567SDFGS', 1, 5),
	(2, 'Harry Potter 1', '2000-01-02', 'um livro de aventura', '1ª', 'Porto Editora', 'Fantasia', 'Fantasia', 'Português', 254, '1234567SDFGS', 1, 5),
	(3, 'Harry Potter 2', '2000-01-03', 'um livro de aventura', '1ª', 'Porto Editora', 'Fantasia', 'Fantasia', 'Português', 254, '1234567SDFGS', 1, 2),
	(4, 'Harry Potter 3', '2000-01-04', 'um livro de aventura', '1ª', 'Porto Editora', 'Fantasia', 'Fantasia', 'Português', 254, '1234567SDFGS', 1, 2),
	(5, 'Harry Potter 4', '2000-01-04', 'um livro de aventura', '1ª', 'Porto Editora', 'Fantasia', 'Fantasia', 'Português', 300, '1234567SDFGS', 1, 2);

-- Dumping structure for table libskilliana_guilhermesoldado_n24.livroestante
DROP TABLE IF EXISTS `livroestante`;
CREATE TABLE IF NOT EXISTS `livroestante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `livro_id` int DEFAULT NULL,
  `estante_id` int DEFAULT NULL,
  `localizacao` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `livro_id` (`livro_id`),
  KEY `estante_id` (`estante_id`),
  CONSTRAINT `livroestante_ibfk_1` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`),
  CONSTRAINT `livroestante_ibfk_2` FOREIGN KEY (`estante_id`) REFERENCES `estante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.livroestante: ~5 rows (approximately)
INSERT INTO `livroestante` (`id`, `livro_id`, `estante_id`, `localizacao`) VALUES
	(1, 1, 2, 'Ponta esquerda'),
	(2, 2, 2, 'Ponta direita'),
	(3, 3, 2, 'Ponta direita'),
	(4, 3, 3, 'Ponta esquerda'),
	(5, 3, 4, 'Ponta esquerda');

-- Dumping structure for table libskilliana_guilhermesoldado_n24.requisitacao
DROP TABLE IF EXISTS `requisitacao`;
CREATE TABLE IF NOT EXISTS `requisitacao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `socio_id` int DEFAULT NULL,
  `utilizador_id` int DEFAULT NULL,
  `livro_id` int DEFAULT NULL,
  `dataRegisto` date DEFAULT NULL,
  `dataPrevista` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `socio_id` (`socio_id`),
  KEY `utilizador_id` (`utilizador_id`),
  KEY `livro_id` (`livro_id`),
  CONSTRAINT `requisitacao_ibfk_1` FOREIGN KEY (`socio_id`) REFERENCES `socio` (`id`),
  CONSTRAINT `requisitacao_ibfk_2` FOREIGN KEY (`utilizador_id`) REFERENCES `utilizador` (`id`),
  CONSTRAINT `requisitacao_ibfk_3` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.requisitacao: ~5 rows (approximately)
INSERT INTO `requisitacao` (`id`, `socio_id`, `utilizador_id`, `livro_id`, `dataRegisto`, `dataPrevista`) VALUES
	(1, 1, 1, 1, '2026-01-01', '2026-01-30'),
	(2, 2, 2, 2, '2026-01-01', '2026-01-30'),
	(3, 3, 3, 3, '2026-01-02', '2026-01-29'),
	(4, 4, 4, 4, '2026-01-03', '2026-01-28'),
	(5, 5, 5, 5, '2026-01-04', '2026-01-27');

-- Dumping structure for table libskilliana_guilhermesoldado_n24.seccao
DROP TABLE IF EXISTS `seccao`;
CREATE TABLE IF NOT EXISTS `seccao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.seccao: ~5 rows (approximately)
INSERT INTO `seccao` (`id`, `descricao`) VALUES
	(1, 'E1'),
	(2, 'E2'),
	(3, 'E3'),
	(4, 'E4'),
	(5, 'E5');

-- Dumping structure for table libskilliana_guilhermesoldado_n24.socio
DROP TABLE IF EXISTS `socio`;
CREATE TABLE IF NOT EXISTS `socio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL DEFAULT '',
  `cc` int NOT NULL,
  `numSocio` int NOT NULL,
  `morada` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(50) NOT NULL DEFAULT '',
  `telefone` int NOT NULL,
  `dataNasc` date NOT NULL,
  `ativo` tinyint NOT NULL DEFAULT (1),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.socio: ~5 rows (approximately)
INSERT INTO `socio` (`id`, `nome`, `cc`, `numSocio`, `morada`, `email`, `telefone`, `dataNasc`, `ativo`) VALUES
	(1, 'Manuel Silva', 1, 45, 'Rua da Porta', 'manuel@gmail.com', 912345678, '1999-02-02', 1),
	(2, 'Joaquim Silva', 1, 46, 'Rua do Sitio 1', 'quim@gmail.com', 912345676, '1999-02-02', 1),
	(3, 'Carlos Silva', 1, 46, 'Rua do Toca 1', 'carlos@gmail.com', 912345677, '1999-02-03', 1),
	(4, 'Joana Silva', 1, 46, 'Rua da Almeira 1', 'joana@gmail.com', 912345674, '1999-02-04', 1),
	(5, 'Hectór Manuel', 1, 46, 'Rua da Almeirim 1', 'hector@gmail.com', 912345673, '1999-02-05', 1);

-- Dumping structure for table libskilliana_guilhermesoldado_n24.tipo
DROP TABLE IF EXISTS `tipo`;
CREATE TABLE IF NOT EXISTS `tipo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `descricao` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.tipo: ~5 rows (approximately)
INSERT INTO `tipo` (`id`, `descricao`) VALUES
	(1, 'Romance'),
	(2, 'Fantasia'),
	(3, 'Terror'),
	(4, 'Aventura'),
	(5, 'Thriller');

-- Dumping structure for table libskilliana_guilhermesoldado_n24.tiposlivro
DROP TABLE IF EXISTS `tiposlivro`;
CREATE TABLE IF NOT EXISTS `tiposlivro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_id` int DEFAULT NULL,
  `livro_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_id` (`tipo_id`),
  KEY `livro_id` (`livro_id`),
  CONSTRAINT `tiposlivro_ibfk_1` FOREIGN KEY (`tipo_id`) REFERENCES `tipo` (`id`),
  CONSTRAINT `tiposlivro_ibfk_2` FOREIGN KEY (`livro_id`) REFERENCES `livro` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.tiposlivro: ~5 rows (approximately)
INSERT INTO `tiposlivro` (`id`, `tipo_id`, `livro_id`) VALUES
	(1, 1, 1),
	(2, 2, 2),
	(3, 2, 3),
	(4, 2, 4),
	(5, 2, 5);

-- Dumping structure for table libskilliana_guilhermesoldado_n24.utilizador
DROP TABLE IF EXISTS `utilizador`;
CREATE TABLE IF NOT EXISTS `utilizador` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL DEFAULT '0',
  `morada` varchar(50) NOT NULL DEFAULT '0',
  `telefone` varchar(9) NOT NULL DEFAULT '0',
  `email` varchar(50) NOT NULL DEFAULT '0',
  `numFunc` int NOT NULL DEFAULT (0),
  `dataNasc` date NOT NULL DEFAULT (0),
  `tipo` varchar(50) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table libskilliana_guilhermesoldado_n24.utilizador: ~5 rows (approximately)
INSERT INTO `utilizador` (`id`, `nome`, `morada`, `telefone`, `email`, `numFunc`, `dataNasc`, `tipo`) VALUES
	(1, 'Manuel Silveira', 'Rua da Almeirim 1', '912345672', 'manuels@gmail.com', 2, '1999-02-05', 'Funcionário'),
	(2, 'Carlos Silveira', 'Rua da Almeirim 2', '912345641', 'carlos@gmail.com', 3, '1999-02-05', 'Funcionário'),
	(3, 'Maria Silveira', 'Rua da Almeirim 3', '912345651', 'maria@gmail.com', 4, '1999-02-05', 'Funcionário'),
	(4, 'José Silveira', 'Rua da Almeirim 4', '912345661', 'jose@gmail.com', 5, '1999-02-06', 'Funcionário'),
	(5, 'Paulo Silveira', 'Rua da Almeirim 5', '912345670', 'paulo@gmail.com', 6, '1999-02-06', 'Funcionário');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
