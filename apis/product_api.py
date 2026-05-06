from apis.api_client import ApiClient

class ProductAPI:
    def __init__(self):
        self.client = ApiClient()

    def get_products(self):
        return self.client.get("/shop/api/products")

    def get_product(self, product_id):
        return self.client.get(f"/shop/api/product/{product_id}")