import threading
import pika
from config.constants import RABBITMQ_CONFIG


class TradingBotConsumer(threading.Thread):
    initialized = False

    def __init__(self, routing_key, trading_bot_action, *args, **kwargs):
        super(TradingBotConsumer, self).__init__(*args, **kwargs)
        self.routing_key = routing_key
        self.trading_bot_action = trading_bot_action
        TradingBotConsumer._initialize()

    @classmethod
    def _initialize(cls):
        if not cls.initialized:
            cls.busy = False
            cls.initialized = True
            cls.lock = threading.Lock()

    @classmethod
    def callback(cls, trading_bot_action, body):
        cls.lock.acquire()
        if not cls.busy:
            trading_bot_action(body)
            cls.lock.release()
        else:
            cls.lock.release()

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=RABBITMQ_CONFIG["exchange"], exchange_type="direct"
        )

        result = channel.queue_declare(queue="", exclusive=True)

        channel.queue_bind(
            result.method.queue,
            exchange=RABBITMQ_CONFIG["exchange"],
            routing_key=self.routing_key,
        )

        channel.basic_consume(
            queue=result.method.queue,
            on_message_callback=lambda channel, method, properties, body: TradingBotConsumer.callback(
                self.trading_bot_action, body
            ),
            auto_ack=True,
        )
        channel.start_consuming()
