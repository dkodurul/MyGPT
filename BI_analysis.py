import query 

import pandas as pd
import matplotlib.pyplot as plt

# Define the path to your Excel file
file_path = 'C:/Users/dkodurul_stu/Projects/MyGPT/query_results.xlsx'

try:
    # Load data from the Excel file
    data = pd.read_excel(file_path)
    
    # Create a bar graph
    plt.figure(figsize=(8, 6))
    plt.bar(data['address'], data['postal_code'])
    plt.xlabel('Name')
    plt.ylabel('Age')
    plt.title('User Ages')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(data['age'], labels=data['name'], autopct='%1.1f%%')
    plt.title('User Age Distribution')
    plt.axis('equal')
    plt.show()
    
except FileNotFoundError:
    print(f'File not found: {file_path}. Please ensure the Excel file exists.')