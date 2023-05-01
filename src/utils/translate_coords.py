from typing import Literal, Tuple

RESOLUTION = (2560, 1440)


def translate_coords(offset_percentage: float, direction: Literal[0, 1]):
    # X - 0, Y - 1
    return int(RESOLUTION[direction] * offset_percentage)


def translate_coords(offset_percentages: Tuple[float, float]):
    return (
        int(RESOLUTION[0] * offset_percentages[0]),
        int(RESOLUTION[1] * offset_percentages[1]),
    )


def translate_coords(offset_x_percentage: float, offset_y_percentage: float):
    return (
        int(RESOLUTION[0] * offset_x_percentage),
        int(RESOLUTION[1] * offset_y_percentage),
    )
