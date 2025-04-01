import mysql.connector
from decouple import config

""" 
    This file will help you to drop every table in the local DB 

"""
""" Select the tables you don't want to drop"""
avoid_drop_tables = ['audittrail','helpdesk_communication']

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

""" Query to anule the foreign_key of tables"""
cursor_1.execute("SET FOREIGN_KEY_CHECKS = 0;")
midb_second.commit()

""" Query to get all the tables in the Main Database"""
cursor_1.execute(f'SHOW TABLES FROM {DB_NAME_LOCAL_}')
response_tables = cursor_1.fetchall()

#print(response_tables)
#exit()

for table in response_tables:

    """ aviod to drop selected tables"""
    if table[0] in avoid_drop_tables:
        continue

    response_create_tables = f"""DROP TABLE IF EXISTS {table[0]}"""
    print(response_create_tables)
    
    cursor_1.execute(response_create_tables)
    midb_second.commit()
    

""" Query to activate the foreign_key of tables"""
cursor_1.execute("SET FOREIGN_KEY_CHECKS = 1;")
midb_second.commit()


""" Close connection """
midb_second.close()