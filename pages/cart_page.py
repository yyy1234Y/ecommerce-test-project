from pages.base_page import BasePage
import allure

class CartPage(BasePage):
    CART_ITEMS = "table tr"
    ITEM_QUANTITY_INPUT = "input[name='quantity']"
    UPDATE_BUTTON = "input[type='submit']"
    REMOVE_LINK = "a[href*='remove']"
    TOTAL_AMOUNT = "p:has-text('总计')"
    CHECKOUT_BUTTON = "a[href*='checkout']"

    def navigate_to_cart(self):
        # 通常通过页面顶部的购物车链接进入，但为了独立，也可以直接访问 URL（需根据实际路由）
        from config.settings import BASE_URL
        self.navigate(f"{BASE_URL}/cart")

    def get_cart_items_count(self) -> int:
        rows = self.page.locator(self.CART_ITEMS).count()
        # 减去表头行（如果存在）
        return rows - 1 if rows > 1 else 0

    def update_quantity(self, item_index: int, quantity: int):
        with allure.step(f"更新第{item_index+1}个商品数量为{quantity}"):
            # 定位到对应行的数量输入框
            row = self.page.locator(self.CART_ITEMS).nth(item_index + 1)  # +1 跳过表头
            row.locator(self.ITEM_QUANTITY_INPUT).fill(str(quantity))
            row.locator(self.UPDATE_BUTTON).click()

    def remove_item(self, item_index: int):
        with allure.step(f"删除第{item_index+1}个商品"):
            row = self.page.locator(self.CART_ITEMS).nth(item_index + 1)
            row.locator(self.REMOVE_LINK).click()

    def get_total_amount(self) -> str:
        return self.get_text(self.TOTAL_AMOUNT)

    def proceed_to_checkout(self):
        with allure.step("去结算"):
            self.page.wait_for_load_state("networkidle")
            self.wait_for_selector(self.CHECKOUT_BUTTON)
            self.click(self.CHECKOUT_BUTTON)