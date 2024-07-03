-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.5.19


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema fetalhealth
--

CREATE DATABASE IF NOT EXISTS fetalhealth;
USE fetalhealth;

--
-- Definition of table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
CREATE TABLE `doctors` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) DEFAULT NULL,
  `Registration_Number` varchar(255) DEFAULT NULL,
  `Contact_Number` bigint(13) DEFAULT NULL,
  `Hospital_Name` varchar(255) DEFAULT NULL,
  `Specialization` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctors`
--

/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` (`ID`,`Username`,`Password`,`Email`,`Full_Name`,`Registration_Number`,`Contact_Number`,`Hospital_Name`,`Specialization`,`Address`) VALUES 
 (2,'eswar','$2b$12$esl8XTK7qy1SIFcJOUbDI.XPtkNnLqDIrr4032rd/.BquRhsKu0b.','eswaranmindsoft@gmail.com','eswar','1234',9902752525,'Default Hospital','Physician','bangalore');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;


--
-- Definition of table `pdffiles`
--

DROP TABLE IF EXISTS `pdffiles`;
CREATE TABLE `pdffiles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `docname` varchar(145) NOT NULL,
  `pname` varchar(145) NOT NULL,
  `trimester` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pdffiles`
--

/*!40000 ALTER TABLE `pdffiles` DISABLE KEYS */;
INSERT INTO `pdffiles` (`id`,`docname`,`pname`,`trimester`) VALUES 
 (1,'eswar','siva','1'),
 (2,'eswar','siva','2'),
 (3,'eswar','siva','3');
/*!40000 ALTER TABLE `pdffiles` ENABLE KEYS */;


--
-- Definition of table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Blood_Group` varchar(255) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `API_Token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`ID`,`Username`,`Password`,`Email`,`Full_Name`,`Address`,`Blood_Group`,`Age`,`API_Token`) VALUES 
 (2,'siva','$2b$12$ShgbEOlNA0uTpQWiHb8ayOfV6dB0XUoBqGHi8E3o0hIU1FcirjqxO','mindsoftblore@gmail.com','siva','bangalore','O+',35,'c2l2YSh+KXNpdmE=');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
