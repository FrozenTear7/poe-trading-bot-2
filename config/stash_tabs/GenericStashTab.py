from typing import List, Literal, Tuple
from config.coordinates import CELL_SIZE
from config.stash_tabs.StashTab import StashTab
from utils.translate_coords import translate_coords


GENERIC_TAB_OFFSET = translate_coords(0.022, 0.142)


class GenericStashTab(StashTab):
    def __init__(
        self,
        mode: Literal["sell", "buy"],
        currencies: List[Tuple[str, str, int, int, int]],
    ) -> None:
        super().__init__(
            mode,
            list(map(lambda x: x[0], currencies)),
            list(map(lambda x: x[0], currencies)),
        )
        self.currency_placements = {}
        self.currency_exchange_names = {}
        self.currency_limits = {}

        for currency in currencies:
            self.currency_placements[currency[0]] = (
                currency[2],
                currency[3],
            )
            self.currency_exchange_names[currency[0]] = currency[1]
            self.currency_limits[currency[0]] = currency[4]

    def get_sub_tab_coords(self, currency_name: str):
        return None

    def get_currency_coords(self, currency_name: str):
        (row, col) = self.currency_placements[currency_name]

        return (
            GENERIC_TAB_OFFSET[0] + (CELL_SIZE[0]) * row,
            GENERIC_TAB_OFFSET[1] + (CELL_SIZE[1]) * col,
        )

    def get_exchange_name(self, currency_name: str):
        return self.currency_exchange_names[currency_name]

    def is_currency_active(self, currency_name: str):
        return True

    def get_buy_limit(self, currency_name: str):
        if self.mode == "sell":
            return None
        else:
            return self.currency_limits[currency_name]
