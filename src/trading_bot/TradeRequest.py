import json


class TradeRequest:
    def __init__(
        self,
        trader_nickname,
        own_currency_amount,
        own_currency_name,
        trader_currency_amount,
        trader_currency_name,
    ):
        self.trader_nickname = trader_nickname
        self.own_currency_amount = int(own_currency_amount)
        self.own_currency_name = own_currency_name
        self.trader_currency_amount = int(trader_currency_amount)
        self.trader_currency_name = trader_currency_name

    def serialize(self):
        return json.dumps(
            {
                "trader_nickname": self.trader_nickname,
                "own_currency_amount": self.own_currency_amount,
                "own_currency_name": self.own_currency_name,
                "trader_currency_amount": self.trader_currency_amount,
                "trader_currency_name": self.trader_currency_name,
            }
        )
