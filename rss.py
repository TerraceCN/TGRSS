# -*- coding: utf-8 -*-
import httpx
from lxml import etree

from config import HTTP_PROXY, HTTPS_PROXY


def get_feeds(url: str) -> list:
    """
    Get feeds from RSS.
    """
    if HTTP_PROXY and HTTPS_PROXY:
        resp = httpx.get(url, proxies={"http": HTTP_PROXY, "https": HTTPS_PROXY})
    else:
        resp = httpx.get(url)
    resp.raise_for_status()
    xml = etree.fromstring(resp.content)
    feeds = []

    item_tags = ["item", "entry"]
    items = []
    for item_tag in item_tags:
        items = xml.xpath(f"//{item_tag}")
        if len(items) != 0:
            break
    
    for item in items:
        title = item.xpath("title")[0].text
        link = item.xpath("link")[0].text
        feeds.append({
            "title": title,
            "link": link,
        })
    return feeds
    