import re
from config.regexes import (
    AFK_MODE_ON_REGEX,
    CHAT_MESSAGE_REGEX,
    NOT_A_PARTY_MEMBER_REGEX,
    PLAYER_HAS_JOINED_THE_AREA_REGEX,
    PLAYER_HAS_LEFT_THE_AREA_REGEX,
    TRADE_ACCEPTED_REGEX,
    TRADE_CANCELLED_REGEX,
    TRADE_REQUEST_REGEX,
)
from config.constants import (
    RABBITMQ_EXCHANGE_NAME,
    RABBITMQ_ROUTING_AFK_MODE,
    RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
    RABBITMQ_ROUTING_NOT_IN_A_PARTY,
    RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
    RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
    RABBITMQ_ROUTING_TRADE_ACCEPTED,
    RABBITMQ_ROUTING_TRADE_CANCELLED,
)
import pyautogui
from config.user_setup import LOG_FILE_LOCATION
from trading_bot.TradeRequest import TradeRequest

from utils.printtime import printtime


class LogListener:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.traders_inside_hideout = []
        self.log_file = open(LOG_FILE_LOCATION, "r", encoding="utf8")
        # calling readlines() at the start sets the cursor at the end of the file, listening for new changes
        self.log_file.readlines()

    def is_afk_mode_on(self, message: str):
        return re.match(AFK_MODE_ON_REGEX, message) is not None

    def has_incoming_trade_request(self, message: str):
        incoming_trade_request_match = re.match(TRADE_REQUEST_REGEX, message)
        # TODO: Check if offered values match the current price we want
        return (
            TradeRequest(
                incoming_trade_request_match.group(2),
                incoming_trade_request_match.group(3),
                incoming_trade_request_match.group(4),
                incoming_trade_request_match.group(5),
                incoming_trade_request_match.group(6),
            )
            if incoming_trade_request_match is not None
            else None
        )

    def has_player_joined_the_area(self, message: str):
        player_has_joined_the_area_match = re.match(
            PLAYER_HAS_JOINED_THE_AREA_REGEX, message
        )
        return (
            player_has_joined_the_area_match.group(1)
            if player_has_joined_the_area_match is not None
            else None
        )

    def has_player_left_the_area(self, message: str):
        player_has_left_the_area_match = re.match(
            PLAYER_HAS_LEFT_THE_AREA_REGEX, message
        )
        return (
            player_has_left_the_area_match.group(1)
            if player_has_left_the_area_match is not None
            else None
        )

    def not_a_party_member(self, message: str):
        return re.match(NOT_A_PARTY_MEMBER_REGEX, message) is not None

    def has_trade_been_accepted(self, message: str):
        return re.match(TRADE_ACCEPTED_REGEX, message) is not None

    def has_trade_been_cancelled(self, message: str):
        return re.match(TRADE_CANCELLED_REGEX, message) is not None

    def listen(self):
        while True:
            pyautogui.sleep(1)

            for line in self.log_file.readlines():
                matched_chat_message_regex = re.match(CHAT_MESSAGE_REGEX, line)

                if matched_chat_message_regex is not None:
                    chat_message = matched_chat_message_regex.group(1)

                    is_afk_mode_on = self.is_afk_mode_on(chat_message)
                    if is_afk_mode_on:
                        printtime("Entered AFK mode")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_AFK_MODE,
                            body="",
                        )
                        continue

                    incoming_trade_request = self.has_incoming_trade_request(
                        chat_message
                    )
                    # Ignore traders that have not left your hideout as we listen for "joined the area" chat message, that would not occur if they whispered you without leaving
                    if (
                        incoming_trade_request is not None
                        and incoming_trade_request.trader_nickname
                        not in self.traders_inside_hideout
                    ):
                        printtime(
                            f"Incoming trade request from: {incoming_trade_request.trader_nickname}, your {incoming_trade_request.own_currency_amount} {incoming_trade_request.own_currency_name} for their {incoming_trade_request.trader_currency_amount} {incoming_trade_request.trader_currency_name}"
                        )
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_INCOMING_TRADE_REQUEST,
                            body=incoming_trade_request.serialize(),
                        )
                        continue

                    player_who_joined_the_area_nickname = (
                        self.has_player_joined_the_area(chat_message)
                    )
                    if player_who_joined_the_area_nickname is not None:
                        printtime(
                            f"Player: {player_who_joined_the_area_nickname}, has joined the area"
                        )
                        self.traders_inside_hideout.append(
                            player_who_joined_the_area_nickname
                        )
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_PLAYER_HAS_JOINED_THE_AREA,
                            body=str(player_who_joined_the_area_nickname),
                        )
                        continue

                    player_who_left_the_area_nickname = self.has_player_left_the_area(
                        chat_message
                    )
                    if player_who_left_the_area_nickname is not None:
                        printtime(
                            f"Player: {player_who_left_the_area_nickname}, has left the area"
                        )
                        if (
                            player_who_left_the_area_nickname
                            in self.traders_inside_hideout
                        ):
                            self.traders_inside_hideout.remove(
                                player_who_left_the_area_nickname
                            )
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_PLAYER_HAS_LEFT_THE_AREA,
                            body=str(player_who_left_the_area_nickname),
                        )
                        continue

                    not_a_party_member = self.not_a_party_member(chat_message)
                    if not_a_party_member:
                        printtime("Trader already left the party")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_NOT_IN_A_PARTY,
                            body="",
                        )
                        continue

                    has_trade_been_accepted = self.has_trade_been_accepted(chat_message)
                    if has_trade_been_accepted:
                        printtime("Trade accepted")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_TRADE_ACCEPTED,
                            body="",
                        )
                        continue

                    if self.has_trade_been_cancelled(chat_message):
                        printtime("Trade cancelled")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_EXCHANGE_NAME,
                            routing_key=RABBITMQ_ROUTING_TRADE_CANCELLED,
                            body="",
                        )
                        continue
