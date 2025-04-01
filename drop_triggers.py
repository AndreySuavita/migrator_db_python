import mysql.connector
from decouple import config

""" 
    This file will help you to drop every trigger in the local DB 

"""
""" -------------- Star creation of tables --------------- """

DB_HOST_LOCAL_ = config('DB_HOST_LOCAL_')
DB_USER_LOCAL_ = config('DB_USER_LOCAL_')
DB_PASSWORD_LOCAL_ = config('DB_PASSWORD_LOCAL_')
DB_NAME_LOCAL_ = config('DB_NAME_LOCAL_')


midb_second = mysql.connector.connect(
    host=DB_HOST_LOCAL_,
    user=DB_USER_LOCAL_,
    password=DB_PASSWORD_LOCAL_,
    database=DB_NAME_LOCAL_
) # Secundary DataBase

cursor_1 = midb_second.cursor()

""" Query to get all the triggers in the Main Database"""
cursor_1.execute("SELECT TRIGGER_NAME FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = 'PE_AWS'")
triggers_names = cursor_1.fetchall()

""" for to go through each trigger and drop it in the new DB"""
for trigger in triggers_names:
    #print(trigger)

    drop_trigger_query =f""" DROP TRIGGER IF EXISTS {trigger[0]} """
    print(drop_trigger_query)

    cursor_1.execute(drop_trigger_query)
    midb_second.commit()


""" Close connection """

midb_second.close()