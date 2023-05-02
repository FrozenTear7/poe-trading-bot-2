from trading_bot.TradingBotStateEnum import TradingBotStateEnum


class TradingBotState:
    def __init__(self) -> None:
        self.state = TradingBotStateEnum.READY
        self.ongoing_trade_request = None
