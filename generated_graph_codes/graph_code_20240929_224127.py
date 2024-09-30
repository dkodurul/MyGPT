import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('seaborn-darkgrid')

#read excel file
df = pd.read_excel('C:\Users\dkodurul_stu\Projects\MyGPT\output-xl_files\query_results_20240929_223614.xlsx')

#process data if needed
df = df[['Column_1', 'Column_2', 'Column_3']]
df = df.rename(columns={'Column_1': 'Year', 'Column_2': 'Runtime', 'Column_3': 'Run Time Units'})
df = pd.melt(df, id_vars=['Year'], value_vars=['Runtime', 'Run Time Units'])

#create graph
fig, ax = plt.subplots()
ax.bar(x='Year', y='value', data=df, hue='variable')
ax.set_title('Bar Graph Comparing Runtime Across Years')
ax.set_xlabel('Year')
ax.set_ylabel('Runtime (in Hours)')
plt.show()

#save graph as png file
fig.savefig('bar_graph_runtime_across_years.png', dpi=300, bbox_inches='tight')