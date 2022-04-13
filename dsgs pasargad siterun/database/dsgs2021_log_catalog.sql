-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: dsgs2021
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `log_catalog`
--

DROP TABLE IF EXISTS `log_catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_catalog` (
  `catalog_id` int NOT NULL,
  `log_name` varchar(100) DEFAULT NULL,
  `description` mediumtext,
  PRIMARY KEY (`catalog_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_catalog`
--

LOCK TABLES `log_catalog` WRITE;
/*!40000 ALTER TABLE `log_catalog` DISABLE KEYS */;
INSERT INTO `log_catalog` VALUES (10001,'Disc situation','Situation of disc changed (Stop to Run)'),(10002,'Disc situation','Situation of disc changed (Run to Stop)'),(20001,'Control mode','Mode of control changed (Manual to Automatic)'),(20002,'Control mode','Mode of control changed (Automatic to Manual)'),(30001,'Projector situation','Situation of projector changed (OFF to ON)'),(30002,'Projector situation','Situation of projector changed (ON to OFF)'),(40001,'Camera situation','Situation of camera changed (OFF to ON)'),(40002,'Camera situation','Situation of camera changed (ON to OFF)'),(50001,'Software situation','Situation of software changed (Start)'),(50002,'Software situation','Situation of software changed (Close)'),(50003,'Software situation','Situation of software changed (Restart)'),(50004,'Software situation','Situation of software changed (Shut down)'),(50005,'Software situation','User login'),(50006,'Software situation','User logout'),(60001,'Speed signal','Speed signal applied (Increased)'),(60002,'Speed signal','Speed signal applied (Decreased)'),(60003,'Speed signal','Speed signal not applied (Increased)'),(60004,'Speed signal','Speed signal not applied (Decreased)'),(70001,'Setting changed','New user added'),(70002,'Setting changed','Password changed'),(70003,'Setting changed','User deleted'),(70004,'Setting changed','User updated'),(70005,'Setting changed','Thresholds changed'),(70006,'Setting changed','System is calibrated'),(70007,'Setting changed','General setting is changed'),(70008,'Setting changed','Calibration setting is changed');
/*!40000 ALTER TABLE `log_catalog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-27  9:07:31
