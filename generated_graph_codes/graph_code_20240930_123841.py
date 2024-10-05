import pandas as pd
import matplotlib.pyplot as plt

# Read Excel file
df = pd.read_excel('C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20240930_123224.xlsx')

# Process data if needed
# df['Column_1'] = ...
# df['Column_2'] = ...
# df['Column_3'] = ...

# Create graph
fig, ax = plt.subplots(figsize=(8,6))
ax.bar(df['Column_1'], height=df['Column_2'], width=0.8)
ax.set_title('Bar Graph: Runtime Over Years')
ax.set_xlabel('Years')
ax.set_ylabel('Runtime (hours)')
ax.legend()

# Save graph as PNG file
fig.savefig('bar_graph_runtime_over_years.png', dpi=300, bbox_inches='tight')