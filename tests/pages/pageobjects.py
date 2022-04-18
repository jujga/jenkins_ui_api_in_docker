# не смог одолеть проблему циклического импорта,
# потому все пейжобжекты поместил в один файл

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.utilities.utils import DriverForAllure
import allure
import datetime
from tests.fixtures.rest_fixt import logger, logger_fixt, Config

class BasePage(object):
    # базовая страница. типа абстрактный класс
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(driver, 10)

    @allure.step('Go back')
    def click_browser_back_button(self):
        self.driver.back()
        do_allure_screenshot(f'Previous page')

    @allure.step('Clicking on a heart button on the goods with index {2}')
    def click_goods_heart_button(self, web_item_list, goods_index):
        def is_heart_picked():
            heart_button = operable_goods.find_element(By.XPATH, './/span[@data-qaid="add_favorite"]')
            heart_dom_attrs = heart_button.get_dom_attribute('data-tg-clicked')
            return False if ':"off",' in heart_dom_attrs else True

        def is_heart_state_changed(is_prev_heart_state):
            """Do REST POST request to make sure goods is added/removed to/from favorites list (instead of selecting from a DB)"""
            import requests
            import json


            url = "https://my.prom.ua/cabinet/user/graphql"
            payload = json.dumps([
                {
                    "operationName": "FavoriteListQuery",
                    "variables": {
                        "page": 1,
                        "perPage": 20,
                        "searchTerm": "",
                        "categoryId": None,
                        "companyId": None,
                        "isFresh": True
                    },
                    "query": "query FavoriteListQuery($perPage: Int!, $page: Int!, $searchTerm: String!, $categoryId: Int, $companyId: Int, $saleFilter: Boolean, $availFilter: Boolean, $isFresh: Boolean) {\n  favoriteList(\n    perPage: $perPage\n    page: $page\n    search: $searchTerm\n    categoryId: $categoryId\n    companyId: $companyId\n    saleFilter: $saleFilter\n    availFilter: $availFilter\n    isFresh: $isFresh\n  ) {\n    heartedProducts {\n      id\n      name\n      status\n      presence\n      sign\n      price\n      priceWithDiscount\n      ecProductPrices\n      isPresenceSure\n      groupId\n      productTypeKey\n      categoryId\n      categoryIds\n      currencyText\n      imageUrl(width: 1400, height: 1400)\n      sku\n      wholesalePrices {\n        price\n        priceCurrencyLocalized\n        minimumOrderQuantity\n        measureUnit\n        __typename\n      }\n      company {\n        id\n        name\n        isContentHidden\n        siteDisabled\n        reviewsCount\n        positiveReviewsPercent\n        opinionsCount\n        catalogUrl\n        siteUrl\n        catalogOpinionList\n        isCertified\n        isPortalChatVisible\n        isShoppingCartEnabled\n        city\n        frameMapUrl\n        address {\n          region_id\n          __typename\n        }\n        branches {\n          id\n          name\n          companyId\n          phone\n          mapUrl\n          address {\n            region_id\n            city\n            zipCode\n            street\n            regionText\n            country {\n              name\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      labels {\n        isNovaPoshtaAvailable\n        isNovaPoshtaWithPromShipping\n        isJustinWithPromShipping\n        isEvoPayEnabled\n        isSuccessfulPurchase\n        isPromShippingEnabled\n        __typename\n      }\n      supplyPeriod\n      isPriceFrom\n      residueStatus\n      residueColorStatus\n      __typename\n    }\n    allCategories {\n      id\n      caption\n      alias\n      __typename\n    }\n    allCompanies {\n      id\n      name\n      __typename\n    }\n    productCount\n    pagesCount\n    saleFiltAvail\n    availFiltAvail\n    isDefCurrencyOnly\n    __typename\n  }\n}\n"
                },
                {
                    "operationName": "besidaQuery",
                    "variables": {},
                    "query": "query besidaQuery {\n  besida {\n    cdn_url\n    desktop_v\n    mobile_v\n    is_besida_enabled\n    __typename\n  }\n}\n"
                }
            ])

            headers = {
                'Cookie': '; '.join([cookie['name'] + '=' + cookie['value'] for cookie in self.driver.get_cookies()]),
                'x-requested-with': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            is_in_fav = True if BasePage.good_name_text(operable_goods) in response.text else False
            return is_in_fav ^ is_prev_heart_state

        operable_goods = web_item_list[goods_index]
        is_heart_picked_prev = is_heart_picked()
        click_time = datetime.datetime.now().timestamp()
        operable_goods.find_element(By.XPATH, './/span[@data-qaid="add_favorite"]').click()
        while not is_heart_state_changed(is_heart_picked_prev):
            if datetime.datetime.now().timestamp() - click_time > 1:
                # done 1s for operation of adding/removing one goods to/from the favorite list
                # if didnt raises assert exception and stops the test
                assert False, 'Global problem about adding/removing goods to/from favorites.' \
                              'Please check internet connection or accessibility of site'
        do_allure_screenshot(f'After clicking on the {goods_index}-th goods/s heart button')

    @staticmethod
    def good_name_text(web_item):
        return web_item.find_element(
            By.XPATH, './/span[@data-qaid="product_name"]').text

    @property
    def sign_in_link(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@data-qaid="sign-in"]')

    @property
    def email_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@data-qaid="email_btn"]')))

    @property
    def email_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="email_field"]')

    @property
    def next_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@id="emailConfirmButton"]')

    @property
    def password_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="enterPassword"]')

    @property
    def submit_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@id="enterPasswordConfirmButton"]')

    def submit_button_click(self):
        self.submit_button.click()

    def go_logined_page(self):
        return LoginedPage(self.driver)


