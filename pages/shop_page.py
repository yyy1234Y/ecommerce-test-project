from pages.base_page import BasePage
from config.settings import BASE_URL
import allure

class ShopPage(BasePage):
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "input[type='submit']"
    CATEGORY_SELECT = "select[name='category']"
    PRODUCT_ITEMS = ".product"
    PRODUCT_LINK = ".product a"

    def navigate_to_shop(self):
        self.navigate(f"{BASE_URL}/shop")

    def search(self, keyword: str):
        with allure.step(f"搜索商品: {keyword}"):
            self.fill(self.SEARCH_INPUT, keyword)
            self.click(self.SEARCH_BUTTON)

    def filter_by_category(self, category: str):
        with allure.step(f"筛选分类: {category}"):
            self.select_option(self.CATEGORY_SELECT, category)
            self.click(self.SEARCH_BUTTON)

    def select_option(self, selector: str, value: str):
        self.page.select_option(selector, value)

    def get_product_names(self) -> list:
        self.wait_for_selector(self.PRODUCT_ITEMS)
        return self.page.eval_on_selector_all(self.PRODUCT_ITEMS, "elements => elements.map(el => el.querySelector('h3')?.innerText || '')")

    def click_first_product(self):
        with allure.step("点击第一个商品"):
            self.wait_for_selector(self.PRODUCT_LINK)
            self.page.locator(self.PRODUCT_LINK).first.click()