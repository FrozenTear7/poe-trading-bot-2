import json
from multiprocessing import Process
from typing import Literal
import pyautogui
from math import ceil
from config.constants import (
    TIMEOUT_BEFORE_TRADE,
    PLAYER_PARTY_INVITE_INACTIVITY_TIME,
    PLAYER_PARTY_INVITE_LOADING_WAIT_TIME,
    TRADE_ACCEPTED_WAIT_RETRIES,
    TRADE_CELL_RETRIES,
    TRADE_RETRIES,
)
from config.coordinates import (
    EQUIPMENT_START,
    PRICE_MENU_OFFSET,
    PRICE_MENU_OFFSET_UNDER_THRESHOLD,
    PRICE_MENU_THRESHOLD,
    STASH_PLACE,
    TRADE_WINDOW_ACCEPT_BUTTON,
    TRADE_WINDOW_ACCEPT_BUTTON_COLOR,
    TRADE_WINDOW_ACCEPT_BUTTON_COLOR_TOLERANCE,
    TRADE_WINDOW_CELLS,
    TRADE_WINDOW_START,
)
from config.user_setup import STASH_TABS
from trading_bot.TradeRequest import TradeRequest
from trading_bot.TradingBotState import TradingBotState, TradingBotStateEnum
from trading_bot.chat_commands import (
    type_afk_off,
    type_invite_trader,
    type_leave_party,
    type_trade_with_trader,
)
from utils.get_currency_buy_limit import get_currency_buy_limit
from utils.get_currency_placement import get_currency_placement
from utils.item_info import (
    get_currency_stack_info,
    get_trade_window_item_info,
    is_price_set,
    item_under_cursor_exists,
)
from utils.equipment_cell_coords_by_index import (
    equipment_cell_coords_by_index,
    trade_window_cell_coords_by_index,
)
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
        else price_calculator.get_sell_note(currency_name, exchange_name)
    )

    printtime(price_note)

    if not is_price_set() or initial_set:
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

            pyautogui.moveTo(equipment_cell_coords_by_index(slots_taken))
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


def return_currency(
    price_calculator: PriceCalculator, currency_amount: int, currency_name: str
):
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

        pyautogui.moveTo(equipment_cell_coords_by_index(i))
        pyautogui.click()

        pyautogui.keyUp("SHIFT")
        pyautogui.keyUp("CTRL")

    printtime("Closing the stash")
    exit_window()

    set_price(price_calculator, currency_name, "sell", False)


