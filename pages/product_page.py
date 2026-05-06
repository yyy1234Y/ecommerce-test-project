from pages.base_page import BasePage
import allure

class ProductPage(BasePage):
    PRODUCT_NAME = "h2"
    PRODUCT_PRICE = "p:first-of-type"
    ADD_TO_CART_BUTTON = "a[href*='add']"
    BACK_LINK = "a[href*='shop']"

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        return self.get_text(self.PRODUCT_PRICE)

    def add_to_cart(self):
        with allure.step("加入购物车"):
            self.click(self.ADD_TO_CART_BUTTON)

    def go_back(self):
        self.click(self.BACK_LINK)