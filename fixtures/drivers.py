import pytest
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from pages.basepage import FavoritePage, MainPage

@pytest.fixture
def driver(request):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(10)

    def fin():
        driver.get('https://my.prom.ua/cabinet/user/favorites')
        # очищается список избранных после каждого теста
        for i in FavoritePage(driver).del_favs_button:
            sleep(0.2)  # пока что ничего лучшего тут не вышло(
            i.click()
        sleep(3)
        driver.close()

    request.addfinalizer(fin)
    return driver

from test_data.credentials import Credentials

@pytest.fixture
def logined_page(driver: driver):
    driver.get('https://prom.ua/Velosipednye-shiny')
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
    driver.get('https://prom.ua/Velosipednye-shiny')
    return MainPage(driver)