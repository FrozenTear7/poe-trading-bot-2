import pyautogui


def type_chat_message(message):
    pyautogui.press("ENTER")
    pyautogui.typewrite(message)
    pyautogui.press("ENTER")


def type_afk_off():
    type_chat_message("/afkoff")


def type_clear_ignore_list():
    type_chat_message("/clear_ignore_list")
