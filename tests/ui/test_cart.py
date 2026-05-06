import allure
import pytest
from utils.data_loader import data_loader
from utils.logger import log

@allure.feature("购物车功能")
class TestCart:

    @allure.story("添加商品到购物车")
    def test_add_to_cart(self, login_page, shop_page, product_page, cart_page):
        # 登录
        user = data_loader.get_user("valid")
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])

        shop_page.navigate_to_shop()
        shop_page.click_first_product()
        product_page.add_to_cart()
        cart_page.navigate_to_cart()
        assert cart_page.get_cart_items_count() >= 1

    @allure.story("更新购物车数量")
    def test_update_cart_quantity(self, login_page, shop_page, product_page, cart_page):
        # 登录
        user = data_loader.get_user("valid")
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])

        shop_page.navigate_to_shop()
        shop_page.click_first_product()
        product_page.add_to_cart()
        cart_page.navigate_to_cart()
        cart_page.update_quantity(0, 3)
        # 可选断言：检查总价是否变化
        total_text = cart_page.get_total_amount()
        assert "¥" in total_text