import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Read Excel file
df = pd.read_excel('C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20241003_102453.xlsx')

# Process data if needed
# df = df[['Column 1', 'Column 2']]

# Create pie chart for number of movies in different genres
fig, ax = plt.subplots(figsize=(8,6))
ax.pie(df['Column 2'], labels=df['Column 1'], autopct='%1.1f%%', startangle=90)
plt.title('Pie Chart for Number of Movies in Different Genres')
plt.axis('equal')

# Save graph as PNG file
fig.savefig('pie_chart.png')