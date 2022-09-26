# by Matias I. Bofarull Oddo - 2022.09.22

import requests
from bs4 import BeautifulSoup

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"

page_href = "COBOL"

sesh = requests.Session()
page = sesh.get(rest_API + page_href, timeout=10)
soup = BeautifulSoup(page.content, "html.parser")

infobox = soup.find("table", {"class": "infobox vevent"})

with open("infobox_" + page_href + ".html", "w", encoding="utf-8") as file:
    file.write(infobox.prettify())

infobox_rows = [row.prettify() for row in soup.find_all("tr")]

section = 0
row_index = 0
data_strings = ["", ""]

for row in infobox_rows:
    if "Influenced" in row:
        data_strings[section] += infobox_rows[row_index]
        data_strings[section] += infobox_rows[row_index + 1]
        section += 1
    row_index += 1

data_influenced_by = BeautifulSoup(data_strings[0], "html.parser")
data_influenced = BeautifulSoup(data_strings[1], "html.parser")

list_influenced_by = [
    str(a["href"])[2:]
    for a in data_influenced_by.find_all(
        "a",
        {"rel": True},
    )
]
list_influenced = [
    str(a["href"])[2:]
    for a in data_influenced.find_all(
        "a",
        {"rel": True},
    )
]

list_href = sorted(set(list_influenced_by + list_influenced))

###############################################################################

print("\n", page_href)

print("\n Influenced by:\n")
for i in list_influenced_by:
    print("\t", i)

print("\n Influenced:\n")
for i in list_influenced:
    print("\t", i)

print()

print(sorted(set(list_influenced_by + list_influenced)))

print()

###############################################################################

test_1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
test_2 = ["A", "B", "C"]
test_3 = ["G", "H", "I"]

print(test_2 + test_3)
