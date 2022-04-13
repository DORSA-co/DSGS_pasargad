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
-- Table structure for table `general_setting_table`
--

DROP TABLE IF EXISTS `general_setting_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `general_setting_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_saving_period` int DEFAULT NULL,
  `database_refresh_period` int DEFAULT NULL,
  `processing_file_path` varchar(300) DEFAULT NULL,
  `projector_check_file_path` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_setting_table`
--

LOCK TABLES `general_setting_table` WRITE;
/*!40000 ALTER TABLE `general_setting_table` DISABLE KEYS */;
INSERT INTO `general_setting_table` VALUES (1,10,30,'D:\\DSGS\\software\\python\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(2,10,30,'D:\\DSGS projector\\software\\python\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(3,10,30,'D:\\DSGS\\software\\python\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(4,60,30,'D:\\DSGS\\software\\python\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(5,10,30,'D:\\DSGS\\software\\python\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(6,10,30,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\circelFinder.py','D:\\DSGS\\software\\python\\projector.py'),(7,10,30,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\processing.py','D:\\DSGS\\software\\python\\projector.py'),(8,10,30,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\circelFinder.py','D:\\DSGS\\software\\python\\projector.py'),(9,10,30,'F:\\arshad\\folad projects\\in progress projects\\DSGS pasargad\\DSGS projector\\processing.py','D:\\DSGS\\software\\python\\projector.py');
/*!40000 ALTER TABLE `general_setting_table` ENABLE KEYS */;
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
