"""Shared fixtures."""
import json
import logging
from _pytest.fixtures import fixture
from src.cfg.cfg_global import settings
from src.utils import utils
from src.clients.web_client import BestBuy

USER_CREDENTIALS_FILE = "user1.json"


@fixture(scope="session")
def web_client(cfg_data):
    """
    start the test's web client.
    :return: test web client.
    """
    logging.info('instantiate the web client')
    web_client = BestBuy(url=settings.url, username=cfg_data.username,
                         password=cfg_data.password)
    web_client.open_page()
    web_client.navigate_to_usa()
    # web_client.login()
    yield web_client
    web_client.tear_down_driver


@fixture(scope="session")
def cfg_data():
    cfg_dir, cfg_fn = settings.cfg_global_dir, USER_CREDENTIALS_FILE
    cfg_data = utils.load_data(cfg_dir, cfg_fn)
    return utils.dict_to_obj(cfg_data)


@fixture(scope="function")
def clean_search_box(web_client):
    web_client.clean_search_box


@fixture(scope="function")
def test_name(request):
    test_name = request.node.name
    return test_name


@fixture(scope="function")
def cfg_test(test_name):
    cfg_dir, cfg_fn = settings.cfg_tests_dir, F"{test_name}.json"
    cfg_data = utils.load_data(cfg_dir, cfg_fn)
    return utils.dict_to_obj(cfg_data)
