Here you can find a guide to migrate the DB in MySql to your local PC or to another location.  Additionally, you need to install Python version 3.12 or later.

1. To activate the migrator, you need to install the following libraries:

	decouple v3.8
	mysql-connector v8.2

- Please run the following lines in your terminal after installing Python:

	pip install mysql-connector-python==8.2.0
	pip install python-decouple==3.8

2. You need to set up a new schema in the main DB by following these steps:

	enter to your local Data Base and run the next query:

		CREATE SCHEMA IF NOT EXISTS `Name_of_new_schema` ;

3. You need to set up the credentials of the DB. Open the file "env.py" and fill in the credentials of the main DB and target DB.
	 
	 The credentials of the main DB are the credentials of the DataBase that already exist and the credentials of the target DB are about the new Database.

4. You need to run the file "schemas_creator.py" to create all the tables in the new DB, this tables are a copy of the main DB, but they are still empty, to run the file you can use this line:

	python schemas_creator.py

5. Open the file "main.py" and add the names of the tables you want to exclude from the migration on line 17. Recommended: "audittrail" and "helpdesk_communication".
 If you want to migrate the entire DB, leave the list as "tables_to_avoid = []". Then, run the file using the following command:

	python main.py

5. If you are migrating the full tables, please skip this step. Open the file "one_table.py" and add the name of the table you want to migrate to the list on line 10. 
	For example, "audittrail" or "helpdesk_communication", and run the next command:

	python one_table.py

6. Add the variable in the file my.ini:
	sql_mode = NO_ENGINE_SUBSTITUTION
	skip-log-bin

	- Or run this lines in your MySQL Workbench but it only works during the session:
	SET GLOBAL sql_mode = 'NO_ENGINE_SUBSTITUTION';
	SELECT @@GLOBAL.sql_mode;
	SELECT @@SESSION.sql_mode;


7. After you need to include the functions of the database, you can find the script in the folder "Scripts_sql", the file is pe_aws_functions

8. The new database is ready to work.