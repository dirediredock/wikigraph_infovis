# by Matias I. Bofarull Oddo - 2022.10.10

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df_data = pd.read_csv("directed_graph.csv")
df_fields = df_data[["0", "1"]]

network = nx.Graph()
network = nx.from_pandas_edgelist(df_fields, source="0", target="1")

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

nx.draw_shell(
    network,
    width=0.1,
    linewidths=0,
    node_size=0.5,
    node_color="k",
    with_labels=False,
)

plt.axis("off")
plt.gca().set_position([0, 0, 1, 1])
plt.savefig("figures/shell_layout.png", dpi=400)
