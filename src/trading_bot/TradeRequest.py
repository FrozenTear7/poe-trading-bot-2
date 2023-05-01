import json


class TradeRequest:
    def __init__(
        self,
        trader_nickname: str,
        own_currency_amount: str,
        own_currency_name: str,
        trader_currency_amount: str,
        trader_currency_name: str,
    ) -> None:
        self.trader_nickname = trader_nickname
        # BUY - We are giving the trader our chaos orbs for their different currencies, which means we're buying
        # SELL - We are giving the trader our different currencies for their chaos orb, which means we're selling
        self.mode = "buy" if own_currency_name == "Chaos Orb" else "sell"
        self.own_currency_amount = int(own_currency_amount)
        self.own_currency_name = own_currency_name
        self.trader_currency_amount = int(trader_currency_amount)
        self.trader_currency_name = trader_currency_name

    def serialize(self):
        return json.dumps(
            {
                "trader_nickname": self.trader_nickname,
                "mode": self.mode,
                "own_currency_amount": self.own_currency_amount,
                "own_currency_name": self.own_currency_name,
                "trader_currency_amount": self.trader_currency_amount,
                "trader_currency_name": self.trader_currency_name,
            }
        )
