# -*- coding: utf-8 -*-
import os


def e(key: str, default: str) -> str:
    """
    Get environment variable.
    """
    return os.environ.get(key, default)


TELEGRAM_TOKEN = e("TELEGRAM_TOKEN", "<YOUR TELEGRAM BOT TOKEN HERE>")

HTTP_PROXY = e("HTTP_PROXY", "http://127.0.0.1:10808")
HTTPS_PROXY = e("HTTPS_PROXY", "http://127.0.0.1:10808")
SSL_VERIFY = e("SSL_VERIFY", "false") == "true"

CONFIG_FILE = e("CONFIG_FILE", "./config.yml")
DATABASE_FILE = e("DATABASE_FILE", "./database.json")
