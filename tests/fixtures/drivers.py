import allure
import pytest
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from tests.test_data.endpoints import PromEndpoints
from tests.pages.pageobjects import FavoritePage
from tests.utilities.utils import DriverForAllure
from tests.common import do_allure_screenshot


@pytest.fixture
@allure.step(f'Running browser')
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Remote(command_executor='http://192.168.0.114:4444/wd/hub', options=options) \
        if request.config.getoption('--start_from_jenkins')\
        else webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    DriverForAllure.driver = driver
    driver.maximize_window()
    driver.implicitly_wait(10)

    @allure.step('Clearing favorite list and closing browser')
    def fin():
        driver.get(PromEndpoints.favorites())
        # очищается список избранных после каждого теста
        for cross_button_index in FavoritePage(driver).del_favs_button:
            sleep(1)  # пока что ничего лучшего тут не вышло(
            cross_button_index.click()
        sleep(1)
        do_allure_screenshot('Favorite list must be empty')
        sleep(1)
        driver.close()

    request.addfinalizer(fin)
    return driver
