"""A module for entity linking
"""

import requests


def perform_wikification(item):
    try:
        url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={item}&language=en&format=json"
        data = requests.get(url).json()

        return data["search"][0]["id"]
    except:
        return "no-data"
