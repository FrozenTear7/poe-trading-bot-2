from typing import Literal, Tuple
from src.config.coordinates import CELL_SIZE
from src.config.stash_tabs.StashTab import StashTab
from src.utils.translate_coords import translate_coords


GENERIC_TAB_OFFSET = translate_coords(0.152, 0.152)


class GenericStashTab(StashTab):
    def __init__(
        self, mode: Literal["sell", "buy"], active_currencies: Tuple[str, int, int]
    ) -> None:
        super().__init__(mode, list(map(lambda x: x[0], active_currencies)))
        self.active_currency_placements = {}

        for active_currency in active_currencies:
            self.active_currency_placements[active_currency[0]] = (
                active_currency[1],
                active_currency[2],
            )

    def get_sub_tab_coords(self, currency_name: str):
        return None

    def get_currency_coords(self, currency_name: str):
        (row, col) = self.active_currency_placements[currency_name]

        return (
            GENERIC_TAB_OFFSET[0] + (CELL_SIZE[0]) * row,
            GENERIC_TAB_OFFSET[1] + (CELL_SIZE[1]) * col,
        )
