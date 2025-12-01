"""
Get A list of all Senate Democrats and their social media accounts.
"""

import os
from typing import TypedDict

import requests
from atproto import Client, IdResolver
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()  # This reads variables from the
# .env file and loads them into os environment.
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")


DEM_CAUCUS_URL = (
    "https://www.democrats.senate.gov"
    "/about-senate-dems/our-caucus"
)


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


def login_bsky() -> Client:
    """Log the current user in to bluesky and return a client."""
    client = Client()
    client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
    return client


def parse_handles(last_name: str) -> str:
    """Take the last name of a candidate and return their bsky handle.
    Even if the candidates account handle involves a custom domain
    ie .senate.gov the .bsky.social
    handle is reserved for them and is the only way to access DIDs"""
    return f"{last_name}.bsky.social"


def get_bsky_did():
    """Receive the handle of a candidate and return their bsky DID.
    This specialspecial identifier is needed for certain calls with
    the bluesky sdk. Docs here:
    https://docs.bsky.app/docs/advanced-guides/resolving-identities
    """
    resolver = IdResolver()
    did = resolver.handle.resolve("alsobrooks.bsky.social")
    return did
