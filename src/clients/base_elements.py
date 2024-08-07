import logging
from typing import Any

from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException, \
    WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.clients.locator import Locator
from selenium.webdriver.common.by import By

LOGGER = logging.getLogger()

EXPECTED_CONDITIONS_ELEMENT = \
    {
        'visibility': 'visibility_of_element_located',
        'presence': 'presence_of_element_located',
        'text': 'text_to_be_present_in_element',
        'clickable': 'element_to_be_clickable'
    }

EXPECTED_CONDITIONS_ELEMENTS = \
    {
        'visibility': 'visibility_of_all_elements_located',
        'presence': 'presence_of_all_elements_located',
        'text': 'text_to_be_present_in_element',
    }


class BaseElements(object):

    def __init__(self, driver):
        self.element = None
        self.driver = driver

    def find(self, by, value, element=None, expected_condition=None, timeout=5) -> object:
        """
        Add a waiting functionality (with expected condition) to the 'find_element' function.
        :param by: locator
        :param value: searched value
        :param element: searching within a given element (instead os the webdriver)
        :param expected_condition: element object
        :param timeout: timeout to wait for the expected_condition to be fulfilled
        :return: the found element
        """
        locator = BaseElements.get_locator(by, value)
        if expected_condition:
            element = WebDriverWait(element if element else self.driver, timeout).until(
                getattr(EC, EXPECTED_CONDITIONS_ELEMENT.get(expected_condition))(locator))
        else:
            element = getattr(element if element else self.driver, 'find_element')(locator.by, locator.value)
        return element

    def find_elements(self, by, value, *args, element=None, phrase=None, expected_condition=None, timeout=10):
        locator = BaseElements.get_locator(by, value)
        if expected_condition:
            elements = WebDriverWait(element if element else self.driver, timeout).until(
                getattr(EC, EXPECTED_CONDITIONS_ELEMENTS.get(expected_condition))(locator))
        else:
            elements = getattr(element if element else self.driver, 'find_elements')(locator.by, locator.value)
        return elements

    @staticmethod
    def get_locator(by, value):
        return Locator(by, value)

    @staticmethod
    def set_value(element, value):
        element.clear()
        element.send_keys(value)
        return None

    def is_exist(self, locator, value, expected_condition='presence', timeout=5) -> bool:
        try:
            self.find(locator, value, expected_condition=expected_condition, timeout=timeout)
            return True
        except NoSuchElementException:
            return False

    @property
    def go_back(self):
        self.driver.back()

    def supress_time_exception(self, locator, value, expected_condition='presence', timeout=2) -> [None | object]:
        """
        supress find element response when time exception raised
        :param locator: locator
        :param value: search value
        :param expected_condition:
        :return: response ot None if exception occurred
        """
        try:
            res = self.find(locator, value, expected_condition=expected_condition, timeout=timeout)
        except TimeoutException:
            return None
        return res

    @staticmethod
    def alerts_handling(func) -> Any:
        """
        execute a given function and return True on Success, False on a failure
        it also overcomes alerts like unexpected login prompt and other unexpected alert.
        if login prompt arisen, it re-login.
        :param func: the function which is decorated with this function.
        :return: True on Success, False on a failure
        """

        def wrapper(self, *args):
            try:
                res = func(self, *args)
            except TimeoutException:
                if self.base_elements.supress_time_exception(By.ID, 'survey_content', expected_condition='presence',
                                                             timeout=2):
                    LOGGER.info(F"an unexpected popup raised")
                    self.base_elements.find(By.XPATH, "//button[@id='survey_invite_no']").click()
                if self.base_elements.is_exist(By.ID, "gh-search-input", expected_condition='clickable'):
                    search_inp = self.base_elements.find(By.ID, "gh-search-input", expected_condition='clickable')
                    search_inp.send_keys([Keys.BACKSPACE] * 20)
                    self.enter_search_term()
                res = func(self, *args)
            return res

        return wrapper

