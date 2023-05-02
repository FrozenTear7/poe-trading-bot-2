from typing import List, Tuple
from config.stash_tabs.StashTab import StashTab
from utils.exceptions.CurrencyInactive import CurrencyInactive
from utils.exceptions.CurrencyNotImplemented import CurrencyNotImplemented
from utils.translate_coords import translate_coords


class CurrencyStashTab(StashTab):
    def __init__(
        self,
        active_currencies: List[Tuple[str, str]],
    ) -> None:
        super().__init__("sell", list(map(lambda x: x[0], active_currencies)))
        self.active_currency_exchange_names = {}

        for active_currency in active_currencies:
            self.active_currency_exchange_names[active_currency[0]] = active_currency[1]

    def get_sub_tab_coords(self, currency_name: str):
        if not currency_name in self.active_currencies:
            raise CurrencyInactive(currency_name, self.mode)

        if currency_name in ["Exalted Orb", "Orb of Alchemy"]:
            return translate_coords(0.127, 0.135)
        elif currency_name in ["Warlord's Exalted Orb"]:
            return translate_coords(0.213, 0.135)

        raise CurrencyNotImplemented(currency_name)

    def get_currency_coords(self, currency_name: str):
        if not currency_name in self.active_currencies:
            raise CurrencyInactive(currency_name, self.mode)

        if currency_name == "Exalted Orb":
            return translate_coords(0.158, 0.252)
        elif currency_name == "Orb of Alchemy":
            return translate_coords(0.257, 0.251)
        # TODO: Add other currencies

        raise CurrencyNotImplemented(currency_name)

    def get_exchange_name(self, currency_name: str):
        return self.active_currency_exchange_names[currency_name]
