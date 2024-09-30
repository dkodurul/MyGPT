from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers.string import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from datetime import datetime

class DataAnalysis:
    def __init__(self):
        self.llm = ChatOllama(model="codellama:13b")
        self.graph_code_dir = 'C:/Users/dkodurul_stu/Projects/MyGPT/generated_graph_codes/'
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        os.makedirs(self.graph_code_dir, exist_ok=True)

    def generate_graph_code(self, graph_prompt, excel_file_path, column_names):
        try:
            prompt = f"""
            Generate Python code to create a graph based on the following request:
            Graph request: {graph_prompt}
            Use the following Excel file as the data source:
            Excel file path: {excel_file_path}
            The Excel file contains the following columns:
            {', '.join(column_names)}
            Include the following in your code:
            1. Import necessary libraries (pandas, matplotlib)
            2. Read the Excel file
            3. Process the data if needed
            4. Create the requested graph
            5. Save the graph as a PNG file
            Return only the Python code without any additional text or space.
            """
            prompt_template = ChatPromptTemplate.from_template(prompt)
            output_parser = StrOutputParser()
            chain = prompt_template | self.llm | output_parser
            graph_code = chain.invoke({"input": prompt})
            return graph_code.strip()
        except Exception as e:
            print("An error occurred while generating graph code:", e)
            return None

    def save_graph_code(self, graph_code):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self._get_unique_file_path(self.graph_code_dir, f'graph_code_{timestamp}', '.py')
        with open(file_path, 'w') as f:
            f.write(graph_code)
        print(f"Graph code saved to {file_path}")

    def _get_unique_file_path(self, directory, base_name, extension):
        file_path = os.path.join(directory, f"{base_name}{extension}")
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name}_{counter}{extension}")
            counter += 1
        return file_path