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
-- Table structure for table `calibration_setting_table`
--

DROP TABLE IF EXISTS `calibration_setting_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calibration_setting_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `calibration_method` int DEFAULT NULL,
  `calibration_file_path` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calibration_setting_table`
--

LOCK TABLES `calibration_setting_table` WRITE;
/*!40000 ALTER TABLE `calibration_setting_table` DISABLE KEYS */;
INSERT INTO `calibration_setting_table` VALUES (1,1,'D:\\DSGS\\software\\python\\calibration.py'),(2,0,'D:\\DSGS\\software\\python\\calibration.py'),(3,1,'D:\\DSGS\\software\\python\\calibration.py'),(4,1,'D:\\DSGS projector\\software\\python\\calibration2.py'),(5,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(6,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(7,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(8,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(9,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(10,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(11,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(12,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(13,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(14,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(15,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(16,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(17,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(18,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(19,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(20,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(21,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(22,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(23,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(24,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(25,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(26,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(27,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(28,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(29,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(30,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(31,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(32,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(33,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(34,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(35,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(36,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(37,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(38,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(39,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(40,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(41,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(42,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(43,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(44,0,'D:\\DSGS projector\\software\\python\\calibration.py'),(45,1,'D:\\DSGS projector\\software\\python\\calibration.py'),(46,1,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\calib.py'),(47,1,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\circelFinder.py'),(48,1,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\calib.py');
/*!40000 ALTER TABLE `calibration_setting_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-27  9:07:32