def kick_trader_for_inactivity(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
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
                price_calculator,
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


def trade_process(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
):
    try:
        pyautogui.sleep(5)
        pyautogui.moveTo(equipment_cell_coords_by_index(0))

        while True:
            if trading_bot_state.state != TradingBotStateEnum.IN_TRADE:
                printtime(f"Trade cancelled, finishing the trade process")
                return
            if item_under_cursor_exists():
                break
            pyautogui.sleep(0.5)

        if trading_bot_state.state != TradingBotStateEnum.IN_TRADE:
            printtime(f"Trade cancelled, finishing the trade process")
            return
        currency_stack_size = get_currency_stack_info()[1]

        total_cells_to_move = ceil(
            trading_bot_state.ongoing_trade_request.own_currency_amount
            / currency_stack_size
        )

        for i in range(total_cells_to_move):
            if trading_bot_state.state != TradingBotStateEnum.IN_TRADE:
                printtime(f"Trade cancelled, finishing the trade process")
                return

            printtime(
                f"Moving equipment cell {i + 1} out of {total_cells_to_move} of currency: {trading_bot_state.ongoing_trade_request.own_currency_name} to the trade window"
            )

            pyautogui.keyDown("CTRL")
            pyautogui.moveTo(equipment_cell_coords_by_index(i))
            pyautogui.click()
            pyautogui.keyUp("CTRL")

        pyautogui.moveTo(TRADE_WINDOW_START)

        i = 0
        retry_counter = 0
        trade_accepted_wait_counter = 0
        ready_to_accept = False
        accepted = False
        counted_amount = 0
        while True:
            if trading_bot_state.state != TradingBotStateEnum.IN_TRADE:
                printtime(f"Trade cancelled, finishing the trade process")
                return

            if not pyautogui.pixelMatchesColor(
                TRADE_WINDOW_ACCEPT_BUTTON[0],
                TRADE_WINDOW_ACCEPT_BUTTON[1],
                TRADE_WINDOW_ACCEPT_BUTTON_COLOR,
                tolerance=TRADE_WINDOW_ACCEPT_BUTTON_COLOR_TOLERANCE,
            ):
                if ready_to_accept:
                    retry_counter += 1
                    continue
                else:
                    printtime(
                        f"Trader changed something in the already put in items, cancelling"
                    )
                    return

            if ready_to_accept:
                if not accepted:
                    pyautogui.click()
                    accepted = True
                elif trade_accepted_wait_counter < TRADE_ACCEPTED_WAIT_RETRIES:
                    pyautogui.sleep(1)
                    trade_accepted_wait_counter += 1
                else:
                    printtime(f"Trade cancelled, finishing the trade process")
                    pyautogui.press('ESC')


            if retry_counter == TRADE_CELL_RETRIES:
                printtime(f"Trade cancelled, finishing the trade process")
                i = 0
                retry_counter = 0
                counted_amount = 0

            # To avoid accidentally hovering over trade window cells that could mess up the check we go around the trade window when changing columns
            if i % TRADE_WINDOW_CELLS[0] == 0:
                current_position = pyautogui.position()
                resolution = pyautogui.size()

                # Move to the bottom
                pyautogui.moveTo(current_position[0], resolution[1])
                # Move to the left
                pyautogui.moveTo(1, current_position[1])
                # Move to the top
                pyautogui.moveTo(1, 1)
                # Move above the current col
                pyautogui.moveTo(trade_window_cell_coords_by_index(i)[0], 1)

            pyautogui.moveTo(trade_window_cell_coords_by_index(i))

            item_info = get_trade_window_item_info()

            if item_info is not None:
                printtime(f"Trade window cell: {i} contains {cell_amount} {item_name}")
                item_name, cell_amount = item_info

                if (
                    item_name
                    != trading_bot_state.ongoing_trade_request.trader_currency_name
                ):
                    pyautogui.press("ESC")
                    printtime(
                        f"Received {item_name} instead of {trading_bot_state.ongoing_trade_request.trader_currency_name}, cancelling the trade"
                    )
                    return

                counted_amount += cell_amount
                printtime(
                    f"Trader has put in {counted_amount} of {trading_bot_state.ongoing_trade_request.trader_currency_amount}"
                )
                i += 1
                retry_counter = 0

                if (
                    counted_amount
                    >= trading_bot_state.ongoing_trade_request.trader_currency_amount
                ):
                    printtime(
                        f"Trader has put in the required amount: {counted_amount} of {trading_bot_state.ongoing_trade_request.trader_currency_amount}, trying to accept the trade"
                    )
                    pyautogui.moveTo(TRADE_WINDOW_ACCEPT_BUTTON)
                    ready_to_accept = True
            else:
                printtime(f"Waiting for trade window cell: {i}")
                pyautogui.sleep(0.1)
                retry_counter += 1

    except:
        printtime(f"Exception during trade, cancelling the process")


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
                target=kick_trader_for_inactivity,
                args=(lock, trading_bot_state, price_calculator),
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

        pyautogui.sleep(TIMEOUT_BEFORE_TRADE)

        # Start the trade if the player hasn't left during the wait time
        lock.acquire()

        if (
            trading_bot_state.state
            == TradingBotStateEnum.TRADER_IN_THE_AREA_TIMEOUT_BEFORE_TRADE
        ):
            pyautogui.press("I")

            type_trade_with_trader(trader_nickname)

            printtime(f"Changing state to: IN_TRADE")
            trading_bot_state.state = TradingBotStateEnum.IN_TRADE

            Thread(
                target=trade_process,
                args=(lock, trading_bot_state, price_calculator),
            ).start()

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
            price_calculator,
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
            price_calculator,
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
    body: str,
):
    lock.acquire()

    printtime(f"Trade succeeded, moving the currency to the stash")

    return_currency(
        price_calculator,
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
    body: str,
):
    lock.acquire()

    if trading_bot_state.ongoing_trade_request.trade_retries != TRADE_RETRIES:
        printtime(
            f"Trade cancelled, retrying (currently {trading_bot_state.ongoing_trade_request.trade_retries} retries out of {TRADE_RETRIES} allowed)"
        )
        trading_bot_state.state = TradingBotStateEnum.TRADE_CANCELLED

        trading_bot_state.ongoing_trade_request.trade_retries += 1

        lock.release()

        pyautogui.sleep(TIMEOUT_BEFORE_TRADE)

        lock.acquire()
        if trading_bot_state.state == TradingBotStateEnum.TRADE_CANCELLED:
            type_trade_with_trader(
                trading_bot_state.ongoing_trade_request.trader_nickname
            )

            printtime(f"Changing state to: IN_TRADE")
            trading_bot_state.state = TradingBotStateEnum.IN_TRADE

            Thread(
                target=trade_process,
                args=(lock, trading_bot_state, price_calculator),
            ).start()
    else:
        printtime(
            f"Trade cancelled, leaving the party and moving the currency to the stash"
        )
        trading_bot_state.state = TradingBotStateEnum.TRADE_CANCELLED

        type_leave_party()

        pyautogui.press("I")

        return_currency(
            price_calculator,
            trading_bot_state.ongoing_trade_request.own_currency_amount,
            trading_bot_state.ongoing_trade_request.own_currency_name,
        )

        printtime(f"Changing state to: READY")
        trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()


def player_not_found_in_this_area_callback(
    lock: Lock,
    trading_bot_state: TradingBotState,
    price_calculator: PriceCalculator,
    body: str,
):
    lock.acquire()

    printtime(
        f"Trader left hideout during the trade, leaving the party and returning the currency back to the stash"
    )

    trading_bot_state.state = TradingBotStateEnum.PLAYER_LEFT_DURING_TRADE

    type_leave_party()

    pyautogui.press("I")

    return_currency(
        price_calculator,
        trading_bot_state.ongoing_trade_request.own_currency_amount,
        trading_bot_state.ongoing_trade_request.own_currency_name,
    )

    printtime(f"Changing state to: READY")
    trading_bot_state.state = TradingBotStateEnum.READY

    lock.release()
