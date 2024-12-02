CREATE DATABASE  IF NOT EXISTS `healthcaresystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `healthcaresystem`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: healthcaresystem
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `emergency_actions`
--

DROP TABLE IF EXISTS `emergency_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergency_actions` (
  `emergency_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `action_date` datetime NOT NULL,
  `action_type` varchar(255) NOT NULL,
  `remarks` text,
  PRIMARY KEY (`emergency_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `emergency_actions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergency_actions`
--

LOCK TABLES `emergency_actions` WRITE;
/*!40000 ALTER TABLE `emergency_actions` DISABLE KEYS */;
INSERT INTO `emergency_actions` VALUES (1,1,'2024-12-01 00:00:00','CPR','Administered CPR after fainting episode'),(2,2,'2024-12-02 00:00:00','Hospitalization','Patient hospitalized for severe allergic reaction'),(3,3,'2024-12-03 00:00:00','Medication','Administered epinephrine for asthma attack'),(4,4,'2024-12-04 00:00:00','Ambulance','Patient transported to hospital after heart attack'),(5,5,'2024-12-05 00:00:00','CPR','CPR performed after sudden collapse'),(6,6,'2024-12-06 00:00:00','Hospitalization','Patient hospitalized for stroke'),(7,7,'2024-12-07 00:00:00','Medication','Administered insulin for diabetic emergency'),(8,8,'2024-12-08 00:00:00','CPR','CPR performed after cardiac arrest'),(9,9,'2024-12-09 00:00:00','Ambulance','Patient transported for a severe asthma attack'),(10,10,'2024-12-10 00:00:00','Hospitalization','Patient hospitalized after car accident'),(11,11,'2024-12-11 00:00:00','Medication','Administered pain relief for severe back injury'),(12,12,'2024-12-12 00:00:00','Ambulance','Patient transported after slipping and falling'),(13,13,'2024-12-13 00:00:00','CPR','CPR performed after drowning incident'),(14,14,'2024-12-14 00:00:00','Hospitalization','Patient hospitalized for heart complications'),(15,15,'2024-12-15 00:00:00','Medication','Administered glucose for hypoglycemic emergency'),(16,16,'2024-12-16 00:00:00','CPR','CPR administered after fainting due to low blood pressure'),(17,17,'2024-12-17 00:00:00','Ambulance','Patient transported after major injury from fall'),(18,18,'2024-12-18 00:00:00','Medication','Administered medication for acute allergic reaction'),(19,19,'2024-12-19 00:00:00','Hospitalization','Patient hospitalized for severe chest pain'),(20,20,'2024-12-20 00:00:00','CPR','CPR performed after unconsciousness due to dehydration');
/*!40000 ALTER TABLE `emergency_actions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-03  1:05:53
