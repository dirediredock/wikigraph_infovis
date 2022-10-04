# by Matias I. Bofarull Oddo - 2022.10.03

import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter


def strip_disambiguation(href):
    step_1 = href.replace("_(programming_language)", "")
    step_2 = step_1.replace("_(programming_environment)", "")
    step_3 = step_2.replace("_programming_language", "")
    step_4 = step_3.replace("_", " ")
    step_5 = step_4.split("#")
    return step_5[0]


def remove_duplicates(list_rray):
    unique_rows = []
    for row in sorted(list_rray):
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows


with open("data_wikigraph.json") as json_file:
    wikigraph = json.load(json_file)
json_file.close()

data_graph = []
data_year = []

for key, fields in wikigraph.items():

    list_first_appeared = fields.get("first_appeared")
    data_year.append(
        [
            strip_disambiguation(key),
            min(list_first_appeared, default=-999),
        ]
    )
    list_influenced_by = fields.get("influenced_by")
    for influenced_by_href in list_influenced_by:
        data_graph.append(
            [
                strip_disambiguation(influenced_by_href),
                strip_disambiguation(key),
            ]
        )
    list_influenced = fields.get("influenced")
    for influenced_href in list_influenced:
        data_graph.append(
            [
                strip_disambiguation(key),
                strip_disambiguation(influenced_href),
            ]
        )

dict_year = {}
year_array = remove_duplicates(data_year)
for row in year_array:
    if row[0] not in dict_year:
        if row[1] > 0:
            dict_year[row[0]] = row[1]

directed_graph = remove_duplicates(data_graph)
list_influencer = []
list_influencee = []
for edge in directed_graph:
    list_influencer.append(edge[0])
    list_influencee.append(edge[1])

dict_influencers_count = Counter(list_influencer)
dict_influencees_count = Counter(list_influencee)

df_directed_graph = pd.DataFrame(directed_graph)
df_directed_graph.to_csv("directed_graph.csv", index=False)

###############################################################################

df_summary = pd.DataFrame(
    {
        "year": pd.Series(dict_year, dtype=int),
        "num_outgoing_links": pd.Series(dict_influencers_count),
        "num_incoming_links": pd.Series(dict_influencees_count),
    }
)

df_summary.index.name = "key"
df_summary.sort_values(by=["key"], inplace=True)
df_summary.to_csv("directed_graph_metadata.csv", index=True)

###############################################################################

plt.rcParams.update({"font.sans-serif": "Consolas"})
plt.rcParams.update({"font.size": 12})

mpl.use("Agg")

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)

plt.scatter(
    df_summary.year,
    df_summary.num_incoming_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c=df_summary.num_outgoing_links,
    alpha=0.7,
    edgecolors="none",
)
plt.scatter(
    df_summary.year,
    df_summary.num_incoming_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c="none",
    alpha=0.7,
    edgecolors="k",
)

plt.ylabel("Number of incoming links\n")
plt.xlim([1940, 2020])
plt.xlabel(
    "\nYear of programming language first appereance\n(size is influence, or number of outgoing links)"
)

plt.savefig("figures/summary_scatterplot.png", dpi=300)

plt.close()

###############################################################################
