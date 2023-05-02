from typing import Literal, Tuple

import pyautogui


def translate_coord(offset_percentage: float, direction: Literal[0, 1]):
    # X - 0, Y - 1
    return int(pyautogui.size()[direction] * offset_percentage)


def translate_coords(offset_percentages: Tuple[float, float]):
    return (
        int(pyautogui.size()[0] * offset_percentages[0]),
        int(pyautogui.size()[1] * offset_percentages[1]),
    )


def translate_coords(offset_x_percentage: float, offset_y_percentage: float):
    return (
        int(pyautogui.size()[0] * offset_x_percentage),
        int(pyautogui.size()[1] * offset_y_percentage),
    )
