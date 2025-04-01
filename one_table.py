import mysql.connector
from decouple import config
from datetime import datetime
# Get date of start 
fecha_hora_actual_1 = datetime.now()
"""
    This file will allow you to migrate one spesific table, you just need to spefic the "table" and condition "where"
"""

""" Select the table """
table = ["businessprofiles_products"] #helpdesk_communication

""" select the condition if exist, if not put '' """
where_ = ''

""" examples of where """
#where_ = ''
#where_ = "WHERE id = 386"
#where_ = "WHERE date_format(audittrail.timestamp,'%Y-%m') >= '2023-11' OR date_format(audittrail.timestamp,'%Y-%m') <= '2014-04'"
#where_ = "WHERE date_format(helpdesk_communication.created_on,'%Y-%m') <= '2020-01'"

""" set the apropiate limit for each table """
limit = 500000
limit_2 = 1000 

""" -------------- Start of migration --------------- """
DB_HOST_ = config('DB_HOST_')
DB_USER_ = config('DB_USER_')
DB_PASSWORD_ = config('DB_PASSWORD_')
DB_NAME_ = config('DB_NAME_')

DB_HOST_LOCAL_ = config('DB_HOST_LOCAL_')
DB_USER_LOCAL_ = config('DB_USER_LOCAL_')
DB_PASSWORD_LOCAL_ = config('DB_PASSWORD_LOCAL_')
DB_NAME_LOCAL_ = config('DB_NAME_LOCAL_')



print("----------------------------------")
print(f"    next table: {table[0]} ")
print("-----------------------------------")

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
# cursor_2.close()
# midb_second.close()

midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
) # Main DataBase
cursor_1 = midb_main.cursor()

# Query to bring the columns of the table"""
cursor_1.execute(f'SHOW COLUMNS FROM {table[0]}')
response_columns = cursor_1.fetchall()

""" Close connection """
cursor_1.close()
midb_main.close()

""" Create query to insert data in the new DB """

# For to set the list with the columns 
list_columnas = []
for columns in response_columns:
    list_columnas.append(f"`{columns[0]}`")

string_1 = (f"INSERT IGNORE INTO {table[0]} {list_columnas}").replace("[","(").replace("]",")")

# For to set the list with Values 
values=''
for y in list_columnas:
    values = values + ',%s'

string_2 = f" VALUES ({values[1:]})"

# union to set the Query insert 
sql_insert = string_1.replace("'","")+ string_2


""" Len of the first table """
# cursor_1.execute(f'SELECT count(*) FROM {table[0]} {where_}')
# resultado_1 = cursor_1.fetchall()
# resultado_len_1 = resultado_1[0][0] 
# print(f'----------- len secundary DB table "{table[0]}": {resultado_len_1}-------------') 

# midb_second = mysql.connector.connect(
#     host=DB_HOST_LOCAL_,
#     user=DB_USER_LOCAL_,
#     password=DB_PASSWORD_LOCAL_,
#     database=DB_NAME_LOCAL_
#     ) # Secundary DataBase
# cursor_2 = midb_second.cursor()

""" Len of the second table """
cursor_2.execute(f'SELECT count(*) FROM {table[0]} ')
resultado_2 = cursor_2.fetchall()
resultado_len_2 = resultado_2[0][0]
print(f'----------- len secundary DB table "{table[0]}": {resultado_len_2}-------------') 

""" Len of the second table """
# cursor_2.execute(f'SELECT id FROM {table[0]} ORDER BY id DESC LIMIT 1; ')
# last_id = cursor_2.fetchall()
# if last_id == []:
#     last_id = 0
# else:
#     last_id = last_id[-1][0]

""" Close connection """
# cursor_2.close()
# midb_second.close()
#print(f'----------- len secundary DB table "{table[0]}": {last_id}-------------') 

""" for to batch pass the data """
#for offset_list in list(range(resultado_len_2,resultado_len_1,limit)): 
offset_list = resultado_len_2
while True:
    print(f"---------------- Current offset of table: {table[0]} -------------------")   
    query_select=f'SELECT * FROM {table[0]} {where_} LIMIT {limit} OFFSET {offset_list}'
    #query_select=f'SELECT * FROM {table[0]} WHERE id > {last_id} ORDER BY id LIMIT {limit};'
    print(query_select)

    midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
    ) # Main DataBase   
    cursor_1 = midb_main.cursor()

    cursor_1.execute(query_select)
    result_1 = cursor_1.fetchall()

    """ Close connection """
    cursor_1.close()
    midb_main.close()

    #print("--result_1--")
    #print(result_1[-1][0])
    #print(len(result_1))
    #exit()
    
    # midb_second = mysql.connector.connect(
    #                 host=DB_HOST_LOCAL_,
    #                 user=DB_USER_LOCAL_,
    #                 password=DB_PASSWORD_LOCAL_,
    #                 database=DB_NAME_LOCAL_
    #             ) # Secundary DataBase
    # cursor_2 = midb_second.cursor()
    #print(sql_insert)
    
    """ for to insert the data in the target DB dividing the result of the first query"""
    for i in range(limit_2, limit+1, limit_2):
        #print("----")
        print(i)
        cursor_2.executemany(sql_insert, result_1[(i-limit_2):i])
        midb_second.commit()
        #print(len(result_1[(i-limit_2):i]))
        """ Stop For bucle when data from Db Main is less than limit_2"""
        if len(result_1[(i-limit_2):i]) < limit_2:
           break
    
    """ while bucle logic"""
    offset_list += limit
    #last_id = result_1[-1][0]
    """ Stop While bucle when data from Db Main is less than limit"""
    if len(result_1) < limit:
        break
    
    """ Close connection """
    # cursor_2.close()
    # midb_second.close()
    
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
