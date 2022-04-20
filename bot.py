# -*- coding: utf-8 -*-
import httpx

from config import TELEGRAM_TOKEN, HTTP_PROXY, HTTPS_PROXY, SSL_VERIFY


if HTTP_PROXY and HTTPS_PROXY:
    c = httpx.Client(
        base_url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}",
        proxies={
            "http://": HTTP_PROXY,
            "https://": HTTPS_PROXY,
        },
        verify=SSL_VERIFY,
    )
else:
    c = httpx.Client(
        base_url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}", verify=SSL_VERIFY
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
    chat_id: int, text: str, *args, **kwargs
) -> dict:
    """
    Send message.
    """
    url = "/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    params.update(kwargs)
    resp = c.post(url, json=params)
    resp.raise_for_status()
    return resp.json()
