import threading

import pika
from config.constants import RABBITMQ_EXCHANGE_NAME
from src.trading_bot.TradingBotState import TradingBotState


class TradingBotConsumer(threading.Thread):
    initialized = False

    def __init__(self, routing_key: str, trading_bot_action, *args, **kwargs):
        super(TradingBotConsumer, self).__init__(*args, **kwargs)
        self.routing_key = routing_key
        self.trading_bot_action = trading_bot_action
        TradingBotConsumer._initialize()

    @classmethod
    def _initialize(cls):
        if not cls.initialized:
            cls.busy = False
            cls.trading_bot_state = TradingBotState()
            cls.lock = threading.Lock()
            cls.initialized = True

    @classmethod
    def callback(cls, trading_bot_action, body: str):
        trading_bot_action(
            cls.lock,
            cls.trading_bot_state,
            body=body,
        )

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost", heartbeat=100)
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=RABBITMQ_EXCHANGE_NAME, exchange_type="direct"
        )

        result = channel.queue_declare(queue="", exclusive=True)

        channel.queue_bind(
            result.method.queue,
            exchange=RABBITMQ_EXCHANGE_NAME,
            routing_key=self.routing_key,
        )

        channel.basic_consume(
            queue=result.method.queue,
            on_message_callback=lambda channel, method, properties, body: TradingBotConsumer.callback(
                self.trading_bot_action, str(body, "utf-8")
            ),
            auto_ack=True,
        )
        channel.start_consuming()
