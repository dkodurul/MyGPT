import pandas as pd
import matplotlib.pyplot as plt

# Read Excel file
df = pd.read_excel(r'C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20240930_093701.xlsx')

# Process data if needed
df = df[['Column_1', 'Column_2', 'Column_3', 'Column_4']]
df = df.set_index('Column_1')

# Create graph
fig, ax = plt.subplots()
ax.bar(df.index, df['Column_2'], label='Runtime')
ax.legend()
plt.title('Bar Graph Comparing Runtime Across Years')
plt.xlabel('Years')
plt.ylabel('Runtime')

# Save graph as PNG file
fig.savefig('bar_graph.png', dpi=300)