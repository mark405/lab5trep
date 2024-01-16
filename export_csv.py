import csv
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

# Output directory for CSV files
output_directory = '/Users/markzavgorodniy/Desktop/lex'


# Function to export data from PostgreSQL table to CSV
def export_table_to_csv(conn, table_name, output_file):
    cursor = conn.cursor()
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Get column names
        cursor.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s"),
                       [table_name])
        column_names = [row[0] for row in cursor.fetchall()]

        # Write header
        csv_writer.writerow(column_names)

        # Fetch and write data
        cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
        for row in cursor.fetchall():
            csv_writer.writerow(row)

    cursor.close()


# Function to export all tables to CSV
def export_all_tables_to_csv(db_params, output_directory):
    conn = psycopg2.connect(**db_params)

    # Specify the tables to export
    tables_to_export = ['stores', 'features', 'train']

    for table_name in tables_to_export:
        output_file = f'{output_directory}/{table_name}.csv'
        export_table_to_csv(conn, table_name, output_file)
        print(f'Data exported from {table_name} table to {output_file}.')

    conn.close()


# Call the export function
export_all_tables_to_csv(db_params, output_directory)
