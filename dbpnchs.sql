-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: dbpnchs
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fingerprints`
--

DROP TABLE IF EXISTS `fingerprints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fingerprints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) DEFAULT NULL,
  `user_name` varchar(150) NOT NULL,
  `fingerprint_template` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `finger_index` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_emp_finger` (`employee_id`,`finger_index`),
  CONSTRAINT `fk_fingerprint_employee` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fingerprints`
--

LOCK TABLES `fingerprints` WRITE;
/*!40000 ALTER TABLE `fingerprints` DISABLE KEYS */;
INSERT INTO `fingerprints` VALUES (1,'EMP-001','John Lenard Bocal','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','2026-03-26 07:39:27',1),(3,'EMP-002','x x','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','2026-04-17 13:16:08',1);
/*!40000 ALTER TABLE `fingerprints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblbiometric_logs`
--

DROP TABLE IF EXISTS `tblbiometric_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblbiometric_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) NOT NULL,
  `log_type` varchar(20) NOT NULL,
  `log_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_bio_emp` (`employee_id`),
  CONSTRAINT `fk_bio_emp` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblbiometric_logs`
--

LOCK TABLES `tblbiometric_logs` WRITE;
/*!40000 ALTER TABLE `tblbiometric_logs` DISABLE KEYS */;
INSERT INTO `tblbiometric_logs` VALUES (9,'EMP-001','IN','2026-04-01 07:45:00'),(10,'EMP-001','OUT','2026-04-01 17:02:00'),(11,'EMP-001','IN','2026-04-02 08:10:00'),(12,'EMP-001','OUT','2026-04-02 16:55:00'),(13,'EMP-001','IN','2026-04-03 07:55:00'),(14,'EMP-001','OUT','2026-04-03 17:10:00'),(15,'EMP-001','IN','2026-04-06 08:05:00'),(16,'EMP-001','OUT','2026-04-06 17:00:00'),(17,'EMP-001','IN','2026-04-07 07:40:00'),(18,'EMP-001','OUT','2026-04-07 16:45:00'),(19,'EMP-001','IN','2026-04-08 08:20:00'),(20,'EMP-001','OUT','2026-04-08 17:05:00'),(21,'EMP-001','IN','2026-04-09 07:50:00'),(22,'EMP-001','OUT','2026-04-09 16:50:00'),(23,'EMP-001','IN','2026-04-10 08:15:00'),(24,'EMP-001','OUT','2026-04-10 17:00:00'),(25,'EMP-001','IN','2026-04-13 07:35:00'),(26,'EMP-001','OUT','2026-04-13 16:40:00'),(27,'EMP-001','IN','2026-04-14 08:00:00'),(28,'EMP-001','OUT','2026-04-14 16:58:00'),(29,'EMP-001','am_time_in','2026-04-17 13:15:44'),(30,'EMP-001','am_time_in','2026-04-17 13:16:14'),(31,'EMP-002','am_time_in','2026-04-17 13:16:25');
/*!40000 ALTER TABLE `tblbiometric_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblemployee`
--

DROP TABLE IF EXISTS `tblemployee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblemployee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `designation` varchar(120) NOT NULL,
  `birthday` date DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `contact` varchar(30) NOT NULL,
  `address` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblemployee`
--

LOCK TABLES `tblemployee` WRITE;
/*!40000 ALTER TABLE `tblemployee` DISABLE KEYS */;
INSERT INTO `tblemployee` VALUES (1,'EMP-001','John Lenard','Bocal','Faculty','2026-03-03','bjohnlenard@gmail.com','+639077888705','P.D. Monfort South, Dumangas, Iloilo','2026-03-03 09:14:21','2026-04-17 10:57:04'),(3,'EMP-002','x','x','Faculty','2026-04-17','x','x','xx','2026-04-17 13:13:42','2026-04-17 13:13:42'),(4,'EMP-003','Jane','Doe','Staff','1995-12-05','jane.doe@example.com','09123456789','123 Test St','2026-04-22 20:00:54','2026-04-22 20:00:54');
/*!40000 ALTER TABLE `tblemployee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblglobal_payheads`
--

DROP TABLE IF EXISTS `tblglobal_payheads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblglobal_payheads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `description` text,
  `amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `mode` enum('Amount','Percentage') DEFAULT 'Amount',
  `percentage_value` decimal(10,2) DEFAULT '0.00',
  `type` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblglobal_payheads`
--

LOCK TABLES `tblglobal_payheads` WRITE;
/*!40000 ALTER TABLE `tblglobal_payheads` DISABLE KEYS */;
INSERT INTO `tblglobal_payheads` VALUES (9,'PERA',NULL,2000.00,'Amount',0.00,'Earning','2026-04-21 12:11:18','2026-04-21 12:11:18'),(11,'GSIS','GSIS Contribution',10000.00,'Amount',0.00,'Deduction','2026-04-22 18:17:08','2026-04-22 18:17:08'),(13,'Standardization Test','',0.00,'Percentage',2.00,'Earning','2026-04-22 19:57:22','2026-04-22 19:57:22');
/*!40000 ALTER TABLE `tblglobal_payheads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblholidays`
--

DROP TABLE IF EXISTS `tblholidays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblholidays` (
  `id` int NOT NULL AUTO_INCREMENT,
  `holiday_date` date NOT NULL,
  `holiday_name` varchar(150) NOT NULL,
  `holiday_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblholidays`
--

LOCK TABLES `tblholidays` WRITE;
/*!40000 ALTER TABLE `tblholidays` DISABLE KEYS */;
INSERT INTO `tblholidays` VALUES (1,'2026-01-01','New Year\'s Day','Regular'),(2,'2026-02-25','EDSA People Power Revolution','Special'),(3,'2026-04-02','Maundy Thursday','Regular'),(4,'2026-04-03','Good Friday','Regular'),(5,'2026-04-09','Araw ng Kagitingan','Regular'),(6,'2026-05-01','Labor Day','Regular'),(7,'2026-06-12','Independence Day','Regular'),(8,'2026-08-21','Ninoy Aquino Day','Special'),(9,'2026-08-31','National Heroes Day','Regular'),(10,'2026-11-01','All Saints\' Day','Special'),(11,'2026-11-30','Bonifacio Day','Regular'),(12,'2026-12-25','Christmas Day','Regular'),(13,'2026-12-30','Rizal Day','Regular');
/*!40000 ALTER TABLE `tblholidays` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblleaves`
--

DROP TABLE IF EXISTS `tblleaves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblleaves` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) NOT NULL,
  `leave_date` date NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `fk_leave_emp` (`employee_id`),
  CONSTRAINT `fk_leave_emp` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblleaves`
--

LOCK TABLES `tblleaves` WRITE;
/*!40000 ALTER TABLE `tblleaves` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblleaves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblpayhead`
--

DROP TABLE IF EXISTS `tblpayhead`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblpayhead` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) NOT NULL,
  `pay_head` varchar(120) NOT NULL,
  `description` text,
  `amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `mode` enum('Amount','Percentage') DEFAULT 'Amount',
  `percentage_value` decimal(10,2) DEFAULT '0.00',
  `category` enum('Earning','Deduction') DEFAULT 'Earning',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_payhead_employee` (`employee_id`),
  CONSTRAINT `fk_payhead_employee` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblpayhead`
--

LOCK TABLES `tblpayhead` WRITE;
/*!40000 ALTER TABLE `tblpayhead` DISABLE KEYS */;
INSERT INTO `tblpayhead` VALUES (10,'EMP-002','Basic Salary',NULL,15000.00,'Amount',0.00,'Earning','2026-04-17 13:13:42','2026-04-17 13:13:42'),(31,'EMP-001','Basic Salary','',30000.00,'Amount',0.00,'Earning','2026-04-22 19:53:44','2026-04-22 19:53:44'),(32,'EMP-001','Bonus','Special performance bonus',1000.00,'Amount',0.00,'Earning','2026-04-22 19:53:44','2026-04-22 19:53:44'),(33,'EMP-001','Loan','',500.00,'Amount',0.00,'Deduction','2026-04-22 19:53:44','2026-04-22 19:53:44'),(34,'EMP-001','Phone Allowance','',600.00,'Percentage',2.00,'Earning','2026-04-22 19:53:44','2026-04-22 19:53:44'),(35,'EMP-001','Individual % Test','',0.30,'Percentage',0.00,'Earning','2026-04-22 19:53:44','2026-04-22 19:53:44'),(36,'EMP-003','Basic Salary','',0.00,'Amount',0.00,'Earning','2026-04-22 20:00:54','2026-04-22 20:00:54');
/*!40000 ALTER TABLE `tblpayhead` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblpayroll`
--

DROP TABLE IF EXISTS `tblpayroll`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblpayroll` (
  `id` int NOT NULL AUTO_INCREMENT,
  `period_key` varchar(20) NOT NULL,
  `year` int NOT NULL,
  `month` int NOT NULL,
  `half` int NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT 'Draft',
  `remarks` text,
  `approved_by` varchar(150) DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `period_key` (`period_key`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblpayroll`
--

LOCK TABLES `tblpayroll` WRITE;
/*!40000 ALTER TABLE `tblpayroll` DISABLE KEYS */;
INSERT INTO `tblpayroll` VALUES (43,'2026-4-1',2026,4,1,'For Approval',NULL,NULL,NULL,'2026-04-22 19:57:36','2026-04-22 20:05:46');
/*!40000 ALTER TABLE `tblpayroll` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblpayroll_details`
--

DROP TABLE IF EXISTS `tblpayroll_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblpayroll_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `period_key` varchar(20) NOT NULL,
  `employee_id` varchar(20) NOT NULL,
  `basic_salary` decimal(10,2) DEFAULT '0.00',
  `half_basic` decimal(10,2) DEFAULT '0.00',
  `other_earnings` decimal(10,2) DEFAULT '0.00',
  `holiday_pay` decimal(10,2) DEFAULT '0.00',
  `other_deductions` decimal(10,2) DEFAULT '0.00',
  `daily_rate` decimal(10,2) DEFAULT '0.00',
  `absent_days` int DEFAULT '0',
  `absent_deduction` decimal(10,2) DEFAULT '0.00',
  `late_minutes` int DEFAULT '0',
  `undertime_minutes` int DEFAULT '0',
  `tardiness_deduction` decimal(10,2) DEFAULT '0.00',
  `undertime_deduction` decimal(10,2) DEFAULT '0.00',
  `sss_ee` decimal(10,2) DEFAULT '0.00',
  `philhealth_ee` decimal(10,2) DEFAULT '0.00',
  `pagibig_ee` decimal(10,2) DEFAULT '0.00',
  `withholding_tax` decimal(10,2) DEFAULT '0.00',
  `statutory_json` text,
  `total_gross` decimal(10,2) DEFAULT '0.00',
  `total_deduct` decimal(10,2) DEFAULT '0.00',
  `net_pay` decimal(10,2) DEFAULT '0.00',
  `is_negative` tinyint(1) DEFAULT '0',
  `dtr_filed` tinyint(1) DEFAULT '0',
  `payheads_json` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pd_payroll` (`period_key`),
  KEY `fk_pd_emp` (`employee_id`),
  CONSTRAINT `fk_pd_emp` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_pd_payroll` FOREIGN KEY (`period_key`) REFERENCES `tblpayroll` (`period_key`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblpayroll_details`
--

LOCK TABLES `tblpayroll_details` WRITE;
/*!40000 ALTER TABLE `tblpayroll_details` DISABLE KEYS */;
INSERT INTO `tblpayroll_details` VALUES (64,'2026-4-1','EMP-001',30000.00,15000.00,2100.00,0.00,10586.50,1363.64,0,0.00,201,54,571.02,153.41,0.00,200.00,0.00,1151.71,'{\"GSIS_LOAN\": 500.0, \"PHIC_RATE\": 750.0, \"PHIC_CAP\": 2500.0, \"PHIC_FLOOR\": 250.0, \"PAGIBIG_EE_RATE\": 300.0, \"PAGIBIG_EE_CAP\": 50.0, \"TEST_RULE_2\": 61.5, \"XD\": 50.0, \"GSIS_PREMIUM\": 500.0, \"PHILHEALTH\": 200.0, \"PAG-IBIG FUND\": 100.0, \"WITHHOLDING TAX\": 275.0, \"ABSENCE\": 0.0, \"TARDINESS\": 571.02, \"UNDERTIME\": 153.41, \"WTAX\": 1151.71}',17100.00,12662.64,4437.36,0,1,'{\"earnings\": [{\"name\": \"Bonus\", \"amount\": 500.0}, {\"name\": \"Phone Allowance\", \"amount\": 300.0}, {\"name\": \"Individual % Test\", \"amount\": 0.0}, {\"name\": \"PERA\", \"amount\": 1000.0}, {\"name\": \"Standardization Test\", \"amount\": 300.0}], \"deductions\": [{\"name\": \"Loan\", \"amount\": 250.0}, {\"name\": \"GSIS\", \"amount\": 5000.0}]}'),(65,'2026-4-1','EMP-002',15000.00,7500.00,1150.00,0.00,9811.50,681.82,11,7500.00,0,0,0.00,0.00,0.00,200.00,0.00,0.00,'{\"GSIS_LOAN\": 500.0, \"PHIC_RATE\": 375.0, \"PHIC_CAP\": 2500.0, \"PHIC_FLOOR\": 250.0, \"PAGIBIG_EE_RATE\": 150.0, \"PAGIBIG_EE_CAP\": 50.0, \"TEST_RULE_2\": 61.5, \"XD\": 50.0, \"GSIS_PREMIUM\": 500.0, \"PHILHEALTH\": 200.0, \"PAG-IBIG FUND\": 100.0, \"WITHHOLDING TAX\": 275.0, \"ABSENCE\": 7500.0, \"TARDINESS\": 0.0, \"UNDERTIME\": 0.0, \"WTAX\": 0.0}',8650.00,17511.50,0.00,1,0,'{\"earnings\": [{\"name\": \"PERA\", \"amount\": 1000.0}, {\"name\": \"Standardization Test\", \"amount\": 150.0}], \"deductions\": [{\"name\": \"GSIS\", \"amount\": 5000.0}]}');
/*!40000 ALTER TABLE `tblpayroll_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblstatutory_registry`
--

DROP TABLE IF EXISTS `tblstatutory_registry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblstatutory_registry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) NOT NULL,
  `config_value` varchar(255) NOT NULL,
  `config_mode` enum('Amount','Percentage') DEFAULT 'Percentage',
  `description` text,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblstatutory_registry`
--

LOCK TABLES `tblstatutory_registry` WRITE;
/*!40000 ALTER TABLE `tblstatutory_registry` DISABLE KEYS */;
INSERT INTO `tblstatutory_registry` VALUES (10,'SSS_ENABLED','1','Amount','Enable SSS calculations (1=Yes, 0=No)','2026-04-22 14:04:14'),(12,'GSIS_LOAN','1000','Amount','GSIS LOAN','2026-04-22 15:18:55'),(13,'PHIC_RATE','5.00','Percentage','PhilHealth employee+employer combined rate','2026-04-22 19:45:41'),(14,'PHIC_CAP','5000.00','Amount','Maximum monthly PhilHealth total contribution','2026-04-22 16:05:21'),(15,'PHIC_FLOOR','500.00','Amount','Minimum monthly PhilHealth total contribution','2026-04-22 16:05:21'),(16,'PAGIBIG_EE_RATE','2.00','Percentage','Pag-IBIG employee rate','2026-04-22 19:45:41'),(17,'PAGIBIG_EE_CAP','100.00','Amount','Maximum semi-monthly Pag-IBIG employee share','2026-04-22 16:05:21'),(18,'BIR_ENABLED','1','Amount','Enable Withholding Tax (1=Yes, 0=No)','2026-04-22 16:05:21'),(19,'TEST_RULE_2','123','Amount','Test Rule Description','2026-04-22 15:46:57'),(21,'XD','100','Amount','sample','2026-04-22 15:55:19'),(22,'GSIS_PREMIUM','1000','Amount','GSIS PREMIUM','2026-04-22 16:21:45'),(23,'PHILHEALTH','400','Amount','PHILHEALTH','2026-04-22 16:23:11'),(24,'PAG-IBIG FUND','200','Amount','PAG-IBIG FUND','2026-04-22 16:23:30'),(25,'WITHHOLDING TAX','550','Amount','WITHHOLDING TAX','2026-04-22 16:23:48');
/*!40000 ALTER TABLE `tblstatutory_registry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbltime_logs`
--

DROP TABLE IF EXISTS `tbltime_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbltime_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(20) NOT NULL,
  `work_date` date NOT NULL,
  `am_time_in` time DEFAULT NULL,
  `am_time_out` time DEFAULT NULL,
  `pm_time_in` time DEFAULT NULL,
  `pm_time_out` time DEFAULT NULL,
  `xtimestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  UNIQUE KEY `unique_employee_day` (`employee_id`,`work_date`),
  CONSTRAINT `fk_employee` FOREIGN KEY (`employee_id`) REFERENCES `tblemployee` (`employee_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbltime_logs`
--

LOCK TABLES `tbltime_logs` WRITE;
/*!40000 ALTER TABLE `tbltime_logs` DISABLE KEYS */;
INSERT INTO `tbltime_logs` VALUES (59,'EMP-001','2026-04-01','07:32:00','11:30:00','13:00:00','17:02:00','2026-04-17 05:04:12'),(60,'EMP-001','2026-04-02','07:45:00','11:25:00','13:05:00','17:00:00','2026-04-17 05:04:12'),(61,'EMP-001','2026-04-03','07:30:00','11:30:00','13:00:00','17:00:00','2026-04-17 05:04:12'),(62,'EMP-001','2026-04-04','08:05:00','11:20:00','13:10:00','16:55:00','2026-04-17 05:04:12'),(63,'EMP-001','2026-04-05','07:35:00','11:30:00','13:02:00','17:05:00','2026-04-17 05:04:12'),(64,'EMP-001','2026-04-06','07:30:00','11:28:00','13:00:00','17:00:00','2026-04-17 05:04:12'),(65,'EMP-001','2026-04-07','07:50:00','11:30:00','13:15:00','17:10:00','2026-04-17 05:04:12'),(66,'EMP-001','2026-04-08','07:33:00','11:30:00','13:00:00','16:58:00','2026-04-17 05:04:12'),(67,'EMP-001','2026-04-09','07:30:00','11:30:00','13:00:00','17:00:00','2026-04-17 05:04:12'),(68,'EMP-001','2026-04-10','08:00:00','11:15:00','13:05:00','17:00:00','2026-04-17 05:04:12'),(69,'EMP-001','2026-04-11','07:40:00','11:30:00','13:00:00','17:03:00','2026-04-17 05:04:12'),(70,'EMP-001','2026-04-12','07:30:00','11:30:00','13:00:00','17:00:00','2026-04-17 05:04:12'),(71,'EMP-001','2026-04-13','07:55:00','11:25:00','13:08:00','16:50:00','2026-04-17 05:04:12'),(72,'EMP-001','2026-04-14','07:30:00','11:30:00','13:00:00','17:00:00','2026-04-17 05:04:12'),(73,'EMP-001','2026-04-15','07:38:00','11:30:00','13:03:00','17:07:00','2026-04-17 05:04:12');
/*!40000 ALTER TABLE `tbltime_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblusers`
--

DROP TABLE IF EXISTS `tblusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblusers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(150) NOT NULL,
  `role` varchar(50) NOT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblusers`
--

LOCK TABLES `tblusers` WRITE;
/*!40000 ALTER TABLE `tblusers` DISABLE KEYS */;
INSERT INTO `tblusers` VALUES (1,'admin','admin123','Overall Admin','Admin',NULL,'2026-04-16 18:34:26','2026-04-16 18:34:26'),(2,'finance','finance123','Finance Dept','Finance',NULL,'2026-04-16 18:34:26','2026-04-16 18:34:26'),(3,'hr','hr1234','HR Dept','HR',NULL,'2026-04-16 18:34:26','2026-04-16 18:34:26'),(4,'bjohnlenard@gmail.com','EMP-001','John Lenard Bocal','Employee','EMP-001','2026-04-16 18:34:26','2026-04-16 18:34:26'),(5,'doe','doe','Jane Doe','Employee','EMP-003','2026-04-22 20:00:54','2026-04-22 20:00:54');
/*!40000 ALTER TABLE `tblusers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 20:37:52
