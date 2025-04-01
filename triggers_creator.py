import mysql.connector
from decouple import config

""" 
    This file will help you to create function in the local DB 
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

""" Query to get all the triggers in the Main Database"""
cursor_1.execute("SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_STATEMENT, ACTION_TIMING FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = 'PE_AWS'")
triggers = cursor_1.fetchall()

""" for to go through each trigger and create it in the new DB"""
for trigger in triggers:
    print(trigger[0])

    trigger_query =f""" CREATE TRIGGER {trigger[0]} {trigger[4]} {trigger[1]} ON {trigger[2]} FOR EACH ROW {trigger[3]}"""
    #print(trigger_query)

    cursor_2.execute(trigger_query)
    midb_second.commit()
    

""" Close connection """
midb_main.close()
midb_second.close()

