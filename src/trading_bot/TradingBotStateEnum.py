from enum import Enum


class TradingBotStateEnum(Enum):
    READY = 1
    WAITING_FOR_TRADER = 2
    TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE = 3
    WAITING_FOR_TRADE_WINDOW = 4
    TRADER_HAS_LEFT = 5
