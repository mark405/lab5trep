import psycopg2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'lab4',
    'user': 'postgres',
    'password': 'postgres'
}

def execute_query(query, cursor):
    cursor.execute(query)

def visualize_view(view_name, x_label, y_label, title):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    try:
        # Execute the view query
        cursor.execute(f"SELECT * FROM {view_name}")
        result = cursor.fetchall()

        # Visualize results
        x_values = [row[0] for row in result]
        y_values = [row[1] for row in result]

        plt.plot(x_values, y_values, marker='o')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    finally:
        conn.close()

def main():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    try:
        # Execute queries to create views

        # Visualize views
        visualize_view('average_weekly_sales_view', 'Store Type', 'Average Weekly Sales', 'Average Weekly Sales by Store Type')
        visualize_view('store_count_view', 'Store Type', 'Number of Stores', 'Number of Stores for Each Store Type')
        visualize_view('max_temperature_view', 'Date', 'Max Temperature', 'Max Temperature by Date')

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
