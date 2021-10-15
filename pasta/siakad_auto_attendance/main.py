"""
    Automatically fill attendance list on SIAKAD
"""

import os

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from halo import Halo

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from flour import log_neko
from . import utils
from . import configure
from . import core
from . import main
from .core import ENDPOINTS

def get_webdriver(browser_name: str):
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

def get_user_agent(driver):
    """ Get user agent from selenium webdriver """
    return driver.execute_script("return navigator.userAgent")

def has_needed_cookies(driver: WebDriver):
    """
        Callback function to check if important cookies exists in a webdriver
    """

    kosogha = driver.get_cookie("kosogha")
    ci_session = driver.get_cookie("ci_session")
    cookie = driver.get_cookie("cookie")

    return kosogha and ci_session and cookie

def attach_cookies_into_browser(cookies: dict, driver: WebDriver):
    """
        Attach cookies into web browser
    """

    for cookie in cookies:
        driver.add_cookie(cookie)

def recaptcha_ok(driver: WebDriver) -> bool:
    """
        Check if recaptcha is checked
    """

    recaptcha_anchor = driver.find_element_by_id("recaptcha-anchor")
    aria_checked_attrib = recaptcha_anchor.get_attribute("aria-checked")
    return "false" not in aria_checked_attrib

def redirected_into_welcome_page(driver: WebDriver) -> bool:
    return driver.current_url == ENDPOINTS["welcome_page"]

def try_signin(driver: WebDriver, email: str, password: str) -> bool:
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
    recaptcha_status = WebDriverWait(driver, recaptcha_wait_amount).until(recaptcha_ok)
    if recaptcha_status is True:
        log_neko.message_info("ReCAPTCHA is identified as checked, signing in...")
    else:
        log_neko.message_warn("Failed to login, please check out the presence form yourself")
        driver.switch_to.parent_frame()
        return False

    driver.switch_to.parent_frame()
    submit_button_element.click()

    WebDriverWait(driver, submit_wait_amount).until(redirected_into_welcome_page,
    """
    Web driver waited too long for it to be redirected into welcome page.
    This indicate that either your internet is unstable or you have put
    the wrong user credentials.
    """)

    # Waits for the page to load session or authentication cookies
    with Halo(text='Waiting for required cookies to load', spinner='dots') as spinner:
        WebDriverWait(driver, cookie_wait_amount).until(has_needed_cookies, "Needed cookies can't be found")
        spinner.succeed("Needed cookies retrieved")

    return True

def is_signed_in(driver: WebDriver) -> bool:
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

def add_user_agent_to_config(user_agent: str):
    config = utils.load_config()

    config["user_agent"] = user_agent

    utils.save_to_config(config)

def do_sign_in_sequence():
    available_browser = ["firefox", "chrome", "edge"]

    config = utils.load_config()

    preferred_webbrowser_name = config.get("browser")

    if preferred_webbrowser_name.lower() not in available_browser:
        log_neko.message_warn("Preferred web browser is not set in siakad_user_credential.json,"
                              " defaulting to firefox (geckodriver)")
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

    user_agent = main.get_user_agent(driver)
    add_user_agent_to_config(user_agent)

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
            log_neko.message_warn(
                "Password and email isn't set in siakad_user_credential.json."
                " Aborting"
            )
            return False

        log_neko.message_info("Please fill in the captcha box")
        signed_in = try_signin(driver, email, password)

    if not signed_in:
        log_neko.message_warn("Sign in attempt failed. Aborting")
        return False

    spinner.start("Storing cookies")
    utils.save_cookies(driver.get_cookies())
    spinner.succeed("Cookies stored")

def start():
    """
        Start attendance fill
    """

    if configure.is_first_run():
        configure.run()

    # TODO(zndf): Check if calling core.is_signed_in here causes any side effects
    # TODO(zndf): Replace core.is_signed_in with try catch SessionInvalidException
    if not (core.session_exists() and core.is_signed_in(core.load_session())):
        do_sign_in_sequence()

    log_neko.message_info("Attempting to fill the attendance")
    success = core.try_fill_attendance(core.Dalu.DARING, core.get_user_agent_from_config())

    if not success:
        log_neko.message_warn("Failed to fill attendance, please check out the form yourself.")
        log_neko.message_info("Task completed unsuccessfully")
    else:
        log_neko.message_info("Action finished successfully, you should've been marked as present.")
        log_neko.message_info("Task completed successfully")
    
    log_neko.message_info("Please submit any bugs into our github issues page at https://github.com/raviolini/ravioli/issues")

    return True
