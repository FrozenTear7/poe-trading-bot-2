# poe-trading-bot-2
This is the new version of my Path of Exile trading bot. Rewritten with RabbitMQ queue exchange and 3 different paralelly running scripts.

## Requirements
Written in Python 3.11 - lower version would work fine, but I'm using hints for better typings control - lower version would require polyfills with libraries if you'd like go this way.
RabbitMQ local installation is also required - read more [here](https://www.rabbitmq.com/download.html).

## How to run the bot
The full setup requires you to run 3 scripts simultaneously:
- `python log_listener.py` will start the brain of the operation, this script checks for new chat messages and sends messages to the Trading Bot containing new events that are occuring
- TODO: Price calculator
- `python trading_bot.py` interacts with the game interface, this script launches threads for each possible message type from the Log listener and Price calculator and acts accordingly, based on the current state of the events (invites the user if not currently trading, awaits the trader's arrival, etc.)

TODO: constants instructions