class MainPage(BasePage):
    # основная страница до логина
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def goods_list(self):
        # эксплисит ждет, пока не появится список товаров
        return self.wait.until(EC.visibility_of_any_elements_located(
            (By.XPATH, '//div[@data-qaid="product_block"]')))

    # def goods_click(self,i):
    #     self.goods_list[i].click()


class LoginedPage(MainPage):
    # страница, когда залогинены
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_page_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@data-qaid = "favorite_cabinet_button"]')

    @allure.step('Jump to favorite page')
    def click_fav_page_button(self):
        self.fav_page_button.click()
        do_allure_screenshot('Favorite page')
        return FavoritePage(self.driver)

    @allure.step('Enter into goods details by clicking on the goods with index {1}')
    def click_on_goods(self, i):
        self.goods_list[i].click()
        do_allure_screenshot('Goods details')
        return GoodsDetail(self.driver)

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(By.XPATH,
                                        '//div[@data-qaid="counter"]').text


class FavoritePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(
            By.XPATH, '//div[@data-qaid="counter"]//span').text

    @property
    def del_favs_button(self):
        return self.driver.find_elements(By.XPATH,
                                         '//span[@data-qaid="delete_icon"]')

    @property
    def fav_list(self):
        return self.driver.find_elements(By.XPATH,
                                         '//a[@data-qaid="product_name"]')


class GoodsDetail(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_add_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//span[@data-qaid="add_favorite"]')

    @allure.step("Clicking on a heart button on the goods's detail")
    def click_fav_add_button(self):
        self.fav_add_button.click()
        do_allure_screenshot(f'After clicking on the heart button')

    @property
    def good_code_text(self):
        return self.driver.find_element(
            By.XPATH, '//span[@data-qaid="product-sku"]').text

    @property
    def good_name_txt(self):
        return self.driver.find_element(
            By.XPATH, '//h1[@data-qaid="product_name"]').text


# HELPERS
def do_allure_screenshot(name):
    allure.attach(DriverForAllure.driver.get_screenshot_as_png(),
                  name=name,
                  attachment_type=allure.attachment_type.PNG)
