from typing import List, Literal, Tuple
from config.coordinates import CELL_SIZE
from config.stash_tabs.StashTab import StashTab
from utils.translate_coords import translate_coords


GENERIC_TAB_OFFSET = translate_coords(0.022, 0.142)


class GenericStashTab(StashTab):
    def __init__(
        self,
        mode: Literal["sell", "buy"],
        active_currencies: List[Tuple[str, str, int, int]],
    ) -> None:
        super().__init__(mode, list(map(lambda x: x[0], active_currencies)))
        self.active_currency_placements = {}
        self.active_currency_exchange_names = {}

        for active_currency in active_currencies:
            self.active_currency_placements[active_currency[0]] = (
                active_currency[2],
                active_currency[3],
            )
            self.active_currency_exchange_names[active_currency[0]] = active_currency[1]

    def get_sub_tab_coords(self, currency_name: str):
        return None

    def get_currency_coords(self, currency_name: str):
        (row, col) = self.active_currency_placements[currency_name]

        return (
            GENERIC_TAB_OFFSET[0] + (CELL_SIZE[0]) * row,
            GENERIC_TAB_OFFSET[1] + (CELL_SIZE[1]) * col,
        )

    def get_exchange_name(self, currency_name: str):
        return self.active_currency_exchange_names[currency_name]
