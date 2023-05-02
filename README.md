# poe-trading-bot-2
This is the new version of my Path of Exile trading bot. Rewritten with RabbitMQ queue exchange and 3 different paralelly running scripts.

## Requirements
- written in Python 3.11 - lower version would work fine, but I'm using hints for better typings control - lower version would require polyfills with libraries if you'd like go this way.
- RabbitMQ local installation is also required - read more [here](https://www.rabbitmq.com/download.html).
- Tesseract local installation - read more [here](https://tesseract-ocr.github.io/tessdoc/Installation.html). Remember to set the correct path in `config/user_setup.py`

## How to run the bot
First of all run `pip install -r requirements.txt` to install all required Python libraries (I recommend creating a virtual environment for that).

The full setup requires you to run 3 scripts simultaneously:
- `python log_listener.py` will start the brain of the operation, this script checks for new chat messages and sends messages to the Trading Bot containing new events that are occuring
- `python trading_bot.py` interacts with the game interface, this script launches threads for each possible message type from the Log listener and Price calculator and acts accordingly, based on the current state of the events (invites the user if not currently trading, awaits the trader's arrival, etc.)

TODO: constants instructions

## Lifecycle of the bot

1. Trader messages us with a trade request
- we check if the provided values in the message match our current pricing
- we check if we have enough currency in stock to complete this trade
- we check if the trader is not currently in our hideout (since we are listening for "joined the area" messages we have to make sure the trader previously left our hideout)
2. When all conditions above are fulfilled we invite the trader to our hideout and take out the required currency from the stash
- if the trader hasn't joined after given amount of time we leave the party, then give the trader some more time in case we left the party, but they were loading into our hideout
- if the trader hasn't arrived after 2 periods of waiting we return to the READY state
3. If the trader has arrived we wait a moment and then send them a trade request
- if the trade has been cancelled we wait a moment and then send the trade request again
- if the second trade hasn't succeeded we leave the party, return the currency to stash and return to the READY state
- if the trade has succeeded we thank the trader, leave the party and move acquired currency to the stash

Each time we move the currency back to the stash we need to check if we have to price the item again in case we took out all the currency and update the stash state if the trade has succeded