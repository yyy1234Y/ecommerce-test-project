from pages.base_page import BasePage
from config.settings import BASE_URL
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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
        # Selenium 的 Select 类处理下拉框
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        select = Select(element)
        select.select_by_visible_text(value)

    def get_product_names(self) -> list:
        # 等待商品列表出现
        self.wait_for_selector(self.PRODUCT_ITEMS)
        products = self.driver.find_elements(By.CSS_SELECTOR, self.PRODUCT_ITEMS)
        names = []
        for product in products:
            # 尝试提取 h3 或 .product-name 或其他可能包含名称的元素
            # 原 Playwright 代码中使用 el.querySelector('h3')?.innerText，我们同样取 h3
            name_elem = product.find_element(By.CSS_SELECTOR, "h3")
            names.append(name_elem.text)
        return names

    def click_first_product(self):
        with allure.step("点击第一个商品"):
            self.wait_for_selector(self.PRODUCT_LINK)
            # 获取所有商品链接，取第一个点击
            links = self.driver.find_elements(By.CSS_SELECTOR, self.PRODUCT_LINK)
            if links:
                links[0].click()
            else:
                raise Exception("未找到任何商品链接")