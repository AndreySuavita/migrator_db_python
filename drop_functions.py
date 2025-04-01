import mysql.connector
from decouple import config

""" 
    This file will help you to drop every function in the local 

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

""" Query to get all the functions in the Main Database"""
cursor_1.execute("SELECT ROUTINE_NAME FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'PE_AWS' AND ROUTINE_TYPE = 'FUNCTION'")
functions_names = cursor_1.fetchall()

""" for to go through each function and drop it in the new DB"""
for function in functions_names:
    name_function = function[0]
    #print(name_function)

    drop_function_query =f""" DROP FUNCTION IF EXISTS {name_function} """
    print(drop_function_query)

    cursor_1.execute(drop_function_query)
    midb_second.commit()
    #exit()


""" Close connection """

midb_second.close()