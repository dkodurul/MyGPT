import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel("C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20241003_102453.xlsx")

# process the data if needed
df = df[["Column_1", "Column_2"]]
df = df.groupby("Column_1").sum()

# create pie chart
plt.pie(df, labels=df.index)

# save graph as PNG file
plt.savefig("C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files\query_results_20241003_102453_graph.png", bbox_inches="tight")