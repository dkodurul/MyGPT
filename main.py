from llama3 import LLaMA3
from analysis import DataAnalysis
from database import Database
import pandas as pd

def main():
    database_path = 'sqlite_sample.db'
    db = Database(database_path)
    llama3 = LLaMA3()
    data_analyzer = DataAnalysis()

    # Get user input
    natural_language_query = input("Enter your query in natural language: ")

    # Generate SQL query
    sql_query = llama3.generate_sql_query(natural_language_query)
    if sql_query:
        print("Generated SQL Query:")
        print(sql_query)
        llama3.save_sql_query(sql_query)

        # Execute query
        query_results = db.execute_query(sql_query)
        if query_results:
            df = pd.DataFrame(query_results)
            excel_file_path = llama3.save_excel_file(df)

            print("Query Results:")
            print(df)

            # Generate graph
            graph_prompt = input("What kind of graph would you like to generate? ")
            graph_code = data_analyzer.generate_graph_code(graph_prompt, excel_file_path, df.columns.tolist())
            if graph_code:
                data_analyzer.save_graph_code(graph_code)
                print("Graph code generated and saved.")
                
                # Execute graph code
                try:
                    exec(graph_code)
                    print("Graph generated successfully.")
                except Exception as e:
                    print(f"Error generating graph: {str(e)}")
            else:
                print("Failed to generate graph code.")
        else:
            print("No results returned from the query.")
    else:
        print("Failed to generate SQL query.")

if __name__ == "__main__":
    main()