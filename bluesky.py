"""
Get raw data on blue sky feeds for politicians.
"""

import os

from atproto import Client
from atproto_client.exceptions import BadRequestError
from dotenv import load_dotenv

from politician_lookup import get_dem_senate_caucus

load_dotenv()  # This reads variables from the
# .env file and loads them into os environment.
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")


class BlueSkyData:
    def __init__(self):
        self.feed_results = []
        self.failed_lookups = []
        self.full_senate_data = []
        self.client = None

    def login_bsky(self) -> Client:
        """Log the current user in to bluesky and return a client."""
        if self.client is None:
            client = Client()
            client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
            self.client = client
            # This will allow us to log in once and avoid hitting
            # bluesky's API limits of 100 logins per 5 minutes.
            return client
        else:
            return self.client

    def parse_handles(self, last_name: str) -> str:
        """Take the last name of a candidate and return their bsky handle.
        Even if the candidates account handle involves a custom domain
        ie .senate.gov the .bsky.social
        handle is reserved for them and is the only way to access DIDs"""
        return f"{last_name}.senate.gov"

    def get_bsky_did(self, last_name: str) -> str:
        """Receive the handle of a candidate and return their bsky DID.
        This specialspecial identifier is needed for certain calls with
        the bluesky sdk. Docs here:
        https://docs.bsky.app/docs/advanced-guides/resolving-identities
        """
        client = self.login_bsky()
        handle = self.parse_handles(last_name)
        did = client.get_profile(actor=handle).did
        return did

    def lookup_feed(
        self,
        politician_last_name: str,
        max_page_count: int = 10,
        page_number: int = 1,
        cursor: str | None = None,
    ) -> list[tuple]:
        """Take the last name of a politician and return that politicians
        bluesky feed. https://docs.bsky.app/docs/tutorials/viewing-feeds"""

        client = self.login_bsky()
        did = self.get_bsky_did(politician_last_name)
        # DID is necessary for bsky get author feed method. Cannot
        # do it by handle.
        data = client.get_author_feed(actor=did, limit=100)
        if data.cursor and page_number < max_page_count:
            page_number += 1
            feed = self.lookup_feed(
                politician_last_name=politician_last_name,
                page_number=page_number,
                cursor=data.cursor,
            )
            self.feed_results.extend(feed)
        else:
            self.feed_results.extend(data.feed)

        return data.feed

    def get_all_sentate_bsky(self) -> list[dict]:
        for senator_dict in get_dem_senate_caucus():
            full_name = (
                f"{senator_dict["first_name"]} "
                f"{senator_dict["last_name"]}"
            )
            print(f"getting {full_name}")
            try:
                senator_feed = self.lookup_feed(
                    senator_dict["last_name"].lower().replace(" ", "")
                )
                this_senators_data = {f"{full_name}": senator_feed}
                self.full_senate_data.append(this_senators_data)
                self.feed_results.clear()
            except BadRequestError as e:
                print(f"Failed lookup for {full_name} due to: {e}")
                self.failed_lookups.append(full_name)
                continue
        return self.full_senate_data


bsky_data = BlueSkyData()
print(bsky_data.get_all_sentate_bsky())
