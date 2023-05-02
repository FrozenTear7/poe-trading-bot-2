from typing import Union
from trading_bot.TradeRequest import TradeRequest
from trading_bot.TradingBotStateEnum import TradingBotStateEnum


class TradingBotState:
    def __init__(self) -> None:
        self.state = TradingBotStateEnum.READY
        self.ongoing_trade_request: Union[TradeRequest, None] = None
