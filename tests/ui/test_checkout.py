import allure
import pytest
from utils.data_loader import data_loader
from utils.logger import log

@allure.feature("下单流程")
class TestCheckout:

    @allure.story("正常下单")
    def test_checkout(self, login_page, shop_page, product_page, cart_page, order_page):
        # 登录
        user = data_loader.get_user("valid")
        log.info(f"使用账号 {user['email']} 登录")
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])

        # 添加商品到购物车
        shop_page.navigate_to_shop()
        shop_page.click_first_product()
        product_page.add_to_cart()

        # 进入购物车并结算
        cart_page.navigate_to_cart()
        cart_page.proceed_to_checkout()

        # 填写地址并提交订单
        address = data_loader.get_address("default")
        log.info(f"使用地址: {address}")
        order_page.fill_address(address)
        order_page.submit_order()

        # 验证成功消息
        success_msg = order_page.get_success_message()
        assert "订单已创建" in success_msg