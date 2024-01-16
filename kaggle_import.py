import psycopg2
from psycopg2 import sql
import csv

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'lab4',
    'user': 'postgres',
    'password': 'postgres'
}

# CSV file path
csv_file_path = '/Users/markzavgorodniy/Downloads/csvkaggle/stores.csv'

# PostgreSQL table and columns
table_name = 'stores'
columns = ['store', 'type', 'size']  # Adjust the column names based on your table structure


# Function to read data from CSV to dictionary
def read_csv_to_dict(csv_file_path):
    data_dict_list = []
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # Convert keys to lowercase to handle case-insensitivity
            data_dict_list.append({key.lower(): value for key, value in row.items()})
    return data_dict_list


# Function to create a SQL query for inserting data into PostgreSQL
def create_insert_query(table_name, data_dict):
    # Extract column names dynamically from the first dictionary
    columns = list(data_dict[0].keys())

    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join([
            sql.SQL('({})').format(sql.SQL(', ').join(map(sql.Literal, [row[col] for col in columns])))
            for row in data_dict
        ])
    )
    return insert_query


# Function to insert data into PostgreSQL
def insert_data_to_postgres(db_params, table_name, data_dict_list):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    try:
        # Create and execute INSERT query
        insert_query = create_insert_query(table_name, data_dict_list)
        cursor.execute(insert_query)

        # Commit the transaction
        conn.commit()
        print(f'Data inserted successfully into {table_name} table.')

    except psycopg2.Error as e:
        print(f'Error: {e}')

    finally:
        # Close the connection
        cursor.close()
        conn.close()


# Read data from CSV to dictionary
data_dict_list = read_csv_to_dict(csv_file_path)

# Call the insert function
insert_data_to_postgres(db_params, table_name, data_dict_list)