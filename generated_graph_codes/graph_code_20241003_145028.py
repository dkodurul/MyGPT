import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

df = pd.read_excel(r'C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20241003_144308.xlsx', header=None)

#process data if needed (e.g., filter, sort, aggregate, etc.)
df = df[['Column_1','Column_2','Column_3']]

#create the requested graph
plt.bar(df['Column_1'], df['Column_2'])
plt.xticks(rotation=90)
plt.title('Runtime vs Genres')
plt.xlabel('Genre')
plt.ylabel('Runtime (minutes)')

#save the graph as a PNG file
plt.savefig('runtime_vs_genres.png', dpi=300)