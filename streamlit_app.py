import streamlit as st
import pandas as pd
from database import Database
from llama3 import LLaMA3

def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon="🔍", layout="wide")
    st.title("🔍 SQL Query Generator and Results Viewer")

    database_path = 'sqlite_sample.db'
    llama3 = LLaMA3()

    natural_language_query = st.text_area("Enter your query in natural language:", height=100)

    if st.button("Generate SQL and Execute"):
        if natural_language_query:
            sql_query = llama3.generate_sql_query(natural_language_query)
            
            if sql_query:
                st.subheader("Generated SQL Query:")
                st.code(sql_query, language="sql")
                
                try:
                    llama3.save_sql_query(sql_query)
                except Exception as e:
                    st.error(f"Error saving SQL query: {e}")
                
                db = Database(database_path)
                results = db.execute_query(sql_query)
                db.close_connection()
                
                if results:
                    st.subheader("Query Results:")
                    df = pd.DataFrame(results)
                    st.dataframe(df)
                    
                    try:
                        llama3.save_excel_file(df)
                        st.success("Results saved to Excel file.")
                    except Exception as e:
                        st.error(f"Error saving Excel file: {e}")
                else:
                    st.warning("No results returned from the query.")
            else:
                st.error("Failed to generate SQL query.")
        else:
            st.warning("Please enter a natural language query.")

if __name__ == "__main__":
    main()