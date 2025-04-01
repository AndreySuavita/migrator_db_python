import mysql.connector
from decouple import config
from datetime import datetime

# Get date of start 
fecha_hora_actual_1 = datetime.now()

"""
- This file allow you to migrate all the tables of one DB to another.
- Set up the credentials of the both DB in the file ".env".
"""

""" add in this list the tables to avoid in the migration"""
tables_to_avoid = []

""" set the appropriate limit for each table """
limit = 2000000
limit_2 = 1000 

""" Limit Weigh for tables"""
LIMIT_WEIGH_TABLES = int(config('LIMIT_WEIGH_TABLES'))

where_ = ""

""" limit for each subtable """
#LIMIT_SUBTABLES = int(config('LIMIT_SUBTABLES'))

""" -------------- Start of migration --------------- """
DB_HOST_ = config('DB_HOST_')
DB_USER_ = config('DB_USER_')
DB_PASSWORD_ = config('DB_PASSWORD_')
DB_NAME_ = config('DB_NAME_')

SUB_DB_NAME_ = config('SUB_DB_NAME_')

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
cursor_2 = midb_second.cursor()

""" Query to anule the foreign_key of tables"""
cursor_2.execute("SET FOREIGN_KEY_CHECKS = 0;")
midb_second.commit()

""" Close connection """
#cursor_2.close()
#midb_second.close()

midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
) # Main DataBase
cursor_1 = midb_main.cursor()

""" Query to get all the tables in the Main Database"""
cursor_1.execute(f'SHOW TABLES FROM {DB_NAME_}')
response_tables = cursor_1.fetchall()

""" Close connection """
cursor_1.close()
midb_main.close()

big_tables=[]

""" Go through every table to get the weigh in GigaBytes and create subtables"""
for table in response_tables:
    """ tables to avoid"""
    if table[0] in tables_to_avoid:
        continue

    midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
    ) # Main DataBase
    cursor_1 = midb_main.cursor()

    """ Query to evaluate the weigh of the table """
    cursor_1.execute(f"""SELECT (data_length + index_length) / 1024 / 1024 /1024 AS 'Size_in_Megabytes'
                    FROM information_schema.tables 
                    WHERE table_schema = '{DB_NAME_}' 
                    AND table_name = '{table[0]}'; """)    
    
    weigh_tabla = cursor_1.fetchone()[0]
    
    """ Close connection """
    cursor_1.close()
    midb_main.close()

    """ Check if the weigh of the tables is over 5 GB """
    if weigh_tabla >= LIMIT_WEIGH_TABLES:
        big_tables.append(table)
        print(f"""Big Table detected "{table[0]}" ({round(weigh_tabla,2)} GigaBytes)""")


def ordenar_tuplas(lista_tuplas, variable):
    # Drop the name of the big table to get only the number of the subtable and sort the list
    lista_ordenada = sorted(lista_tuplas, key=lambda x: int(x[0].replace(variable + "_", "")))
    return lista_ordenada

