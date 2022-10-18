# by Matias I. Bofarull Oddo - 2022.10.18

import pandas as pd

# DATA AND METADATA

dataCSV = pd.read_csv("dataCSV/directed_graph.csv")
key_source = list(dataCSV["0"])
key_target = list(dataCSV["1"])

dataCSV = pd.read_csv("dataCSV/directed_graph_year.csv")
key_year = list(dataCSV["0"])

dataCSV = pd.read_csv("dataCSV/directed_graph_paradigm.csv")
key_paradigm = list(dataCSV["0"])

dataCSV = pd.read_csv("dataCSV/directed_graph_type_system.csv")
key_type = list(dataCSV["0"])

# SANITY CHECK

all_keys = sorted(list(set(key_source + key_target)))

print(all_keys == key_year)
print(all_keys == key_paradigm)
print(all_keys == key_type)
