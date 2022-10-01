# by Matias I. Bofarull Oddo - 2022.09.22

import os
import requests
from bs4 import BeautifulSoup

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"

list_wikiscrape_href = []
list_empty_href = []
list_error_href = []
list_link_count = []


def wikiscrape_infobox(page_href):

    try:

        if page_href not in list_wikiscrape_href:
            list_wikiscrape_href.append(page_href)

        sesh = requests.Session()
        page = sesh.get(rest_API + page_href, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        infobox_HTML = soup.find("table", {"class": "infobox vevent"})

        with open(
            "infoboxes/infobox_"
            + page_href.replace("_(programming_language)", "")
            + ".html",
            "w",
            encoding="utf-8",
        ) as file:
            try:
                file.write(infobox_HTML.prettify())
            except Exception as error_prettify:
                print("ERROR prettify(): " + str(error_prettify))
                file.close()
                os.remove(file.name)

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

        if len(list_href) == 0:
            print()
            print("EMPTY [" + page_href + "]", end="")
            if page_href not in list_empty_href:
                list_empty_href.append(page_href)

        if page_href in list_wikiscrape_href:
            print()
            print(page_href)
            print(list_influenced_by)
            print(list_influenced)

        for href in list_href:
            if href not in list_wikiscrape_href:
                list_wikiscrape_href.append(href)
                list_link_count.append(len(list_href))
                wikiscrape_infobox(href)

    except Exception as error_message:
        list_error_href.append(page_href)
        print()
        print("FAILED [" + page_href + "]")
        print("ERROR: " + str(error_message))


if __name__ == "__main__":

    wikiscrape_infobox("C++")


final_list = []

for href in list_wikiscrape_href:
    if href not in (list_empty_href + list_error_href):
        final_list.append(href)

print()
print(sorted(list_error_href))
print()
print("ERROR", len(list_error_href))
print()
print(sorted(list_empty_href))
print()
print("LEAF NODES", len(list_empty_href))
print()
print(sorted(final_list))
print()
print("NETWORK NODES", len(final_list))
print()
print(list_link_count)
print()
print("NETWORK LINKS", sum(list_link_count))
print()
print("LEAF + NETWORK LINKS", sum(list_link_count) + len(list_link_count))
print()
