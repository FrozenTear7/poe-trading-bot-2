import json
from multiprocessing import Process
from typing import Literal
import pyautogui
from math import ceil
from config.constants import (
    PLAYER_JOINED_AREA_TRADE_WAIT_TIME,
    PLAYER_PARTY_INVITE_INACTIVITY_TIME,
    PLAYER_PARTY_INVITE_LOADING_WAIT_TIME,
    TRADE_RETRIES,
)
from config.coordinates import (
    EQUIPMENT_START,
    PRICE_MENU_OFFSET,
    PRICE_MENU_OFFSET_UNDER_THRESHOLD,
    PRICE_MENU_THRESHOLD,
    STASH_PLACE,
)
from config.user_setup import STASH_TABS
from trading_bot.TradeRequest import TradeRequest
from trading_bot.TradingBotState import TradingBotState
from trading_bot.TradingBotStateEnum import TradingBotStateEnum
from trading_bot.chat_commands import (
    type_afk_off,
    type_invite_trader,
    type_leave_party,
    type_trade_with_trader,
)
from utils.get_currency_buy_limit import get_currency_buy_limit
from utils.get_currency_placement import get_currency_placement
from utils.item_info import get_currency_stack_info, is_price_set
from utils.equipmentCellCoordsByIndex import equipmentCellCoordsByIndex
from utils.printtime import printtime
from trading_bot.PriceCalculator import PriceCalculator
from threading import Lock, Thread


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


def set_price(
    price_calculator: PriceCalculator,
    currency_name: str,
    mode: Literal["sell", "buy"],
    initial_set: bool,
):
    printtime(f"Settings price for {currency_name} in {mode} mode")

    (
        stash_index,
        sub_tab_placement,
        currency_placement,
        exchange_name,
    ) = get_currency_placement(currency_name, mode)

    printtime(f"Opening the stash to tab nr: {stash_index}")
    open_stash_to_tab(stash_index)

    if sub_tab_placement is not None:
        printtime("Opening the sub tab")
        pyautogui.moveTo(sub_tab_placement)
        pyautogui.click()

    pyautogui.moveTo(currency_placement)

    price_note = (
        price_calculator.get_buy_note(currency_name, exchange_name)
        if mode == "buy"
        else price_calculator.get_sell_note(currency_name)
    )

    printtime(price_note)

    if is_price_set():
        pyautogui.click(button="RIGHT")
        pyautogui.typewrite(price_note)
        pyautogui.press("ENTER")
    elif initial_set:
        pyautogui.click(button="RIGHT")

        current_cursor_position = pyautogui.position()
        if current_cursor_position[0] <= PRICE_MENU_THRESHOLD:
            pyautogui.moveRel(PRICE_MENU_OFFSET_UNDER_THRESHOLD)
        else:
            pyautogui.moveRel(PRICE_MENU_OFFSET)

        pyautogui.click()
        pyautogui.press("UP")
        pyautogui.press("UP")
        pyautogui.press("ENTER")
        pyautogui.hotkey("CTRL", "A")
        pyautogui.typewrite(price_note)
        pyautogui.press("ENTER")

    printtime("Closing the stash")
    exit_window()


def take_currency(currency_amount: int, currency_name: str):
    (
        stash_index,
        sub_tab_placement,
        currency_placement,
        exchange_name,
    ) = get_currency_placement(currency_name, "sell")

    printtime(f"Opening the stash to tab nr: {stash_index}")
    open_stash_to_tab(stash_index)

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

            pyautogui.moveTo(equipmentCellCoordsByIndex(slots_taken))
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


def return_currency(currency_amount: int, currency_name: str):
    (
        stash_index,
        sub_tab_placement,
        currency_placement,
        exchange_name,
    ) = get_currency_placement(currency_name, "sell")

    printtime(f"Opening the stash to tab nr: {stash_index}")
    open_stash_to_tab(stash_index)

    if sub_tab_placement is not None:
        printtime("Opening the sub tab")
        pyautogui.moveTo(sub_tab_placement)
        pyautogui.click()

    pyautogui.moveTo(EQUIPMENT_START)
    currency_stack_size = get_currency_stack_info()[1]

    total_cells_to_move = ceil(currency_amount / currency_stack_size)

    for i in range(total_cells_to_move):
        printtime(
            f"Moving equipment cell {i + 1} out of {total_cells_to_move} of currency: {currency_name} back to the stash"
        )

        pyautogui.keyDown("CTRL")
        pyautogui.keyDown("SHIFT")

        pyautogui.moveTo(equipmentCellCoordsByIndex(i))
        pyautogui.click()

        pyautogui.keyUp("SHIFT")
        pyautogui.keyUp("CTRL")

    pyautogui.moveTo(currency_placement)
    # TODO: Price the currency again

    printtime("Closing the stash")
    exit_window()


def kick_trader_for_inactivity(
    lock: Lock,
    trading_bot_state: TradingBotState,
):
    pyautogui.sleep(PLAYER_PARTY_INVITE_INACTIVITY_TIME)
    lock.acquire()
    if trading_bot_state.state == TradingBotStateEnum.WAITING_FOR_TRADER:
        printtime(
            f"Leaving the party after {PLAYER_PARTY_INVITE_INACTIVITY_TIME}s of waiting"
        )
        type_leave_party()
        lock.release()

        printtime(
            f"Waiting another {PLAYER_PARTY_INVITE_LOADING_WAIT_TIME}s in case the trader was loading into our hideout"
        )
        pyautogui.sleep(PLAYER_PARTY_INVITE_LOADING_WAIT_TIME)

        lock.acquire()
        if trading_bot_state.state == TradingBotStateEnum.WAITING_FOR_TRADER:
            printtime(
                f"Trader has not loaded into the hideout after {PLAYER_PARTY_INVITE_LOADING_WAIT_TIME}s, moving the currency back to the stash"
            )
            return_currency(
                trading_bot_state.ongoing_trade_request.own_currency_amount,
                trading_bot_state.ongoing_trade_request.own_currency_name,
            )
            printtime(f"Changing state to: READY")
            trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()


