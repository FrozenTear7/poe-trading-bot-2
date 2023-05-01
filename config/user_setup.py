from config.stash_tabs.CurrencyStashTab import CurrencyStashTab
from config.stash_tabs.GenericStashTab import GenericStashTab


OWN_NICKNAME = "RainbowPablo"
LEAGUE_NAME = "Crucible"

# Steam
LOG_FILE_LOCATION = (
    "C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt"
)
# Standalone client
# LOG_FILE_LOCATION = (
#     "C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt"
# )

STASH_TABS = [
    CurrencyStashTab(["Orb of Alchemy"]),
    GenericStashTab("buy", [("Orb of Alchemy", 1, 1)]),
]
