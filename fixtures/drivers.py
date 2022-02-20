import pytest
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import test_data.endpoints
from pages.basepage import FavoritePage

@pytest.fixture
def driver(request):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(10)

    def fin():
        driver.get(test_data.endpoints.favorites_url)
        # очищается список избранных после каждого теста
        for cross_button_index in FavoritePage(driver).del_favs_button:
            sleep(0.2)  # пока что ничего лучшего тут не вышло(
            cross_button_index.click()
        sleep(3)
        driver.close()

    request.addfinalizer(fin)
    return driver

