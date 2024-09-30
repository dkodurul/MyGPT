import streamlit as st
from llama3 import LLaMA3
from analysis import DataAnalysis
from database import Database
import pandas as pd
import matplotlib.pyplot as plt
import io

class StreamlitApp:
    def __init__(self):
        self.database_path = 'sqlite_sample.db'
        self.db = Database(self.database_path)
        self.llama3 = LLaMA3()
        self.data_analyzer = DataAnalysis()

    def run(self):
        st.title("Natural Language to SQL & Graph Generator")

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

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )

                        generate_graph = st.radio("Do you want to generate a graph?", ('Yes', 'No'))
                        if generate_graph == 'Yes':
                            graph_prompt = st.text_input("What kind of graph would you like to generate?")
                            if st.button("Generate Graph"):
                                with st.spinner("Generating graph..."):
                                    graph_code = self.data_analyzer.generate_graph_code(graph_prompt, excel_file_path, df.columns.tolist())
                                if graph_code:
                                    st.subheader("Generated Graph Code:")
                                    st.code(graph_code, language='python')
                                    self.data_analyzer.save_graph_code(graph_code)
                                    
                                    try:
                                        exec(graph_code)
                                        st.pyplot(plt)
                                        plt.close()
                                    except Exception as e:
                                        st.error(f"Error generating graph: {str(e)}")
                    else:
                        st.error("No results returned from the query.")
                else:
                    st.error("Failed to generate SQL query.")
            else:
                st.warning("Please enter a natural language query.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()