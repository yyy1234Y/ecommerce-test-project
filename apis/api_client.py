import requests
import allure
from config.settings import BASE_URL
from utils.logger import log


class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def get(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        log.info(f"GET {url}")
        resp = self.session.get(url, **kwargs)
        self._attach_to_allure("GET", url, kwargs, resp)
        return resp

    def post(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        log.info(f"POST {url}")
        resp = self.session.post(url, **kwargs)
        self._attach_to_allure("POST", url, kwargs, resp)
        return resp

    # ========== 认证相关 API ==========

    def login(self, email, password):
        """用户登录"""
        path = "/auth/api/login"
        data = {
            "email": email,
            "password": password
        }
        return self.post(path, json=data)

    def register(self, email, password):
        """用户注册"""
        path = "/auth/api/register"
        data = {
            "email": email,
            "password": password
        }
        return self.post(path, json=data)

    def logout(self):
        """用户退出登录"""
        path = "/auth/api/logout"
        return self.post(path)

    def get_current_user(self):
        """获取当前登录用户信息"""
        path = "/auth/api/user"
        return self.get(path)

    def _attach_to_allure(self, method, url, kwargs, resp):
        allure.attach(f"{method} {url}", "请求", allure.attachment_type.TEXT)
        if "json" in kwargs:
            allure.attach(str(kwargs["json"]), "请求体", allure.attachment_type.JSON)
        allure.attach(str(resp.status_code), "状态码", allure.attachment_type.TEXT)
        allure.attach(resp.text[:1000], "响应体", allure.attachment_type.TEXT)