def get_currency_amount_in_stash(currency_name: str):
    (
        stash_index,
        sub_tab_placement,
        currency_placement,
        exchange_name,
    ) = get_currency_placement(currency_name, "sell")

    printtime(f"Opening the stash to tab nr: {stash_index}")
    open_stash_to_tab(stash_index)

    if sub_tab_placement is not None:
        printtime("Opening the sub tab")
        pyautogui.moveTo(sub_tab_placement)
        pyautogui.click()

    pyautogui.moveTo(currency_placement)
    currency_stack_info = get_currency_stack_info()

    printtime("Closing the stash")
    exit_window()

    return currency_stack_info


# Callbacks


def afk_off_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    body: str,
):
    lock.acquire()

    if trading_bot_state.state == TradingBotStateEnum.READY:
        type_afk_off()
        pyautogui.sleep(3)

    lock.release()


def incoming_trade_request_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
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

        own_currency_amount_in_stash = get_currency_amount_in_stash(
            incoming_trade_request.own_currency_name
        )[0]
        trader_currency_amount_in_stash = get_currency_amount_in_stash(
            incoming_trade_request.trader_currency_name
        )[0]
        currency_buy_limit = get_currency_buy_limit(
            incoming_trade_request.trader_currency_name
        )

        if own_currency_amount_in_stash < incoming_trade_request.own_currency_amount:
            printtime(
                f"Insufficient amount of currency: {incoming_trade_request.own_currency_name} - required: {incoming_trade_request.own_currency_amount}, in stash: {own_currency_amount_in_stash}"
            )
        elif (
            incoming_trade_request.mode == "buy"
            and trader_currency_amount_in_stash
            + incoming_trade_request.trader_currency_amount
            > currency_buy_limit
        ):
            printtime(
                f"Acquiring {incoming_trade_request.trader_currency_amount} {incoming_trade_request.trader_currency_name} would go above the set buy limit of: {currency_buy_limit}, currently in stash: {trader_currency_amount_in_stash}"
            )
        else:
            type_invite_trader(incoming_trade_request.trader_nickname)

            take_currency(
                incoming_trade_request.own_currency_amount,
                incoming_trade_request.own_currency_name,
            )

            printtime(f"Changing state to: WAITING_FOR_TRADER")
            trading_bot_state.state = TradingBotStateEnum.WAITING_FOR_TRADER

            Thread(
                target=kick_trader_for_inactivity, args=(lock, trading_bot_state)
            ).start()

    lock.release()


def player_has_joined_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    trader_nickname: str,
):
    lock.acquire()

    if (
        trading_bot_state.state == TradingBotStateEnum.WAITING_FOR_TRADER
        and trader_nickname == trading_bot_state.ongoing_trade_request.trader_nickname
    ):
        printtime(f"Changing state to: TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE")
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

            printtime(f"Changing state to: WAITING_FOR_TRADE_WINDOW")
            trading_bot_state.state = TradingBotStateEnum.WAITING_FOR_TRADE_WINDOW

        lock.release()

        # TODO: Thread with a function that checks if the window has appeared
    else:
        lock.release()


def player_has_left_the_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    trader_nickname: str,
):
    lock.acquire()

    if (
        trading_bot_state.state
        == TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        and trader_nickname == trading_bot_state.ongoing_trade_request.trader_nickname
    ):
        printtime(
            f"Trader left the party during the before trade wait period, leave the party and moving the currency back to the stash"
        )

        type_leave_party()

        return_currency(
            trading_bot_state.ongoing_trade_request.own_currency_amount,
            trading_bot_state.ongoing_trade_request.own_currency_name,
        )

        printtime(f"Changing state to: READY")
        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()


def not_in_the_party_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    trader_nickname: str,
):
    lock.acquire()

    if trading_bot_state.state == TradingBotStateEnum.WAITING_FOR_TRADER:
        printtime(
            f"Trader has already left the party, moving the currency back to the stash"
        )
        return_currency(
            trading_bot_state.ongoing_trade_request.own_currency_amount,
            trading_bot_state.ongoing_trade_request.own_currency_name,
        )
        printtime(f"Changing state to: READY")
        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()


def trade_accepted_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    trader_nickname: str,
):
    lock.acquire()

    printtime(f"Trade succeeded, moving the currency to the stash")

    return_currency(
        trading_bot_state.ongoing_trade_request.trader_currency_amount,
        trading_bot_state.ongoing_trade_request.trader_currency_name,
    )

    printtime(f"Changing state to: READY")
    trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()


def trade_cancelled_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    trader_nickname: str,
):
    lock.acquire()

    if trading_bot_state.ongoing_trade_request.trade_retries != TRADE_RETRIES:
        trading_bot_state.ongoing_trade_request.trade_retries += 1
    else:
        printtime(
            f"Trade cancelled, leaving the party and moving the currency to the stash"
        )

        type_leave_party()

        return_currency(
            trading_bot_state.ongoing_trade_request.own_currency_amount,
            trading_bot_state.ongoing_trade_request.own_currency_name,
        )

        printtime(f"Changing state to: READY")
        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()
