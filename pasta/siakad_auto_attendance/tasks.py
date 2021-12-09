"""
    List of tasks that can be used called with events
"""

from flour import log_neko

from . import configure as _configure

from .core import try_sign_in
from .core_browserless import try_fill_attendance
from .globals import Dalu
from pasta.siakad_auto_attendance import core, utils

from pasta.siakad_auto_attendance import core_browserless

def configure():
    log_neko.message_info("Configuring siakad_auto_attendance")
    return_value = _configure.run()
    log_neko.message_info("Finished configuring")
    return return_value

def sign_in():
    log_neko.message_info("Attempting sign in")
    return_value = try_sign_in()
    log_neko.message_info("Attempt finished")
    return return_value

def fill_attendance():
    log_neko.message_info("Attempting to fill the attendance")

    dalu = Dalu.DARING

    if utils.yn_choice("Are you schooling from home?"):
        dalu = Dalu.DARING
    else:
        dalu = Dalu.LURING

    if try_fill_attendance(dalu):
        log_neko.message_info("Action finished successfully, you should've been marked as present.")
        return True

    log_neko.message_warn("Failed to fill attendance, please check out the form yourself.")
    log_neko.message_info("Please submit any bugs into our github issues page at https://github.com/raviolini/ravioli/issues")

    log_neko.message_info("Attempt finished")

    return False

def clean_login_information():
    log_neko.message_info("Attempting to clean login information")
    core.clean_login_information()
    core_browserless.clean_login_information()
    log_neko.message_info("Attempt finished")
