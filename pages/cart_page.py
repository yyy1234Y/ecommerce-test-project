from pages.base_page import BasePage
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_ITEMS = "table tr"
    ITEM_QUANTITY_INPUT = "input[name='quantity']"
    UPDATE_BUTTON = "input[type='submit']"
    REMOVE_LINK = "a[href*='remove']"
    TOTAL_AMOUNT = "p:has-text('总计')"          # 注意：Selenium 不支持 :has-text，下面会特殊处理
    CHECKOUT_BUTTON = "a[href*='checkout']"

    def navigate_to_cart(self):
        from config.settings import BASE_URL
        self.navigate(f"{BASE_URL}/cart")

    def get_cart_items_count(self) -> int:
        # 获取所有商品行（不含表头）
        rows = self.driver.find_elements(By.CSS_SELECTOR, self.CART_ITEMS)
        # 如果第一行是表头，则商品行数 = 总行数 - 1；否则就取全部行（根据实际情况调整）
        # 通常表格第一行是 <th>，因此减 1
        return len(rows) - 1 if len(rows) > 1 else 0

    def update_quantity(self, item_index: int, quantity: int):
        with allure.step(f"更新第{item_index+1}个商品数量为{quantity}"):
            # 获取所有表行（包括表头）
            rows = self.driver.find_elements(By.CSS_SELECTOR, self.CART_ITEMS)
            # 第 item_index 行需要 +1 来跳过表头（假设第0行是表头）
            target_row = rows[item_index + 1] if len(rows) > item_index + 1 else None
            if not target_row:
                raise IndexError(f"未找到第 {item_index+1} 个商品行")
            # 该行内的数量输入框
            qty_input = target_row.find_element(By.CSS_SELECTOR, self.ITEM_QUANTITY_INPUT)
            qty_input.clear()
            qty_input.send_keys(str(quantity))
            # 更新按钮
            update_btn = target_row.find_element(By.CSS_SELECTOR, self.UPDATE_BUTTON)
            update_btn.click()

    def remove_item(self, item_index: int):
        with allure.step(f"删除第{item_index+1}个商品"):
            rows = self.driver.find_elements(By.CSS_SELECTOR, self.CART_ITEMS)
            target_row = rows[item_index + 1] if len(rows) > item_index + 1 else None
            if not target_row:
                raise IndexError(f"未找到第 {item_index+1} 个商品行")
            remove_link = target_row.find_element(By.CSS_SELECTOR, self.REMOVE_LINK)
            remove_link.click()

    def get_total_amount(self) -> str:
        # 由于 Selenium 不支持 CSS 伪类 :has-text，我们改用 XPath 或基于文本定位
        # 方法1：使用 XPath 查找包含“总计”文本的元素
        total_xpath = "//p[contains(text(), '总计')]"
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, total_xpath))
        )
        return element.text
        # 若原 Playwright 代码中 self.get_text(self.TOTAL_AMOUNT) 能正常工作，但 Selenium 不支持 :has-text，
        # 所以这里覆盖 get_total_amount 方法，直接使用 XPath。

    def proceed_to_checkout(self):
        with allure.step("去结算"):
            # 等待结算按钮可见并点击
            self.wait_for_selector(self.CHECKOUT_BUTTON)   # BasePage 中有 wait_for_selector
            self.click(self.CHECKOUT_BUTTON)