"""
    Automatic attendance fill core module

    This module contains functions essential for the fillng action
"""

from enum import Enum
import os
import re

import pickle
import requests

from . import utils

ENDPOINTS = {
    "welcome_page": "https://siswa.smktelkom-mlg.sch.id/welcome",
    "presence_status": "https://siswa.smktelkom-mlg.sch.id/welcome/get_status_hadir",
    "presence_fill": "https://siswa.smktelkom-mlg.sch.id/presnow/chsts",
    "presence_page": "https://siswa.smktelkom-mlg.sch.id/presnow",
    "login": "https://siswa.smktelkom-mlg.sch.id/login/act_login"
}

SESSION_FILENAME = "session.pkl"

class Dalu(Enum):
    """ Dalu enum for choosing between Daring and Luring """
    DARING = 0
    LURING = 1

def dalu_to_str(dalu: Dalu) -> str:
    """ Converts Dalu enum to valid post-able string argument """
    if dalu == Dalu.DARING:
        return "daring"
    if dalu == Dalu.LURING:
        return "luring"
    raise RuntimeError("Invalid Dalu enum value")

def load_session():
    """ Loads session file """
    with open(SESSION_FILENAME, "rb") as session_file:
        return pickle.load(session_file)

def save_session(session: requests.Session):
    """ Saves session file """
    with open(SESSION_FILENAME, "wb") as session_file:
        pickle.dump(session, session_file)

def session_exists():
    """ Checks if session file exists """
    return os.path.exists(SESSION_FILENAME)

def set_cookies_to_session(cookies: dict, session: requests.Session):
    """
        Set required cookies to session object in order to fill the attendance
        form
    """
    for cookie in cookies:
        name = cookie["name"]
        value = cookie["value"]

        if name in ("ci_session", "kosogha", "loginsiswa_id_siswa"):
            session.cookies.set(
                name = name,
                value = value,
                path = cookie.get("path"),
                domain = cookie.get("domain"),
                secure = cookie.get("secure"),
                rest = {"HttpOnly": cookie.get("httpOnly")},
                expires = cookie.get("expiry")
            )

def get_user_agent_from_config() -> str:
    return utils.load_config().get("user_agent")

def is_present(session: requests.Session):
    """ Checks the user's presence status """
    response = session.post(ENDPOINTS["presence_status"])
    return "masuk" in response.json()["status_presensi"][0].lower()

def get_page_title(response: requests.Response):
    """ Gets title of a HTML response """
    response_text = response.text
    return re.search('<\W*title\W*(.*)</title', response_text, re.IGNORECASE).group(1)

def is_signed_in(session: requests.Session):
    """ Checks if the user is already signed in """
    response = session.get(ENDPOINTS["welcome_page"])
    page_title = get_page_title(response)
    return "Login" not in page_title

def post_attendance(session: requests.Session, dalu: Dalu):
    """ Do a post request to fill the attendance """
    headers = {
        "Referer": ENDPOINTS["presence_page"]
    }

    params = {
        "ijin": (None, "M", None),
        "dalu": (None, dalu_to_str(dalu), None),
    }

    return session.post(
        url = ENDPOINTS["presence_fill"],
        files = params,
        headers = headers,
    )

def load_presence_page(session: requests.Session):
    """ Load the presence page in order to get attendance token """
    headers = {
        "Referer": ENDPOINTS["welcome_page"]
    }

    return session.get(
        url = ENDPOINTS["presence_page"],
        headers = headers
    )

def remove_ci_session_cookie(session: requests.Session):
    """
        Remove ci_session cookie to prevent it from getting outdated. This way
        ci_session will be regenerated when accessing ENDPOINTS["presence_page"]
    """
    session.cookies.set(name = "ci_session", value = None)

def try_fill_attendance(dalu: Dalu, user_agent: str):
    """
        Tries to fill the attendance form for the user
    """
    if not session_exists():
        cookies = utils.load_cookies()
        session = requests.Session()

        session.headers.update({"User-Agent": user_agent})

        set_cookies_to_session(cookies, session)
    else:
        session = load_session()

    print("Checking if the login session is valid...")
    print("Signed In:", is_signed_in(session))

    print("Attempting to load token...")
    load_presence_page(session)

    print("Attempting fill presence...")
    post_attendance(session, dalu)

    presence_status = is_present(session)
    print("Presence:", presence_status)

    remove_ci_session_cookie(session)

    save_session(session)

    return presence_status
