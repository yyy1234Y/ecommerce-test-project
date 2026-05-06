import allure
import pytest
from utils.data_loader import data_loader
from utils.logger import log


@allure.feature("注册功能")
class TestRegisterAPI:

    @allure.story("正常注册")
    @allure.title("测试新用户注册成功")
    def test_register_success(self, auth_api, unique_email):
        """测试正常注册：新邮箱能成功注册"""
        log.info(f"测试注册邮箱: {unique_email}")

        resp = auth_api.register(unique_email, "test123")

        assert resp.status_code == 200
        json_data = resp.json()
        assert json_data["code"] == 200
        assert json_data["message"] == "注册成功"
        assert json_data["email"] == unique_email
        assert "user_id" in json_data

    @allure.story("重复注册")
    @allure.title("测试重复邮箱注册失败")
    def test_register_duplicate_email(self, auth_api):
        """测试重复注册：已存在的邮箱不能重复注册"""
        # 使用唯一邮箱确保第一次注册成功
        import time
        unique_email = f"dup_test_{int(time.time())}@example.com"

        # 第一次注册 - 应该成功
        resp1 = auth_api.register(unique_email, "test123")
        assert resp1.status_code == 200
        json_data1 = resp1.json()
        assert json_data1["code"] == 200

        # 第二次用同一邮箱注册 - 应该失败
        resp2 = auth_api.register(unique_email, "test123")
        assert resp2.status_code == 409
        json_data2 = resp2.json()
        assert json_data2["code"] == 409
        assert json_data2["message"] == "邮箱已注册"

    @allure.story("参数校验")
    @allure.title("测试注册缺少邮箱")
    def test_register_missing_email(self, auth_api):
        """测试注册：缺少邮箱字段"""
        # 直接调用 post 方法发送不完整的请求
        resp = auth_api.post("/auth/api/register", json={"password": "test123"})

        assert resp.status_code == 400
        json_data = resp.json()
        assert "邮箱" in json_data["message"]

    @allure.story("参数校验")
    @allure.title("测试注册缺少密码")
    def test_register_missing_password(self, auth_api):
        """测试注册：缺少密码字段"""
        resp = auth_api.post("/auth/api/register", json={"email": "test@example.com"})

        assert resp.status_code == 400
        json_data = resp.json()
        assert "密码" in json_data["message"]

    @allure.story("参数校验")
    @allure.title("测试注册空请求体")
    def test_register_empty_body(self, auth_api):
        """测试注册：空请求体"""
        resp = auth_api.post("/auth/api/register", json={})

        assert resp.status_code == 400
        json_data = resp.json()
        assert "不能为空" in json_data["message"]