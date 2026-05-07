from pages.base_page import BasePage
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # 获取第 order_index 个订单的状态文本（假设订单列表是 <ul><li>...状态: pending</li>...</ul>）
        # 使用 CSS 选择器定位所有订单项
        wait = WebDriverWait(self.driver, self.timeout)
        items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.ORDER_LIST)))
        if order_index >= len(items):
            raise IndexError(f"订单索引 {order_index} 超出列表长度 {len(items)}")
        item = items[order_index]
        return item.text