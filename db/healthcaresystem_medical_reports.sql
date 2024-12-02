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
-- Table structure for table `medical_reports`
--

DROP TABLE IF EXISTS `medical_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_reports` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `report_date` date NOT NULL,
  `diagnosis` text NOT NULL,
  `recommendations` text,
  PRIMARY KEY (`report_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `medical_reports_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `medical_reports_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_reports`
--

LOCK TABLES `medical_reports` WRITE;
/*!40000 ALTER TABLE `medical_reports` DISABLE KEYS */;
INSERT INTO `medical_reports` VALUES (1,1,101,'2024-12-02','Normal health, no major issues detected.','Continue routine health monitoring, maintain diet plan.'),(2,2,101,'2024-12-02','Diagnosed with Diabetes, blood sugar levels above normal.','Adhere to medication, avoid sugar, monitor blood sugar daily.'),(3,3,101,'2024-12-03','Mild Asthma, increased breathlessness in cold weather.','Use inhaler as needed, avoid cold air, regular checkups.'),(4,4,101,'2024-12-03','General fatigue, no major conditions found.','Rest and hydration recommended, checkup in 1 month.'),(5,5,101,'2024-12-04','High blood pressure, borderline hypertension.','Follow prescribed medication, reduce salt intake, exercise regularly.'),(6,6,102,'2024-12-04','Routine blood work shows no significant issues.','Maintain a balanced diet and regular physical activity.'),(7,7,102,'2024-12-05','Mild obesity, elevated cholesterol levels.','Adopt a low-fat diet, exercise regularly, and monitor cholesterol.'),(8,8,102,'2024-12-05','Cholesterol slightly elevated, no cardiovascular risk currently.','Continue monitoring, improve diet, and increase physical activity.'),(9,9,102,'2024-12-06','No major health issues found during routine checkup.','Keep maintaining a healthy lifestyle.'),(10,10,102,'2024-12-06','Fatigue, suspected vitamin D deficiency.','Start vitamin D supplementation and regular exercise.'),(11,11,103,'2024-12-07','Routine checkup, all vitals normal.','Continue healthy living, regular checkups every 6 months.'),(12,12,103,'2024-12-07','General wellness checkup, no serious concerns found.','Maintain current diet, stay active, routine checkup in 6 months.'),(13,13,103,'2024-12-08','Asthma follow-up, no significant changes since last checkup.','Continue medication, monitor symptoms during cold weather.'),(14,14,103,'2024-12-08','Hypertension, blood pressure remains high.','Continue medication, regular blood pressure monitoring, stress management.'),(15,15,103,'2024-12-09','Routine checkup, no issues found.','Maintain lifestyle, stay active, next checkup in 1 year.'),(16,16,104,'2024-12-09','Cholesterol levels elevated, borderline hypertension.','Dietary changes and exercise, monitor cholesterol levels regularly.'),(17,17,104,'2024-12-10','Sleep issues related to stress, no serious conditions detected.','Stress management techniques, improve sleep hygiene, follow-up in 1 month.'),(18,18,104,'2024-12-10','Nutritional deficiencies, poor dietary habits.','Start nutrition supplements, improve diet with guidance from a nutritionist.'),(19,19,104,'2024-12-11','Anxiety, stress-related health issues.','Start therapy, manage stress, consider anxiety medication if necessary.'),(20,20,104,'2024-12-11','Hypertension, blood pressure elevated.','Continue prescribed medications, reduce sodium intake, monitor blood pressure.');
/*!40000 ALTER TABLE `medical_reports` ENABLE KEYS */;
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
