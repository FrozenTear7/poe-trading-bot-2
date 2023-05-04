from math import floor
from config.coordinates import (
    CELL_SIZE,
    EQUIPMENT_START,
    TRADE_WINDOW_CELLS,
    TRADE_WINDOW_START,
)


def equipment_cell_coords_by_index(index: int):
    eq_start_x, eq_start_y = EQUIPMENT_START

    row_offset = CELL_SIZE[0] * floor(index / TRADE_WINDOW_CELLS[0])
    col_offset = CELL_SIZE[1] * (index % TRADE_WINDOW_CELLS[0])

    return (eq_start_x + row_offset, eq_start_y + col_offset)


def trade_window_cell_coords_by_index(index: int):
    trade_window_start_x, trade_window_start_y = TRADE_WINDOW_START

    row_offset = CELL_SIZE[0] * floor(index / TRADE_WINDOW_CELLS[0])
    col_offset = CELL_SIZE[1] * (index % TRADE_WINDOW_CELLS[0])

    return (trade_window_start_x + row_offset, trade_window_start_y + col_offset)
