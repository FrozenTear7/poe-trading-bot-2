import pyautogui
from config.constants import RABBITMQ_CONFIG
from src.TradingBot import TradingBot
from src.TradingBotConsumer import TradingBotConsumer
from src.trading_bot.chat_commands import type_afk_off, type_clear_ignore_list
from utils.printtime import printtime
import pika


if __name__ == "__main__":
    try:
        printtime("Starting the Trading bot")

        printtime("Clearing the ignore list")
        type_clear_ignore_list()

        printtime("Starting the consumer threads")

        afk_mode_consumer = TradingBotConsumer(
            RABBITMQ_CONFIG["routing_keys"]["afk_mode"], lambda _body: type_afk_off()
        ).start()
        gigatest_consumer = TradingBotConsumer(
            RABBITMQ_CONFIG["routing_keys"]["gigatest"], lambda _body: print("gigatest")
        ).start()

        printtime("Finished starting the consumer threads")
    except KeyboardInterrupt:
        printtime("Stopping the Trading bot")
    except Exception as e:
        printtime("Encountered an exception:")
        print(e)
