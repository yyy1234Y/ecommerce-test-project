import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.order_page import OrderPage
from config.settings import SCREENSHOT_DIR
import os
from utils.logger import log


@pytest.fixture(scope="function")
def driver():
    log.info("启动浏览器...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # 使用本地 ChromeDriver（确保已安装）
    # 或者让 Selenium 自动使用 PATH 中的驱动
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    log.info("浏览器已启动")
    yield driver
    log.info("关闭浏览器...")
    driver.quit()


# 其余 fixtures 保持不变（login_page, shop_page, etc.）

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def shop_page(driver):
    return ShopPage(driver)

@pytest.fixture
def product_page(driver):
    return ProductPage(driver)

@pytest.fixture
def cart_page(driver):
    return CartPage(driver)

@pytest.fixture
def order_page(driver):
    return OrderPage(driver)

@pytest.fixture
def logged_in_page(driver, login_page):
    """已登录的页面 fixture，避免每个用例重复写登录"""
    log.info("使用 logged_in_page fixture，执行登录...")
    login_page.navigate_to_login()
    login_page.login("test@example.com", "test123")
    log.info("登录成功，返回已登录页面")
    return driver

@pytest.fixture(scope="function", autouse=True)
def clean_before_test():
    """每个用例执行前的清理"""
    log.info("执行测试前清理...")

@pytest.fixture(scope="function")
def unique_email():
    """生成唯一邮箱，避免用例间数据冲突"""
    import time
    email = f"test_{int(time.time())}@example.com"
    log.info(f"生成唯一邮箱: {email}")
    return email

# 失败自动截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        log.error(f"测试失败: {item.name}")
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{item.name}_failed.png")
            driver.save_screenshot(screenshot_path)
            log.error(f"失败截图已保存: {screenshot_path}")
            print(f"\n失败截图已保存: {screenshot_path}")

# 记录测试边界
@pytest.fixture(scope="function", autouse=True)
def log_test_boundary(request):
    log.info(f"========== 开始执行测试用例: {request.node.name} ==========")
    yield
    log.info(f"========== 测试用例执行结束: {request.node.name} ==========")

# API 客户端 fixture（保持不变）
@pytest.fixture
def auth_api():
    """提供 API 测试客户端"""
    try:
        from apis.api_client import ApiClient
        return ApiClient()
    except ImportError as e:
        log.error(f"导入 ApiClient 失败: {e}")
        pytest.skip("API 客户端不可用")