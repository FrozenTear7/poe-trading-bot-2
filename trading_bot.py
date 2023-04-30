from config.constants import (
    RABBITMQ_ROUTING_AFK_MODE,
    RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
    RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
    RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
)
from src.trading_bot.chat_commands import type_clear_ignore_list
from src.trading_bot.trading_bot_functions import (
    afk_off_callback,
    incoming_trade_request_callback,
    player_has_joined_the_area_callback,
    player_has_left_the_area_callback,
)
from utils.printtime import printtime
from src.trading_bot.TradingBotConsumer import TradingBotConsumer


if __name__ == "__main__":
    try:
        printtime("Starting the Trading bot")

        printtime("Clearing the ignore list")
        type_clear_ignore_list()

        printtime("Starting the consumer threads")
        afk_mode_consumer = TradingBotConsumer(
            RABBITMQ_ROUTING_AFK_MODE, afk_off_callback
        ).start()
        incoming_trade_request_consumer = TradingBotConsumer(
            RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST, incoming_trade_request_callback
        ).start()
        player_has_joined_the_area_consumer = TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
            player_has_joined_the_area_callback,
        ).start()
        player_has_left_the_area_consumer = TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA, player_has_left_the_area_callback
        ).start()

    except KeyboardInterrupt:
        printtime("Stopping the Trading bot")
    except Exception as e:
        printtime("Encountered an exception:")
        print(e)
