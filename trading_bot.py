import pytesseract
import pyautogui
from typing import List
from config.constants import (
    RABBITMQ_ROUTING_AFK_MODE,
    RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
    RABBITMQ_ROUTING_NOT_IN_A_PARTY,
    RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
    RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
    RABBITMQ_ROUTING_PLAYER_NOT_FOUND_IN_THIS_AREA,
    RABBITMQ_ROUTING_TRADE_ACCEPTED,
    RABBITMQ_ROUTING_TRADE_CANCELLED,
)
from config.user_setup import STASH_TABS, TESSERACT_PATH
from trading_bot.PriceCalculator import PriceCalculator
from trading_bot.chat_commands import type_clear_ignore_list
from trading_bot.trading_bot_functions import (
    afk_off_callback,
    incoming_trade_request_callback,
    not_in_the_party_callback,
    player_has_joined_the_area_callback,
    player_has_left_the_area_callback,
    player_not_found_in_this_area_callback,
    set_price,
    trade_accepted_callback,
    trade_cancelled_callback,
)
from utils.printtime import printtime
from trading_bot.TradingBotConsumer import TradingBotConsumer


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    consumer_threads: List[TradingBotConsumer] = []
    price_calculator = PriceCalculator()

    printtime("Starting the Trading bot")
    pyautogui.sleep(3)

    printtime("Setting prices in the stash")
    # for stash_tab in STASH_TABS:
    #     for currency in stash_tab.active_currencies:
    #         set_price(price_calculator, currency, stash_tab.mode, True)

    printtime("Clearing the ignore list")
    type_clear_ignore_list()

    printtime("Starting the consumer threads")

    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_AFK_MODE, afk_off_callback, price_calculator
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
            incoming_trade_request_callback,
            price_calculator,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
            player_has_joined_the_area_callback,
            price_calculator,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
            player_has_left_the_area_callback,
            price_calculator,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_NOT_IN_A_PARTY, not_in_the_party_callback, price_calculator
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_TRADE_ACCEPTED,
            trade_accepted_callback,
            price_calculator,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_TRADE_CANCELLED,
            trade_cancelled_callback,
            price_calculator,
        )
    )
    consumer_threads.append(
        TradingBotConsumer(
            RABBITMQ_ROUTING_PLAYER_NOT_FOUND_IN_THIS_AREA,
            player_not_found_in_this_area_callback,
            price_calculator,
        )
    )

    for consumer_thread in consumer_threads:
        consumer_thread.start()

    for consumer_thread in consumer_threads:
        consumer_thread.join()
