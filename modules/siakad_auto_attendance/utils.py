import json
import pickle
import os

config_filename = "config.json"
cookies_filename = "cookies.pkl"

def is_empty(filename) -> bool:
    return os.path.getsize(filename) == 0

def load_config() -> dict:
    if not os.path.exists(config_filename) or is_empty(config_filename):
        return {}

    with open(config_filename, "r") as config:
        return json.load(config)

def save_to_config(config) -> None:
    with open(config_filename, "w") as config_file:
        json.dump(config, config_file)

def load_cookies() -> dict:
    if not os.path.exists(cookies_filename) or is_empty(cookies_filename):
        return {}

    with open(cookies_filename, "rb") as cookies_file:
        return pickle.load(cookies_file)

def save_cookies(cookies: dict) -> None:
    with open(cookies_filename, "wb") as cookie_storage:
        pickle.dump(cookies, cookie_storage)
