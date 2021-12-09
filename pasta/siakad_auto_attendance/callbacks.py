from selenium.webdriver.remote.webdriver import WebDriver

from .globals import ENDPOINTS

def has_needed_cookies(driver: WebDriver):
    """
        Callback function to check if important cookies exists in a webdriver
    """

    kosogha = driver.get_cookie("kosogha")
    ci_session = driver.get_cookie("ci_session")
    cookie = driver.get_cookie("cookie")

    return kosogha and ci_session and cookie

def recaptcha_ok(driver: WebDriver) -> bool:
    """
        Check if recaptcha is checked
    """

    recaptcha_anchor = driver.find_element_by_id("recaptcha-anchor")
    aria_checked_attrib = recaptcha_anchor.get_attribute("aria-checked")
    return "false" not in aria_checked_attrib

def redirected_into_welcome_page(driver: WebDriver) -> bool:
    return driver.current_url == ENDPOINTS["welcome_page"]

