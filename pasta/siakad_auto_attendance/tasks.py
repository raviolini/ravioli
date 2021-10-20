"""
    List of tasks that can be used called with events
"""

from flour import log_neko

from . import configure as _configure

from .core import try_sign_in
from .core_browserless import try_fill_attendance
from .globals import Dalu

def configure():
    return _configure.run()

def sign_in():
    return try_sign_in()

def fill_attendance():
    log_neko.message_info("Attempting to fill the attendance")

    if try_fill_attendance(Dalu.DARING):
        log_neko.message_info("Action finished successfully, you should've been marked as present.")
        return True

    log_neko.message_warn("Failed to fill attendance, please check out the form yourself.")
    log_neko.message_info("Please submit any bugs into our github issues page at https://github.com/raviolini/ravioli/issues")

    return False

