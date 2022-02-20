import pytest
import pytest_check as check

from pages.basepage import FavoritePage, LoginedPage, MainPage

# credentials
# mail dytaza@mailto.plus
# password qwerty654321


# параметризуем массивом индексов товаров и признаком, добавляем в избранное из списка или из товара

@pytest.mark.parametrize('fav_numbers, add_fav_from_detail',(
                          ((0,1), 'add_from_goods_list'),
                          ((0, 2, 5), 'add_from_goods_list'),
                          ((2, 5), 'add_from_goods_detail'),))
def test_add2fav(driver, logined_page, fav_numbers: tuple, add_fav_from_detail: str):
    # goods_for_fav = logined_page.goods_list
    fav_good_names_expected = []
    for goods_index in fav_numbers:
        match  add_fav_from_detail:
            case 'add_from_goods_list': # добавляем в избранное, проходясь по списку товаров
                goods_for_fav = logined_page.goods_list
                # набиваем список названий товаров, чтобы потом их искать в избранном
                fav_good_names_expected.append(LoginedPage.good_name_text(goods_for_fav[goods_index]))
                # клик по сердцу - добавление в избранное
                LoginedPage.goods_heart_button(goods_for_fav[goods_index]).click()
            case 'add_from_goods_detail': # добавляем в избранное, зайдя на товар
                # проваливаемся в товар
                goodsdetail_page = logined_page.goods_click(goods_index)
                # запоминаем товар
                fav_good_names_expected.append(goodsdetail_page.good_name_text)
                goodsdetail_page.fav_add_button.click()
                goodsdetail_page.browser_back_button_click()


    check.equal(logined_page.fav_button_counter_text,
                str(len(fav_numbers)), 'Индекс количества элементов в избранном на странице с товарами')
    favorite_page = logined_page.fav_page_button_click()

    check.equal(favorite_page.fav_button_counter_text, str(len(fav_numbers)),
                'Индекс количества элементов в избранном на странице Избранное')
    assert {i.text for i in favorite_page.fav_list} == \
           {i for i in fav_good_names_expected}, \
        'Набор товаров в избранном равен набору, который добавлялся в избранное'


# def test_add2fav_without_login(driver: driver, main_page: main_page):
#     f = main_page.goods_list
#     assert 1 == 2