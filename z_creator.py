x=["'id', 'transaction_id', 'user_id', 'action_type', 'table_name', 'record_id', 'field_name', 'old_value', 'new_value', 'timestamp'"]
x=x[0].split(",")
print(len(x))

palabra=''
for y in x:
    palabra = palabra + ',%s'
print(palabra)