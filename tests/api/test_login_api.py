import allure
import pytest
from utils.data_loader import data_loader


@allure.feature("登录接口")
class TestLoginAPI:
    @allure.story("正常登录")
    def test_login_success(self, auth_api):
        user = data_loader.get_user("valid")
        resp = auth_api.login(user["email"], user["password"])

        # 添加打印信息
        # print(f"\n请求: POST {auth_api.base_url}/auth/api/login")
        # print(f"请求参数: {{'email': '{user['email']}', 'password': '***'}}")
        # print(f"响应状态码: {resp.status_code}")
        # print(f"响应内容: {resp.json()}")

        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert resp.json()["message"] == "登录成功"

    @allure.story("密码错误")
    def test_login_wrong_password(self, auth_api):
        user = data_loader.get_user("valid")
        resp = auth_api.login(user["email"], "wrongpassword")

        # 添加打印信息
        # print(f"\n请求: POST {auth_api.base_url}/auth/api/login")
        # print(f"请求参数: {{'email': '{user['email']}', 'password': 'wrongpassword'}}")
        # print(f"响应状态码: {resp.status_code}")
        # print(f"响应内容: {resp.json()}")

        assert resp.status_code == 401
        assert resp.json()["code"] == 401
        assert resp.json()["message"] == "邮箱或密码错误"