use pe_aws;

CREATE TABLE `cruiseship_schedules_ports` (
   `id` int unsigned NOT NULL AUTO_INCREMENT,
   `schedule_id` int unsigned NOT NULL,
   `day` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `title` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `port_id` int unsigned DEFAULT NULL,
   `arrive_date` date DEFAULT NULL,
   `arrive_time` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `depart_date` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `depart_time` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `updated_on` datetime NOT NULL,
   `updated_by` int DEFAULT NULL,
   PRIMARY KEY (`id`),
   #KEY `schedule_id` (`schedule_id`),
   KEY `port_id_idx` (`port_id`),
   CONSTRAINT `port_id` FOREIGN KEY (`port_id`) REFERENCES `transportation` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
   #CONSTRAINT `schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `cruiseship_schedules` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
 ) ENGINE=InnoDB AUTO_INCREMENT=281197947 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
 
 CREATE TABLE `emails_unsubscribe` (
   `id` int NOT NULL AUTO_INCREMENT,
   `type` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `email` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
   `created_on` datetime DEFAULT NULL,
   `created_by` int unsigned NOT NULL,
   `updated_by` int DEFAULT NULL,
   PRIMARY KEY (`id`),
   UNIQUE KEY `id2_UNIQUE` (`id`),
   KEY `updated_by21` (`created_by`),
   KEY `email_idx` (`email`(255)),
   KEY `email` (`email`),
   CONSTRAINT `created_by1email` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
   #CONSTRAINT `email` FOREIGN KEY (`email`) REFERENCES `emails` (`email`) ON DELETE RESTRICT ON UPDATE RESTRICT
 ) ENGINE=InnoDB AUTO_INCREMENT=4794 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
 
 

                        
SET SQL_SAFE_UPDATES = 0;