import pandas as pd
from database import Database
from llama3 import LLaMA3

def main():
    database_path = 'sqlite_sample.db'
    
    # Initialize LLaMA3
    llama3 = LLaMA3()

    # Get user input
    natural_language_query = input("Enter your query in natural language: ")

    # Generate SQL query
    sql_query = llama3.generate_sql_query(natural_language_query)
    
    if sql_query:
        print("Generated SQL Query:", sql_query)
        try:
            llama3.save_sql_query(sql_query)
        except Exception as e:
            print(f"Error saving SQL query: {e}")

        # Execute query
        db = Database(database_path)
        results = db.execute_query(sql_query)
        db.close_connection()

        if results:
            print("Results:")
            for row in results:
                print(row)

            # Create DataFrame and save to Excel
            df = pd.DataFrame(results)
            try:
                llama3.save_excel_file(df)
            except Exception as e:
                print(f"Error saving Excel file: {e}")
        else:
            print("No results returned from the query.")
    else:
        print("Failed to generate SQL query.")

if __name__ == "__main__":
    main()