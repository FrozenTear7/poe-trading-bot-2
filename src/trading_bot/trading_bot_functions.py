import json
from typing import Literal
import pyautogui
from config.constants import PLAYER_JOINED_AREA_TRADE_WAIT_TIME
from config.coordinates import STASH_PLACE
from config.user_setup import STASH_TABS
from src.trading_bot.TradeRequest import TradeRequest
from src.trading_bot.TradingBotState import TradingBotState
from src.trading_bot.TradingBotStateEnum import TradingBotStateEnum
from src.trading_bot.chat_commands import (
    type_afk_off,
    type_invite_trader,
    type_leave_party,
    type_trade_with_trader,
)
from utils.get_currency_placement import get_currency_placement
from utils.item_info import get_currency_stack_info
from utils.nextFreeEquipmentCellCoords import nextFreeEquipmentCellCoords

from utils.printtime import printtime
from threading import Lock


def reset_stash_tabs():
    for _ in range(len(STASH_TABS)):
        pyautogui.press("LEFT")


def move_to_stash_tab(target_tab_index: int):
    for _ in range(target_tab_index):
        pyautogui.press("RIGHT")


def open_stash_to_tab(target_tab_index: int):
    pyautogui.moveTo(STASH_PLACE)
    pyautogui.click()
    reset_stash_tabs()
    move_to_stash_tab(target_tab_index)


def exit_window():
    pyautogui.press("ESC")


def take_currency(
    currency_amount: int, currency_name: str, mode: Literal["sell", "buy"]
):
    stash_index, sub_tab_placement, currency_placement = get_currency_placement(
        currency_name, mode
    )

    printtime(f"Opening the stash to tab nr: {stash_index}")
    open_stash_to_tab(stash_index)
    pyautogui.sleep(2)

    # TODO: Handle sub tab
    if sub_tab_placement is not None:
        printtime("Opening the sub tab")
        pyautogui.moveTo(sub_tab_placement)
        pyautogui.click()

    pyautogui.moveTo(currency_placement)
    currency_stack_size = get_currency_stack_info()[1]

    currency_taken = 0
    slots_taken = 0
    while currency_taken < currency_amount:
        if currency_amount - currency_taken < currency_stack_size:
            currency_amount_to_take = currency_amount % currency_stack_size
            printtime(
                f"Taking {currency_amount_to_take} {currency_name} out of {currency_amount} required, currently taken: {currency_taken}"
            )

            pyautogui.keyDown("SHIFT")
            pyautogui.click()
            pyautogui.keyUp("SHIFT")

            for _ in range(currency_amount_to_take - 1):
                pyautogui.press("RIGHT")

            pyautogui.press("ENTER")

            pyautogui.moveTo(nextFreeEquipmentCellCoords(slots_taken))
            pyautogui.click()

            currency_taken += currency_amount_to_take
        else:
            printtime(
                f"Taking {currency_stack_size} {currency_name} out of {currency_amount} required, currently taken: {currency_taken}"
            )

            pyautogui.keyDown("CTRL")
            pyautogui.click()
            pyautogui.keyUp("CTRL")

            currency_taken += currency_stack_size

        slots_taken += 1

    printtime("Closing the stash")
    exit_window()


# Callbacks


def afk_off_callback(lock: Lock, trading_bot_state: TradingBotState, body: str):
    lock.acquire()

    if trading_bot_state.state == TradingBotStateEnum.READY:
        type_afk_off()
        pyautogui.sleep(3)

    lock.release()


def incoming_trade_request_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    serialized_trade_request_json: str,
):
    lock.acquire()

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
            f"Handling trade request from: {incoming_trade_request.trader_nickname}, your {incoming_trade_request.own_currency_amount} {incoming_trade_request.own_currency_name} for their {incoming_trade_request.trader_currency_amount} {incoming_trade_request.trader_currency_name}"
        )

        type_invite_trader(incoming_trade_request.trader_nickname)

        # TODO: Prepare currency from stash
        take_currency(
            incoming_trade_request.own_currency_amount,
            incoming_trade_request.own_currency_name,
            incoming_trade_request.mode,
        )

        trading_bot_state.state = TradingBotStateEnum.WAITING_FOR_TRADER

    lock.release()


def player_has_joined_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    trader_nickname: str,
):
    lock.acquire()

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

        # TODO: Thread with a function that checks if the window has appeared
    else:
        lock.release()


def player_has_left_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    trader_nickname: str,
):
    lock.acquire()

    if (
        trading_bot_state.state
        == TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        and trader_nickname == trading_bot_state.ongoing_trade_request.trader_nickname
    ):
        type_leave_party()

        # TODO: Move the currency back to the stash
        # pyautogui.sleep(3)

        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()
