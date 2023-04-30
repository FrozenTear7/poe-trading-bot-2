import json
from threading import Lock
from typing import TypedDict, Unpack, cast

import pyautogui
from config.constants import PLAYER_JOINED_AREA_TRADE_WAIT_TIME
from src.trading_bot.TradeRequest import TradeRequest
from src.trading_bot.TradingBotState import TradingBotState
from src.trading_bot.TradingBotStateEnum import TradingBotStateEnum
from src.trading_bot.chat_commands import (
    type_afk_off,
    type_invite_trader,
    type_leave_party,
    type_trade_with_trader,
)
from utils.printtime import printtime


class CallbackKwargs(TypedDict):
    body: str


def afk_off_callback(lock: Lock, trading_bot_state: TradingBotState):
    lock.acquire()

    if trading_bot_state.state == TradingBotStateEnum.READY:
        type_afk_off()
        pyautogui.sleep(3)

    lock.release()


def incoming_trade_request_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    **kwargs: Unpack[CallbackKwargs],
):
    lock.acquire()

    serialized_trade_request_json = kwargs["body"]

    if trading_bot_state.state == TradingBotStateEnum.READY:
        json_body = json.loads(serialized_trade_request_json)
        incoming_trade_request = TradeRequest(
            json_body["trader_nickname"],
            json_body["own_currency_amount"],
            json_body["own_currency_name"],
            json_body["trader_currency_amount"],
            json_body["trader_currency_name"],
        )
        trading_bot_state.ongoing_trade_request = incoming_trade_request
        printtime(
            f"Handling trade request from: {incoming_trade_request.trader_nickname}, your {incoming_trade_request.own_currency_amount} of {incoming_trade_request.own_currency_name} for their {incoming_trade_request.trader_currency_amount} of {incoming_trade_request.trader_currency_name}"
        )

        type_invite_trader(incoming_trade_request.trader_nickname)

        # TODO: Prepare currency from stash
        # pyautogui.sleep(3)

        trading_bot_state.state = TradingBotStateEnum.WAITING_FOR_TRADER

    lock.release()


def player_has_joined_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    **kwargs: Unpack[CallbackKwargs],
):
    lock.acquire()

    trader_nickname = kwargs["body"]

    if (
        trading_bot_state.state == TradingBotStateEnum.WAITING_FOR_TRADER
        and trader_nickname == trading_bot_state.ongoing_trade_request.trader_nickname
    ):
        trading_bot_state.state = (
            TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        )
        lock.release()

        pyautogui.sleep(PLAYER_JOINED_AREA_TRADE_WAIT_TIME)

        # Start the trade if the player hasn't left during the wait time
        lock.acquire()
        if (
            trading_bot_state.state
            == TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        ):
            type_trade_with_trader(trader_nickname)

            trading_bot_state.state = TradingBotStateEnum.WAITING_FOR_TRADE_WINDOW

        lock.release()

        # TODO: Thread with a function that checks if the windows has appeared
    else:
        lock.release()


def player_has_left_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    **kwargs: Unpack[CallbackKwargs],
):
    lock.acquire()

    trader_nickname = kwargs["body"]

    if (
        trading_bot_state.state
        == TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        and trader_nickname == trading_bot_state.ongoing_trade_request.trader_nickname
    ):
        type_leave_party()
        trading_bot_state.state = TradingBotStateEnum.TRADER_HAS_LEFT
        lock.release()

        # TODO: Move the currency back to the stash
        # pyautogui.sleep(3)

        lock.acquire()
        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()
