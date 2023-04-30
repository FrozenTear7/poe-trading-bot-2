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
    consumer_threads = []

    printtime("Starting the Trading bot")

    printtime("Clearing the ignore list")
    # type_clear_ignore_list()

    printtime("Starting the consumer threads")

    consumer_threads.append(
        TradingBotConsumer(RABBITMQ_ROUTING_AFK_MODE, afk_off_callback)
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST, incoming_trade_request_callback
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
            player_has_joined_the_area_callback,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
            player_has_left_the_area_callback,
        )
    )

    for consumer_thread in consumer_threads:
        consumer_thread.start()

    for consumer_thread in consumer_threads:
        consumer_thread.join()
