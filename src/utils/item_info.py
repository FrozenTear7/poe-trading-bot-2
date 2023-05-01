import re
from typing import Tuple
import pyautogui
import pyperclip

from src.config.regexes import ITEM_INFO_SECTION_DIVIDER, STACKS_SIZE_REGEX
from src.utils.exceptions.CurrencyWrongCursorPlacement import (
    CurrencyWrongCursorPlacement,
)


def get_currency_stack_info() -> Tuple[int, int]:
    pyperclip.copy("")
    pyautogui.hotkey("CTRL", "C")

    currency_info = pyperclip.paste()

    try:
        stack_info_match = re.match(
            STACKS_SIZE_REGEX, currency_info.split(ITEM_INFO_SECTION_DIVIDER)[1]
        )

        return (int(stack_info_match.group(1)), int(stack_info_match.group(2)))
    except Exception:
        raise CurrencyWrongCursorPlacement()
