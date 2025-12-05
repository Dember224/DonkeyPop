"""
Get lists of politicians who we want information on.
"""

from typing import TypedDict

import requests
from bs4 import BeautifulSoup

DEM_CAUCUS_URL = "https://www.democrats.senate.gov" "/about-senate-dems/our-caucus"


class NameDict(TypedDict):
    first_name: str
    last_name: str


def get_dem_senate_caucus() -> list[NameDict]:
    """Lookup a list of dictionaries of senate Democrat's  first
    and last names so that we know who to retrieve socials for."""
    response = requests.get(DEM_CAUCUS_URL)

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    senator_list = []
    for senator in soup.find_all("div", class_="MemberBox__name"):
        senator_name_list = [
            name.get_text()
            for name in senator.find_all("span")
            if "Senator" not in name.get_text()
        ]
        senator_name_dict: NameDict = {
            "first_name": senator_name_list[0],
            "last_name": senator_name_list[1],
        }
        senator_list.append(senator_name_dict)

    return senator_list
