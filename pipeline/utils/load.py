import pandas as pd
import pyodbc

#TODO - Implementar abordagem mais eficaz na carga de dados
# Teste 01 - Inserir arquivo .csv com BULK INSERT

def does_table_exist(cursor, table_name):
    cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL SELECT 1 ELSE SELECT 0")
    result = cursor.fetchone()
    return result[0] == 1

def toProperStr(table_name):
    if table_name == "Open":
        new_table_name = "open_price"
    elif table_name == "Close":
        new_table_name = "close_price"
    else:
        new_table_name = table_name.lower().replace(" ", "_")
    return new_table_name

def insert_table(table_name_str, data, str_conn):
    dataframe = data
    table_name = toProperStr(table_name_str)
    connection = pyodbc.connect(str_conn)

    if connection:
        print('Conexão estabelecida!')
        cursor = connection.cursor()

        if does_table_exist(cursor, table_name):
            drop_table_query = f"DROP TABLE {table_name}"
            cursor.execute(drop_table_query)
            print(f"Tabela {table_name} excluída com sucesso!")

        create_table_query = f"CREATE TABLE {table_name} (id INT IDENTITY(1,1) PRIMARY KEY)"
        cursor.execute(create_table_query)

        dataframe = dataframe.infer_objects()

        for column in dataframe.columns:
            data_type_str = 'varchar(255)'
            column_str = toProperStr(column)
            add_column_query = f'ALTER TABLE {table_name} ADD "{column_str}" {data_type_str}' 
            cursor.execute(add_column_query)

        for _, row in dataframe.iterrows():
            values = [str(value) for value in row]
            values_str = ', '.join(['?' for _ in values])
            column_names = [toProperStr(col) for col in dataframe.columns]
            column_names_str = ', '.join(column_names)
            query = f"INSERT INTO {table_name} ({column_names_str}) VALUES ({values_str})"
            cursor.execute(query, values) 

        connection.commit()
        print(f'Dados da tabela: {table_name} atualizados com sucesso')
        cursor.close()
        connection.close()
        print('Conexão encerrada!')

