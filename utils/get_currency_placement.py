from typing import Literal, cast
from config.stash_tabs.StashTab import StashTab
from config.user_setup import STASH_TABS
from utils.exceptions.CurrencyInvalidConfig import CurrencyInvalidConfig


def get_currency_placement(currency_name: str, mode: Literal["sell", "buy"]):
    stash_tabs_with_given_currency = list(
        filter(
            lambda x: x.mode == mode and currency_name in x.active_currencies,
            STASH_TABS,
        )
    )
    if len(stash_tabs_with_given_currency) != 1:
        raise CurrencyInvalidConfig(currency_name, mode)

    found_stash_tab = cast(StashTab, stash_tabs_with_given_currency[0])

    stash_index = STASH_TABS.index(found_stash_tab)
    sub_tab_placement = found_stash_tab.get_sub_tab_coords(currency_name)
    currency_placement = found_stash_tab.get_currency_coords(currency_name)
    exchange_name = found_stash_tab.get_exchange_name(currency_name)

    return [stash_index, sub_tab_placement, currency_placement, exchange_name]
