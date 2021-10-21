"""
    Utilities
"""

import json
import pickle
import os
import urllib
#import requests
import asyncio
from flour import log_neko
import sys

CONFIG_FILENAME = "siakad_user_credential.json"
COOKIES_FILENAME = "cookies.pkl"
ENCODING = "utf-8"

def is_empty(filename) -> bool:
    """
        Check if a file is empty
    """

    return os.path.getsize(filename) == 0

def load_config() -> dict:
    """
        Load config into a dictionary
    """

    if not os.path.exists(CONFIG_FILENAME) or is_empty(CONFIG_FILENAME):
        return {}

    with open(CONFIG_FILENAME, "r", encoding=ENCODING) as config:
        return json.load(config)

def save_to_config(config) -> None:
    """
        Save a dict to config file
    """

    with open(CONFIG_FILENAME, "w", encoding=ENCODING) as config_file:
        json.dump(config, config_file)

def load_cookies() -> dict:
    """
        Load cookies
    """

    if not os.path.exists(COOKIES_FILENAME) or is_empty(COOKIES_FILENAME):
        return {}

    with open(COOKIES_FILENAME, "rb") as cookies_file:
        return pickle.load(cookies_file)

def save_cookies(cookies: dict) -> None:
    """
        Save cookies
    """

    with open(COOKIES_FILENAME, "wb") as cookie_storage:
        pickle.dump(cookies, cookie_storage)

def add_entry_to_config(name: str, value: str):
    config = load_config()

    config[name] = value

    save_to_config(config)

async def checkConnection():
    while True:
        try:
            urllib.request.urlopen("google.com")
            #if requests.get('https://google.com').ok:
            log_neko.message_info("\rYou are online")
            sys.stdout.flush()
        except TimeoutError:
            log_neko.message_warn("\rYou are Offline, please connect into internet")
            sys.stdout.flush()
        

def isOnline():
    log_neko.message_warn("Still Under Construction (SETA")
    looper = asyncio.new_event_loop()
    asyncio.set_event_loop(looper)
    try:
        looper.run_until_complete(checkConnection())
    finally:
        looper.run_until_complete(looper.shutdown_asyncgens())
        looper.close()