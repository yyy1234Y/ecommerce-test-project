"""测试数据清理工具"""
from models import User, Order, Cart  # 如果直接操作数据库需要导入
import requests
from config.settings import BASE_URL


class DataCleaner:
    """通过 API 或直接操作数据库清理测试数据"""

    @staticmethod
    def delete_user_by_email(email: str):
        """删除测试用户（需要商城提供 API）"""
        # 方案1：调用商城 API（推荐）
        # requests.delete(f"{BASE_URL}/api/user/{email}")
        pass

    @staticmethod
    def clear_cart(user_id: int):
        """清空购物车"""
        # 调用商城 API 或直接操作数据库
        pass

    @staticmethod
    def cancel_order(order_id: int):
        """取消订单"""
        pass