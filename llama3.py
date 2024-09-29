from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers.string import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from datetime import datetime

class LLaMA3:
    def __init__(self):
        self.llm = ChatOllama(model="llama-sql")
        self.sql_query_dir = 'C:/Users/dkodurul_stu/Projects/MyGPT/generated_queries'
        self.excel_output_dir = 'C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files'
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        os.makedirs(self.sql_query_dir, exist_ok=True)
        os.makedirs(self.excel_output_dir, exist_ok=True)

    def generate_sql_query(self, natural_language_query):
        try:
            prompt = f"{natural_language_query}"
            
            prompt_template = ChatPromptTemplate.from_template(prompt)
            output_parser = StrOutputParser()
            chain = prompt_template | self.llm | output_parser
            
            sql_query = chain.invoke({"input": prompt})
            return sql_query.strip()
        except Exception as e:
            print("An error occurred while generating SQL query:", e)
            return None

    def save_sql_query(self, sql_query):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self._get_unique_file_path(self.sql_query_dir, f'query_sql_{timestamp}', '.txt')
        with open(file_path, 'w') as f:
            f.write(sql_query)
        print(f"SQL query saved to {file_path}")

    def save_excel_file(self, df):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self._get_unique_file_path(self.excel_output_dir, f'query_results_{timestamp}', '.xlsx')
        df.to_excel(file_path, index=False)
        print(f"Data exported to {file_path}")

    def _get_unique_file_path(self, directory, base_name, extension):
        file_path = os.path.join(directory, f"{base_name}{extension}")
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}{extension}")
            counter += 1
        return file_path