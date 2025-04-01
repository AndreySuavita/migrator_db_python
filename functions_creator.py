import mysql.connector
from decouple import config

""" 
    This file will help you to create every trigger in the local DB from the Main DB

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

""" Query to allow user to create no deterministic function"""
cursor_2.execute("SET GLOBAL log_bin_trust_function_creators = 1")
midb_second.commit()

""" Query to get all the functions in the Main Database"""
cursor_1.execute("SELECT ROUTINE_NAME, ROUTINE_TYPE, DATA_TYPE, ROUTINE_DEFINITION FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'PE_AWS' AND ROUTINE_TYPE = 'FUNCTION'")
functions = cursor_1.fetchall()


""" for to go through each function and create it in the new DB"""
for function in functions:
    name_function = function[0]
    print(name_function)

    cursor_1.execute(f'SHOW CREATE FUNCTION {function[0]}')
    create_functions = cursor_1.fetchall()

    function_query = create_functions[0][2].replace("""DEFINER=`PEDBA`@`%`""","")#.replace("CREATE  FUNCTION","CREATE FUNCTION IF NOT EXISTS")
    #print(function_query)

    cursor_2.execute(function_query)
    midb_second.commit()
    #exit()


""" Close connection """
midb_main.close()
midb_second.close()

