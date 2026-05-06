import allure
import pytest
from utils.logger import log


@allure.feature("退出登录功能")
class TestLogoutAPI:

    @allure.story("正常退出")
    @allure.title("测试已登录用户退出成功")
    def test_logout_success(self, auth_api):
        """测试已登录用户能成功退出"""
        # 先登录
        login_resp = auth_api.login("test@example.com", "test123")
        assert login_resp.status_code == 200

        # 再退出
        logout_resp = auth_api.logout()

        assert logout_resp.status_code == 200
        json_data = logout_resp.json()
        assert json_data["code"] == 200
        assert json_data["message"] == "退出成功"

    @allure.story("未登录退出")
    @allure.title("测试未登录用户调用退出接口")
    def test_logout_without_login(self, auth_api):
        """测试未登录时调用退出接口"""
        # 使用新的 client 实例，未登录
        logout_resp = auth_api.logout()

        # 应该返回 401 未授权
        assert logout_resp.status_code == 401
        json_data = logout_resp.json()
        # Flask-Login 返回的是 HTML 页面的 401，可能需要调整
        # 如果返回的是 HTML，可以检查响应文本
        if "text/html" in logout_resp.headers.get("Content-Type", ""):
            assert "Login" in logout_resp.text or "登录" in logout_resp.text
        else:
            assert "未登录" in json_data.get("message", "")

    @allure.story("退出后访问受限接口")
    @allure.title("测试退出后无法访问用户信息接口")
    def test_access_after_logout(self, auth_api):
        """测试退出后，需要登录的接口无法访问"""
        # 先登录
        auth_api.login("test@example.com", "test123")

        # 退出
        auth_api.logout()

        # 尝试获取用户信息（需要登录）
        user_resp = auth_api.get_current_user()

        # 应该返回 401 未授权
        assert user_resp.status_code == 401