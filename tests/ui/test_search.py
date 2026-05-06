import allure
import pytest
from utils.data_loader import data_loader

@allure.feature("商品搜索与筛选")
class TestSearch:

    @allure.story("搜索商品")
    @pytest.mark.parametrize("product_name", [
        data_loader.get_all_products()[0]['name'],
        data_loader.get_all_products()[1]['name']
    ])
    def test_search_product(self, shop_page, product_name):
        shop_page.navigate_to_shop()
        shop_page.search(product_name)
        product_names = shop_page.get_product_names()
        assert any(product_name in name for name in product_names)

    @allure.story("按分类筛选")
    def test_filter_by_category(self, shop_page):
        # 从 YAML 中获取第一个商品的分类（假设“电子”）
        products = data_loader.get_all_products()
        category = products[0].get('category', '电子') if products else '电子'
        shop_page.navigate_to_shop()
        shop_page.filter_by_category(category)
        product_names = shop_page.get_product_names()
        assert any(product_names)  # 确保有商品显示