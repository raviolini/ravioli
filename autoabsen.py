#!env python
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from halo import Halo
import pickle
import json
import code

def has_needed_cookies(driver: WebDriver):
    return True if driver.get_cookie("kosogha") is not None else False

def recaptcha_ok(driver: WebDriver):
    recaptcha_anchor = driver.find_element_by_id("recaptcha-anchor")
    aria_checked_attrib = recaptcha_anchor.get_attribute("aria-checked")
    if "false" in aria_checked_attrib:
        return False
    return True

def load_config():
    with open("config.json", "r+") as config:
        return json.load(config)

def try_signin(driver: WebDriver):
    recaptcha_xpath = "//iframe[@title='reCAPTCHA']"
    recaptcha_frame = driver.find_element_by_xpath(recaptcha_xpath)
    recaptcha_wait_amount = 999

    config = load_config()

    account_email = config.get("email")
    account_password = config.get("password")

    if config.get("email") is None:
        print("Can't load email from config.json")
        return False

    if config.get("password") is None:
        print("Can't load password from config.json")
        return False

    email_input_element = driver.find_element_by_name("email")
    password_input_element = driver.find_element_by_name("password")
    submit_button_element = driver.find_element_by_name("masuk")

    email_input_element.clear()
    password_input_element.clear()

    email_input_element.send_keys(account_email)
    password_input_element.send_keys(account_password)

    driver.switch_to.frame(recaptcha_frame)
    recaptcha_status = WebDriverWait(driver, recaptcha_wait_amount).until(recaptcha_ok)
    if recaptcha_status is True:
        print("ReCAPTCHA is identified as checked, signing in...")
    else:
        print("Failed to login, please check out the presence form yourself")
        driver.switch_to.parent_frame()
        return False

    driver.switch_to.parent_frame()
    submit_button_element.click()

    # TODO(zndf): Check if login is successful or not
    return True

def start_auto_absen():
    cookies_storage_filename = "cookies.pkl"
    cookies = None

    spinner = Halo(spinner="dots")

    spinner.start("Loading cookies from previous session")
    try:
        with open(cookies_storage_filename, "rb") as cookie_storage:
            cookies = pickle.load(cookie_storage)
        spinner.succeed("Previous cookies successfully loaded")
    except OSError:
        spinner.fail("Can't open cookies file. Will generate one later")

    spinner.start("Starting firefox web browser")
    driver = webdriver.Firefox()
    spinner.succeed("Firefox webdriver started")

    spinner.start("Retrieving SIAKAD page")
    driver.get("https://siswa.smktelkom-mlg.sch.id/does_not_exist")
    spinner.succeed("SIAKAD successfully retrieved")

    # Remove presetted login cookies incase the does_not_exist
    # page inserts new cookies that will intervere with the old ones
    driver.delete_all_cookies()

    if cookies is not None:
        spinner.start("Loading cookies into web browser")
        for cookie in cookies:
            driver.add_cookie(cookie)
        spinner.succeed("Cookies loaded into web browser")

    spinner.start("Reloading SIAKAD page")
    driver.get("https://siswa.smktelkom-mlg.sch.id/")
    spinner.succeed("SIAKAD successfully reloaded")

    signed_in = "Login" not in driver.title

    if not signed_in:
        print("Sign in needed. Attempting sign in")
        signed_in = try_signin(driver)

    if not signed_in:
        print("Sign in attempt failed. Aborting")
        return False

    WebDriverWait(driver, 60).until(has_needed_cookies, "Needed cookies can't be found")
    with open("cookies.pkl", "wb") as cookie_storage:
        pickle.dump(driver.get_cookies(), cookie_storage)

    return True
