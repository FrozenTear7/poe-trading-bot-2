from threading import Thread
from config.constants import RABBITMQ_CONFIG
from src.trading_bot.chat_commands import type_afk_off
import pyautogui


class TradingBot:
    def __init__(self, channel) -> None:
        self.channel = channel

    def on_afk_mode_callback(self, ch, method, properties, body):
        print("giga")
        pyautogui.sleep(5)
        # type_afk_off()

    def run(self):
        thread = Thread(
            target=self.channel.basic_consume(
                queue=RABBITMQ_CONFIG["queue"],
                on_message_callback=self.on_afk_mode_callback,
                auto_ack=True,
            ),
        )
        thread.start()
        # self.channel.basic_consume(
        #     queue=RABBITMQ_CONFIG["queue"],
        #     on_message_callback=lambda ch, method, properties, body: self.queue_callback_wrapper(
        #         self.on_afk_mode_callback, ch, method, properties, body
        #     ),
        #     auto_ack=True,
        # )

        self.channel.start_consuming()
