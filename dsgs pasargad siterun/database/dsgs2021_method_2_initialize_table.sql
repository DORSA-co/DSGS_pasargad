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
-- Table structure for table `method_2_initialize_table`
--

DROP TABLE IF EXISTS `method_2_initialize_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `method_2_initialize_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `method_2_id` int DEFAULT NULL,
  `disc_number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `method_2_initialize_table`
--

LOCK TABLES `method_2_initialize_table` WRITE;
/*!40000 ALTER TABLE `method_2_initialize_table` DISABLE KEYS */;
INSERT INTO `method_2_initialize_table` VALUES (6,77,'disc 30'),(7,78,'disc 30'),(8,120,'disc 30'),(9,123,'disc 26'),(10,122,'disc 26'),(11,123,'disc 26'),(12,124,'disc 26'),(13,124,'disc 26'),(14,0,'disc 26'),(15,0,'disc 27'),(16,0,'disc 27'),(17,23,'disc 28'),(18,23,'disc 28'),(19,123,'disc 26'),(20,124,'disc 26'),(21,123,'disc 26'),(22,123,'disc 26'),(23,123,'disc 26'),(24,123,'disc 26'),(25,61,'disc 29'),(26,123,'disc 26'),(27,123,'disc 26'),(28,43,'disc 27'),(29,129,'disc 27'),(30,135,'disc 26'),(31,129,'disc 27'),(32,131,'disc 28'),(33,132,'disc 29'),(34,132,'disc 29'),(35,133,'disc 30');
/*!40000 ALTER TABLE `method_2_initialize_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-27  9:07:27
