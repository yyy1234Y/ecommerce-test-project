import yaml
import os
from typing import Dict, Any, List


class DataLoader:
    """数据工厂单例，加载 YAML 并提供数据"""

    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load(self) -> Dict:
        if self._data is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            yaml_path = os.path.join(base_dir, 'config', 'test_data.yaml')
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self._data = yaml.safe_load(f)
        return self._data

    def get_user(self, user_type: str = "valid") -> Dict[str, str]:
        """获取用户数据，支持 valid / invalid / admin"""
        data = self._load()
        return data.get('users', {}).get(user_type, {})

    def get_product(self, index: int = 0) -> Dict:
        """获取商品数据，index 0 为第一个商品"""
        data = self._load()
        products = data.get('products', [])
        return products[index] if index < len(products) else {}

    def get_all_products(self) -> List[Dict]:
        """获取所有商品"""
        data = self._load()
        return data.get('products', [])

    def get_address(self, address_type: str = "default") -> str:
        """获取完整地址字符串"""
        data = self._load()
        addr = data.get('addresses', {}).get(address_type, {})
        return f"{addr.get('street')}, {addr.get('city')}, {addr.get('zipcode')}"

    def get_base_url(self) -> str:
        data = self._load()
        return data.get('base_url', 'http://127.0.0.1:5000')


# 全局单例实例
data_loader = DataLoader()