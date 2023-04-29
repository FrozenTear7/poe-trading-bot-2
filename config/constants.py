PLAYER_NICKNAME = "xdd"
LEAGUE_NAME = "Crucible"

# Steam
LOG_FILE_LOCATION = (
    "C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt"
)
# Standalone client
# LOG_FILE_LOCATION = (
#     "C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt"
# )

RABBITMQ_CONFIG = {
    "exchange": "trading-bot-exchange",
    "routing_keys": {"afk_mode": "afk_mode", "gigatest": "gigatest"},
}
