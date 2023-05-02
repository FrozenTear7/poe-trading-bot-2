from config.user_setup import LEAGUE_NAME
from utils.get_fraction_approximation import (
    get_fractional_representation_under_limit,
)
import requests


class CurrencyPrice:
    def __init__(
        self,
        name: str,
        buy_price_own_chaos: int,
        buy_price_trader_currency: int,
        sell_price_own_currency: int,
        sell_price_trader_chaos: int,
    ) -> None:
        self.name = name
        self.buy_price_own_chaos = buy_price_own_chaos
        self.buy_price_trader_currency = buy_price_trader_currency
        self.sell_price_own_currency = sell_price_own_currency
        self.sell_price_trader_chaos = sell_price_trader_chaos

    def get_buy_note(self, exchange_name: str):
        return f"~price {self.buy_price_trader_currency}/{self.buy_price_own_chaos} {exchange_name}"

    def get_sell_note(self):
        return f"~price {self.sell_price_trader_chaos}/{self.sell_price_own_currency} chaos"


class PriceCalculator:
    def __init__(
        self,
    ) -> None:
        currency_json = requests.get(
            f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE_NAME}&type=Currency&language=en"
        ).json()

        self.currency_config = {}

        for line in currency_json["lines"]:
            try:
                receive_fraction_approximation = (
                    get_fractional_representation_under_limit(
                        float(line["receive"]["value"])
                    )
                )
                pay_fraction_approximation = get_fractional_representation_under_limit(
                    float(line["pay"]["value"])
                )

                self.currency_config[line["currencyTypeName"]] = CurrencyPrice(
                    line["currencyTypeName"],
                    receive_fraction_approximation[0],
                    receive_fraction_approximation[1],
                    pay_fraction_approximation[0],
                    pay_fraction_approximation[1],
                )
            except:
                pass

    def get_buy_note(self, currency_name: str, exchange_name: str):
        return self.currency_config[currency_name].get_buy_note(exchange_name)

    def get_sell_note(self, currency_name: str):
        return self.currency_config[currency_name].get_sell_note()
