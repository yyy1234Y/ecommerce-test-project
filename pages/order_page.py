from pages.base_page import BasePage
import allure

class OrderPage(BasePage):
    ADDRESS_INPUT = "input[name='address']"
    SUBMIT_BUTTON = "input[type='submit']"
    ORDER_SUCCESS_MSG = ".flash"
    ORDER_LIST = "ul li"
    ORDER_STATUS_LINK = "a[href*='status']"

    def fill_address(self, address: str):
        with allure.step(f"填写收货地址: {address}"):
            self.fill(self.ADDRESS_INPUT, address)

    def submit_order(self):
        with allure.step("提交订单"):
            self.click(self.SUBMIT_BUTTON)

    def get_success_message(self) -> str:
        self.wait_for_selector(self.ORDER_SUCCESS_MSG)
        return self.get_text(self.ORDER_SUCCESS_MSG)

    def navigate_to_orders(self):
        from config.settings import BASE_URL
        self.navigate(f"{BASE_URL}/order/list")

    def get_order_status(self, order_index: int = 0) -> str:
        # 获取第一个订单的状态文本（简化）
        order_item = self.page.locator(self.ORDER_LIST).nth(order_index)
        status_text = order_item.inner_text()
        # 假设状态包含在文本中，例如 "状态: pending"
        return status_text