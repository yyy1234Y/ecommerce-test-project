import allure
import pytest
from utils.data_loader import data_loader   # 导入数据工厂
from utils.logger import log

@allure.feature("登录模块")
class TestLogin:

    @allure.story("正常登录")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, login_page):
        user = data_loader.get_user("valid")   # 从 YAML 读取有效用户
        log.info(f"使用账号 {user['email']} 登录")
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])
        assert "shop" in login_page.get_current_url()
        assert user['email'] in login_page.page.content()

    @allure.story("密码错误")
    def test_invalid_login(self, login_page):
        user = data_loader.get_user("invalid")  # 从 YAML 读取无效用户
        login_page.navigate_to_login()
        login_page.login(user['email'], user['password'])
        error_msg = login_page.get_error_message()
        assert "邮箱或密码错误" in error_msg