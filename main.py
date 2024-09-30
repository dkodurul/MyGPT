from llama3 import LLaMA3
from analysis import DataAnalysis
from database import Database
import pandas as pd

def generate_graph(graph_prompt, excel_file_path, column_names):
    data_analyzer = DataAnalysis()
    # Generate graph code and save it
    graph_code = data_analyzer.generate_graph_code(graph_prompt, excel_file_path, column_names)
    if graph_code:
        data_analyzer.save_graph_code(graph_code)
        # Execute the generated Python code to produce the graph
        exec(graph_code)
        print("Graph generated successfully.")
    else:
        print("Failed to generate graph code.")

def main():
    database_path = 'sqlite_sample.db'
    db = Database(database_path)
    llama3 = LLaMA3()

    # Get user input
    natural_language_query = input("Enter your query in natural language: ")

    # Generate SQL query and execute it to produce an Excel file
    sql_query = llama3.generate_sql_query(natural_language_query)
    if sql_query:
        # Save SQL query to a text file
        llama3.save_sql_query(sql_query)

        query_results = db.execute_query(sql_query)
        if query_results:
            df = pd.DataFrame(query_results)
            excel_file_path = llama3.save_excel_file(df)

            # Ask if user wants to generate a graph
            generate_graph_choice = input("Do you want to generate a graph? (yes/no): ").lower()

            if generate_graph_choice == 'yes':
                graph_prompt = input("What kind of graph would you like to generate? ")
                generate_graph(graph_prompt, excel_file_path, df.columns.tolist())
        else:
            print("No results returned from the query.")
    else:
        print("Failed to generate SQL query.")

if __name__ == "__main__":
    main()