from selenium.webdriver.common.by import By
from src.cfg.cfg_global import settings
import logging

LOGGER = logging.getLogger()


def test_phrase_in_result(web_client, clean_search_box):
    """ verify hello Kitty term in all result """
    res = web_client.verify_phrase_in_search_results(search_term=settings.search_term)
    assert res is False, F"phrase {settings.phrase} isn't expected to exist in all search suggestions"


def test_suggested_products_changed(web_client, cfg_test, clean_search_box):
    """ verify that for each suggested product in search list, there are different suggested products """
    web_client.enter_search_term(settings.search_term)
    first_product = web_client.return_product_suggestion(cfg_test.first_product_location_in_list).text
    LOGGER.info(F"suggested product when selecting item: {cfg_test.first_product_location_in_list}, {first_product}")
    second_product = web_client.return_product_suggestion(cfg_test.second_product_location_in_list).text
    LOGGER.info(F"suggested product when selecting item: {cfg_test.second_product_location_in_list}, {second_product}")
    assert first_product != second_product, F"both selected items are wrongly equalled: {first_product}"


def test_price_exist_and_30px(web_client, cfg_test, clean_search_box):
    """ verify that for a price exist for a selected product and verify its fonts size """
    web_client.enter_search_term(settings.search_term)
    product_selection = web_client.return_product_suggestion(cfg_test.product_location_in_list)
    LOGGER.info(F"suggested product when selecting item: {cfg_test.product_location_in_list}, {product_selection.text}")
    product_selection.click()
    is_price_exist = web_client.base_elements.is_exist(locator=By.XPATH, value="//div[@data-testid='customer-price']")
    assert is_price_exist is True, F"wrongly can't find a price for {product_selection.text}"
    price = web_client.base_elements.find(By.XPATH, "//div[@data-testid='customer-price']", expected_condition='presence')
    fonts_size = web_client.get_elements_size(price)
    assert fonts_size == '30px', F"fonts aren't 30px as expected. actual fonts size: {fonts_size}"