""" Pass big tables"""
for table in big_tables:
    
    print("----------------------------------")
    print(f"    next table: {table[0]} ")
    print("-----------------------------------")
    """ Tables to avoid"""
    if table[0] in tables_to_avoid:
        continue
    
    midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
    ) # Main DataBase
    cursor_1 = midb_main.cursor()

    """ Query to bring the columns of the current table"""
    cursor_1.execute(f'SHOW COLUMNS FROM {table[0]}')
    response_columns = cursor_1.fetchall()
    
    """ Close connection """
    cursor_1.close()
    midb_main.close()

    """ For to set the list with the columns"""
    list_columnas = []
    for columns in response_columns:
        list_columnas.append(f"`{columns[0]}`")

    string_1 = (f"INSERT IGNORE INTO {table[0]} {list_columnas}").replace("[","(").replace("]",")")

    """ For to set the list with Values"""
    values=''
    for y in list_columnas:
        values = values + ',%s'
    string_2 = f" VALUES ({values[1:]})"

    """ Query to insert the data in the table of the target DB """
    """ union to set the Query insert """
    sql_insert = string_1.replace("'","")+ string_2


    midb_main_secundary = mysql.connector.connect(
        host=DB_HOST_,
        user=DB_USER_,
        password=DB_PASSWORD_,
        database=SUB_DB_NAME_
    ) # Main DataBase subtables
    cursor_1_secundary = midb_main_secundary.cursor()

    """ Query to get all the subtables from the one big table in the second schema from Database"""
    cursor_1_secundary.execute(f"""SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema = '{SUB_DB_NAME_}'
                                AND table_name LIKE '%{table[0]}%';""")
    response_big_tables = cursor_1_secundary.fetchall()

    # sort subtables 
    response_big_tables = ordenar_tuplas(response_big_tables, table[0])

    if len(response_big_tables) == 0:
        continue
    """ Query to set properly the LIMIT_SUBTABLES"""
    cursor_1_secundary.execute(f"""SELECT count(*) FROM {response_big_tables[0][0]}""")
    LIMIT_SUBTABLES = cursor_1_secundary.fetchone()[0]
    
    """ Close connection """
    cursor_1_secundary.close()
    midb_main_secundary.close()
    
    # midb_second = mysql.connector.connect(
    # host=DB_HOST_LOCAL_,
    # user=DB_USER_LOCAL_,
    # password=DB_PASSWORD_LOCAL_,
    # database=DB_NAME_LOCAL_
    # ) # Secundary DataBase
    # cursor_2 = midb_second.cursor()

    """ Len of the second table """
    cursor_2.execute(f'SELECT count(*) FROM {table[0]} ')
    resultado_2 = cursor_2.fetchall()
    resultado_len_2 = resultado_2[0][0]
    print(f'----------- len secundary DB table "{table[0]}": {resultado_len_2}-------------') 
    #exit()
    """ Close connection """
    # cursor_2.close()
    # midb_second.close()
    #exit()
    # Number of the current subtable
    num_current_subtable = int(resultado_len_2/LIMIT_SUBTABLES)+1
    #print(f"Number current subtable: {num_current_subtable}")

    for subtable in response_big_tables:    
        """ Logic to set the right subtable """
        # Number of table
        num_subtable = int(subtable[0].replace(table[0]+"_",""))
        #print(f"Number subtable :{num_subtable} ")

        # If number of subtable is smaller than current subtable, continue until to find the right subtable
        if num_subtable < num_current_subtable:
            continue

        """ Logic to set the right number to bring the data in the subtable"""    
        len_in_current_subtable = max(0,(resultado_len_2 - (num_subtable-1)*LIMIT_SUBTABLES))
        print(f"len_in_current_subtable {len_in_current_subtable}")

        """ For to pass the data, batch after batch """
        #for offset_list in list(range(len_in_current_subtable,LIMIT_SUBTABLES,limit)): 
        offset_list = len_in_current_subtable
        while True:
            print(f"---------------- Current offset of table: {table[0]} -------------------")
            if offset_list == 0:
                query_select=f'SELECT * FROM {subtable[0]} {where_} LIMIT {limit}'
            else:
                query_select=f'SELECT * FROM {subtable[0]} {where_} LIMIT {limit} OFFSET {offset_list}'
            print(query_select)

            midb_main_secundary = mysql.connector.connect(
                host=DB_HOST_,
                user=DB_USER_,
                password=DB_PASSWORD_,
                database=SUB_DB_NAME_
            ) # Main DataBase subtables
            cursor_1_secundary = midb_main_secundary.cursor()

            cursor_1_secundary.execute(query_select)
            result_1 = cursor_1_secundary.fetchall()
            
            """ Close connection """
            cursor_1_secundary.close()
            midb_main_secundary.close()
            #print(result_1)
            #exit()
            # midb_second = mysql.connector.connect(
            #         host=DB_HOST_LOCAL_,
            #         user=DB_USER_LOCAL_,
            #         password=DB_PASSWORD_LOCAL_,
            #         database=DB_NAME_LOCAL_
            #     ) # Secundary DataBase
            # cursor_2 = midb_second.cursor()
 

            """ For to insert the data in the target DB dividing the result of the first query"""
            for i in range(limit_2, limit+1, limit_2):
                #print("--i--")
                print(i)
                #print(sql_insert)
                cursor_2.executemany(sql_insert, result_1[(i-limit_2):i])
                midb_second.commit()
                #print(len(result_1[(i-limit_2):i]))
                """ Stop For bucle when data from Db Main is less than limit_2"""
                if len(result_1[(i-limit_2):i]) < limit_2:
                    break

            """ while bucle logic"""
            offset_list += limit
            """ Stop while bucle when data from Db Main is less than limit"""
            if len(result_1) < limit:
                break
            #exit()
            """ Close connection """
            # cursor_2.close()
            # midb_second.close()
            # exit()
# midb_second = mysql.connector.connect(
#     host=DB_HOST_LOCAL_,
#     user=DB_USER_LOCAL_,
#     password=DB_PASSWORD_LOCAL_,
#     database=DB_NAME_LOCAL_
# ) # Secundary DataBase
# cursor_2 = midb_second.cursor()

""" Query to activate the foreign_key of tables"""
cursor_2.execute("SET FOREIGN_KEY_CHECKS = 1;")
midb_second.commit()

""" Close connection """
cursor_2.close()
midb_second.close()

# Get date of end
fecha_hora_actual_2 = datetime.now()

print("Date of start:", fecha_hora_actual_1)
print("Date of end:", fecha_hora_actual_2)

# dates diff
diferencia = fecha_hora_actual_2 - fecha_hora_actual_1
horas_diferencia = diferencia.total_seconds() / 3600


print(f"proccess takes: {round(horas_diferencia,2)} hours")