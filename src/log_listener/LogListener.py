import re
from config.regexes import AFK_MODE_ON_REGEX, CHAT_MESSAGE_REGEX
from config.constants import LOG_FILE_LOCATION, RABBITMQ_CONFIG
import pyautogui

from utils.printtime import printtime


class LogListener:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.log_file = open(LOG_FILE_LOCATION, "r", encoding="utf8")
        # calling readlines() at the start sets the cursor at the end of the file, listening for new changes
        self.log_file.readlines()

    def is_afk_mode_on(self, message):
        return message == AFK_MODE_ON_REGEX

    def listen(self):
        while True:
            pyautogui.sleep(0.25)

            for line in self.log_file.readlines():
                matched_chat_message_regex = re.match(CHAT_MESSAGE_REGEX, line)

                if matched_chat_message_regex is not None:
                    chat_message = matched_chat_message_regex.group(1)

                    if self.is_afk_mode_on(chat_message):
                        printtime("Entered AFK mode")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_CONFIG["exchange"],
                            routing_key=RABBITMQ_CONFIG["routing_keys"]["afk_mode"],
                            body="test body",
                        )
                    elif chat_message == "gigatest":
                        printtime("Test 2nd routing")
                        self.channel.basic_publish(
                            exchange=RABBITMQ_CONFIG["exchange"],
                            routing_key=RABBITMQ_CONFIG["routing_keys"]["gigatest"],
                            body="test body2",
                        )
