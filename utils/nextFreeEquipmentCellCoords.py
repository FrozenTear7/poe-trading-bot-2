from math import floor
from config.coordinates import CELL_SIZE, EQUIPMENT_START, TRADE_WINDOW_CELLS


def nextFreeEquipmentCellCoords(index: int):
    eq_start_x, eq_start_y = EQUIPMENT_START

    row_offset = CELL_SIZE[0] * floor(index / TRADE_WINDOW_CELLS[0])
    col_offset = CELL_SIZE[1] * (index % TRADE_WINDOW_CELLS[0])

    return (eq_start_x + row_offset, eq_start_y + col_offset)
