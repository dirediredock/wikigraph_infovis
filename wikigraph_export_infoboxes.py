# by Matias I. Bofarull Oddo - 2022.09.26

import os
import re
import requests
from bs4 import BeautifulSoup

year_regex = re.compile(r"[1|2]\d{3}")

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"

dict_wikigraph = {}


def wikiscrape_infobox(page_href):

    try:

        if page_href not in dict_wikigraph:
            dict_wikigraph[page_href] = {}

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

        row_index = 0
        data_strings = {
            "influenced_by": "",
            "influenced": "",
            "first_appeared": "",
        }

        for row in infobox_rows:
            if "Influenced by" in row:
                data_strings["influenced_by"] += infobox_rows[row_index]
                data_strings["influenced_by"] += infobox_rows[row_index + 1]
            elif "Influenced" in row:
                data_strings["influenced"] += infobox_rows[row_index]
                data_strings["influenced"] += infobox_rows[row_index + 1]
            elif "appeared" in row:
                data_strings["first_appeared"] += row
            row_index += 1

        data_influenced_by = BeautifulSoup(
            data_strings["influenced_by"],
            "html.parser",
        )
        list_influenced_by = [
            str(a["href"])[2:]
            for a in data_influenced_by.find_all(
                "a",
                {"rel": True},
            )
        ]

        data_influenced = BeautifulSoup(
            data_strings["influenced"],
            "html.parser",
        )
        list_influenced = [
            str(a["href"])[2:]
            for a in data_influenced.find_all(
                "a",
                {"rel": True},
            )
        ]

        data_first_appeared = BeautifulSoup(
            data_strings["first_appeared"],
            "html.parser",
        )
        first_appeared = []
        for s in data_first_appeared.find_all("td", class_="infobox-data"):
            infobox_string = s.get_text()
            regex_match = year_regex.search(infobox_string)
            if regex_match:
                first_appeared.append(int(regex_match.group(0)))

        list_href = sorted(set(list_influenced_by + list_influenced))

        if page_href in dict_wikigraph:
            dict_wikigraph[page_href]["first_appeared"] = first_appeared
            dict_wikigraph[page_href]["influenced_by"] = list_influenced_by
            dict_wikigraph[page_href]["influenced"] = list_influenced
            print()
            print(page_href)
            print(first_appeared)
            print(list_influenced_by)
            print(list_influenced)
            print("Links:", len(list_href))

        for href in list_href:
            if href not in dict_wikigraph:
                wikiscrape_infobox(href)

    except Exception as error_message:
        print()
        print("FAILED [" + page_href + "]")
        print("ERROR: " + str(error_message))


if __name__ == "__main__":

    wikiscrape_infobox("C++")


print()
