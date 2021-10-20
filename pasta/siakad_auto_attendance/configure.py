"""
    Script to configure siakad_auto_attendance
"""

from flour import log_neko
from pasta.siakad_auto_attendance.core import AVAILABLE_BROWSER
from . import utils

def is_first_run():
    """
        Checks if it's the first time running configure.py. It's considered to
        be the first run if config is empty or it does not exist.
    """

    config = utils.load_config()
    return not config

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values

def configure():
    """
        Configure siakad_user_credential.json interactively.
    """

    email = input("Email: ")
    password = input("Password: ")

    print("Currently supported browser: ")
    for browser in AVAILABLE_BROWSER:
        print(" -", browser)

    browser = input("Browser: ")

    if browser == "":
        if yn_choice(log_neko.compose_warn("Preferred browser is not set. Are you sure?"), 'n'):
            print("Continuing with firefox")
        else:
            browser = input("Browser: ")

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
        if yn_choice(log_neko.compose_warn("This is not your first run, are you sure to reconfigure?"), 'n'):
            configure()

if __name__ == '__main__':
    run()
