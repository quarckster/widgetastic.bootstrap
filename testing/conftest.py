import codecs
import os
import sys

import allure
import pytest
from selenium import webdriver

from widgetastic.browser import Browser


selenium_browser = None


class CustomBrowser(Browser):
    @property
    def product_version(self):
        return "1.0.0"


@pytest.fixture(scope="session")
def browser_name():
    return os.environ["BROWSER"]


@pytest.fixture(scope="session")
def selenium(browser_name):
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True
        driver = webdriver.Firefox(options=firefox_options)
    global selenium_browser
    selenium_browser = driver
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def browser(selenium, httpserver):
    this_module = sys.modules[__name__]
    path = os.path.dirname(this_module.__file__)
    testfilename = path + "/testing_page.html"
    httpserver.serve_content(
        codecs.open(testfilename, mode="r", encoding="utf-8").read(),
        headers=[("Content-Type", "text/html")])
    selenium.get(httpserver.url)
    return CustomBrowser(selenium)


def pytest_exception_interact(node, call, report):
    if selenium_browser is not None:
        allure.attach(
            "Error screenshot", selenium_browser.get_screenshot_as_png(), allure.attach_type.PNG)
        allure.attach("Error traceback", str(report.longrepr), allure.attach_type.TEXT)
