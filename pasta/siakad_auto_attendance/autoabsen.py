import json
import pickle
import requests
import os
from pprint import pprint

endpoints = {
    "presence_status": "https://siswa.smktelkom-mlg.sch.id/welcome/get_status_hadir",
    "presence_fill": "https://siswa.smktelkom-mlg.sch.id/presnow/chsts",
    "presence_page": "https://siswa.smktelkom-mlg.sch.id/presnow",
    "login": "https://siswa.smktelkom-mlg.sch.id/login/act_login"
}

def load_cookies():
    with open("cookies.pkl", "rb") as cookies_file:
        return pickle.load(cookies_file)

def load_session():
    with open("session.pkl", "rb") as session_file:
        return pickle.load(session_file)

def save_session(session):
    with open("session.pkl", "wb") as session_file:
        pickle.dump(session, session_file)

def set_cookies_to_session(cookies: dict, session: requests.Session):
    for cookie in cookies:
        if cookie["name"] == "ci_session" or cookie["name"] == "kosogha":
            session.cookies.set(
                name = cookie["name"],
                value = cookie["value"],
            )

    session.cookies.update({"loginsiswa_id_siswa": "3690"})

def is_session_exist():
    return os.path.exists("session.pkl")

def is_present(session: requests.Session):
    response = session.post(endpoints["presence_status"])
    return "masuk" in response.json()["status_presensi"][0].lower()

def fill_presence(session: requests.Session):
    headers = {
        "Referer": "https://siswa.smktelkom-mlg.sch.id/presnow"
    }

    params = {
        "ijin": (None, "M", None),
        "dalu": (None, "daring", None),
    }

    return session.post(
        url = endpoints["presence_fill"],
        files = params,
        headers = headers,
    )

def load_presence_page(session: requests.Session):
    headers = {
        "Referer": "https://siswa.smktelkom-mlg.sch.id/welcome"
    }

    return session.get(
        url = endpoints["presence_page"],
        headers = headers
    )

def remove_ci_session_cookie(session: requests.Session):
    session.cookies.set(name = "ci_session", value = None)

def print_headers(response: requests.Request or requests.Response):
    for key, value in response.headers.items():
        print(key + ": " + value)

def print_response_body(response: requests.Response):
    print(response.text)

def print_request_body(request: requests.Request):
    print(request.body.decode("utf-8"))

if __name__ == "__main__":

    if not is_session_exist():
        cookies = load_cookies()
        session = requests.Session()

        session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})

        set_cookies_to_session(cookies, session)
    else:
        session = load_session()

    print("Attempting to load token...")
    response = load_presence_page(session)
    print(response.cookies)

    print("Attempting fill presence...")
    response = fill_presence(session)

    print("=== Request")
    print("Headers:")
    print_headers(response.request)
    print("\n")
    print("Body:")
    print_request_body(response.request)
    print("\n")

    print("=== Response")
    print("Headers:")
    print_headers(response)
    print("\n")
    print("Body:")
    print_response_body(response)
    print("\n")
    print("Presence:", is_present(session))

    remove_ci_session_cookie(session)

    save_session(session)
