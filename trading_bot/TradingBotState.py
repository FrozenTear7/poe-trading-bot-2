from typing import Union
from trading_bot.TradeRequest import TradeRequest
from enum import Enum


class TradingBotStateEnum(Enum):
    SETTING_PRICES = 1
    READY = 2
    WAITING_FOR_TRADER = 3
    TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE = 4
    IN_TRADE = 5
    TRADE_CANCELLED = 6
    PLAYER_LEFT_DURING_TRADE = 6


class TradingBotState:
    def __init__(self) -> None:
        self.state = TradingBotStateEnum.READY
        self.ongoing_trade_request: Union[TradeRequest, None] = None
