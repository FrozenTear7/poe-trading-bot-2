from utils.translate_coords import translate_coords, translate_coord

TRADE_WINDOW_CELLS = (5, 12)

CELL_SIZE = translate_coords(0.027, 0.049)
STASH_PLACE = translate_coords(0.52, 0.483)
EQUIPMENT_START = translate_coords(0.675, 0.569)
TRADE_WINDOW_START = translate_coords(0.176, 0.212)

TRADE_WINDOW_ACCEPT_BUTTON = translate_coords(0.163, 0.783)
TRADE_WINDOW_ACCEPT_BUTTON_COLOR = (63, 23, 5)
TRADE_WINDOW_ACCEPT_BUTTON_COLOR_TOLERANCE = 10

TRADE_WINDOW_HELPER_TEXT = translate_coords(0.239, 0.754)
TRADE_WINDOW_HELPER_SIZE = translate_coords(0.17, 0.042)

PRICE_MENU_THRESHOLD = translate_coord(0.137, 0)
PRICE_MENU_OFFSET = translate_coords(-0.048, 0.083)
PRICE_MENU_OFFSET_UNDER_THRESHOLD = translate_coords(0, 0.083)
