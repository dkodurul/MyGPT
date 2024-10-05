import pandas as pd
import matplotlib.pyplot as plt

# read Excel file into pandas dataframe
df = pd.read_excel("C:/Users/dkodurul_stu/Projects/MyGPT/output-xl_files/query_results_20240930_101431.xlsx")

# process data if needed
# df = ...

# create bar graph comparing runtime, imdb score over years
ax = df.plot(kind="bar", x="Year", y=["Runtime (min)", "IMDB Score"], figsize=(10,5))

# add title and labels
ax.set_title("Bar Graph Comparing Runtime, IMDB Score Over Years")
ax.set_xlabel("Year")
ax.set_ylabel("Runtime (min) / IMDB Score")

# save graph as PNG file
plt.savefig("bar_graph.png")