# by Matias I. Bofarull Oddo - 2022.10.08

import json
import pandas as pd


def remove_duplicates(list_rray):
    unique_rows = []
    for row in sorted(list_rray):
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows


with open("data_wikigraph.json") as json_file:
    wikigraph = json.load(json_file)
json_file.close()

data_year = []
data_graph = []

for key, fields in wikigraph.items():

    list_first_appeared = fields.get("first_appeared")
    data_year.append(
        [
            wikigraph[key]["true_href"],
            min(list_first_appeared, default=""),
        ]
    )
    list_influenced_by = fields.get("influenced_by")
    for influenced_by_href in list_influenced_by:
        data_graph.append(
            [
                wikigraph[influenced_by_href]["true_href"],
                wikigraph[key]["true_href"],
            ]
        )
    list_influenced = fields.get("influenced")
    for influenced_href in list_influenced:
        data_graph.append(
            [
                wikigraph[key]["true_href"],
                wikigraph[influenced_href]["true_href"],
            ]
        )

directed_graph = remove_duplicates(data_graph)
metadata = remove_duplicates(data_year)

# SCATTERPLOTS

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

dict_year = {}
for row in metadata:
    if row[0] not in dict_year:
        if type(row[1]) == type(1):
            dict_year[row[0]] = row[1]

list_influencer = []
list_influencee = []

for edge in directed_graph:
    list_influencer.append(edge[0])
    list_influencee.append(edge[1])

dict_influencers_count = Counter(list_influencer)
dict_influencees_count = Counter(list_influencee)

df_summary = pd.DataFrame(
    {
        "year": pd.Series(dict_year, dtype=int),
        "num_outgoing_links": pd.Series(dict_influencers_count),
        "num_incoming_links": pd.Series(dict_influencees_count),
    }
)

df_summary.index.name = "keys"
df_summary.sort_values(by=["keys"], inplace=True)


def strip_disambiguation(href):
    step_1 = href.replace("_(programming_language)", "")
    step_2 = step_1.replace("_(programming_environment)", "")
    step_3 = step_2.replace("_programming_language", "")
    step_4 = step_3.replace("_", " ")
    step_5 = step_4.split("#")
    return step_5[0]


def width_constrained_text(string_input, max_characters_per_line):
    count = 0
    lines_array = []
    segments = string_input.split(" ")
    for segment in segments:
        if len(segment) < max_characters_per_line:
            segment_plus = ""
            required_length = 0
            if count == 0:
                required_length = len(segment)
                segment_plus = segment
            else:
                required_length = len(segment) + 1
                segment_plus = " " + segment
            if count + required_length < max_characters_per_line:
                if count == 0:
                    lines_array.append(segment_plus)
                else:
                    lines_array[-1] += segment_plus
                count += required_length
            else:
                count = len(segment)
                lines_array.append(segment)
        else:
            lines_array.append(segment)
    return "\n".join(lines_array)


plt.rcParams.update({"font.sans-serif": "Consolas"})
plt.rcParams.update({"font.size": 12})

# Bubble scatterplot of `year` vs `influenced_by`

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
plt.ylabel("Number of 'Influenced by' edges\n")
plt.xlim([1940, 2020])
plt.xlabel(
    "\nYear of programming language first appereance\n(size is number of 'Influenced' edges)"
)
plt.savefig("figures/summary_A_plot.png", dpi=300)
plt.close()

# Text scatterplot of `year` vs `influenced_by`

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
for i, key in enumerate(df_summary.index):
    if not np.isnan(df_summary.year[i]):
        if not np.isnan(df_summary.num_incoming_links[i]):
            plt.text(
                df_summary.year[i],
                df_summary.num_incoming_links[i],
                width_constrained_text(strip_disambiguation(key), 9),
                fontsize=(df_summary.num_outgoing_links[i] + 4) * 1.01,
                ha="center",
                va="center",
            )
plt.scatter(
    df_summary.year,
    df_summary.num_incoming_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c="none",
    alpha=0.25,
    edgecolors="gray",
    linewidth=4,
)
plt.ylabel("Number of 'Influenced by' edges\n")
plt.xlim([1940, 2020])
plt.xlabel(
    "\nYear of programming language first appereance\n(size is number of 'Influenced' edges)"
)
plt.savefig("figures/summary_A_text.png", dpi=300)
plt.close()

# Bubble scatterplot of `year` vs `influenced`

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
plt.scatter(
    df_summary.year,
    df_summary.num_outgoing_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c=df_summary.num_outgoing_links,
    alpha=0.7,
    edgecolors="none",
)
plt.scatter(
    df_summary.year,
    df_summary.num_outgoing_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c="none",
    alpha=0.7,
    edgecolors="k",
)
plt.ylabel("Number of 'Influenced' edges\n")
plt.xlim([1940, 2020])
plt.xlabel(
    "\nYear of programming language first appereance\n(size is number of 'Influenced' edges)"
)
plt.savefig("figures/summary_B_plot.png", dpi=300)
plt.close()

# Text scatterplot of `year` vs `influenced`

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
for i, key in enumerate(df_summary.index):
    if not np.isnan(df_summary.year[i]):
        if not np.isnan(df_summary.num_outgoing_links[i]):
            plt.text(
                df_summary.year[i],
                df_summary.num_outgoing_links[i],
                width_constrained_text(strip_disambiguation(key), 9),
                fontsize=(df_summary.num_outgoing_links[i] + 4) * 1.01,
                ha="center",
                va="center",
            )
plt.scatter(
    df_summary.year,
    df_summary.num_outgoing_links,
    s=(df_summary.num_outgoing_links + 2) ** 2.75,
    c="none",
    alpha=0.25,
    edgecolors="gray",
    linewidth=4,
)
plt.ylabel("Number of 'Influenced' edges\n")
plt.xlim([1940, 2020])
plt.xlabel(
    "\nYear of programming language first appereance\n(size is number of 'Influenced' edges)"
)
plt.savefig("figures/summary_B_text.png", dpi=300)
plt.close()
