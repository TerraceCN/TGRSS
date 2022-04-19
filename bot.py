# -*- coding: utf-8 -*-
import httpx

from config import TELEGRAM_TOKEN, HTTP_PROXY, HTTPS_PROXY, SSL_VERIFY


c = httpx.Client(
    base_url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}",
    proxies={
        "http://": HTTP_PROXY,
        "https://": HTTPS_PROXY,
    },
    verify=SSL_VERIFY,
)


def get_updates(offset: int = None) -> dict:
    """
    Get updates.
    """
    url = "/getUpdates"
    if offset:
        url += f"?offset={offset}"
    resp = c.get(url)
    resp.raise_for_status()
    return resp.json()["result"]


def send_message(
    chat_id: int, text: str, parse_mode: str = "markdown", disable_notification: bool = False
) -> dict:
    """
    Send message.
    """
    url = "/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_notification": disable_notification,
    }
    resp = c.get(url, params=params)
    resp.raise_for_status()
    return resp.json()
