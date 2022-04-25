import pytest
import allure
import pytest_check as check
from tests.pages.pageobjects import LoginedPage, MainPage
import tests.common as common
from tests.pages.pageobjects import do_allure_screenshot


def idfn_x(val):
    return "Goods indices: {0} ".format(str(val)) if type(val) == tuple else " adding option: {0}".format(str(val))


@allure.title('Adding some goods to favorites when user is logined')
@pytest.mark.ui
@pytest.mark.parametrize('fav_numbers, add_fav_from_detail', (
        ((0, 1), 'add_from_goods_list'),
        ((0, 2, 3), 'add_from_goods_list'),
        ((2, 5), 'add_from_goods_detail')), ids=idfn_x)
def test_add2fav(logined_page, fav_numbers: tuple, add_fav_from_detail: str):
    goods_for_fav = logined_page.goods_list
    fav_goods_names_expected = []
    for goods_index in fav_numbers:
        match add_fav_from_detail:
            case 'add_from_goods_list':
                fav_goods_names_expected.append(
                    LoginedPage.good_name_text(goods_for_fav[goods_index]))
                logined_page.click_goods_heart_button(goods_for_fav, goods_index)
            case 'add_from_goods_detail':  # test adds goods to favorites from goods detail page
                goodsdetail_page = logined_page.click_on_goods(goods_index)
                fav_goods_names_expected.append(goodsdetail_page.good_name_txt)
                goodsdetail_page.click_fav_add_button()
                goodsdetail_page.click_browser_back_button()

    assert_index_goods_list(logined_page.fav_button_counter_text, str(len(fav_numbers)))
    favorite_page = logined_page.click_fav_page_button()
    assert_index_favorites(favorite_page.fav_button_counter_text, str(len(fav_numbers)))
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


@allure.title('Adding second product in the list to the favorites without first login in')
@pytest.mark.ui
def test_add2fav_out_of_login(main_page):
    goods_index = 1
    fav_goods_names_expected = \
        {(MainPage.good_name_text(main_page.goods_list[goods_index]))}
    MainPage.click_goods_heart_button(main_page.goods_list, goods_index)
    common.login_steps(main_page)
    logined_page = main_page.go_logined_page()
    assert_index_goods_list(logined_page.fav_button_counter_text, '1')
    favorite_page = logined_page.click_fav_page_button()
    assert_index_favorites(favorite_page.fav_button_counter_text, '1')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


@allure.title('Sequence of actions like adding and removing from favorites')
@pytest.mark.ui
@pytest.mark.parametrize('sequence_of_goods_heart_clicking', ((1, 2, 1), (1, 1, 2, 2, 3)))
def test_add2fav_and_remove(logined_page, sequence_of_goods_heart_clicking: tuple):
    # expected_goods_indices_dict: keys - goods's index in the page, value - flag means resulting adding to the favs
    # True value - There is odd clicks on the goods according to the given sequence.
    # It means goods will be added to the favorites in sum.
    # False value - There are even clicks.
    # It means goods won't be added to the favorites
    expected_goods_indices = \
        [i for i in set(sequence_of_goods_heart_clicking) if sequence_of_goods_heart_clicking.count(i) % 2 != 0]
    goods_for_fav = logined_page.goods_list
    fav_goods_names_expected = {LoginedPage.good_name_text(goods_for_fav[i]) for i in expected_goods_indices}
    for goods_index in sequence_of_goods_heart_clicking:
        logined_page.click_goods_heart_button(goods_for_fav, goods_index)
    favorite_page = logined_page.click_fav_page_button()
    assert_index_favorites(favorite_page.fav_button_counter_text, f'{len(expected_goods_indices)}')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# HELPERS
@allure.step('Comparing actual favorite list with expected')
def assert_goodsnames_in_fav(actual_fav_goods_set, expected_fav_goods_set):
    assert {i.text for i in actual_fav_goods_set} == {i for i in expected_fav_goods_set}, \
        'Set of goods have added is not equal to goods in the favorites list'
    do_allure_screenshot(f'Goods in the favorites list')


def assert_index_goods_list(actual, expected):
    check.equal(actual, expected,
                'Goods list page. Index on the heart icon is not equal to number of goods was added to favorites')


def assert_index_favorites(actual, expected):
    check.equal(actual, expected,
                'Favorites page. Index on the heart icon is not equal to number of goods was added to favorites')
