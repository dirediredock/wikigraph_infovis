# by Matias I. Bofarull Oddo - 2022.10.10

import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote_plus, unquote_plus

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"
param_API = "?redirect=true&stash=false"
url_regex = re.compile(r"\/page\/html\/(.*?)[\?|^]")

dict_wikigraph = {}


def wikiscrape_infobox(page_href):

    try:

        if page_href not in dict_wikigraph:
            dict_wikigraph[page_href] = {}

        sesh = requests.Session()
        page = sesh.get(
            rest_API + quote_plus(page_href) + param_API,
            timeout=30,
        )
        url_match = url_regex.search(page.url)
        true_href = unquote_plus(url_match.group(1))

        soup = BeautifulSoup(page.content, "html.parser")

        infobox_HTML = soup.find("table", {"class": "infobox vevent"})

        with open(
            "infoboxes.html",
            "a",
            encoding="utf-8",
        ) as file:
            try:
                file.write("<br><h1>" + page_href + "</h1><br>")
                file.write(infobox_HTML.prettify())
            except Exception as error_prettify:
                print("ERROR prettify(): " + str(error_prettify))

        infobox_rows = [row.prettify() for row in soup.find_all("tr")]

        row_index = 0
        data_strings = {
            "influenced_by": "",
            "influenced": "",
        }

        for row in infobox_rows:
            if "Influenced by" in row:
                data_strings["influenced_by"] += infobox_rows[row_index]
                data_strings["influenced_by"] += infobox_rows[row_index + 1]
            elif "Influenced" in row:
                data_strings["influenced"] += infobox_rows[row_index]
                data_strings["influenced"] += infobox_rows[row_index + 1]
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

        if page_href in dict_wikigraph:

            dict_wikigraph[page_href]["influenced_by"] = list_influenced_by
            dict_wikigraph[page_href]["influenced"] = list_influenced
            dict_wikigraph[page_href]["redirect_href"] = url_match.group(1)
            dict_wikigraph[page_href]["true_href"] = true_href

            print()
            print(page_href)
            print(true_href)
            print(list_influenced_by)
            print(list_influenced)

        list_href = sorted(set(list_influenced_by + list_influenced))
        for href in list_href:
            if href not in dict_wikigraph:
                wikiscrape_infobox(href)

    except Exception as error_message:
        print()
        print("FAILED [" + page_href + "]")
        print("ERROR: " + str(error_message))


if __name__ == "__main__":

    wikiscrape_infobox("Fortran")


print()
