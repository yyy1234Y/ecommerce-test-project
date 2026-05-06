import allure
import pytest
from utils.data_loader import data_loader
from utils.logger import log

@allure.feature("端到端完整流程")
class TestEndToEnd:

    @allure.story("用户完整购买流程")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_full_purchase_flow(self, login_page, shop_page, product_page, cart_page, order_page):
        # 1. 登录
        user = data_loader.get_user("valid")
        log.info(f"登录用户: {user['email']}")
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])

        # 2. 搜索商品（使用第一个商品名）
        products = data_loader.get_all_products()
        keyword = products[0]['name'] if products else "测试商品1"
        log.info(f"搜索商品: {keyword}")
        shop_page.navigate_to_shop()
        shop_page.search(keyword)

        # 3. 进入详情并加入购物车
        shop_page.click_first_product()
        product_page.add_to_cart()

        # 4. 进入购物车并结算
        cart_page.navigate_to_cart()
        cart_page.proceed_to_checkout()

        # 5. 填写地址并下单
        address = data_loader.get_address("beijing")  # 使用北京地址
        order_page.fill_address(address)
        order_page.submit_order()

        # 6. 验证下单成功
        success_msg = order_page.get_success_message()
        assert "订单已创建" in success_msg

        # 7. 验证订单列表中显示该订单
        order_page.navigate_to_orders()
        assert "pending" in order_page.get_order_status()