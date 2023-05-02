from enum import Enum


class TradingBotStateEnum(Enum):
    SETTING_PRICES = 1
    READY = 2
    WAITING_FOR_TRADER = 3
    TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE = 4
    WAITING_FOR_TRADE_WINDOW = 5
