from typing import List
from src.config.stash_tabs.StashTab import StashTab
from src.utils.exceptions.CurrencyInactive import CurrencyInactive
from src.utils.exceptions.CurrencyNotImplemented import CurrencyNotImplemented
from src.utils.translate_coords import translate_coords


class CurrencyStashTab(StashTab):
    def __init__(
        self,
        active_currencies: List[str],
    ) -> None:
        super().__init__("sell", active_currencies)

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
