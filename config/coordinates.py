from utils.translate_coords import translate_coords, translate_coord

TRADE_WINDOW_CELLS = (5, 12)

CELL_SIZE = translate_coords(0.027, 0.049)
STASH_PLACE = translate_coords(0.52, 0.483)
EQUIPMENT_START = translate_coords(0.675, 0.569)

PRICE_MENU_THRESHOLD = translate_coord(0.137, 0)
PRICE_MENU_OFFSET = translate_coords(-0.048, 0.083)
PRICE_MENU_OFFSET_UNDER_THRESHOLD = translate_coords(0, 0.083)
