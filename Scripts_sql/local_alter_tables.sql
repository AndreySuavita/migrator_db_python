SET FOREIGN_KEY_CHECKS = 0;

#drop database prd_pe_aws;
#drop database pe_aws;
use PE_AWS;
SET GLOBAL log_bin_trust_function_creators = 1;

/*-------------------------------------PE_AWS-----------------------------------------------*/
ALTER TABLE pe_aws.businessprofiles_products MODIFY COLUMN created_on DATETIME NULL;

ALTER TABLE pe_aws.crm_contacts MODIFY COLUMN created_on DATETIME NULL;
ALTER TABLE pe_aws.crm_contacts MODIFY COLUMN updated_on DATETIME NULL;

ALTER TABLE pe_aws.crm_interactions MODIFY COLUMN created_on DATETIME NULL;
ALTER TABLE pe_aws.crm_interactions MODIFY COLUMN updated_on DATETIME NULL;

ALTER TABLE pe_aws.fielddefinitions MODIFY COLUMN updated_on DATETIME NULL;
#ALTER TABLE prd_pe_aws.fielddefinitions MODIFY COLUMN updated_on DATETIME NULL;

ALTER TABLE pe_aws.tags MODIFY COLUMN updated_on DATETIME NULL;
ALTER TABLE pe_aws.tags MODIFY COLUMN created_on DATETIME NULL;

/*-----------------------------------------------test queries to filter data in helpdesk_communication ---------------------------------------------*/
use PE_AWS;

SELECT count(*) from helpdesk_communication; #2251976
SELECT count(*) from helpdesk_communication WHERE date_format(helpdesk_communication.created_on,'%Y-%m') >= '2024-01'; #498232 # select the last part of the table
SELECT count(*) from helpdesk_communication WHERE date_format(helpdesk_communication.created_on,'%Y-%m') < '2024-01'; # 1753744 # select the first part of the table

SELECT count(*) from helpdesk_communication WHERE date_format(helpdesk_communication.created_on,'%Y-%m') >= '2023-11' OR date_format(helpdesk_communication.created_on,'%Y-%m') <= '2014-04'; #473460

SELECT count(*) FROM helpdesk_communication WHERE date_format(helpdesk_communication.created_on,'%Y-%m') >= '2020-01';

SELECT * FROM helpdesk_communication WHERE date_format(helpdesk_communication.created_on,'%Y-%m') >= '2024-01' LIMIT 1000 offset 0;
/*-------DB loads-------*/
SELECT table_schema "Base de Datos",
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) "Tamaño (MB)"
FROM information_schema.TABLES
GROUP BY table_schema;

SHOW STATUS;
SHOW PROCESSLIST;
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

#KILL 561473;

/*------------------------------ len of each table-----------------------------------------*/
SELECT table_name, table_rows
FROM information_schema.tables
WHERE table_schema = 'PE_AWS';

/*------------------------get queries to drop the triggers--------------------------------*/
/*
SELECT CONCAT('DROP TRIGGER IF EXISTS ', TRIGGER_NAME, ' ON ', EVENT_OBJECT_TABLE, ';') AS drop_command
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = 'PE_AWS';
*/
SELECT CONCAT('DROP TRIGGER IF EXISTS ', TRIGGER_NAME,  ';') AS drop_command
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = 'PE_AWS';

/*-----------------------------------------------query to order batch of data by year-----------------------------------------------------------------------*/
SELECT concat(date_format(created_on,'%Y')) as Year_, count(id) FROM helpdesk_communication 
	GROUP BY Year_; 