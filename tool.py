import pickle
import requests

def load_cookies():
    with open("cookies.pkl", "rb") as cookies_file:
        cookies = pickle.load(cookies_file)
    return cookies

def print_cookies(cookies):
    for cookie in cookies:
        for key, value in cookie.items():
            print(key, ":", value)

def print_cookie_keys(cookies):
    keys = []
    for cookie in cookies:
        for key, value in cookie.items():
            if key not in keys:
                keys.append(key)
    print("Keys", ":", keys)

if __name__ == "__main__":
    print_cookies(load_cookies())
    print_cookie_keys(load_cookies())
