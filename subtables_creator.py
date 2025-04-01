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
tables_to_avoid = []#audittrail

""" limit for each subtable """
#LIMIT_SUBTABLES = int(config('LIMIT_SUBTABLES'))

""" Limit Weigh for tables"""
LIMIT_WEIGH_TABLES = int(config('LIMIT_WEIGH_TABLES'))

where_ = ""
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


midb_main = mysql.connector.connect(
    host=DB_HOST_,
    user=DB_USER_,
    password=DB_PASSWORD_,
    database=DB_NAME_
) # Main DataBase

midb_main_secundary = mysql.connector.connect(
        host=DB_HOST_,
        user=DB_USER_,
        password=DB_PASSWORD_
) # Main DataBase subtables


cursor_1 = midb_main.cursor()
cursor_1_secundary = midb_main_secundary.cursor()

""" Query to get all the tables in the Main Database"""
cursor_1.execute(f'SHOW TABLES FROM {DB_NAME_}')
response_tables = cursor_1.fetchall()

""" Go through every table to get the weigh in GigaBytes and create subtables"""
for table in response_tables:
    """ tables to avoid"""
    if table[0] in tables_to_avoid:
        continue
    """ Query to evaluate the weigh of the table """
    cursor_1.execute(f"""SELECT (data_length + index_length) / 1024 / 1024 /1024 AS 'Size_in_Megabytes'
                    FROM information_schema.tables 
                    WHERE table_schema = '{DB_NAME_}' 
                    AND table_name = '{table[0]}'; """)    
    
    weigh_tabla = cursor_1.fetchone()[0]
    
    """ Check if the weigh of the tables is over LIMIT WEIGHT GB """
    if weigh_tabla >= LIMIT_WEIGH_TABLES:
        print(f"""Table "{table[0]}" is to long ({round(weigh_tabla,2)} GigaBytes), Creating Subtables...""")

        """ Prepare the appropiate limit for the len of subtables """
        #Query to bring the weigh of a row from the table
        cursor_1.execute(f"""SELECT 
                            (data_length + index_length) / table_rows AS size_per_row_bytes
                        FROM 
                            information_schema.tables
                        WHERE 
                            table_schema = '{DB_NAME_}'
                            AND table_name = '{table[0]}';
                        """)    
        
        weigh_row = cursor_1.fetchone()[0]
        print(f'Weigh per row {weigh_row}')
        # Logic to assign the limit for subtables 
        if weigh_row < 500: #355
            LIMIT_SUBTABLES = 2000000
        else: #19230
            LIMIT_SUBTABLES = 200000

        """ In the main database Create new schema if not exist """    
        cursor_1_secundary.execute(f"CREATE DATABASE IF NOT EXISTS {SUB_DB_NAME_}")

        cursor_1_secundary.close()
        midb_main_secundary.close()

        midb_main_secundary = mysql.connector.connect(
        host=DB_HOST_,
        user=DB_USER_,
        password=DB_PASSWORD_,
        database=SUB_DB_NAME_
        )# Main DataBase subtables

        cursor_1_secundary = midb_main_secundary.cursor()

        """ Query to anule the foreign_key of tables"""
        cursor_1_secundary.execute("SET FOREIGN_KEY_CHECKS = 0;")
        midb_main_secundary.commit()

        cursor_1.execute(f'SHOW CREATE TABLE {table[0]}')
        response_create_tables = cursor_1.fetchall()[0][1]

        """ The most resent versions of MySQL doesn't admit '0000-00-00 00:00:00' in datetime columns"""
        response_create_tables = response_create_tables.replace("datetime NOT NULL DEFAULT '0000-00-00 00:00:00'","datetime DEFAULT NULL")
        #print(response_create_tables)
        #exit()

        """ Len of the first table """
        # cursor_1.execute(f'SELECT count(*) FROM {table[0]} {where_}')
        # resultado_1 = cursor_1.fetchall()
        # resultado_len_1 = resultado_1[0][0] 
        # print(f'----------- len secundary DB table "{table[0]}": {resultado_len_1}-------------') 

        """ Close connection """
        cursor_1.close()
        cursor_1_secundary.close()

        midb_main.close()
        midb_main_secundary.close()

        """ Create subtables and fill it with data from original table"""
        subtabla=""
        #for num_subtabla in list(range(1,int(resultado_len_1/LIMIT_SUBTABLES)+1)):
        num_subtabla = 1
        while True:
            midb_main = mysql.connector.connect(
            host=DB_HOST_,
            user=DB_USER_,
            password=DB_PASSWORD_,
            database=DB_NAME_
            ) # Main DataBase
            cursor_1 = midb_main.cursor()

            midb_main_secundary = mysql.connector.connect(
                host=DB_HOST_,
                user=DB_USER_,
                password=DB_PASSWORD_,
                database=SUB_DB_NAME_
            ) # Main DataBase subtables
            cursor_1_secundary = midb_main_secundary.cursor()

            """ Logic to create table without CONSTRAINT"""
            new_table = f"{table[0]}_{num_subtabla}"
            subtabla = (response_create_tables.replace(f"CREATE TABLE `{table[0]}`",f"CREATE TABLE IF NOT EXISTS `{SUB_DB_NAME_}`.`{new_table}`")
                .split("CONSTRAINT"))
            
            # If query has CONSTRAIN"""
            if len(subtabla) > 1:
                subtabla = subtabla[0][:-4] + ")" + "\n ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC"
            else:
                subtabla = subtabla[0]

            print(f"CREATE subtable # {num_subtabla} for table {table[0]}" )

            cursor_1_secundary.execute(subtabla)
            midb_main_secundary.commit()

            """ Check if new table contains data """
            cursor_1_secundary.execute(f'SELECT EXISTS (SELECT 1 FROM {new_table} {where_} LIMIT 1) AS has_data;')
            len_new_table = cursor_1_secundary.fetchall()
            len_new_table = int(len_new_table[0][0])
            """If the table is not empty then don't insert data"""
            if len_new_table == 1:
                num_subtabla += 1
                print("Data already exit in the subtable")
                """ Len of new subtable """
                cursor_1_secundary.execute(f'SELECT count(*) FROM {new_table} {where_}')
                len_new_table = cursor_1_secundary.fetchall()
                len_new_table = int(len_new_table[0][0])
                if len_new_table < LIMIT_SUBTABLES:
                    break
                continue

            """ Fill the table with data """
            # Query to bring the columns of the table"""
            cursor_1.execute(f'SHOW COLUMNS FROM {table[0]}')
            response_columns = cursor_1.fetchall()

            # For to set the list with the columns 
            list_columnas = []
            for columns in response_columns:
                list_columnas.append(f"`{columns[0]}`")
            #print(list_columnas)

            # Set up query to insert data
            string_1 = (f"INSERT INTO {SUB_DB_NAME_}.{new_table} {list_columnas}").replace("[","(").replace("]",")")
            string_1 = string_1.replace("'","")

            string_2 = (f" SELECT {list_columnas}").replace("[","").replace("]","")
            string_2 = string_2.replace("'","")
            # union to set the Query insert 
            sql_insert = string_1 +"\n"+ string_2 + f"\n FROM {DB_NAME_}.{table[0]} LIMIT {LIMIT_SUBTABLES} OFFSET {(num_subtabla-1)*LIMIT_SUBTABLES};"
            #print(sql_insert)
            #exit()
            
            """ Insert Data in the new schema"""
            cursor_1_secundary.execute(sql_insert)
            midb_main_secundary.commit()
            print("Data inserted successfully.")


            """ Len of new subtable """
            cursor_1_secundary.execute(f'SELECT count(*) FROM {new_table} {where_}')
            len_new_table = cursor_1_secundary.fetchall()
            len_new_table = int(len_new_table[0][0])

            """ while bucle logic"""
            num_subtabla += 1
            """ Stop while bucle when data from Db Main is less than limit"""
            if len_new_table < LIMIT_SUBTABLES:
                break
            
            """ Close connection """
            cursor_1.close()
            cursor_1_secundary.close()

            midb_main.close()
            midb_main_secundary.close()

""" Query to anule the foreign_key of tables"""
cursor_1_secundary.execute("SET FOREIGN_KEY_CHECKS = 1;")
midb_main_secundary.commit()

# Get date of end
fecha_hora_actual_2 = datetime.now()

print("Date of start:", fecha_hora_actual_1)
print("Date of end:", fecha_hora_actual_2)

# dates diff
diferencia = fecha_hora_actual_2 - fecha_hora_actual_1
horas_diferencia = diferencia.total_seconds() / 3600


print(f"proccess takes: {round(horas_diferencia,2)} hours")