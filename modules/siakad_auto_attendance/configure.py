from . import log_neko
from . import utils

from selenium import webdriver
from pathlib import Path
from halo import Halo
from colorama import Fore

import json
import os

def is_first_run():
    # Considered first run if config is empty or it does not exist
    config = utils.load_config()
    return not config

def run():
    if not first_run():
        log_neko.message_warn("This is not your first run, are you sure to reconfigure?")
        try:
            input("Press enter to continue or Ctrl+C to quit ")
        except KeyboardInterrupt:
            exit(log_neko.message_info("Quit"))

    email = str(input("Email: "))
    password = str(input("Password: "))
    browser = str(input("Browser: "))

    config = utils.load_config()

    config["email"] = email
    config["password"] = password
    config["browser"] = browser

    save_to_config(config)

if __name__ == '__main__':
    run()
