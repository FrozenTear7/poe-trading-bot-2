import json
from statistics import median
from typing import Literal

import pyautogui
from config.user_setup import POESESSID, STASH_TABS

import requests

from utils.printtime import printtime


class CurrencyPrice:
    def __init__(
        self,
        name: str,
        mode: Literal["sell", "buy"],
        price: float,
    ) -> None:
        self.name = name
        self.mode: Literal["sell", "buy"] = mode
        self.price = price

    def get_note(self, exchange_name: str):
        if self.mode == "buy":
            return f"~price {self.price} {exchange_name}"
        else:
            return f"~price {self.price} chaos"


class PriceCalculator:
    def __init__(
        self,
    ) -> None:
        self.buy_currency_config = {}
        self.sell_currency_config = {}

        for stash_tab in STASH_TABS:
            for currency in stash_tab.active_currencies:
                printtime(
                    f"Fetching exchange info for: {currency}, in {stash_tab.mode} mode"
                )
                res = requests.post(
                    "https://www.pathofexile.com/api/trade/exchange/Crucible",
                    data=json.dumps(
                        {
                            "query": {
                                "status": {"option": "online"},
                                "have": [
                                    "chaos"
                                    if stash_tab.mode == "sell"
                                    else stash_tab.get_exchange_name(currency)
                                ],
                                "want": [
                                    "chaos"
                                    if stash_tab.mode == "buy"
                                    else stash_tab.get_exchange_name(currency)
                                ],
                            },
                            "sort": {"have": "asc"},
                            "engine": "new",
                        }
                    ),
                    headers={
                        "User-Agent": "poe-trading-bot-2",
                        "Content-Type": "application/json",
                        "Cookie": f"POESESSID={POESESSID}",
                    },
                ).json()

                if res["total"] < 20:
                    raise Exception("Currency: {currency} doesn't have enough listings")

                listings = list(res["result"].values())
                listings_values = list(
                    map(
                        lambda x: round(
                            x["listing"]["offers"][0]["exchange"]["amount"]
                            / x["listing"]["offers"][0]["item"]["amount"],
                            4,
                        ),
                        listings,
                    )
                )
                listings_values = listings_values[5:20]

                if stash_tab.mode == "buy":
                    self.buy_currency_config[currency] = CurrencyPrice(
                        currency, stash_tab.mode, median(listings_values)
                    )
                else:
                    self.sell_currency_config[currency] = CurrencyPrice(
                        currency, stash_tab.mode, median(listings_values)
                    )
                pyautogui.sleep(3)

    def get_buy_note(self, currency_name: str, exchange_name: str):
        return self.buy_currency_config[currency_name].get_note(exchange_name)

    def get_sell_note(self, currency_name: str, exchange_name: str):
        return self.sell_currency_config[currency_name].get_note(exchange_name)
