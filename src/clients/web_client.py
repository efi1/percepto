import time
from src.clients.base_elements import BaseElements
from src.clients.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
import logging

LOGGER = logging.getLogger()


class BestBuy(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = kwargs.get('url')
        self.base_elements = BaseElements(self.driver)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    @BaseElements.alerts_handling
    def login(self):
        account_button = self.base_elements.find(By.ID, 'account-menu-account-button', expected_condition='clickable')
        account_button.click()
        sign_in_button = self.base_elements.find(By.XPATH, "//a[contains(text(), 'Sign In')]",
                                                 expected_condition='clickable')
        sign_in_button.click()
        email_box = self.base_elements.find(By.XPATH, "//input[@type='email']", expected_condition='clickable')
        email_box.send_keys(self.username)
        pass_box = self.base_elements.find(By.XPATH, "//input[@type='password']")
        pass_box.send_keys(self.password)
        sign_in_button = self.base_elements.find(By.XPATH, "//button[contains(text(), 'Sign In')]",
                                                 expected_condition='clickable')
        sign_in_button.click()
        is_exist = self.base_elements.is_exist(By.XPATH, "//div[contains(text(), 'Sorry, something went wrong')]",
                                               expected_condition='visibility', timeout=10)
        if is_exist:
            self.open_page()
            LOGGER.info(F"failed to login via {self.username}")

    @BaseElements.alerts_handling
    def open_page(self):
        self.driver.get(self.url)

    @BaseElements.alerts_handling
    def navigate_to_usa(self):
        select_country = self.base_elements.find(By.XPATH, "//div[@lang='en']/div/a[@class='us-link']",
                                                 expected_condition='clickable')
        select_country.click()

    def enter_search_term(self, search_term) -> object:
        search_inp = self.base_elements.find(By.ID, "gh-search-input", expected_condition='presence')
        search_inp.send_keys(search_term)
        time.sleep(3)
        return search_inp

    @BaseElements.alerts_handling
    def return_product_suggestion(self, suggested_order: int) -> object:
        element = self.base_elements.find(By.CSS_SELECTOR, F".v-p-left-xxs:nth-child({suggested_order}) > .text-info "
                                                           F"> span", expected_condition='presence')
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.base_elements.find(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        selected_product = self.base_elements.find(By.CSS_SELECTOR, ".text-underline", expected_condition='clickable')
        return selected_product

    @classmethod
    def is_phrase_exist(cls, suggestion_list: list, phrase: str) -> bool:
        """
        Check if a phrase exist in a given suggestion list
        :param suggestion_list: suggested list as generated while searching a term.
        :param phrase: a searching phrase
        :return: True if exist
        """
        for elem in suggestion_list:
            if any([elem.startswith('Show related products'), 'review' in elem.lower()]):
                continue
            if phrase not in elem.lower():
                return False
        return True

    def verify_phrase_in_search_results(self, search_term='hello', phrase='hello kitty'):
        """
        Check if a phrase exist in suggestion list
        :param search_term:
        :param phrase: the phrase to be looked in the suggestion list
        :return: True if exist
        """
        self.enter_search_term(search_term)
        suggestions_result = self.base_elements.find(By.ID, "suggestViewClientComponent").text
        suggestions_list = suggestions_result.split('\n')
        return self.is_phrase_exist(suggestions_list, phrase)

    @classmethod
    def get_elements_size(cls, element: object) -> int:
        return element.value_of_css_property("font-size")

    @property
    def clean_search_box(self):
        if self.base_elements.is_exist(By.ID, "gh-search-input", expected_condition='clickable'):
            search_inp = self.base_elements.find(By.ID, "gh-search-input", expected_condition='clickable')
            search_inp.send_keys([Keys.BACKSPACE] * 20)

