# pages/base_page.py - Selenium 版本
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import allure
from config.settings import DEFAULT_TIMEOUT, SCREENSHOT_DIR
from utils.logger import log
import os
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = DEFAULT_TIMEOUT
        self.retry_count = 3

    def navigate(self, url: str):
        with allure.step(f"打开页面: {url}"):
            log.info(f"导航至: {url}")
            self.driver.get(url)

    def click(self, selector: str, retry: bool = True):
        """带重试机制的点击（支持 CSS_SELECTOR 字符串）"""
        with allure.step(f"点击元素: {selector}"):
            log.info(f"尝试点击: {selector}")
            if retry:
                for i in range(self.retry_count):
                    try:
                        elem = WebDriverWait(self.driver, self.timeout).until(
                            EC.element_to_be_clickable(("css selector", selector))
                        )
                        elem.click()
                        log.info(f"点击成功: {selector}")
                        return
                    except (TimeoutException, StaleElementReferenceException) as e:
                        if i == self.retry_count - 1:
                            log.error(f"点击失败，已重试{self.retry_count}次: {selector}")
                            raise e
                        log.warning(f"点击失败，第{i+2}次重试...")
                        time.sleep(1)
            else:
                elem = WebDriverWait(self.driver, self.timeout).until(
                    EC.element_to_be_clickable(("css selector", selector))
                )
                elem.click()
                log.info(f"点击成功: {selector}")

    def fill(self, selector: str, text: str, retry: bool = True):
        """带重试机制的输入（先清空再填入）"""
        with allure.step(f"输入文本: {text[:50]}"):
            log.info(f"输入文本: {text} 到 {selector}")
            if retry:
                for i in range(self.retry_count):
                    try:
                        elem = WebDriverWait(self.driver, self.timeout).until(
                            EC.presence_of_element_located(("css selector", selector))
                        )
                        elem.clear()
                        elem.send_keys(text)
                        log.info(f"输入成功: {selector}")
                        return
                    except (TimeoutException, StaleElementReferenceException) as e:
                        if i == self.retry_count - 1:
                            log.error(f"输入失败，已重试{self.retry_count}次: {selector}")
                            raise e
                        log.warning(f"输入失败，第{i+2}次重试...")
                        time.sleep(1)
            else:
                elem = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(("css selector", selector))
                )
                elem.clear()
                elem.send_keys(text)
                log.info(f"输入成功: {selector}")

    def wait_for_selector(self, selector: str, timeout: int = None):
        """显式等待元素出现在 DOM 中（不要求可见）"""
        timeout = timeout or self.timeout
        log.info(f"等待元素出现: {selector}")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(("css selector", selector))
        )

    def wait_for_element_visible(self, selector: str, timeout: int = None):
        """等待元素可见"""
        timeout = timeout or self.timeout
        log.info(f"等待元素可见: {selector}")
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(("css selector", selector))
        )

    def wait_for_element_hidden(self, selector: str, timeout: int = None):
        """等待元素隐藏或不存在"""
        timeout = timeout or self.timeout
        log.info(f"等待元素隐藏: {selector}")
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(("css selector", selector))
        )

    def get_text(self, selector: str, retry: bool = True) -> str:
        """带重试的获取元素文本"""
        if retry:
            for i in range(self.retry_count):
                try:
                    elem = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located(("css selector", selector))
                    )
                    text = elem.text
                    log.info(f"获取文本成功: {selector} -> {text[:50]}")
                    return text
                except (TimeoutException, StaleElementReferenceException) as e:
                    if i == self.retry_count - 1:
                        log.error(f"获取文本失败，已重试{self.retry_count}次: {selector}")
                        raise e
                    log.warning(f"获取文本失败，第{i+2}次重试...")
                    time.sleep(1)
        else:
            elem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(("css selector", selector))
            )
            text = elem.text
            log.info(f"获取文本成功: {selector} -> {text[:50]}")
            return text

    def take_screenshot(self, name: str = "screenshot"):
        """截图并附加到 Allure"""
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
        self.driver.save_screenshot(path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)
        log.info(f"截图已保存: {path}")
        return path

    def get_current_url(self) -> str:
        url = self.driver.current_url
        log.info(f"当前URL: {url}")
        return url