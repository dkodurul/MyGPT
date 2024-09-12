import openai
import pandas as pd
from sqlalchemy import create_engine
from neo4j import GraphDatabase
import json

# Configuration
OPENAI_API_KEY = 'your_openai_api_key'
NEO4J_URI = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = 'your_neo4j_password'
SQL_URI = 'postgresql://username:password@localhost:5432/your_database'

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Initialize the Neo4j driver
graph_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Initialize the SQLAlchemy engine
sql_engine = create_engine(SQL_URI)

def log_queries_to_file(sql_query, cypher_query, file_path='llm_queries_log.json'):
    log_data = {'sql_query': sql_query, 'cypher_query': cypher_query}
    with open(file_path, 'a') as log_file:
        json.dump(log_data, log_file)
        log_file.write('\n')

def query_sql(sql_query):
    with sql_engine.connect() as connection:
        result = connection.execute(sql_query)
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def query_graph(cypher_query):
    with graph_driver.session() as session:
        result = session.run(cypher_query)
        return pd.DataFrame([record.data() for record in result])

def save_results_to_file(dataframe, csv_path='query_results.csv', excel_path='query_results.xlsx'):
    dataframe.to_csv(csv_path, index=False)
    dataframe.to_excel(excel_path, index=False)
    print(f'Results saved to {csv_path} and {excel_path}')

def execute_queries(query):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Convert the following natural language query into SQL and Cypher: {query}',
        max_tokens=150
    )
    llm_response = response.choices[0].text.strip()
    sql_query, cypher_query = llm_response.split('Cypher:')[0], llm_response.split('Cypher:')[1]
    
    log_queries_to_file(sql_query, cypher_query)
    
    sql_results = query_sql(sql_query)
    graph_results = query_graph(cypher_query)
    
    save_results_to_file(sql_results)
    save_results_to_file(graph_results)
    
    return sql_results