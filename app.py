from flask import Flask, render_template, request, jsonify, send_file
from llama3 import LLaMA3
from analysis import DataAnalysis
from database import Database
import pandas as pd
import os
import traceback

app = Flask(__name__)

database_path = 'sqlite_sample.db'
db = Database(database_path)
llama3 = LLaMA3()
data_analyzer = DataAnalysis()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    try:
        natural_language_query = request.form['query']
        sql_query = llama3.generate_sql_query(natural_language_query)
        if sql_query:
            llama3.save_sql_query(sql_query)
            return jsonify({'success': True, 'sql_query': sql_query})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate SQL query'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()})

@app.route('/execute_query', methods=['POST'])
def execute_query():
    try:
        sql_query = request.form['sql_query']
        query_results = db.execute_query(sql_query)
        if query_results:
            df = pd.DataFrame(query_results)
            excel_file_path = llama3.save_excel_file(df)
            return jsonify({
                'success': True,
                'results': df.to_dict(orient='records'),
                'excel_file': excel_file_path
            })
        else:
            return jsonify({'success': False, 'error': 'No results returned from the query'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()})

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    try:
        graph_prompt = request.form['graph_prompt']
        excel_file_path = request.form['excel_file_path']
        df = pd.read_excel(excel_file_path)
        graph_code = data_analyzer.generate_graph_code(graph_prompt, excel_file_path, df.columns.tolist())
        if graph_code:
            data_analyzer.save_graph_code(graph_code)
            # Note: We're not executing the graph code here for safety reasons
            return jsonify({'success': True, 'graph_code': graph_code})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate graph code'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)