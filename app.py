# app.py
import streamlit as st
from query_handler import execute_queries

def main():
    st.title('Natural Language SQL and Graph Query Generator')
    
    user_query = st.text_area('Enter your natural language query:')
    if st.button('Generate Query'):
        if user_query:
            results = execute_queries(user_query)
            if results is not None:
                st.write('Query executed successfully!')
                st.dataframe(results)
                st.download_button('Download CSV', results.to_csv(index=False), file_name='query_results.csv')
                st.download_button('Download Excel', results.to_excel(index=False), file_name='query_results.xlsx')
            else:
                st.warning('No results to display.')
        else:
            st.warning('Please enter a query.')

if __name__ == '__main__':
    main()