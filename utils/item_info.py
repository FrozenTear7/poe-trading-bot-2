import re
from typing import Tuple
import pyautogui
import pyperclip

from config.regexes import (
    INNER_SECTION_DIVIDER,
    ITEM_INFO_SECTION_DIVIDER,
    PRICE_SET_REGEX,
    STACK_SIZE_REGEX,
)
from utils.exceptions.CurrencyWrongCursorPlacement import (
    CurrencyWrongCursorPlacement,
)


def get_currency_stack_info() -> Tuple[int, int]:
    pyperclip.copy("")
    pyautogui.hotkey("CTRL", "C")

    currency_info = pyperclip.paste()

    try:
        stack_info_match = re.match(
            STACK_SIZE_REGEX, currency_info.split(ITEM_INFO_SECTION_DIVIDER)[1]
        )

        return (int(stack_info_match.group(1)), int(stack_info_match.group(2)))
    except:
        raise CurrencyWrongCursorPlacement()


def is_price_set() -> bool:
    pyperclip.copy("")
    pyautogui.hotkey("CTRL", "C")

    currency_info = pyperclip.paste()

    try:
        stack_info_match = re.match(
            PRICE_SET_REGEX, currency_info.split(ITEM_INFO_SECTION_DIVIDER)[4]
        )

        return stack_info_match is not None
    except:
        return False


def item_under_cursor_exists() -> bool:
    pyperclip.copy("")
    pyautogui.hotkey("CTRL", "C")
    return pyperclip.paste() != ""


def get_trade_window_item_info() -> Tuple[str, int]:
    pyperclip.copy("")
    pyautogui.hotkey("CTRL", "C")

    currency_info = pyperclip.paste()

    try:
        item_name = currency_info.split(ITEM_INFO_SECTION_DIVIDER)[0].split(
            INNER_SECTION_DIVIDER
        )[2]
        stack_info_match = re.match(
            STACK_SIZE_REGEX, currency_info.split(ITEM_INFO_SECTION_DIVIDER)[1]
        )

        return (item_name, int(stack_info_match.group(1)))
    except:
        return None
