import streamlit as st
from llama3 import LLaMA3
from analysis import DataAnalysis
from database import Database
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

class StreamlitApp:
    def __init__(self):
        self.database_path = 'sqlite_sample.db'
        self.db = Database(self.database_path)
        self.llama3 = LLaMA3()
        self.data_analyzer = DataAnalysis()

    def run(self):
        st.title("Natural Language to SQL & Graph Generator")

        # Query Generation Section
        st.header("Query Generation")
        natural_language_query = st.text_input("Enter your query in natural language:")

        if st.button("Generate SQL and Execute Query"):
            if natural_language_query:
                with st.spinner("Generating SQL query..."):
                    sql_query = self.llama3.generate_sql_query(natural_language_query)
                
                if sql_query:
                    st.subheader("Generated SQL Query:")
                    st.code(sql_query, language='sql')
                    self.llama3.save_sql_query(sql_query)

                    with st.spinner("Executing query..."):
                        query_results = self.db.execute_query(sql_query)
                    
                    if query_results:
                        df = pd.DataFrame(query_results)
                        excel_file_path = self.llama3.save_excel_file(df)

                        st.subheader("Query Results:")
                        st.dataframe(df)

                        # CSV download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )

                        # Excel download button
                        with open(excel_file_path, "rb") as file:
                            st.download_button(
                                label="Download Excel",
                                data=file,
                                file_name="query_results.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

                        # Store the excel_file_path in session state for later use
                        st.session_state.excel_file_path = excel_file_path
                        st.session_state.df = df
                    else:
                        st.error("No results returned from the query.")
                else:
                    st.error("Failed to generate SQL query.")
            else:
                st.warning("Please enter a natural language query.")

        # Graph Generation Section
        st.header("Graph Generation")
        if 'excel_file_path' in st.session_state and 'df' in st.session_state:
            graph_prompt = st.text_input("What kind of graph would you like to generate?")
            if st.button("Generate Graph"):
                if graph_prompt:
                    with st.spinner("Generating graph code..."):
                        graph_code = self.data_analyzer.generate_graph_code(graph_prompt, st.session_state.excel_file_path, st.session_state.df.columns.tolist())
                    if graph_code:
                        st.subheader("Generated Graph Code:")
                        st.code(graph_code, language='python')
                        self.data_analyzer.save_graph_code(graph_code)
                        
                        try:
                            # Create a new figure
                            plt.figure(figsize=(10, 6))
                            
                            # Execute the graph code
                            exec(graph_code, globals())
                            
                            # Display the plot
                            st.pyplot(plt)
                            
                            # Close the figure to free up memory
                            plt.close()
                        except Exception as e:
                            st.error(f"Error generating graph: {str(e)}")
                    else:
                        st.error("Failed to generate graph code.")
                else:
                    st.warning("Please enter a graph prompt.")
        else:
            st.warning("Please generate and execute a query first before creating a graph.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()