# -*- coding: utf-8 -*-
import re
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
    for rname, rdetail in group.items():
        feeds[rname] = []

        if isinstance(rdetail, str):
            rurl = rdetail
        elif isinstance(rdetail, dict):
            rurl = rdetail["url"]
        else:
            logger.error(f"Invalid RSS config for {rname}")
            continue
        
        try:
            rss_feeds = get_feeds(rurl)
        except Exception as e:
            logger.error(f"Error while getting RSS feeds from {rurl}")
            continue

        # Save feeds to dict
        for feed in rss_feeds:
            feed.update({"group": gname})
            feeds[rname].append(feed)
        
        logger.info(f"Get {len(feeds[rname])} feeds from {gname} - {rname}")

# Interate over the chat_id array
for chat_id, group in config_yml["chat_ids"].items():
    logger.info(f"Processing chat_id {chat_id}")

    # Get RSS name and url from user
    for rname, rdetail in group.items():
        
        if isinstance(rdetail, str):
            rurl = rdetail
            fold = False
            fold_regex = []
        elif isinstance(rdetail, dict):
            rurl = rdetail["url"]
            fold = rdetail.get("fold", False)
            fold_regex = rdetail.get("fold_regex", [])
        else:
            logger.error(f"Invalid RSS config for {rname}")
            continue

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

            logger.info(f"Get {len(feeds[rname])} feeds from Delicated - {rname}")
        
        # Send message to user if there is new feed
        fold_list = []
        for feed in feeds[rname]:
            if db.search((query.chat_id == chat_id) & (query.link == feed["link"])):
                continue
            
            if fold:
                fold_list.append((feed["title"], feed["link"]))
            elif len(fold_regex) > 0:
                for regex in fold_regex:
                    if re.match(regex, feed["link"]):
                        fold_list.append((feed["title"], feed["link"]))
                        break
            else:
                try:
                    send_message(
                        chat_id,
                        (
                            f"Group: #{feed['group']}\n"
                            f"Source: #{rname}\n"
                            f"[{feed['title']}]({feed['link']})\n"
                        ),
                        parse_mode="markdown",
                        disable_notification=True,
                    )
                    logger.info(f"Send feed: {feed['title']} => {chat_id}")
                except Exception:
                    logger.error(f"Error while sending message to {chat_id}")
                    continue
            db.insert({
                "chat_id": chat_id,
                "link": feed["link"],
                "time": int(time.time()),
            })
        
        for i in range(0, len(fold_list), 15):
            text = ""
            try:
                send_message(
                    chat_id,
                    f"Group: #{feed['group']}\nSource: #{rname}\n" + "\n".join(
                        [f"[{f[0]}]({f[1]})" for f in fold_list[i:i+15]]
                    ),
                    parse_mode="markdown",
                    disable_notification=True,
                    disable_web_page_preview=True,
                )
                logger.info(f"Send {len(fold_list[i:i+15])} folded feeds => {chat_id}")
            except Exception as e:
                logger.error(f"Error while sending message to {chat_id}")
                continue
            
