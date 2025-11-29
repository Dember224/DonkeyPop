"""
Get A list of all Senate Democrats and their social media accounts.
"""

import requests
from bs4 import BeautifulSoup


def get_dem_senate_caucus():
    """Lookup a list of dictionaries of senate Democrat's  first
    and last names so that we know who to retrieve socials for."""
    response = requests.get(
        "https://www.democrats.senate.gov/about-senate-dems/our-caucus"
    )

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    senator_list = []
    for senator in soup.find_all("div", class_="MemberBox__name"):
        senator_name_list = [
            name.get_text()
            for name in senator.find_all("span")
            if "Senator" not in name.get_text()
        ]
        senator_name_dict = {
            "first_name": senator_name_list[0],
            "last_name": senator_name_list[1],
        }
        senator_list.append(senator_name_dict)

    return senator_list
