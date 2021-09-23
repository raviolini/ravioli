from . import log_neko
from . import utils
from . import configure

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from halo import Halo

from enum import Enum
import pickle
import json
import os

def get_webdriver(browser_name: str):
    os.environ['WDM_LOG_LEVEL'] = '0' # Silence the webdriver_manager log

    if browser_name == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "chrome":
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == "edge":
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise RuntimeError("Web browser isn't recognized or supported")

    return driver

def has_needed_cookies(driver: WebDriver):
    kosogha = driver.get_cookie("kosogha")
    ci_session = driver.get_cookie("ci_session")
    cookie = driver.get_cookie("cookie")

    return kosogha and ci_session and cookie

def attach_cookies_into_browser(cookies: dict, driver: WebDriver):
    for cookie in cookies:
        driver.add_cookie(cookie)

def recaptcha_ok(driver: WebDriver) -> bool:
    recaptcha_anchor = driver.find_element_by_id("recaptcha-anchor")
    aria_checked_attrib = recaptcha_anchor.get_attribute("aria-checked")
    return False if "false" in aria_checked_attrib else True

def try_signin(driver: WebDriver, email: str, password: str) -> bool:
    recaptcha_xpath = "//iframe[@title='reCAPTCHA']"
    recaptcha_frame = driver.find_element_by_xpath(recaptcha_xpath)
    recaptcha_wait_amount = 999

    email_input_element = driver.find_element_by_name("email")
    password_input_element = driver.find_element_by_name("password")
    submit_button_element = driver.find_element_by_name("masuk")

    email_input_element.clear()
    password_input_element.clear()

    email_input_element.send_keys(email)
    password_input_element.send_keys(password)

    driver.switch_to.frame(recaptcha_frame)
    recaptcha_status = WebDriverWait(driver, recaptcha_wait_amount).until(recaptcha_ok)
    if recaptcha_status is True:
        log_neko.message_info("ReCAPTCHA is identified as checked, signing in...")
    else:
        log_neko.message_W("Failed to login, please check out the presence form yourself")
        driver.switch_to.parent_frame()
        return False

    driver.switch_to.parent_frame()
    submit_button_element.click()

    # TODO(zndf): Check if login is successful or not
    return True

def start():
    if configure.is_first_run():
        configure.run()

    config = utils.load_config()

    preferred_webbrowser_name = config.get("browser")

    if preferred_webbrowser_name is None:
        log_neko.message_warn("Preferred web browser is not set in config.json, defaulting to firefox (geckodriver)")
        preferred_webbrowser_name = "firefox"

    log_neko.message_info(f"Preferred web browser identified as {preferred_webbrowser_name}")

    cookies = utils.load_cookies()

    if not cookies:
        log_neko.message_warn("Cookie is empty")

    spinner = Halo(spinner="dots")

    spinner.start("Starting web browser")
    driver = get_webdriver(preferred_webbrowser_name)
    spinner.succeed("Web browser started")

    spinner.start("Loading 404 page")
    driver.get("https://siswa.smktelkom-mlg.sch.id/does_not_exist")
    spinner.succeed("404 page loaded")

    driver.delete_all_cookies()
    attach_cookies_into_browser(cookies, driver)

    spinner.start("Reloading SIAKAD page")
    driver.get("https://siswa.smktelkom-mlg.sch.id/welcome")
    spinner.succeed("SIAKAD successfully reloaded")

    signed_in = "Login" not in driver.title

    if not signed_in:
        log_neko.message_info("Sign in needed. Attempting sign in")

        email = config.get("email")
        password = config.get("password")

        if not email or not password:
            log_neko.message_warn("Password and email isn't set in config.json. Aborting")
            return False

        log_neko.message_info("Please fill in the captcha box")
        signed_in = try_signin(driver, email, password)

    if not signed_in:
        log_neko.message_warn("Sign in attempt failed. Aborting")
        return False

    spinner.start("Waiting for required cookies to load")
    WebDriverWait(driver, 60).until(has_needed_cookies, "Needed cookies can't be found")
    spinner.succeed("Needed cookies retrieved")

    # TODO(zndf): Check if token really exists
    spinner.start("Loading attendance page to retrieve token")
    driver.get("https://siswa.smktelkom-mlg.sch.id/presnow")
    spinner.succeed("Attendance page loaded")

    spinner.start("Storing cookies")
    utils.save_cookies(driver.get_cookies())
    spinner.succeed("Cookies stored")

    log_neko.message_info("Task completed")

    return True
