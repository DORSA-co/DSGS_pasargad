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
-- Table structure for table `grading_disc_03`
--

DROP TABLE IF EXISTS `grading_disc_03`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grading_disc_03` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `category1` double DEFAULT NULL,
  `category2` double DEFAULT NULL,
  `category3` double DEFAULT NULL,
  `category4` double DEFAULT NULL,
  `category5` double DEFAULT NULL,
  `category6` double DEFAULT NULL,
  `category7` double DEFAULT NULL,
  `category8` double DEFAULT NULL,
  `disc_situation` varchar(45) DEFAULT NULL,
  `control_mode` varchar(45) DEFAULT NULL,
  `camera_situation` varchar(45) DEFAULT NULL,
  `projector_situation` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20477 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grading_disc_03`
--

LOCK TABLES `grading_disc_03` WRITE;
/*!40000 ALTER TABLE `grading_disc_03` DISABLE KEYS */;
INSERT INTO `grading_disc_03` VALUES (20473,'2022/02/21','16:30:04',6.54,20.65,3.86,68.01,0,0,0,0,'Run','Auto','ON','OFF'),(20474,'2022/02/21','17:10:01',23.9,34.35,41.4,0,0,0,0,0,'Run','Auto','ON','OFF'),(20475,'2022/02/22','16:10:04',24.98,21.55,53.37,0,0,0,0,0,'Run','Auto','ON','OFF'),(20476,'2022/02/22','18:50:03',19.78,21.59,50.35,6.5,0,0,0,0,'Run','Auto','ON','OFF');
/*!40000 ALTER TABLE `grading_disc_03` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-27  9:07:38
