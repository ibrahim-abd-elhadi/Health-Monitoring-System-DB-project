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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` enum('Patient','Doctor','Admin') NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ahmed El-Sayed','ahmed@example.com','password123','01234567890','Patient','profile_pic.jpg','Male','2000-09-11','2024-12-01 18:56:42'),(2,'Fatma Mohamed','fatma@example.com','password123','01234567891','Patient','profile_pic.jpg','Female','2000-09-11','2024-12-01 18:56:42'),(3,'Mohamed Hassan','mohamed@example.com','password123','01234567892','Patient','profile_pic.jpg','Male','2000-09-11','2024-12-01 18:56:42'),(4,'Sara Ali','sara@example.com','password123','01234567893','Patient','profile_pic.jpg','Female','2000-09-11','2024-12-01 18:56:42'),(5,'Mona Khaled','mona@example.com','password123','01234567894','Patient','profile_pic.jpg','Female','2000-09-11','2024-12-01 18:56:42'),(6,'Tarek Fawzy','tarek@example.com','password123','01234567895','Patient','profile_pic.jpg','Male','2000-09-11','2024-12-01 18:56:42'),(7,'Amina Abdelrahman','amina@example.com','password123','01234567896','Patient','profile_pic.jpg','Female','2000-09-11','2024-12-01 18:56:42'),(8,'Omar Nasser','omar@example.com','password123','01234567897','Patient','profile_pic.jpg','Male','2000-09-11','2024-12-01 18:56:42'),(9,'Noha Youssef','noha@example.com','password123','01234567898','Patient','profile_pic.jpg','Female','2000-09-11','2024-12-01 18:56:42'),(10,'Khaled Ibrahim','khaled@example.com','password123','01234567899','Patient','profile_pic.jpg','Male','2000-09-11','2024-12-01 18:56:42'),(11,'Layla Saad','layla@example.com','password123','01234567900','Patient','profile_pic.jpg','Female','2003-04-11','2024-12-01 18:56:42'),(12,'Hossam Rami','hossam@example.com','password123','01234567901','Patient','profile_pic.jpg','Male','2003-04-11','2024-12-01 18:56:42'),(13,'Reem Gamil','reem@example.com','password123','01234567902','Patient','profile_pic.jpg','Female','2003-04-11','2024-12-01 18:56:42'),(14,'Mahmoud Taha','mahmoud@example.com','password123','01234567903','Patient','profile_pic.jpg','Male','2003-04-11','2024-12-01 18:56:42'),(15,'mariam kamal','mariam@example.com','password123','01234567904','Patient','profile_pic.jpg','Female','2003-04-11','2024-12-01 18:56:42'),(16,'Ramy Sabry','ramy@example.com','password123','01234567905','Patient','profile_pic.jpg','Male','2003-04-11','2024-12-01 18:56:42'),(17,'Dalia Hossam','dalia@example.com','password123','01234567906','Patient','profile_pic.jpg','Female','2003-04-11','2024-12-01 18:56:42'),(18,'Yasser Sherif','yasser@example.com','password123','01234567907','Patient','profile_pic.jpg','Male','2003-04-11','2024-12-01 18:56:42'),(19,'Hala Sami','hala@example.com','password123','01234567908','Patient','profile_pic.jpg','Female','2003-04-11','2024-12-01 18:56:42'),(20,'Maged Zaki','maged@example.com','password123','01234567909','Patient','profile_pic.jpg','Male','2003-04-11','2024-12-01 18:56:42'),(101,'Dr. Ahmed Saleh','ahmed.saleh@example.com','password123','01012345678','Doctor',NULL,'Male','2003-04-11','2024-12-01 20:05:32'),(102,'Dr. Mona Ali','mona.ali@example.com','password123','01023456789','Doctor',NULL,'Female','2003-04-11','2024-12-01 20:05:32'),(103,'Dr. Youssef Khaled','youssef.khaled@example.com','password123','01034567890','Doctor',NULL,'Male','2003-04-11','2024-12-01 20:05:32'),(104,'Dr. Samar Hossam','samar.hossam@example.com','password123','01045678901','Doctor',NULL,'Female','2003-04-11','2024-12-01 20:05:32'),(1000,'ibrahim abd-elhady','iam.ibrahim.abd.elhadi@gmail.com','admin1235879','1141065853','Admin','','Male','2003-04-11','2024-12-01 20:27:05');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-05 12:56:55
