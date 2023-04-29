from config.constants import RABBITMQ_CONFIG
from src.log_listener.LogListener import LogListener
from utils.printtime import printtime
import pika


if __name__ == "__main__":
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=RABBITMQ_CONFIG["exchange"], exchange_type="direct"
        )

        printtime("Starting the Log Listener")
        log_listener = LogListener(channel)
        log_listener.listen()
    except KeyboardInterrupt:
        printtime("Stopping the Log Listener")
        connection.close()
    except Exception as e:
        printtime("Encountered an exception:")
        print(e)
        connection.close()
