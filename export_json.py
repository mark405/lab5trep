import json
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'lab4',
    'user': 'postgres',
    'password': 'postgres'
}

# Output file for JSON
output_file = '/Users/markzavgorodniy/Desktop/lex/all_tables.json'


# Function to export data from PostgreSQL table to JSON
def export_table_to_json(conn, table_name, output_data):
    cursor = conn.cursor()

    # Get column names
    cursor.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s"), [table_name])
    column_names = [row[0] for row in cursor.fetchall()]

    # Fetch and format data
    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
    table_data = []
    for row in cursor.fetchall():
        table_data.append(dict(zip(column_names, row)))

    # Add data to the output dictionary
    output_data[table_name] = table_data

    cursor.close()


# Function to export all tables to JSON
def export_all_tables_to_json(db_params, output_file):
    conn = psycopg2.connect(**db_params)

    # Specify the tables to export
    tables_to_export = ['stores', 'features', 'train']

    output_data = {}
    for table_name in tables_to_export:
        export_table_to_json(conn, table_name, output_data)

    # Write data to JSON file
    with open(output_file, 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

    conn.close()
    print(f'Data exported to {output_file}.')

# Call the export function
export_all_tables_to_json(db_params, output_file)
