import os
import sqlite3
import pandas as pd

# Define the directory and ensure it exists
path_dir = 'C:/Users/dkodurul_stu/Projects/MyGPT'
filename = 'query_results.xlsx'

# Create directory if it doesn't exist
os.makedirs(path_dir, exist_ok=True)

# Full path for the Excel file
file_path = os.path.join(path_dir, filename)

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('sqlite_sample.db')

try:
    # Create a cursor object
    cursor = conn.cursor()

    # Execute SQL queries
    cursor.execute("SELECT * FROM address")

    # Fetch query results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Get the column names from the cursor description
    columns = [description[0] for description in cursor.description]

    # Create a DataFrame from the results using the column names
    df = pd.DataFrame(results, columns=columns)

    # Export the DataFrame to an Excel file at the specified path
    df.to_excel(file_path, index=False)

    print(f"Data exported to {file_path}")

    # Commit changes
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()