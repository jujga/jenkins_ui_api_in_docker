import pytest
from test_data.credentials import Credentials
from pages.basepage import MainPage
from fixtures.drivers import driver
import test_data.endpoints

@pytest.fixture
def logined_page(driver: driver):
    driver.get(test_data.endpoints.velosipednye_shiny_url)
    main_page = MainPage(driver)
    main_page.voiti_link.click()
    main_page.email_button.click()
    main_page.email_field.send_keys(Credentials.login_email)
    main_page.next_button.click()
    main_page.password_field.send_keys(Credentials.login_passw)
    page = main_page.comein_button_click()
    return page

@pytest.fixture
def main_page(driver: driver):
    driver.get(test_data.endpoints.velosipednye_shiny_url)
    return MainPage(driver)