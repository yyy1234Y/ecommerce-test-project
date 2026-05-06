from playwright.sync_api import Page
import allure
from config.settings import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utils.logger import log  # 新增：导入日志
import os
import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = DEFAULT_TIMEOUT
        self.retry_count = 3  # 重试次数

    def navigate(self, url: str):
        with allure.step(f"打开页面: {url}"):
            log.info(f"导航至: {url}")
            self.page.goto(url)

    def click(self, selector: str, retry: bool = True):
        """带重试机制的点击"""
        with allure.step(f"点击元素: {selector}"):
            log.info(f"尝试点击: {selector}")
            if retry:
                for i in range(self.retry_count):
                    try:
                        self.page.click(selector, timeout=self.timeout)
                        log.info(f"点击成功: {selector}")
                        return
                    except Exception as e:
                        if i == self.retry_count - 1:
                            log.error(f"点击失败，已重试{self.retry_count}次: {selector}")
                            raise e
                        log.warning(f"点击失败，第{i+2}次重试...")
                        time.sleep(1)
            else:
                self.page.click(selector, timeout=self.timeout)
                log.info(f"点击成功: {selector}")

    def fill(self, selector: str, text: str, retry: bool = True):
        """带重试机制的输入"""
        with allure.step(f"输入文本: {text[:50]}"):
            log.info(f"输入文本: {text} 到 {selector}")
            if retry:
                for i in range(self.retry_count):
                    try:
                        # 先清空再输入
                        self.page.fill(selector, "", timeout=self.timeout)
                        self.page.fill(selector, text, timeout=self.timeout)
                        log.info(f"输入成功: {selector}")
                        return
                    except Exception as e:
                        if i == self.retry_count - 1:
                            log.error(f"输入失败，已重试{self.retry_count}次: {selector}")
                            raise e
                        log.warning(f"输入失败，第{i+2}次重试...")
                        time.sleep(1)
            else:
                self.page.fill(selector, text, timeout=self.timeout)
                log.info(f"输入成功: {selector}")

    def wait_for_selector(self, selector: str, timeout: int = None):
        """显式等待元素出现"""
        timeout = timeout or self.timeout
        log.info(f"等待元素出现: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def wait_for_element_visible(self, selector: str, timeout: int = None):
        """等待元素可见"""
        timeout = timeout or self.timeout
        log.info(f"等待元素可见: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def wait_for_element_hidden(self, selector: str, timeout: int = None):
        """等待元素隐藏"""
        timeout = timeout or self.timeout
        log.info(f"等待元素隐藏: {selector}")
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)

    def get_text(self, selector: str, retry: bool = True) -> str:
        """带重试的获取文本"""
        if retry:
            for i in range(self.retry_count):
                try:
                    text = self.page.text_content(selector, timeout=self.timeout)
                    log.info(f"获取文本成功: {selector} -> {text[:50]}")
                    return text
                except Exception as e:
                    if i == self.retry_count - 1:
                        log.error(f"获取文本失败，已重试{self.retry_count}次: {selector}")
                        raise e
                    log.warning(f"获取文本失败，第{i+2}次重试...")
                    time.sleep(1)
        text = self.page.text_content(selector, timeout=self.timeout)
        log.info(f"获取文本成功: {selector} -> {text[:50]}")
        return text

    def take_screenshot(self, name: str = "screenshot"):
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        self.page.screenshot(path=path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        log.info(f"截图已保存: {path}")
        return path

    def get_current_url(self) -> str:
        url = self.page.url
        log.info(f"当前URL: {url}")
        return url