"""
    Script to configure siakad_auto_attendance
"""

import sys

import log_neko
from . import utils

def is_first_run():
    """
        Checks if it's the first time running configure.py. It's considered to
        be the first run if config is empty or it does not exist.
    """

    config = utils.load_config()
    return not config

def configure():
    """
        Configure siakad_user_credential.json interactively.
    """

    email = str(input("Email: "))
    password = str(input("Password: "))
    browser = str(input("Browser: "))

    config = utils.load_config()

    config["email"] = email
    config["password"] = password
    config["browser"] = browser

    utils.save_to_config(config)

def run():
    """
        Run configure with first time check.
    """

    if not is_first_run():
        log_neko.message_warn("This is not your first run, are you sure to reconfigure?")
        try:
            input("Press enter to continue or Ctrl+C to quit ")
        except KeyboardInterrupt:
            sys.exit(log_neko.message_info("Quit"))
            

    configure()

if __name__ == '__main__':
    run()
