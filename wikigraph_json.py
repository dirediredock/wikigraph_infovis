# by Matias I. Bofarull Oddo - 2022.09.26

import json
import requests
from bs4 import BeautifulSoup

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"

dict_wikigraph = {}


def wikiscrape_infobox(page_href):

    try:

        if page_href not in dict_wikigraph:
            dict_wikigraph[page_href] = {}

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
        list_influenced_by = [
            str(a["href"])[2:]
            for a in data_influenced_by.find_all(
                "a",
                {"rel": True},
            )
        ]
        data_influenced = BeautifulSoup(data_strings[1], "html.parser")
        list_influenced = [
            str(a["href"])[2:]
            for a in data_influenced.find_all(
                "a",
                {"rel": True},
            )
        ]

        list_href = sorted(set(list_influenced_by + list_influenced))

        if page_href in dict_wikigraph:
            dict_wikigraph[page_href]["influenced_by"] = list_influenced_by
            dict_wikigraph[page_href]["influenced"] = list_influenced
            print()
            print(page_href)
            print(list_influenced_by)
            print(list_influenced)

        for href in list_href:
            if href not in dict_wikigraph:
                wikiscrape_infobox(href)

    except Exception as error_message:
        print()
        print("FAILED [" + page_href + "]")
        print("ERROR: " + str(error_message))


if __name__ == "__main__":

    wikiscrape_infobox("C++")


with open("data_wikigraph.json", "w") as json_file:
    json.dump(dict_wikigraph, json_file, sort_keys=False, indent=4)
