from typing import List
from config.stash_tabs.CurrencyStashTab import CurrencyStashTab
from config.stash_tabs.GenericStashTab import GenericStashTab
from config.stash_tabs.StashTab import StashTab


OWN_NICKNAME = "RainbowPablo"
LEAGUE_NAME = "Crucible"

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
            # ("Orb of Alchemy", "alch"),
            ("Exalted Orb", "exalted", True),
            # ("Cartographer's Chisel", "chisel"),
            # ("Divine Orb", "divine"),
            ("Chaos Orb", "chaos", False),
        ]
    ),
    GenericStashTab(
        "buy",
        [
            # ("Orb of Alchemy", "alch", 0, 0),
            ("Exalted Orb", "exalted", 6, 6, 20),
            # ("Cartographer's Chisel", "chisel", 4, 4),
            # ("Divine Orb", "divine", 6, 6),
        ],
    ),
]
