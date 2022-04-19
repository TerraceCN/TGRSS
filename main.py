# -*- coding: utf-8 -*-
import time

import yaml
from loguru import logger
from tinydb import TinyDB, Query

from config import CONFIG_FILE, DATABASE_FILE
from rss import get_feeds
from bot import send_message

# Load RSS config
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config_yml = yaml.load(f, Loader=yaml.FullLoader)

# Load database
db = TinyDB(DATABASE_FILE)
query = Query()

feeds = {}

# Iterate over the RSS group
for gname, group in config_yml["rss_groups"].items():
    logger.info(f"Processing group {gname}")

    # Get RSS name and url from group
    for rname, rurl in group.items():
        feeds[rname] = []
        try:
            rss_feeds = get_feeds(rurl)
        except Exception:
            logger.error(f"Error while getting RSS feeds from {rurl}")
            continue

        # Save feeds to dict
        for feed in rss_feeds:
            feed.update({"group": gname})
            feeds[rname].append(feed)
            logger.info(f"Get feed: {feed['title']} [{gname} - {rname}]")

# Interate over the chat_id array
for chat_id, group in config_yml["chat_ids"].items():
    logger.info(f"Processing chat_id {chat_id}")

    # Get RSS name and url from user
    for rname, rurl in group.items():

        # Get delicated RSS of user
        if rname not in feeds:
            feeds[rname] = []
            try:
                rss_feeds = get_feeds(rurl)
            except Exception:
                logger.error(f"Error while getting RSS feeds from {rurl}")
                continue
            for feed in rss_feeds:
                feed.update({"group": "Delicated"})
                feeds[rname].append(feed)
                logger.info(f"Get feed: {feed['title']} [Delicated - {rname}]")
        
        # Send message to user if there is new feed
        for feed in feeds[rname]:
            if db.search((query.chat_id == chat_id) & (query.link == feed["link"])):
                continue
            try:
                send_message(
                    chat_id,
                    (
                        f"*{feed['group']} - {rname}*\n"
                        f"[{feed['title']}]({feed['link']})\n"
                    ),
                    disable_notification=True,
                )
            except Exception:
                logger.error(f"Error while sending message to {chat_id}")
                continue
            logger.info(f"Send feed: {feed['title']} => {chat_id}")
            db.insert({
                "chat_id": chat_id,
                "link": feed["link"],
                "time": int(time.time()),
            })
