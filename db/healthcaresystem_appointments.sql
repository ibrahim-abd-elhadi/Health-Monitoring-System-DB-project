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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `date_time` datetime NOT NULL,
  `status` enum('Pending','Confirmed','Cancelled') NOT NULL,
  `reason` text,
  PRIMARY KEY (`appointment_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,1,101,'2024-12-02 09:00:00','Pending','Routine Checkup'),(2,2,101,'2024-12-02 11:30:00','Confirmed','Follow-up for Diabetes'),(3,3,101,'2024-12-03 14:00:00','Pending','Consultation for Asthma'),(4,4,101,'2024-12-03 16:00:00','Cancelled','General Checkup'),(5,5,101,'2024-12-04 10:30:00','Pending','Hypertension Follow-up'),(6,6,102,'2024-12-04 13:00:00','Pending','Routine Blood Work'),(7,7,102,'2024-12-05 08:30:00','Confirmed','Consultation for Diet'),(8,8,102,'2024-12-05 15:00:00','Pending','Follow-up on Cholesterol'),(9,9,102,'2024-12-06 09:30:00','Confirmed','Routine Checkup'),(10,10,102,'2024-12-06 12:00:00','Pending','Consultation for Fatigue'),(11,11,103,'2024-12-07 11:00:00','Confirmed','Routine Checkup'),(12,12,103,'2024-12-07 14:30:00','Pending','General Wellness Consultation'),(13,13,103,'2024-12-08 09:00:00','Cancelled','Follow-up for Asthma'),(14,14,103,'2024-12-08 16:00:00','Pending','Consultation for Hypertension'),(15,15,103,'2024-12-09 10:00:00','Confirmed','Routine Checkup'),(16,16,104,'2024-12-09 13:30:00','Pending','Follow-up for Cholesterol'),(17,17,104,'2024-12-10 08:00:00','Confirmed','Consultation for Sleep Issues'),(18,18,104,'2024-12-10 15:00:00','Pending','Diet and Nutrition Advice'),(19,19,104,'2024-12-11 11:30:00','Cancelled','Consultation for Anxiety'),(20,20,104,'2024-12-11 14:00:00','Pending','Follow-up for Hypertension');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
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
