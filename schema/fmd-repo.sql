-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: fmd-repo
-- ------------------------------------------------------
-- Server version	8.0.30-0ubuntu0.20.04.2

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
-- Table structure for table `bees`
--

DROP TABLE IF EXISTS `bees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bees` (
  `bee_no` int unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_no` varchar(100) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bee_no`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_account`
--

DROP TABLE IF EXISTS `co_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_account` (
  `co_account_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_account_name` varchar(100) NOT NULL,
  `co_account_no` varchar(100) NOT NULL,
  `co_account_currency` varchar(100) NOT NULL,
  `co_account_host` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_company`
--

DROP TABLE IF EXISTS `co_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_company` (
  `co_company_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_fund_id` int unsigned NOT NULL,
  `co_company_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_company_id`),
  KEY `co_company__co_fund_idx` (`co_fund_id`),
  CONSTRAINT `co_company__co_fund` FOREIGN KEY (`co_fund_id`) REFERENCES `co_fund` (`co_fund_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_fund`
--

DROP TABLE IF EXISTS `co_fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_fund` (
  `co_fund_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_fund_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_fund_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_loans`
--

DROP TABLE IF EXISTS `co_loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_loans` (
  `co_loans_id` int unsigned NOT NULL AUTO_INCREMENT,
  `bee_no` int unsigned NOT NULL,
  `co_loans_type_id` int unsigned NOT NULL,
  `co_company_id` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_loans_id`),
  KEY `co_loans--co_company_idx` (`co_company_id`),
  KEY `co_loans__bee_no_idx` (`bee_no`),
  KEY `co_loans__co_loans_type_idx` (`co_loans_type_id`),
  CONSTRAINT `co_loans__bee_no` FOREIGN KEY (`bee_no`) REFERENCES `bees` (`bee_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_loans__co_company` FOREIGN KEY (`co_company_id`) REFERENCES `co_company` (`co_company_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_loans__co_loans_type` FOREIGN KEY (`co_loans_type_id`) REFERENCES `co_loans_type` (`co_loans_type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_loans_type`
--

DROP TABLE IF EXISTS `co_loans_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_loans_type` (
  `co_loans_type_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_loans_type_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_loans_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_operations`
--

DROP TABLE IF EXISTS `co_operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_operations` (
  `co_operations_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_operations_desc` varchar(100) NOT NULL,
  `co_company_id` int unsigned NOT NULL,
  `co_operations_type_id` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_operations_id`),
  KEY `co_operations__co_company_id_idx` (`co_company_id`),
  KEY `co_operations__co_operations_type_idx` (`co_operations_type_id`),
  CONSTRAINT `co_operations__co_company_id` FOREIGN KEY (`co_company_id`) REFERENCES `co_company` (`co_company_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_operations__co_operations_type` FOREIGN KEY (`co_operations_type_id`) REFERENCES `co_operations_type` (`co_operations_type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_operations_type`
--

DROP TABLE IF EXISTS `co_operations_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_operations_type` (
  `co_operations_type_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_operations_type_desc` varchar(100) NOT NULL,
  `last_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_operations_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_salaries`
--

DROP TABLE IF EXISTS `co_salaries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_salaries` (
  `co_salaries_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_fund_id` int unsigned NOT NULL,
  `bee_no` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_salaries_id`),
  KEY `co_salaries__co_fund_idx` (`co_fund_id`),
  KEY `co_salaries__bee_no_idx` (`bee_no`),
  CONSTRAINT `co_salaries__bee_no` FOREIGN KEY (`bee_no`) REFERENCES `bees` (`bee_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_salaries__co_fund` FOREIGN KEY (`co_fund_id`) REFERENCES `co_fund` (`co_fund_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_transaction`
--

DROP TABLE IF EXISTS `co_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_transaction` (
  `co_transaction_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_account_id` int unsigned NOT NULL,
  `co_transtatus_id` int unsigned NOT NULL,
  `co_loans_id` int unsigned DEFAULT NULL,
  `co_operations_id` int unsigned DEFAULT NULL,
  `co_salaries_id` int unsigned DEFAULT NULL,
  `money_in` decimal(15,4) DEFAULT NULL,
  `money_out` decimal(15,4) DEFAULT NULL,
  `date_of_transaction` datetime NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_transaction_id`),
  KEY `co_transactions__co_operations_idx` (`co_operations_id`),
  KEY `co_transactions__co_transtatus_idx` (`co_transtatus_id`),
  KEY `co_transactions__co_account_idx` (`co_account_id`),
  KEY `co_transactions__co_loans_idx` (`co_loans_id`),
  KEY `co_transactions__co_salaries_idx` (`co_salaries_id`),
  CONSTRAINT `co_transactions__co_account` FOREIGN KEY (`co_account_id`) REFERENCES `co_account` (`co_account_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_transactions__co_loans` FOREIGN KEY (`co_loans_id`) REFERENCES `co_loans` (`co_loans_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_transactions__co_operations` FOREIGN KEY (`co_operations_id`) REFERENCES `co_operations` (`co_operations_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_transactions__co_salaries` FOREIGN KEY (`co_salaries_id`) REFERENCES `co_salaries` (`co_salaries_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `co_transactions__co_transtatus` FOREIGN KEY (`co_transtatus_id`) REFERENCES `co_transtatus` (`co_transtatus_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=282 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `co_transtatus`
--

DROP TABLE IF EXISTS `co_transtatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `co_transtatus` (
  `co_transtatus_id` int unsigned NOT NULL AUTO_INCREMENT,
  `co_transtatus_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`co_transtatus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pay`
--

DROP TABLE IF EXISTS `pay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pay` (
  `pay_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_bees_id` int unsigned NOT NULL,
  `pay_amount` decimal(15,4) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pay_id`),
  KEY `pay_project_bees_idx` (`project_bees_id`),
  CONSTRAINT `pay-project_bees` FOREIGN KEY (`project_bees_id`) REFERENCES `project_bees` (`project_bees_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf32;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project` (
  `project_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_name` varchar(100) NOT NULL,
  `client_name` varchar(100) NOT NULL,
  `project_category_id` int unsigned NOT NULL,
  `project_source_id` int unsigned NOT NULL,
  `date_commencment` date NOT NULL,
  `date_completion` date DEFAULT NULL,
  `project_status_id` int unsigned NOT NULL,
  `project_fund_id` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`),
  KEY `project_fund_idx1` (`project_fund_id`),
  KEY `project-project_categoy_idx` (`project_category_id`),
  KEY `project-project_source_idx` (`project_source_id`),
  KEY `project_project_status_idx` (`project_status_id`),
  CONSTRAINT `project-project_categoy` FOREIGN KEY (`project_category_id`) REFERENCES `project_category` (`project_category_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project-project_fund` FOREIGN KEY (`project_fund_id`) REFERENCES `project_fund` (`project_fund_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project-project_source` FOREIGN KEY (`project_source_id`) REFERENCES `project_source` (`project_source_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_project_status` FOREIGN KEY (`project_status_id`) REFERENCES `project_status` (`project_status_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_bees`
--

DROP TABLE IF EXISTS `project_bees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_bees` (
  `project_bees_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL,
  `bee_no` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_bees_id`),
  KEY `project_bees-project_idx` (`project_id`),
  KEY `project_bees-bees_idx` (`bee_no`),
  CONSTRAINT `project_bees-bees` FOREIGN KEY (`bee_no`) REFERENCES `bees` (`bee_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_bees-project` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_category`
--

DROP TABLE IF EXISTS `project_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_category` (
  `project_category_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_category_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_fund`
--

DROP TABLE IF EXISTS `project_fund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_fund` (
  `project_fund_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_fund` decimal(15,4) DEFAULT NULL,
  `company_fund` decimal(15,4) DEFAULT NULL,
  `salaries_fund` decimal(15,4) DEFAULT NULL,
  `tax` decimal(15,4) DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_fund_id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_scope`
--

DROP TABLE IF EXISTS `project_scope`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_scope` (
  `project_scope_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL,
  `scope_id` int unsigned NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_scope_id`),
  KEY `project_scope-project_idx` (`project_id`),
  KEY `project_scope-scope_idx` (`scope_id`),
  CONSTRAINT `project_scope-project` FOREIGN KEY (`project_id`) REFERENCES `project` (`project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_scope-scope` FOREIGN KEY (`scope_id`) REFERENCES `scope` (`scope_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_source`
--

DROP TABLE IF EXISTS `project_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_source` (
  `project_source_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_source_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_source_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_status`
--

DROP TABLE IF EXISTS `project_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_status` (
  `project_status_id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_status_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scope`
--

DROP TABLE IF EXISTS `scope`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scope` (
  `scope_id` int unsigned NOT NULL AUTO_INCREMENT,
  `scope_desc` varchar(100) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`scope_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-09 21:57:35
