# by Matias I. Bofarull Oddo - 2022.09.26

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, unquote_plus

rest_API = "https://en.wikipedia.org/api/rest_v1/page/html/"
param_API = "?redirect=true&stash=false"
year_regex = re.compile(r"[1|2]\d{3}")
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
            elif "Initial release" in row:
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

        if page_href in dict_wikigraph:
            dict_wikigraph[page_href]["first_appeared"] = first_appeared
            dict_wikigraph[page_href]["influenced_by"] = list_influenced_by
            dict_wikigraph[page_href]["influenced"] = list_influenced
            dict_wikigraph[page_href]["redirect_href"] = url_match.group(1)
            dict_wikigraph[page_href]["true_href"] = true_href

            print()
            print(page_href)
            print(true_href)
            print(first_appeared)
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


with open("data_wikigraph.json", "w") as json_file:
    json.dump(dict_wikigraph, json_file, sort_keys=True, indent=4)


# Each wikipedia page related to a programming language has an infobox that has three fields of interest, year of language first appereance, list of langages it influenced, and list of languages it was influenced by.
# This scraper uses Wikipedia's REST API and Python's BeautifulSoup to parse the HTML page content.
# Scraping starts with a given href and recursively crawls all other hrefs listed in the infobox of a page, until all hrefs are exhausted.
# When the recursive scraping is complete each unique href becomes a key in JSON file, with four subfields:
# `first_appeared` is the year
# `influenced` is a list of hrefs, the outgoing links in a graph
# `influenced_by` is a list of hrefs, the incoming links in a graph
# `redirect_href` is the encoded HTML redirect href
# `true_href` is the page href that resolves synonyms
