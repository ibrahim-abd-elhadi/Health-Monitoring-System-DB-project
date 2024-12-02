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
-- Table structure for table `medications`
--

DROP TABLE IF EXISTS `medications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medications` (
  `medication_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `medication_name` varchar(255) NOT NULL,
  `dosage` varchar(50) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `instructions` text,
  PRIMARY KEY (`medication_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `medications_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `medications_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medications`
--

LOCK TABLES `medications` WRITE;
/*!40000 ALTER TABLE `medications` DISABLE KEYS */;
INSERT INTO `medications` VALUES (1,1,101,'Paracetamol','500mg','2024-01-01','2024-01-07','Take one tablet every 6 hours after meals'),(2,2,101,'Amoxicillin','250mg','2024-02-01','2024-02-10','Take one capsule every 8 hours with water'),(3,3,101,'Ibuprofen','400mg','2024-03-01','2024-03-05','Take one tablet every 8 hours after meals'),(4,4,101,'Metformin','500mg','2024-04-01','2024-04-30','Take one tablet twice a day before meals'),(5,5,101,'Atorvastatin','20mg','2024-05-01','2024-05-30','Take one tablet at bedtime'),(6,6,102,'Salbutamol','2 puffs','2024-06-01','2024-06-15','Use inhaler as needed for shortness of breath'),(7,7,102,'Losartan','50mg','2024-07-01','2024-07-30','Take one tablet in the morning with water'),(8,8,102,'Cetrizine','10mg','2024-08-01','2024-08-10','Take one tablet once a day for allergies'),(9,9,102,'Ranitidine','150mg','2024-09-01','2024-09-10','Take one tablet before bedtime for acid reflux'),(10,10,102,'Vitamin D','2000 IU','2024-10-01','2024-10-31','Take one capsule daily with food'),(11,11,103,'Omeprazole','20mg','2024-11-01','2024-11-15','Take one tablet before breakfast'),(12,12,103,'Prednisolone','5mg','2024-12-01','2024-12-07','Take one tablet three times a day after meals'),(13,13,103,'Hydrochlorothiazide','25mg','2024-01-01','2024-01-31','Take one tablet in the morning with water'),(14,14,103,'Aspirin','75mg','2024-02-01','2024-02-28','Take one tablet daily after breakfast'),(15,15,103,'Levothyroxine','50mcg','2024-03-01','2024-03-31','Take one tablet in the morning on an empty stomach'),(16,16,104,'Clarithromycin','500mg','2024-04-01','2024-04-14','Take one tablet every 12 hours with food'),(17,17,104,'Furosemide','40mg','2024-05-01','2024-05-15','Take one tablet in the morning with water'),(18,18,104,'Insulin','10 units','2024-06-01','2024-06-30','Inject subcutaneously before meals'),(19,19,104,'Montelukast','10mg','2024-07-01','2024-07-31','Take one tablet daily in the evening'),(20,20,104,'Azithromycin','500mg','2024-08-01','2024-08-05','Take one tablet once a day for five days');
/*!40000 ALTER TABLE `medications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-03  1:05:52
