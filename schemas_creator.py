import mysql.connector
from decouple import config

""" 
    This file will help you to create every table in the local DB from the Main DB,
    - you first need to create the schema in the Local DB, for that use this sentence:
        CREATE SCHEMA IF NOT EXISTS `Name_of_new_schema` ;
"""
""" -------------- Star creation of tables --------------- """
DB_HOST_ = config('DB_HOST_')
DB_USER_ = config('DB_USER_')
DB_PASSWORD_ = config('DB_PASSWORD_')
DB_NAME_ = config('DB_NAME_')

DB_HOST_LOCAL_ = config('DB_HOST_LOCAL_')
DB_USER_LOCAL_ = config('DB_USER_LOCAL_')
DB_PASSWORD_LOCAL_ = config('DB_PASSWORD_LOCAL_')
DB_NAME_LOCAL_ = config('DB_NAME_LOCAL_')

midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
) # Main DataBase
midb_second = mysql.connector.connect(
    host=DB_HOST_LOCAL_,
    user=DB_USER_LOCAL_,
    password=DB_PASSWORD_LOCAL_,
    database=DB_NAME_LOCAL_
) # Secundary DataBase

cursor_1 = midb_main.cursor()
cursor_2 = midb_second.cursor()

""" Query to anule the foreign_key of tables"""
cursor_2.execute("SET FOREIGN_KEY_CHECKS = 0;")
midb_second.commit()

""" Query to get all the tables in the Main Database"""
cursor_1.execute(f'SHOW TABLES FROM {DB_NAME_}')
response_tables = cursor_1.fetchall()

#print(response_tables)
#exit()

for table in response_tables:
    print(table[0])
    # if table[0] in ['cruiseship_schedules_ports','emails_unsubscribe']:
    #     continue
    cursor_1.execute(f'SHOW CREATE TABLE {table[0]}')
    response_create_tables = cursor_1.fetchall()[0][1]
    response_create_tables = response_create_tables.replace("CREATE TABLE",f"CREATE TABLE IF NOT EXISTS `{DB_NAME_LOCAL_}`.")
    """ The most resent versions of MySQL doesn't admit '0000-00-00 00:00:00' in datetime columns"""
    response_create_tables = response_create_tables.replace("datetime NOT NULL DEFAULT '0000-00-00 00:00:00'","datetime DEFAULT NULL")
    #print(response_create_tables)
    #exit()
    cursor_2.execute(response_create_tables)
    midb_second.commit()
    #exit()


""" Query to activate the foreign_key of tables"""
cursor_2.execute("SET FOREIGN_KEY_CHECKS = 1;")
midb_second.commit()


""" Close connection """
midb_main.close()
midb_second.close()