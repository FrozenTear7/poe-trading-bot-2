import pyautogui
from src.config.user_setup import OWN_NICKNAME

from src.utils.printtime import printtime


def type_logout():
    pyautogui.press("ENTER")
    pyautogui.typewrite("/exit")
    pyautogui.press("ENTER")


def type_chat_message(message: str):
    pyautogui.press("ENTER")
    pyautogui.typewrite(message)
    pyautogui.press("ENTER")


def type_afk_off():
    printtime("/afkoff")
    type_chat_message("/afkoff")


def type_clear_ignore_list():
    printtime("/clear_ignore_list")
    type_chat_message("/clear_ignore_list")


def type_invite_trader(trader_nickname: str):
    printtime(f"/invite {trader_nickname}")
    type_chat_message(f"/invite {trader_nickname}")


def type_trade_with_trader(trader_nickname: str):
    printtime(f"/tradewith {trader_nickname}")
    type_chat_message(f"/tradewith {trader_nickname}")


def type_leave_party():
    printtime(f"/kick {OWN_NICKNAME}")
    type_chat_message(f"/kick {OWN_NICKNAME}")
