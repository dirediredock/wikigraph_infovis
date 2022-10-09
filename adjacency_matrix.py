# by Matias I. Bofarull Oddo - 2022.10.08

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

scriptsPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptsPath)

with open("directed_graph.csv", newline="") as csv_file:
    directed_graph = list(csv.reader(csv_file))
csv_file.close()

href_index = {}

count = 0
for row in directed_graph[1:]:
    for href in row:
        if href not in href_index:
            href_index[href] = count
            count += 1

empty_matrix = [[0] * len(href_index) for _ in range(len(href_index))]

for row in directed_graph[1:]:
    empty_matrix[href_index[row[0]]][href_index[row[1]]] += 2
    empty_matrix[href_index[row[1]]][href_index[row[0]]] += 1

matrix_csv = pd.DataFrame(empty_matrix)
matrix_csv.to_csv("adjacency_matrix.csv", index=True)


def strip_disambiguation(href):
    step_1 = href.replace("_(programming_language)", "")
    step_2 = step_1.replace("_(programming_environment)", "")
    step_3 = step_2.replace("_programming_language", "")
    step_4 = step_3.replace("_", " ")
    step_5 = step_4.split("#")
    return step_5[0]


def vectorize_matrix(matrix):
    x = []
    y = []
    z = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])
    return x, y, z


print()
for key in sorted(href_index.keys()):
    print(strip_disambiguation(key))
print()

x, y, z = vectorize_matrix(empty_matrix)

df_matrix = pd.DataFrame(
    {
        "X": x,
        "Y": y,
        "Z": z,
    }
)

dir_backward = df_matrix[df_matrix["Z"] == 1]
dir_forwards = df_matrix[df_matrix["Z"] == 2]
dir_bothways = df_matrix[df_matrix["Z"] == 3]

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
ax.scatter(dir_forwards.X, dir_forwards.Y, marker="s", c="k", s=4)
plt.gca().set_position([0, 0, 1, 1])
plt.axis("off")
plt.savefig("figures/adjacency_forwards.png", dpi=300)

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
ax.scatter(
    dir_backward.X,
    dir_backward.Y,
    marker="s",
    c="k",
    s=4,
)
plt.gca().set_position([0, 0, 1, 1])
plt.axis("off")
plt.savefig("figures/adjacency_backward.png", dpi=300)

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111)
ax.scatter(
    dir_bothways.X,
    dir_bothways.Y,
    marker="s",
    c="k",
    s=10,
)
plt.gca().set_position([0, 0, 1, 1])
plt.axis("off")
plt.savefig("figures/adjacency_bothways.png", dpi=300)
