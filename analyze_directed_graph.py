# by Matias I. Bofarull Oddo - 2022.10.08

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def remove_duplicates(list_rray):
    unique_rows = []
    for row in sorted(list_rray):
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows


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


def bubble_scatterplot(
    var_X,
    var_Y,
    var_S,
    yticks,
    string_v,
    string_h,
    save_file,
):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    plt.scatter(
        var_X,
        var_Y,
        s=(var_S + 1.8) ** 2.75,
        c=var_S,
        alpha=0.7,
        edgecolors="none",
    )
    plt.scatter(
        var_X,
        var_Y,
        s=(var_S + 1.8) ** 2.75,
        c="none",
        alpha=0.7,
        edgecolors="k",
    )
    ax.set_yticks(yticks)
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(year_labels)
    plt.ylabel("Number of " + string_v + " edges\n")
    plt.xlim([year_ticks[0] - 10, year_ticks[-1] + 10])
    plt.xlabel(
        "\nYear of programming language first appereance\n(size is number of "
        + string_h
        + " edges)"
    )
    plt.savefig(save_file, dpi=300)
    plt.close()


def text_scatterplot(
    var_X,
    var_Y,
    var_S,
    var_I,
    yticks,
    string_v,
    string_h,
    save_file,
):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    for i, key in enumerate(var_I):
        if not np.isnan(var_X[i]):
            if not np.isnan(var_Y[i]):
                plt.text(
                    var_X[i],
                    var_Y[i],
                    width_constrained_text(strip_disambiguation(key), 5),
                    fontsize=(var_S[i] + 4) * 1.01,
                    linespacing=0.75,
                    ha="center",
                    va="center",
                )
    plt.scatter(
        var_X,
        var_Y,
        s=(var_S + 2) ** 2.75,
        c="none",
        alpha=0.25,
        edgecolors="gray",
        linewidth=4,
    )
    ax.set_yticks(yticks)
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(year_labels)
    plt.ylabel("Number of " + string_v + " edges\n")
    plt.xlim([year_ticks[0] - 10, year_ticks[-1] + 10])
    plt.xlabel(
        "\nYear of programming language first appereance\n(size is number of "
        + string_h
        + " edges)"
    )
    plt.savefig(save_file, dpi=300)
    plt.close()


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
        if wikigraph[influenced_by_href]["true_href"] == wikigraph[key]["true_href"]:
            continue
        data_graph.append(
            [
                wikigraph[influenced_by_href]["true_href"],
                wikigraph[key]["true_href"],
            ]
        )
    list_influenced = fields.get("influenced")
    for influenced_href in list_influenced:
        if wikigraph[influenced_href]["true_href"] == wikigraph[key]["true_href"]:
            continue
        data_graph.append(
            [
                wikigraph[key]["true_href"],
                wikigraph[influenced_href]["true_href"],
            ]
        )

directed_graph = remove_duplicates(data_graph)
metadata = remove_duplicates(data_year)

year_ticks = [1950, 1970, 1990, 2010, 2030]
year_labels = [1950, 1970, 1990, 2010, "No Data"]

dict_year = {}
for row in metadata:
    if row[0] not in dict_year:
        if type(row[1]) == type(1):
            dict_year[row[0]] = row[1]
        else:
            dict_year[row[0]] = 2030

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

plt.rcParams.update({"font.sans-serif": "Consolas"})
plt.rcParams.update({"font.size": 12})

bubble_scatterplot(
    df_summary.year,
    df_summary.num_incoming_links,
    df_summary.num_outgoing_links,
    [0, 5, 10, 15, 20],
    "'Influenced by'",
    "'Influenced'",
    "figures/summary_A_plot.png",
)
bubble_scatterplot(
    df_summary.year,
    df_summary.num_outgoing_links,
    df_summary.num_outgoing_links,
    [0, 5, 10, 15, 20, 25, 30, 40, 50],
    "'Influenced'",
    "'Influenced'",
    "figures/summary_B_plot.png",
)
text_scatterplot(
    df_summary.year,
    df_summary.num_incoming_links,
    df_summary.num_outgoing_links,
    df_summary.index,
    [0, 5, 10, 15, 20],
    "'Influenced by'",
    "'Influenced'",
    "figures/summary_A_text.png",
)
text_scatterplot(
    df_summary.year,
    df_summary.num_outgoing_links,
    df_summary.num_outgoing_links,
    df_summary.index,
    [0, 5, 10, 15, 20, 25, 30, 40, 50],
    "'Influenced'",
    "'Influenced'",
    "figures/summary_B_text.png",
)
