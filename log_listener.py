from config.constants import (
    RABBITMQ_EXCHANGE_NAME,
    RABBITMQ_KILL_ALL_TRADING_BOT_THREADS,
    RABBITMQ_ROUTING_AFK_MODE,
    RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
    RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
    RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
    RABBITMQ_ROUTING_TRADE_ACCEPTED,
    RABBITMQ_ROUTING_TRADE_CANCELLED,
)
from src.log_listener.LogListener import LogListener
from utils.printtime import printtime
import pika


if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", heartbeat=0)
        # pika.ConnectionParameters("localhost", heartbeat=None)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE_NAME, exchange_type="direct")

    try:
        printtime("Starting the Log Listener")
        log_listener = LogListener(channel)
        log_listener.listen()
    except KeyboardInterrupt:
        printtime("Stopping the Log Listener")
    except Exception as e:
        printtime("Encountered an exception:")
        print(e)
    finally:
        printtime("Killing all Trading bot threads")

        # Kill all Trading bot threads before closing
        trading_bot_routings_to_close = [
            RABBITMQ_ROUTING_AFK_MODE,
            RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
            RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
            RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
            RABBITMQ_ROUTING_TRADE_ACCEPTED,
            RABBITMQ_ROUTING_TRADE_CANCELLED,
        ]

        for trading_bot_route in trading_bot_routings_to_close:
            channel.basic_publish(
                exchange=RABBITMQ_EXCHANGE_NAME,
                routing_key=trading_bot_route,
                body=RABBITMQ_KILL_ALL_TRADING_BOT_THREADS,
            )

        connection.close()
