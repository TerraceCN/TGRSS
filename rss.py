# -*- coding: utf-8 -*-
import httpx
from lxml import etree


def get_feeds(url: str) -> list:
    """
    Get feeds from RSS.
    """
    resp = httpx.get(url)
    resp.raise_for_status()
    xml = etree.fromstring(resp.content)
    feeds = []
    for item in xml.xpath("//item"):
        title = item.xpath("title")[0].text
        desc = item.xpath("description")[0].text
        link = item.xpath("link")[0].text
        feeds.append({
            "title": title,
            "desc": desc,
            "link": link,
        })
    return feeds
    