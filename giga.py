import json
from statistics import median
import requests


if __name__ == "__main__":
    res = requests.post(
        "https://www.pathofexile.com/api/trade/exchange/Crucible",
        data=json.dumps(
            {
                "query": {
                    "status": {"option": "online"},
                    "have": ["chaos"],
                    "want": ["exalted"],
                },
                "sort": {"have": "asc"},
                "engine": "new",
            }
        ),
        headers={"User-Agent": "poe-trading-bot-2", "Content-Type": "application/json"},
    ).json()

    listings = list(res["result"].values())
    listings_values = list(
        map(
            lambda x: x["listing"]["offers"][0]["exchange"]["amount"]
            / x["listing"]["offers"][0]["item"]["amount"],
            listings,
        )
    )
    if len(listings_values) % 2 == 0:
        listings_values = listings_values[5 : (min(20, res["total"]))]

    print(len(listings_values))
    print(median(listings_values))
