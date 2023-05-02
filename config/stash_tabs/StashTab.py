from typing import List, Literal, Tuple


class StashTab:
    def __init__(
        self,
        mode: Literal["sell", "buy"],
        currencies: List[str],
        active_currencies: List[str],
    ) -> None:
        self.mode = mode
        self.currencies = currencies
        self.active_currencies = active_currencies

    def get_sub_tab_coords(self, currency_name: str) -> Tuple[int, int]:
        ...

    def get_currency_coords(self, currency_name: str) -> Tuple[int, int]:
        ...

    def get_exchange_name(self, currency_name: str) -> str:
        ...

    def is_currency_active(self, currency_name: str) -> bool:
        ...

    def get_buy_limit(self, currency_name: str) -> int:
        ...
