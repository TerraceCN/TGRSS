# -*- coding: utf-8 -*-
from time import sleep

from bot import get_updates


def get_chat_id():
    print("Ctrl-C to stop.")
    offset = -1
    while True:
        for update in get_updates(offset):
            chat_id = update["message"]["chat"]["id"]
            username = update["message"]["chat"]["username"]
            offset = update["update_id"] + 1
            print(f"{username}: {chat_id}")
        sleep(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print("Usage: python3 tools.py <function>")
        print("Functions:")
        print("- get_chat_id")
        print("  Get chat_id of user who send /start to the bot.")
    elif sys.argv[1] == "get_chat_id":
        get_chat_id()
