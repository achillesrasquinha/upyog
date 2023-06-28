import os.path as osp
import time
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from upyog.config import PATH, environment
from upyog.util.system  import (
    makedirs, make_temp_dir, unzip, move, make_exec
)
from upyog.model.base import BaseObject
from upyog.util.request import joinurl
from upyog.util.request import download_file
from upyog.util.string  import check_url
import upyog.log as log

NAME = __name__

_DRIVER = None

_CHROME_DRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com/113.0.5672.126/"

INCOGNITO = True
DELAY     = 5
EXIT      = True

logger = log.get_logger(NAME)

def get_driver_basedir(exist_ok = True):
    path = osp.join(PATH["CACHE"], "psy", "drivers")
    makedirs(path, exist_ok = exist_ok)

    return path

def get_driver_path(type_):
    driver_path = osp.join(get_driver_basedir(), type_)
    return driver_path

def download_chrome_driver(target_path):
    env = environment()
    suffix = None

    if "macos" in env["os"].lower() and "arm" in env["os"]:
        suffix = "mac_arm64"
    elif "linux" in env["os"].lower():
        suffix = "linux64"
    else:
        raise ValueError("Unsupported OS %s" % env["os"])

    url = joinurl(_CHROME_DRIVER_BASE_URL, "chromedriver_%s.zip" % suffix)

    with make_temp_dir() as temp_dir:
        path_zip = osp.join(temp_dir, "chromedriver_%s.zip" % suffix)
        download_file(url, path_zip)
        unzip(path_zip, temp_dir)

        path_exe = osp.join(temp_dir, "chromedriver")

        move(path_exe, dest = target_path)
        make_exec(target_path)

def get_chrome_driver(**kwargs):
    driver_path = get_driver_path("chromedriver")

    if not osp.exists(driver_path):
        download_chrome_driver(driver_path)

    headless = kwargs.pop("headless", False)
    detach   = kwargs.pop("detach", False)
    
    options  = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    if detach:
        options.add_experimental_option("detach", True)

    instance = webdriver.Chrome(driver_path, options = options)
    
    return instance

_DRIVERS = {
    "chrome": get_chrome_driver,
}

def get_driver(type_ = "chrome", **kwargs):
    if not type_ in _DRIVERS:
        raise ValueError("Driver type %s not found." % type_)

    driver   = _DRIVERS[type_]
    instance = driver(**kwargs)

    return instance
    
@log.log_fn
def visit(url, **kwargs):
    global _DRIVER, EXIT

    if not _DRIVER:
        _DRIVER = get_driver(detach = not EXIT, **kwargs)

    if not check_url(url, raise_err = False):
        base_url = _DRIVER.current_url
        url = joinurl(base_url, url)

    return _DRIVER.get(url)

@log.log_fn
def wait(timeout = 5):
    time.sleep(timeout)

class BasePsy(BaseObject):
    def humane_delay(self, min_ = 0.1, max_ = 0.3):
        delay = random.uniform(min_, max_)
        time.sleep(delay)

    def type(self, text):
        global INCOGNITO

        if INCOGNITO:
            self.humane_delay()

            for char in text:
                self._s_element.send_keys(char)
                self.humane_delay()
        else:
            self._s_element.send_keys(text)

        return self
    
    def tab(self):
        self.type(Keys.TAB)

    def click(self):
        global INCOGNITO

        if INCOGNITO:
            self.humane_delay()

        self._s_element.click()
        self._refresh()

        return self
    
def _get_by(selector):
    by = By.CSS_SELECTOR
    if selector.startswith("//"):
        by = By.XPATH
    return by

class Element(BasePsy):
    def __init__(self, driver, selector):
        self._driver   = driver
        self._selector = selector

        self._refresh()

    def _refresh(self):
        global INCOGNITO, DELAY

        by = _get_by(self._selector)

        try:
            if INCOGNITO:
                self._s_element = WebDriverWait(self._driver, DELAY).until(
                    EC.visibility_of_element_located((by, self._selector))
                )
            else:
                self._s_element = self._driver.find_element(by, self._selector)
        except TimeoutException:
            logger.warning("Element %s not found." % self._selector)

    def attr(self, name):
        return self._s_element.get_attribute(name)

@log.log_fn
def get(selector):
    global _DRIVER

    if not _DRIVER:
        raise ValueError("Driver not initialized.")

    element = Element(_DRIVER, selector)
    return element

@log.log_fn
def exists(selector):
    try:
        return get(selector)
    except:
        pass

    return False

@log.log_fn
def contains(selector, content):
    element = get(selector)
    if content in element._s_element.text:
        return element
    else:
        raise ValueError("Element %s does not contain %s" % (selector, content))