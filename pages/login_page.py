from pages.base_page import BasePage
from config.settings import BASE_URL
import allure

class LoginPage(BasePage):
    # 定位器
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = "input[type='submit']"
    ERROR_MESSAGE = ".flash"
    REGISTER_LINK = "a[href*='register']"

    def navigate_to_login(self):
        self.navigate(f"{BASE_URL}/auth/login")

    def login(self, email: str, password: str):
        with allure.step(f"登录: {email}"):
            self.fill(self.EMAIL_INPUT, email)
            self.fill(self.PASSWORD_INPUT, password)
            self.click(self.SUBMIT_BUTTON)

    def get_error_message(self) -> str:
        self.wait_for_selector(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def click_register_link(self):
        self.click(self.REGISTER_LINK)