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
data_paradigm = []
data_type_sys = []

for key, fields in wikigraph.items():

    list_first_appeared = fields.get("first_appeared")
    data_year.append(
        [
            wikigraph[key]["true_href"],
            min(list_first_appeared, default=""),
        ]
    )
    list_paradigm = fields.get("paradigm")
    data_paradigm.append(
        [
            wikigraph[key]["true_href"],
            list_paradigm,
        ]
    )
    list_type_sys = fields.get("type_system")
    data_type_sys.append(
        [
            wikigraph[key]["true_href"],
            list_type_sys,
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
df_directed_graph = pd.DataFrame(directed_graph)
df_directed_graph.to_csv("dataCSV/directed_graph.csv", index=False)

metadata = remove_duplicates(data_year)
df_metadata = pd.DataFrame(metadata)
df_metadata.to_csv("dataCSV/directed_graph_year.csv", index=False)

paradigm = remove_duplicates(data_paradigm)
df_paradigm = pd.DataFrame(paradigm)
df_paradigm.to_csv("dataCSV/directed_graph_paradigm.csv", index=False)

type_sys = remove_duplicates(data_type_sys)
df_type_sys = pd.DataFrame(type_sys)
df_type_sys.to_csv("dataCSV/directed_graph_type_system.csv", index=False)
