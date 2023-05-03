from typing import List
from config.stash_tabs.CurrencyStashTab import CurrencyStashTab
from config.stash_tabs.GenericStashTab import GenericStashTab
from config.stash_tabs.StashTab import StashTab


OWN_NICKNAME = "RainbowPablo"
# OWN_NICKNAME = "RecedingHairlineLOL"
LEAGUE_NAME = "Crucible"

POESESSID = "42efa60a7eb016f3ecfb82bb541aa6ac"

TESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract"

# Steam
LOG_FILE_LOCATION = (
    "C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt"
)
# Standalone client
# LOG_FILE_LOCATION = (
#     "C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt"
# )

STASH_TABS: List[StashTab] = [
    CurrencyStashTab(
        [
            ("Orb of Alchemy", "alch", True),
            ("Exalted Orb", "exalted", True),
            # ("Orb of Transmutation", "transmute", True),
            # ("Cartographer's Chisel", "chisel"),
            # ("Divine Orb", "divine"),
            ("Chaos Orb", "chaos", False),
        ]
    ),
    GenericStashTab(
        "buy",
        [
            ("Orb of Alchemy", "alch", 0, 0, 20),
            ("Exalted Orb", "exalted", 1, 1, 20),
            # ("Orb of Transmutation", "exalted", 1, 1, 400),
            # ("Cartographer's Chisel", "chisel", 4, 4),
            # ("Divine Orb", "divine", 6, 6),
        ],
    ),
]
