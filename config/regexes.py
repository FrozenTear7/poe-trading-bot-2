from config.user_setup import LEAGUE_NAME

# Chat regexes

CHAT_MESSAGE_REGEX = (
    "\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2} \d+ \w+ \[INFO Client \d+\] :? ?(.+)"
)
AFK_MODE_ON_REGEX = 'AFK mode is now ON. Autoreply "This player is AFK."'
TRADE_REQUEST_REGEX = f"@From (<.+> )?(.+): Hi, I'd like to buy your (\d+) (.+) for my (\d+) (.+) in {LEAGUE_NAME}"
PLAYER_HAS_JOINED_THE_AREA_REGEX = "(.+) has joined the area\."
PLAYER_HAS_LEFT_THE_AREA_REGEX = "(.+) has left the area\."
NOT_A_PARTY_MEMBER_REGEX = "The target of this operation was not a party member\."
TRADE_ACCEPTED_REGEX = "Trade accepted\."
TRADE_CANCELLED_REGEX = "Trade cancelled\."
PLAYER_NOT_FOUND_IN_THIS_AREA_REGEX = "Player not found in this area\."

# Item regexes

ITEM_INFO_SECTION_DIVIDER = "--------\r\n"
INNER_SECTION_DIVIDER = "\r\n"
STACK_SIZE_REGEX = "Stack Size: (\d+)\/(\d+)"
PRICE_SET_REGEX = "Note: .+"
