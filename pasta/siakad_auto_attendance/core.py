"""
    Automatic attendance fill core module

    This module contains functions essential for the fillng action
"""

import os

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from flour import log_neko

from . import utils
from . import callbacks
from .globals import ENDPOINTS

def try_sign_in():
    config = utils.load_config()
    cookies = utils.load_cookies()

    if not config:
        log_neko.message_warn("It seems like you haven't configured this module. Please configure")
        return False

    if not cookies:
        log_neko.message_warn("Cookie is empty")

    preferred_browser = config["browser"]
    email = config["email"]
    password = config["password"]

    # Try to instantiate webdriver based on string that was set in the config
    if preferred_browser.lower() not in AVAILABLE_BROWSER:
        log_neko.message_warn("Preffered browser isn't supported defaulting to firefox (geckodriver)")
        preferred_browser = "firefox"

    log_neko.message_info(f"Preferred web browser identified as {preferred_browser}")

    driver = make_webdriver_from_browser_name(preferred_browser)

    # Load 404 page to be able to attach cookies into browser without triggering errors
    driver.get("https://siswa.smktelkom-mlg.sch.id/does_not_exist")

    # Clear `noise` cookies
    driver.delete_all_cookies()

    # Attach cookies from the stored file (if exists)
    attach_cookies_into_browser(cookies, driver)

    # Go to welcome page to test if it's logged in or not and act accordingly
    driver.get("https://siswa.smktelkom-mlg.sch.id/welcome")

    if "Login" in driver.title:
        log_neko.message_info("Sign in needed. Attempting sign in")
        log_neko.message_info("Please fill in the captcha box")

        signed_in = fill_login_form_and_wait_for_recaptcha(driver, email, password)

        if not signed_in:
            log_neko.message_warn("Sign in attempt failed")
            return False
    else:
        log_neko.message_warn("The browser's title doesn't contain `Login`. Skipping as signed in")
        return True

    # Save user agent string for browserless use
    user_agent = get_user_agent_from_browser(driver)
    utils.add_entry_to_config("user_agent", user_agent)

    # Save cookies for future (browserless) use
    utils.save_cookies(driver.get_cookies())

def fill_login_form_and_wait_for_recaptcha(driver: WebDriver, email: str, password: str) -> bool:
    """
        Attempts to sign in into siakad
    """
    recaptcha_wait_amount = 999
    cookie_wait_amount = 60
    submit_wait_amount = 120

    recaptcha_xpath = "//iframe[@title='reCAPTCHA']"
    recaptcha_frame = driver.find_element_by_xpath(recaptcha_xpath)

    email_input_element = driver.find_element_by_name("email")
    password_input_element = driver.find_element_by_name("password")
    submit_button_element = driver.find_element_by_name("masuk")

    email_input_element.clear()
    password_input_element.clear()

    email_input_element.send_keys(email)
    password_input_element.send_keys(password)

    driver.switch_to.frame(recaptcha_frame)
    recaptcha_status = WebDriverWait(driver, recaptcha_wait_amount).until(callbacks.recaptcha_ok)

    if recaptcha_status is True:
        log_neko.message_info("ReCAPTCHA is identified as checked, signing in...")
    else:
        log_neko.message_warn("Failed to login, please check out the presence form yourself")
        driver.switch_to.parent_frame()
        return False

    driver.switch_to.parent_frame()
    submit_button_element.click()

    WebDriverWait(driver, submit_wait_amount).until(callbacks.redirected_into_welcome_page,
    """
    Web driver waited too long for it to be redirected into welcome page.
    This indicate that either your internet is unstable or you have put
    the wrong user credentials.
    """)

    # Waits for the page to load session or authentication cookies
    WebDriverWait(driver, cookie_wait_amount).until(callbacks.has_needed_cookies, "Needed cookies can't be found")

    return True

def is_signed_in_webdriver(driver: WebDriver) -> bool:
    """
        Checks if the user is signed in by going to welcome page and
        checking if the page has redirected the web browser to the
        login page.

        NOTE: This method doesn't guarantee it will restore the previous
        loaded page with the same state as it was before.
    """
    previous_url = driver.current_url

    driver.get(ENDPOINTS["welcome_page"])
    signed_in = "Login" not in driver.title

    driver.get(previous_url)
    return signed_in

AVAILABLE_BROWSER = ["firefox", "chrome", "edge"]
def make_webdriver_from_browser_name(browser_name: str):
    """
        Instantiate respective webdriver specified in browser_name
    """

    os.environ['WDM_PRINT_FIRST_LINE'] = 'False' #remove the space from log
    os.environ['WDM_LOG_LEVEL'] = '0' # Silence the webdriver_manager log

    browser_name = browser_name.lower()

    if browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == "edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    else:
        raise RuntimeError("Web browser isn't recognized or supported")

    return driver

def attach_cookies_into_browser(cookies: dict, driver: WebDriver):
    """
        Attach cookies into web browser
    """

    for cookie in cookies:
        driver.add_cookie(cookie)

def get_user_agent_from_browser(driver: WebDriver):
    """ Get user agent from selenium webdriver """
    return driver.execute_script("return navigator.userAgent")

def clean_login_information():
    if os.path.exists(utils.COOKIES_FILENAME):
        os.remove(utils.COOKIES_FILENAME)
    if os.path.exists(utils.CONFIG_FILENAME):
        os.remove(utils.CONFIG_FILENAME)
