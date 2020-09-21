"""Locators module"""
from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    INPUT_AREA = (By.CSS_SELECTOR, ".CodeMirror-lines")
    RUNSQL_BUTTON = (By.CSS_SELECTOR, ".w3-green.w3-btn")
    RESULT_TABLE = (By.CSS_SELECTOR, ".w3-table-all.notranslate")
    RESULT_ROWS =(By.TAG_NAME, "tr")
    RESULT_COLS = (By.TAG_NAME, "td")
    RESULT_COLNAMES = (By.TAG_NAME, "th")