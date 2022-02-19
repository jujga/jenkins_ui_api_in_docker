from time import sleep
import pytest
import pytest_check as check
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from webdriver_manager import firefox

from selenium.webdriver.common.by import By
from pages.mainpage import MainPage
from pages.basepage import FavoritePage, LoginedPage

# credentials
# mail dytaza@mailto.plus
# password qwerty654321

from test_data.credentials import Credentials


# @pytest.fixture
# def driver():
#     driver = webdriver.Firefox(executable_path=firefox.GeckoDriverManager().install())
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#
#     yield driver
#     driver.get('https://my.prom.ua/cabinet/user/favorites')
#     for i in FavoritePage(driver).del_favs_button:
#         i.click()
#     driver.close()

@pytest.fixture
def driver(request):
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    # driver = webdriver.Firefox(executable_path=firefox.GeckoDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(10)

    # yield driver

    def fin():
        driver.get('https://my.prom.ua/cabinet/user/favorites')
        # driver.find_element(By.XPATH, '//div[text()="✕"]').click()
        # очищаем список избранных после себя
        for i in FavoritePage(driver).del_favs_button:
            sleep(1)  # пока что ничего лучшего тут не вышло(
            i.click()
        sleep(3)
        # driver.close()

    request.addfinalizer(fin)
    return driver


@pytest.fixture
def logined_page(driver: driver):
    # в предустановках будет логин + очистка старого избранного. когда-то потом.
    driver.get('https://prom.ua/Velosipednye-shiny')
    main_page = MainPage(driver)
    main_page.voiti_link.click()
    main_page.email_button.click()
    main_page.email_field.send_keys(Credentials.login_email)
    main_page.dalee_button
    main_page.password_field.send_keys(Credentials.login_passw)
    page = main_page.voiti_button_click()
    return page
    # конец предустановок ================


def t1est1(driver: driver, logined_page: logined_page):
    from time import sleep
    sleep(3)
    # login.list_goods_heart_button.click()
    logined_page.fav_page_button.click()

    def get_fav_list(logined_page):
        return {i.text for i in logined_page.fav_list}
        # sett = list()
        # for i in range(len(mass)):
        #     sett.append(mass[i].find_element(By.XPATH, '//a[@data-qaid="product_name"]').text)

    assert get_fav_list(logined_page) == {'Покрышка на велосипед KENDA Small Block Eight 29x2.10 (54-622) K-1047',
                                          'Шина 255 х 55 для детского велосипеда'}

    # assert logined_page.fav_list[0].find_element(By.XPATH, '//a[@data-qaid="product_name"]').text == 'вермишель'

    # driver.get('https://prom.ua/Velosipednye-shiny')


@pytest.mark.parametrize('fav_numbers', (((1)),((1, 2, 5))))
def test_add2fav(logined_page: logined_page, fav_numbers):
    # fav_number_expected = 2  # количество товаров, добавляемых в избранное. Сделать с параметризацией!
    goods_for_fav = logined_page.goods_list
    iterator_goods = [goods_list[i] if i == in fav_numbers  for i in range(len(goods_list))]
    fav_good_names_expected = []
    for i in range(fav_number_expected):
        # набиваем список названий товаров, чтобы потом их искать в избранном
        fav_good_names_expected.append(LoginedPage.good_name_text(goods_for_fav[i]))
        # клик по сердцу - добавление в избранное
        LoginedPage.goods_heart_button(goods_for_fav[i]).click()

    check.equal(logined_page.fav_button_counter_text,
                str(fav_number_expected), 'Индекс количества элементов в избранном на странице с товарами')
    favorite_page = logined_page.fav_page_button_click()

    check.equal(favorite_page.fav_button_counter_text, str(fav_number_expected),
                'Индекс количества элементов в избранном на странице Избранное')
    assert {i.text for i in favorite_page.fav_list} == \
           {i for i in fav_good_names_expected}, \
        'Набор товаров в избранном равен набору, который добавлялся в избранное'


def test2_add2fav_from_goods(driver: driver, logined_page: logined_page):
    fav_number_expected = 1  # количество товаров, добавляемых в избранное. Сделать с параметризацией!
    goods_for_fav = logined_page.goods_list
    goodsdetail_page = logined_page.goods_click(2)
    goodsdetail_page.fav_add_button.click()
    driver.back()
    goodsdetail_page = logined_page.goods_click(3)
    goodsdetail_page.fav_add_button.click()

    # fav_good_names_expected = []
    # for i in range(fav_number_expected):
    #     goods_for_fav[i].click()
    #     # набиваем список названий товаров, чтобы потом их искать в избранном
    #     # fav_good_names_expected.append(LoginedPage.good_name_text(goods_for_fav[i]))
    #     # клик по сердцу - добавление в избранное
    #     # LoginedPage.goods_heart_button(goods_for_fav[i]).click()
    #
    # check.equal(logined_page.fav_button_counter_text,
    #             str(fav_number_expected), 'Индекс количества элементов в избранном на странице с товарами')
    # favorite_page = logined_page.fav_page_button_click()
    #
    # check.equal(favorite_page.fav_button_counter_text, str(fav_number_expected),
    #             'Индекс количества элементов в избранном на странице Избранное')
    # assert {i.text for i in favorite_page.fav_list} == \
    #        {i for i in fav_good_names_expected}, \
    #     'Набор товаров в избранном равен набору, который добавлялся в избранное'
