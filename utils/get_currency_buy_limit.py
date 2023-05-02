from typing import Literal, cast
from config.stash_tabs.StashTab import StashTab
from config.user_setup import STASH_TABS
from utils.exceptions.CurrencyInvalidConfig import CurrencyInvalidConfig


def get_currency_buy_limit(currency_name: str):
    if currency_name == "Chaos Orb":
        return 999999999

    stash_tabs_with_given_currency = list(
        filter(
            lambda x: x.mode == "buy" and currency_name in x.currencies,
            STASH_TABS,
        )
    )
    if len(stash_tabs_with_given_currency) != 1:
        raise CurrencyInvalidConfig(currency_name, "buy")

    found_stash_tab = cast(StashTab, stash_tabs_with_given_currency[0])

    return found_stash_tab.get_buy_limit(currency_name)
