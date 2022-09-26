# by Matias I. Bofarull Oddo - 2022.09.22

import requests
from bs4 import BeautifulSoup

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"

page_href = "C++"

main_list = {}


def extract_infobox(page_href):

    sesh = requests.Session()
    page = sesh.get(rest_API + page_href, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
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

    return list_href, list_influenced_by, list_influenced


list_href, list_influenced_by, list_influenced = extract_infobox(page_href)

print()
print(page_href)
print()
print(list_href)
print()
