Here you can find a guide to migrate the DB in MySQL to your local PC or to another location. Additionally, you need to install Python version 3.12 or later.

1. To activate the migrator, you need to install the following libraries:
   - decouple v3.8
   - mysql-connector v8.2

   Please run the following lines in your terminal after installing Python:
   ```bash
   pip install mysql-connector-python==8.2.0
   pip install python-decouple==3.8
   ```

2. You need to set up a new schema in the main DB by following these steps:
   Enter to your local Data Base and run the next query:
   ```sql
   CREATE SCHEMA IF NOT EXISTS `Name_of_new_schema`;
   ```

3. You need to set up the credentials of the DB. Open the file "env.py" and fill in the credentials of the main DB and target DB.
   
   The credentials of the main DB are the credentials of the DataBase that already exists and the credentials of the target DB are about the new Database.

4. You need to run the file "schemas_creator.py" to create all the tables in the new DB. These tables are a copy of the main DB, but they are still empty. To run the file you can use this line:
   ```bash
   python schemas_creator.py
   ```

5. Deal with Big tables, you can run the file 'subtables_creator.py' in order to find tables too big in the original DB. This program will create a sub DB with a lot of subtables. This takes a little bit of time but you only need to do this once. If another person wants to migrate the database and these subtables already exist, you can avoid this step. This action will help to migrate the big tables. You can modify the value to find big tables in the file .env in the variable 'LIMIT_WEIGH_TABLES'.
   ```bash
   python subtables_creator.py
   ```

6. Open the file "pass_little_tables.py" and add the names of the tables you want to exclude from the migration on line 17. Recommended: "audittrail" and "helpdesk_communication". If you want to migrate the entire DB, leave the list as "tables_to_avoid = []". Then, run the file using the following command:
   ```bash
   python pass_little_tables.py
   ```

7. Simultaneously you can open another terminal and run the file 'pass_big_tables.py'. This file will migrate the big tables since the subtables created in step 5. Be sure the subtables are already created before executing this step.
   ```bash
   python pass_big_tables.py
   ```

8. If you are migrating the full tables, please skip this step. Open the file "one_table.py" and add the name of the table you want to migrate to the list on line 10. For example, "audittrail" or "helpdesk_communication", and run the next command:
   ```bash
   python one_table.py
   ```

9. Add the variable in the file my.ini:
   ```ini
   sql_mode = NO_ENGINE_SUBSTITUTION
   skip-log-bin
   ```

   Or run these lines in your MySQL Workbench (but it only works during the session):
   ```sql
   SET GLOBAL sql_mode = 'NO_ENGINE_SUBSTITUTION';
   SELECT @@GLOBAL.sql_mode;
   SELECT @@SESSION.sql_mode;
   ```

10. After you need to run the next lines in the command line to create the functions and the triggers:
    ```bash
    python functions_creator.py
    python triggers_creator.py
    ```

    If you want to drop the functions or the triggers you can run in the command line:
    ```bash
    python drop_functions.py
    python drop_triggers.py
    ```

11. The new database is ready to work.


