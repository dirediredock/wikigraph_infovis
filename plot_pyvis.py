# by Matias I. Bofarull Oddo - 2022.10.09

import pandas as pd
from pyvis.network import Network

dataCSV = pd.read_csv("directed_graph.csv")

network = Network(
    height="1000px",
    width="100%",
    bgcolor="white",
    font_color="black",
    select_menu=True,
)

network.force_atlas_2based()
network_data = zip(dataCSV["0"], dataCSV["1"])

for edge in network_data:

    network.add_node(edge[0], edge[0], title="")
    network.add_node(edge[1], edge[1], title="")
    network.add_edge(edge[0], edge[1], value=3)

neighbor_map = network.get_adj_list()

for node in network.nodes:

    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])

network.show("wikigraph_pyvis_network.html")
