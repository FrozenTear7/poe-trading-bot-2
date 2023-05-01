from typing import List, Literal


class StashTab:
    def __init__(
        self,
        mode: Literal["sell", "buy"],
        active_currencies: List[str],
    ) -> None:
        self.type = type
        self.mode = mode
        self.active_currencies = active_currencies

    def get_sub_tab_coords(self, currency_name: str):
        ...

    def get_currency_coords(self, currency_name: str):
        ...
